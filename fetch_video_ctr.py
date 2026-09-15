#!/usr/bin/env python3
"""
Fetch per-video impressions + impressions CTR from the YouTube Analytics API
and merge with the Data API catalog (title, thumbnail, published date).

Needs a broader OAuth scope (yt-analytics.readonly) than the Data-API-only
token.json used elsewhere in this repo, so this script authenticates
separately into token_analytics.json to avoid disturbing the existing token.
"""

import os
import json
import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

CREDENTIALS_FILE = "client_secret.json"
TOKEN_FILE = "token_analytics.json"
OUTPUT_FILE = "video_ctr_data.json"


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Warning loading token file: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8912, open_browser=False)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def main():
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    yta = build("youtubeAnalytics", "v2", credentials=creds)

    channel_resp = youtube.channels().list(mine=True, part="snippet,contentDetails").execute()
    channel = channel_resp["items"][0]
    channel_id = channel["id"]
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    # Pull full video catalog (title, thumbnail, published date) via Data API
    videos = {}
    page_token = None
    while True:
        pl = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part="contentDetails",
            maxResults=50,
            pageToken=page_token,
        ).execute()
        ids = [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        print(f"Playlist page: {len(ids)} items, nextPageToken={pl.get('nextPageToken')}")
        if ids:
            vresp = youtube.videos().list(id=",".join(ids), part="snippet,statistics").execute()
            for item in vresp.get("items", []):
                snippet = item["snippet"]
                stats = item.get("statistics", {})
                videos[item["id"]] = {
                    "id": item["id"],
                    "title": snippet.get("title"),
                    "published_at": snippet.get("publishedAt"),
                    "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url")
                        or snippet.get("thumbnails", {}).get("default", {}).get("url"),
                    "view_count": int(stats.get("viewCount", 0)),
                }
        page_token = pl.get("nextPageToken")
        if not page_token:
            break

    print(f"Catalog: {len(videos)} videos")

    end_date = datetime.date.today().isoformat()
    start_date = "2020-01-01"

    # True impressions / thumbnail-CTR metrics (videoThumbnailImpressions,
    # videoThumbnailImpressionsClickRate, and the older impressions /
    # impressionsClickThroughRate names) are rejected by this API client for
    # every query shape tried (channel totals, per-video, per-day, filtered
    # to one video) with "query not supported" -- this is YouTube's Reach
    # metrics restriction: they're gated to audited/allowlisted OAuth
    # clients and are otherwise Studio-only. So this script pulls the
    # engagement metrics that ARE available for dimensions=video and uses
    # them as a packaging-risk proxy instead of fabricating a CTR number.
    ctr_restricted = True
    ctr_restriction_note = (
        "videoThumbnailImpressions / impressionsClickThroughRate metrics are "
        "restricted (Reach report) for this OAuth client -- YouTube Analytics "
        "API returned \"query not supported\" for every dimension/filter "
        "combination tried. Real per-video CTR is Studio-only: Studio -> "
        "Content -> select video -> Analytics -> Reach tab."
    )

    metrics = "views,averageViewPercentage,subscribersGained,likes,comments"
    result = yta.reports().query(
        ids=f"channel=={channel_id}",
        startDate=start_date,
        endDate=end_date,
        metrics=metrics,
        dimensions="video",
        sort="-views",
        maxResults=200,
    ).execute()

    headers = [h["name"] for h in result.get("columnHeaders", [])]
    rows = result.get("rows", [])
    print(f"Analytics rows returned: {len(rows)}")

    stats_by_video = {}
    for row in rows:
        rec = dict(zip(headers, row))
        vid = rec.get("video")
        stats_by_video[vid] = rec

    merged = []
    for vid, meta in videos.items():
        rec = stats_by_video.get(vid, {})
        merged.append({
            **meta,
            "impressions": None,
            "impressions_ctr_pct": None,
            "analytics_views": rec.get("views"),
            "avg_view_pct": rec.get("averageViewPercentage"),
            "subscribers_gained": rec.get("subscribersGained"),
            "likes": rec.get("likes"),
            "comments": rec.get("comments"),
        })

    merged.sort(key=lambda v: (v.get("analytics_views") or v.get("view_count") or 0), reverse=True)

    out = {
        "pulled_at": datetime.datetime.utcnow().isoformat() + "Z",
        "channel_id": channel_id,
        "channel_title": channel["snippet"]["title"],
        "window": {"start": start_date, "end": end_date},
        "metrics_used": metrics,
        "ctr_restricted": ctr_restricted,
        "ctr_restriction_note": ctr_restriction_note,
        "videos": merged,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_FILE} with {len(merged)} videos")


if __name__ == "__main__":
    main()

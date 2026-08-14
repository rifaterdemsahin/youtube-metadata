#!/usr/bin/env python3
"""
CLI Script to append your Skool community link to all YouTube video descriptions.
Usage:
  python append_skool_link.py --dry-run
  python append_skool_link.py --apply
"""

import argparse
import json
import sys
import os
from datetime import datetime
import youtube_client

SKOOL_LINK_DEFAULT = "https://www.skool.com/delivery-pilot-8938"
REPORT_FILE = "update_report.json"

def main():
    parser = argparse.ArgumentParser(description="Append Skool link to all YouTube video descriptions.")
    parser.add_argument("--link", default=SKOOL_LINK_DEFAULT, help="The link to append to video descriptions")
    parser.add_argument("--prefix", default="\n\n🚀 Join our community:\n", help="Prefix text before the link")
    parser.add_argument("--apply", action="store_true", help="Apply actual updates to YouTube (default is dry-run)")
    args = parser.parse_args()

    dry_run = not args.apply
    print("=" * 60)
    print("YouTube Studio Metadata Updater - Skool Link Syncer")
    print(f"Mode: {'DRY RUN (Simulated)' if dry_run else '🔴 LIVE UPDATE (Applying changes)'}")
    print(f"Target Link: {args.link}")
    print("=" * 60)

    try:
        youtube = youtube_client.get_youtube_service()
    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {e}")
        print("Make sure 'client_secret.json' is placed in the project root folder.")
        sys.exit(1)

    print("Fetching uploaded videos...")
    channels = youtube.channels().list(mine=True, part="contentDetails,snippet").execute()
    if not channels.get("items"):
        print("No channel found for authenticated account.")
        sys.exit(1)

    channel_name = channels["items"][0]["snippet"]["title"]
    uploads_id = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    print(f"Connected to channel: '{channel_name}'")

    updated_videos = []
    skipped_videos = []
    page_token = None

    while True:
        pl_req = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=page_token
        )
        pl_res = pl_req.execute()
        video_ids = [item["contentDetails"]["videoId"] for item in pl_res.get("items", [])]

        if not video_ids:
            break

        v_res = youtube.videos().list(id=",".join(video_ids), part="snippet,status").execute()
        for v in v_res.get("items", []):
            vid = v["id"]
            title = v["snippet"]["title"]
            desc = v["snippet"].get("description", "")
            privacy = v.get("status", {}).get("privacyStatus", "unknown")

            if args.link in desc:
                skipped_videos.append({
                    "id": vid,
                    "title": title,
                    "privacy": privacy,
                    "reason": "Link already present"
                })
                print(f"  [SKIPPED] {title} ({vid}) - Already has link")
            else:
                new_desc = desc.rstrip() + args.prefix + args.link
                if not dry_run:
                    v["snippet"]["description"] = new_desc
                    youtube.videos().update(part="snippet", body={"id": vid, "snippet": v["snippet"]}).execute()
                    print(f"  [UPDATED] {title} ({vid})")
                else:
                    print(f"  [WOULD UPDATE] {title} ({vid})")

                updated_videos.append({
                    "id": vid,
                    "title": title,
                    "privacy": privacy,
                    "status": "Updated" if not dry_run else "Pending (Dry Run)",
                    "updated_at": datetime.now().isoformat()
                })

        page_token = pl_res.get("nextPageToken")
        if not page_token:
            break

    report_data = {
        "channel_name": channel_name,
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "link": args.link,
        "total_checked": len(updated_videos) + len(skipped_videos),
        "total_updated": len(updated_videos),
        "total_skipped": len(skipped_videos),
        "updated_videos": updated_videos,
        "skipped_videos": skipped_videos
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report_data, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Execution Completed!")
    print(f"Total Videos Checked: {report_data['total_checked']}")
    print(f"Targeted for Update: {report_data['total_updated']}")
    print(f"Skipped (Already present): {report_data['total_skipped']}")
    print(f"Report saved to: {REPORT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()

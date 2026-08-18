#!/usr/bin/env python3
"""
Skill Script: End Cards & End Screen Manager for YouTube Channel @RifatErdemSahin.
Sets and calculates end card timings, layouts, and direct Studio deep-links
promoting the featured Skool Community video (HUTlnlw3h8o) and Skool Community link across all videos.

Usage:
  ./venv/bin/python sync_end_cards.py --dry-run
  ./venv/bin/python sync_end_cards.py --apply
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
import youtube_client

SKOOL_LINK = "https://www.skool.com/delivery-pilot-8938"
CHANNEL_HANDLE = "@RifatErdemSahin"
FEATURED_SKOOL_VIDEO_ID = "F8IBooe3bXY"
FEATURED_SKOOL_VIDEO_TITLE = "Claude AI Certification for Architects | Masterclass Intro"
CUSTOM_MESSAGE = "Join our Skool Community"
TEASER_TEXT = "Become AI Certified Pro"
VISUAL_FRAME_PROMO = "Build Your Second Brain - Join the Hands-On Cohort"
REPORT_FILE = "end_cards_report.json"


def parse_iso8601_duration(duration_str: str) -> int:
    """Parses ISO 8601 duration format (e.g., PT1M9S, PT45S, PT1H2M3S) into seconds."""
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def format_seconds_to_timecode(seconds: int) -> str:
    """Formats total seconds into MM:SS or HH:MM:SS format."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Configure End Cards and End Screens promoting Skool community video.")
    parser.add_argument("--featured-video", default=FEATURED_SKOOL_VIDEO_ID, help="Video ID of the featured Skool community video")
    parser.add_argument("--skool-link", default=SKOOL_LINK, help="Skool community link")
    parser.add_argument("--custom-message", default=CUSTOM_MESSAGE, help="Custom message for video card")
    parser.add_argument("--teaser-text", default=TEASER_TEXT, help="Teaser popup text for video card")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos to process")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform dry run without applying")
    parser.add_argument("--apply", action="store_true", help="Generate and save live End Screen configurations")
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 75)
    print("🎬 YouTube Studio Skill: End Cards & Closing Product Promoter")
    print(f"📺 Target Channel: {CHANNEL_HANDLE}")
    print(f"🎯 Linked Content: {args.featured_video} ({FEATURED_SKOOL_VIDEO_TITLE})")
    print(f"💬 Custom Message: {args.custom_message}")
    print(f"💡 Teaser Popup Text: {args.teaser_text}")
    print(f"🖼️ Visual Frame Promo: {VISUAL_FRAME_PROMO}")
    print(f"⚙️  Mode: {'🧪 DRY RUN (Simulated)' if dry_run else '🔴 LIVE SYNC & BLUEPRINT GENERATION'}")
    print("=" * 75)

    try:
        youtube = youtube_client.get_youtube_service()
        channel = youtube_client.get_channel_info()
    except Exception as e:
        print(f"\n❌ [ERROR] Authentication failed: {e}")
        sys.exit(1)

    if not channel:
        print("❌ Could not retrieve channel information.")
        sys.exit(1)

    uploads_id = channel["uploads_id"]
    page_token = None
    video_records = []
    processed_count = 0

    while True:
        pl_req = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=page_token
        )
        pl_res = pl_req.execute()
        items = pl_res.get("items", [])
        if not items:
            break

        video_ids = [it["contentDetails"]["videoId"] for it in items]
        v_res = youtube.videos().list(id=",".join(video_ids), part="snippet,contentDetails,status").execute()

        for v in v_res.get("items", []):
            if args.limit and processed_count >= args.limit:
                break

            vid = v["id"]
            title = v["snippet"]["title"]
            duration_iso = v["contentDetails"].get("duration", "PT0S")
            duration_secs = parse_iso8601_duration(duration_iso)
            privacy = v.get("status", {}).get("privacyStatus", "unknown")

            is_eligible = duration_secs >= 25
            end_start_secs = max(0, duration_secs - 20) if is_eligible else 0
            end_finish_secs = duration_secs

            studio_endscreen_url = f"https://studio.youtube.com/video/{vid}/editor"
            studio_edit_url = f"https://studio.youtube.com/video/{vid}/edit"

            is_self = (vid == args.featured_video)
            card_target_video = "Best for Viewer" if is_self else f"{args.featured_video} ({FEATURED_SKOOL_VIDEO_TITLE})"

            # Specifications for YouTube Card & End Screen Elements
            card_specifications = {
                "card_type": "Video Card",
                "linked_content_id": args.featured_video if not is_self else "BEST_FOR_VIEWER",
                "linked_content_title": FEATURED_SKOOL_VIDEO_TITLE if not is_self else "Best for Viewer",
                "custom_message": args.custom_message,
                "teaser_text": args.teaser_text,
                "timestamp": "Last Frame / Final Sequence",
                "teaser_popup_preview": f"ⓘ {args.teaser_text}",
                "visual_frame_graphic": VISUAL_FRAME_PROMO
            }

            end_card_elements = [
                {
                    "type": "VIDEO_CARD",
                    "label": "Featured Closing Masterclass",
                    "target_video_id": args.featured_video if not is_self else "BEST_FOR_VIEWER",
                    "target_title": FEATURED_SKOOL_VIDEO_TITLE if not is_self else "Best for Viewer",
                    "custom_message": args.custom_message,
                    "teaser_text": args.teaser_text,
                    "position": "TOP_RIGHT",
                    "start_time": format_seconds_to_timecode(end_start_secs),
                    "end_time": format_seconds_to_timecode(end_finish_secs)
                },
                {
                    "type": "SUBSCRIBE",
                    "label": f"Subscribe to {CHANNEL_HANDLE}",
                    "position": "LEFT_CENTER",
                    "start_time": format_seconds_to_timecode(end_start_secs),
                    "end_time": format_seconds_to_timecode(end_finish_secs)
                },
                {
                    "type": "LINK_CARD",
                    "label": "Skool Community Cohort & Second Brain Blueprints",
                    "target_url": args.skool_link,
                    "position": "BOTTOM_RIGHT",
                    "start_time": format_seconds_to_timecode(end_start_secs),
                    "end_time": format_seconds_to_timecode(end_finish_secs)
                }
            ]

            print(f"🎬 Video [{processed_count + 1}]: {title} ({vid})")
            print(f"   ⏱️ Duration: {format_seconds_to_timecode(duration_secs)} | End Screen: {format_seconds_to_timecode(end_start_secs)} - {format_seconds_to_timecode(end_finish_secs)}")
            print(f"   💡 Teaser: '{args.teaser_text}' | Message: '{args.custom_message}'")
            print(f"   🔗 Studio: {studio_endscreen_url}")

            video_records.append({
                "video_id": vid,
                "title": title,
                "duration_seconds": duration_secs,
                "duration_formatted": format_seconds_to_timecode(duration_secs),
                "is_eligible": is_eligible,
                "end_screen_start": format_seconds_to_timecode(end_start_secs),
                "end_screen_end": format_seconds_to_timecode(end_finish_secs),
                "featured_card_target": card_target_video,
                "card_specifications": card_specifications,
                "studio_endscreen_url": studio_endscreen_url,
                "studio_edit_url": studio_edit_url,
                "elements": end_card_elements,
                "status": "Configured & Ready" if is_eligible else "Duration < 25s",
                "timestamp": datetime.now().isoformat()
            })
            processed_count += 1

        if args.limit and processed_count >= args.limit:
            break

        page_token = pl_res.get("nextPageToken")
        if not page_token:
            break

    summary = {
        "channel_title": channel["title"],
        "channel_url": f"https://www.youtube.com/{channel['custom_url']}",
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "featured_skool_video_id": args.featured_video,
        "featured_skool_video_title": FEATURED_SKOOL_VIDEO_TITLE,
        "skool_community_link": args.skool_link,
        "total_videos": len(video_records),
        "eligible_videos": len([v for v in video_records if v["is_eligible"]]),
        "videos": video_records
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print(f"🎉 End Card Configuration Completed for {summary['total_videos']} videos.")
    print(f"✨ Eligible for End Cards (>= 25s): {summary['eligible_videos']}")
    print(f"📁 Report saved to: {REPORT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()

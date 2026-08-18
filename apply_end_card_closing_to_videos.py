#!/usr/bin/env python3
"""
CLI Script to implement End Video Closing & Product Card callouts live across all YouTube videos.
Target Channel: https://www.youtube.com/@RifatErdemSahin (@RifatErdemSahin)

Usage:
  ./venv/bin/python apply_end_card_closing_to_videos.py --dry-run
  ./venv/bin/python apply_end_card_closing_to_videos.py --apply
"""

import argparse
import json
import os
import sys
from datetime import datetime
import youtube_client

FEATURED_VIDEO_ID = "F8IBooe3bXY"
FEATURED_VIDEO_TITLE = "Claude AI Certification for Architects | Masterclass Intro"
SKOOL_LINK = "https://www.skool.com/delivery-pilot-8938"
REPORT_FILE = "end_cards_implementation_report.json"

CLOSING_BLOCK_TEMPLATE = """
🎓 FEATURED CLOSING MASTERCLASS (End Screen Video Card)
👉 Claude AI Certification for Architects: https://youtu.be/F8IBooe3bXY
💡 Become AI Certified Pro · Join our Skool Community: https://www.skool.com/delivery-pilot-8938
🧠 Build Your Second Brain - Join the Hands-On Cohort
""".strip()

CLOSING_BLOCK_SELF = """
🚀 JOIN THE HANDS-ON COHORT & ACCESS BLUEPRINTS
👉 Join our Skool Community: https://www.skool.com/delivery-pilot-8938
💡 Become AI Certified Pro · Build Your Second Brain
""".strip()


def inject_closing_block(description: str, video_id: str) -> str:
    """Injects or updates the closing product card block in the video description."""
    block_to_use = CLOSING_BLOCK_SELF if video_id == FEATURED_VIDEO_ID else CLOSING_BLOCK_TEMPLATE
    
    # Check if closing block already present
    if "FEATURED CLOSING MASTERCLASS" in description or "Become AI Certified Pro" in description:
        return description  # Already matching
        
    # Append cleanly before tags or at the end
    cleaned = description.rstrip()
    new_desc = f"{cleaned}\n\n{block_to_use}"
    
    # Respect YouTube 5000 character limit
    if len(new_desc) > 4990:
        # Trim from middle/bottom to stay within 4980 chars
        new_desc = new_desc[:4975].rsplit("\n", 1)[0] + f"\n\n{block_to_use}"
        if len(new_desc) > 4990:
            new_desc = new_desc[:4980]
            
    return new_desc


def main():
    parser = argparse.ArgumentParser(description="Apply End Card & Closing Product placement live across videos.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos to update")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform dry run")
    parser.add_argument("--apply", action="store_true", help="Apply updates live to YouTube")
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 75)
    print("🎬 YouTube Studio Live Implementation: End Video Closing & Product Cards")
    print(f"📺 Target Channel: @RifatErdemSahin")
    print(f"🎯 Featured Product: {FEATURED_VIDEO_ID} ({FEATURED_VIDEO_TITLE})")
    print(f"⚙️  Mode: {'🧪 DRY RUN (Simulated)' if dry_run else '🔴 LIVE UPDATE (Applying to YouTube)'}")
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
    results = []
    count = 0

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
            if args.limit and count >= args.limit:
                break

            vid = v["id"]
            title = v["snippet"]["title"]
            desc = v["snippet"].get("description", "")
            duration_iso = v["contentDetails"].get("duration", "PT0S")
            
            new_desc = inject_closing_block(desc, vid)

            if new_desc == desc:
                status = "already_matching"
                print(f"  ⏭️  [MATCH] {title} ({vid}) - Closing callout already present.")
            else:
                status = "updated" if not dry_run else "would_update"
                print(f"  ✏️  [{'WOULD UPDATE' if dry_run else 'UPDATING'}] {title} ({vid})")
                if not dry_run:
                    v["snippet"]["description"] = new_desc
                    youtube.videos().update(
                        part="snippet",
                        body={"id": vid, "snippet": v["snippet"]}
                    ).execute()
                    print(f"  ✅ [SUCCESS] Video updated with closing product card.")

            results.append({
                "video_id": vid,
                "title": title,
                "duration": duration_iso,
                "status": status,
                "featured_product": FEATURED_VIDEO_ID,
                "studio_editor_url": f"https://studio.youtube.com/video/{vid}/editor",
                "timestamp": datetime.now().isoformat()
            })
            count += 1

        if args.limit and count >= args.limit:
            break

        page_token = pl_res.get("nextPageToken")
        if not page_token:
            break

    summary = {
        "channel_title": channel["title"],
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "total_checked": len(results),
        "total_updated": len([r for r in results if r["status"] in ("updated", "would_update")]),
        "already_matching": len([r for r in results if r["status"] == "already_matching"]),
        "featured_product_id": FEATURED_VIDEO_ID,
        "featured_product_title": FEATURED_VIDEO_TITLE,
        "results": results
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 75)
    print(f"🎉 Implementation Completed for {summary['total_checked']} Videos!")
    print(f"✨ Updated Live: {summary['total_updated']} | Already Matching: {summary['already_matching']}")
    print(f"📁 Report saved to: {REPORT_FILE}")
    print("=" * 75)


if __name__ == "__main__":
    main()

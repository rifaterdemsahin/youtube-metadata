#!/usr/bin/env python3
"""
CLI Script to ensure the first 2 lines of YouTube video descriptions are dedicated to a high-converting Skool CTA.
Target Channel: https://www.youtube.com/@RifatErdemSahin (@RifatErdemSahin)

Usage:
  ./venv/bin/python update_first_lines_skool.py --dry-run
  ./venv/bin/python update_first_lines_skool.py --apply
  ./venv/bin/python update_first_lines_skool.py --apply --limit 2
"""

import argparse
import json
import os
import sys
from datetime import datetime
import youtube_client

SKOOL_LINK_DEFAULT = "https://www.skool.com/delivery-pilot-8938"
CHANNEL_HANDLE_DEFAULT = "@RifatErdemSahin"
DEFAULT_CTA_LINE_1 = "🚀 Join our AI Architect & Builder Community: https://www.skool.com/delivery-pilot-8938"
REPORT_FILE = "first_lines_report.json"


def format_description_with_cta(original_desc: str, cta_line_1: str) -> str:
    """
    Ensures the top 2 lines contain the primary Skool CTA link while respecting YouTube's 5000 char limit.
    """
    lines = original_desc.splitlines()
    
    # Check if the first line or second line already starts with Skool link / CTA
    top_block = "\n".join(lines[:3]) if len(lines) >= 3 else "\n".join(lines)
    
    if "skool.com" in top_block.lower():
        # Already has skool link in the first few lines
        if lines and lines[0].strip() == cta_line_1.strip():
            return original_desc
        lines[0] = cta_line_1
        return "\n".join(lines)
    
    # If not in top lines, prepend CTA as line 1 followed by an empty line
    cleaned_original = original_desc.strip()
    
    # Check if bottom has duplicate Skool footer and clean it if needed to save space
    bottom_patterns = [
        "\n\n🚀 Join our AI Builders & Architects Community:\n👉 https://www.skool.com/delivery-pilot-8938",
        "\n\n🚀 Join our AI Architect & Builder Community:\n👉 https://www.skool.com/delivery-pilot-8938",
        "\n\n🚀 Join our AI Architect & Builder Community on Skool:\n👉 https://www.skool.com/delivery-pilot-8938",
        "\n🚀 Join our AI Builders & Architects Community:\n👉 https://www.skool.com/delivery-pilot-8938"
    ]
    for pattern in bottom_patterns:
        if cleaned_original.endswith(pattern.strip()):
            cleaned_original = cleaned_original[:-len(pattern.strip())].rstrip()
    
    result = f"{cta_line_1}\n\n{cleaned_original}"
    
    # YouTube character limit is 5000 characters
    if len(result) > 4990:
        result = result[:4980].rsplit("\n", 1)[0]
        
    return result



def main():
    parser = argparse.ArgumentParser(description="Ensure first 2 lines of video descriptions feature Skool CTA.")
    parser.add_argument("--cta", default=DEFAULT_CTA_LINE_1, help="First line Call-To-Action text")
    parser.add_argument("--link", default=SKOOL_LINK_DEFAULT, help="The Skool link to promote")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos to process")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform a dry run without modifying YouTube")
    parser.add_argument("--apply", action="store_true", help="Apply changes live to YouTube")
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 70)
    print("📌 YouTube Studio Skill: Top 2 Lines Skool CTA Description Syncer")
    print(f"📺 Target Channel: {CHANNEL_HANDLE_DEFAULT}")
    print(f"⚙️  Mode: {'🧪 DRY RUN (Simulated)' if dry_run else '🔴 LIVE UPDATE (Applying changes)'}")
    if args.limit:
        print(f"🔢 Limit: Maximum {args.limit} video(s)")
    print(f"🎯 Header Line 1 CTA:\n{args.cta}")
    print("=" * 70)

    try:
        youtube = youtube_client.get_youtube_service()
        channel = youtube_client.get_channel_info()
    except Exception as e:
        print(f"\n❌ [ERROR] Authentication failed: {e}")
        sys.exit(1)

    if not channel:
        print("❌ Could not retrieve channel information.")
        sys.exit(1)

    print(f" Connected to channel: '{channel['title']}' ({channel['custom_url']})")

    uploads_id = channel["uploads_id"]
    page_token = None
    processed_count = 0
    results = []

    while True:
        pl_req = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet,contentDetails",
            maxResults=min(50, args.limit) if args.limit else 50,
            pageToken=page_token
        )
        pl_res = pl_req.execute()
        items = pl_res.get("items", [])
        if not items:
            break

        video_ids = [it["contentDetails"]["videoId"] for it in items]
        v_res = youtube.videos().list(id=",".join(video_ids), part="snippet,status").execute()

        for v in v_res.get("items", []):
            if args.limit and processed_count >= args.limit:
                break

            vid = v["id"]
            title = v["snippet"]["title"]
            desc = v["snippet"].get("description", "")
            privacy = v.get("status", {}).get("privacyStatus", "unknown")

            new_desc = format_description_with_cta(desc, args.cta)

            if new_desc == desc:
                status = "already_matching"
                print(f"  ⏭️  [MATCH] {title} ({vid}) - Top lines already match CTA.")
            else:
                status = "would_update" if dry_run else "updated"
                print(f"  ✏️  [{'WOULD UPDATE' if dry_run else 'UPDATING'}] {title} ({vid})")
                if not dry_run:
                    v["snippet"]["description"] = new_desc
                    youtube.videos().update(
                        part="snippet",
                        body={"id": vid, "snippet": v["snippet"]}
                    ).execute()
                    print(f"  ✅ [SUCCESS] Description updated with top CTA.")

            results.append({
                "video_id": vid,
                "title": title,
                "privacy": privacy,
                "status": status,
                "first_line": new_desc.splitlines()[0] if new_desc else "",
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
        "cta_line": args.cta,
        "total_processed": len(results),
        "updated_count": len([r for r in results if r["status"] in ("updated", "would_update")]),
        "matching_count": len([r for r in results if r["status"] == "already_matching"]),
        "results": results
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print(f"🎉 Completed processing {summary['total_processed']} videos.")
    print(f"✨ Updated / Formatted: {summary['updated_count']} | Already Matching: {summary['matching_count']}")
    print(f"📁 Report written to: {REPORT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CLI Script to create or update pinned/featured comments promoting the Skool community across YouTube videos.
Target Channel: https://www.youtube.com/@RifatErdemSahin (@RifatErdemSahin)

Usage:
  ./venv/bin/python sync_pinned_comments.py --dry-run
  ./venv/bin/python sync_pinned_comments.py --apply
  ./venv/bin/python sync_pinned_comments.py --apply --limit 2
"""

import argparse
import json
import os
import sys
from datetime import datetime
import youtube_client

SKOOL_LINK_DEFAULT = "https://www.skool.com/delivery-pilot-8938"
CHANNEL_HANDLE_DEFAULT = "@RifatErdemSahin"
DEFAULT_COMMENT_TEXT = (
    "🚀 Join our AI Architect & Builder Community on Skool to access full masterclasses, "
    "blueprints, cohort materials & live sessions:\n"
    "👉 https://www.skool.com/delivery-pilot-8938"
)
REPORT_FILE = "pinned_comments_report.json"


def main():
    parser = argparse.ArgumentParser(description="Create or update featured Skool promo comments on YouTube videos.")
    parser.add_argument("--comment", default=DEFAULT_COMMENT_TEXT, help="The comment text to post/update")
    parser.add_argument("--link", default=SKOOL_LINK_DEFAULT, help="The Skool link to promote")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos to process")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform a dry run without modifying YouTube")
    parser.add_argument("--apply", action="store_true", help="Apply changes live to YouTube")
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 70)
    print("💬 YouTube Studio Skill: Pinned / Featured Comments Skool Promoter")
    print(f"📺 Target Channel: {CHANNEL_HANDLE_DEFAULT}")
    print(f"⚙️  Mode: {'🧪 DRY RUN (Simulated)' if dry_run else '🔴 LIVE UPDATE (Applying changes)'}")
    if args.limit:
        print(f"🔢 Limit: Maximum {args.limit} video(s)")
    print(f"📝 Comment Copy:\n{args.comment}")
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

    print(f" Connected to channel: '{channel['title']}' ({channel['custom_url']}) [ID: {channel['id']}]")

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

        for item in items:
            if args.limit and processed_count >= args.limit:
                break

            vid = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]

            print(f"\n🎬 Processing Video [{processed_count + 1}]: {title} ({vid})")

            # Check existing comments
            comments = youtube_client.list_video_comments(vid, max_results=20)
            owner_comment = None
            for c in comments:
                top_snippet = c.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                author_id = top_snippet.get("authorChannelId", {}).get("value")
                text = top_snippet.get("textOriginal", "")
                if author_id == channel["id"]:
                    owner_comment = {
                        "id": c.get("snippet", {}).get("topLevelComment", {}).get("id"),
                        "text": text
                    }
                    break

            if owner_comment:
                action_needed = "update"
                current_text = owner_comment["text"]
                if current_text.strip() == args.comment.strip():
                    status = "already_matching"
                    print(f"  ✨ [MATCH] Owner comment already contains the exact copy.")
                else:
                    status = "would_update" if dry_run else "updated"
                    print(f"  🔄 [{'WOULD UPDATE' if dry_run else 'UPDATING'}] Existing comment ({owner_comment['id']})")
                    if not dry_run:
                        youtube.comments().update(
                            part="snippet",
                            body={"id": owner_comment["id"], "snippet": {"textOriginal": args.comment}}
                        ).execute()
                        print(f"  ✅ [SUCCESS] Comment updated.")
            else:
                action_needed = "create"
                status = "would_create" if dry_run else "created"
                print(f"  ➕ [{'WOULD CREATE' if dry_run else 'CREATING'}] New top-level promo comment.")
                if not dry_run:
                    new_cmt = youtube.commentThreads().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "videoId": vid,
                                "topLevelComment": {"snippet": {"textOriginal": args.comment}}
                            }
                        }
                    ).execute()
                    print(f"  ✅ [SUCCESS] Comment posted with ID: {new_cmt.get('id')}")

            results.append({
                "video_id": vid,
                "title": title,
                "action": action_needed,
                "status": status,
                "existing_comment_id": owner_comment["id"] if owner_comment else None,
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
        "total_processed": len(results),
        "created_count": len([r for r in results if r["status"] in ("created", "would_create")]),
        "updated_count": len([r for r in results if r["status"] in ("updated", "would_update")]),
        "matching_count": len([r for r in results if r["status"] == "already_matching"]),
        "results": results
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print(f"🎉 Completed processing {summary['total_processed']} videos.")
    print(f"✨ Created: {summary['created_count']} | Updated: {summary['updated_count']} | Already Matching: {summary['matching_count']}")
    print(f"📁 Report written to: {REPORT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()

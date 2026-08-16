#!/usr/bin/env python3
"""
CLI Utility to update YouTube video metadata (title, description, tags, privacy status)
and upload custom thumbnails.

Usage:
  ./venv/bin/python update_video_metadata_cli.py l7bc8KTOyMo \
    --title "My Video Title" \
    --description-file my_desc.txt \
    --thumbnail thumbnails/my_thumb.jpg \
    --privacy unlisted \
    --append-skool
"""

import argparse
import sys
import os
import youtube_client

SKOOL_LINK_DEFAULT = "https://www.skool.com/delivery-pilot-8938"
SKOOL_PREFIX_DEFAULT = "\n\n🚀 Join our AI Builders & Architects Community:\n👉 "

def main():
    parser = argparse.ArgumentParser(description="Update YouTube video metadata and thumbnails.")
    parser.add_argument("video_id", help="11-character YouTube video ID or URL")
    parser.add_argument("--title", help="New video title")
    parser.add_argument("--description", help="New video description text")
    parser.add_argument("--description-file", help="Path to text file containing video description")
    parser.add_argument("--tags", help="Comma-separated tags (e.g. 'AI,Obsidian,Gemini')")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], help="Update privacy status")
    parser.add_argument("--thumbnail", help="Path to custom thumbnail JPG/PNG image")
    parser.add_argument("--append-skool", action="store_true", help="Ensure Skool community link is appended")
    parser.add_argument("--skool-link", default=SKOOL_LINK_DEFAULT, help="Custom Skool community URL")

    args = parser.parse_args()

    # Extract clean video ID if URL was passed
    video_id = args.video_id
    if "youtube.com" in video_id or "youtu.be" in video_id:
        import re
        m = re.search(r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', video_id)
        if m:
            video_id = m.group(1)

    print("=" * 60)
    print(f"🎬 YouTube Studio Updater for Video ID: {video_id}")
    print("=" * 60)

    # Determine description
    desc = args.description
    if args.description_file:
        if not os.path.exists(args.description_file):
            print(f"❌ Description file not found: {args.description_file}")
            sys.exit(1)
        with open(args.description_file, "r", encoding="utf-8") as f:
            desc = f.read()

    if args.append_skool and desc is not None:
        if args.skool_link not in desc:
            desc = desc.rstrip() + SKOOL_PREFIX_DEFAULT + args.skool_link

    # Parse tags
    tags_list = None
    if args.tags:
        tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]

    # Update metadata if any field is provided
    if any([args.title is not None, desc is not None, tags_list is not None, args.privacy is not None]):
        print("📝 Updating video metadata...")
        res = youtube_client.update_video_metadata(
            video_id=video_id,
            title=args.title,
            description=desc,
            tags=tags_list,
            privacy_status=args.privacy
        )
        if res.get("error"):
            print(f"❌ Metadata update failed: {res['error']}")
            sys.exit(1)
        print("✅ Metadata updated successfully:")
        print(f"   • Title: {res.get('title')}")
        print(f"   • Privacy: {res.get('privacy_status')}")

    # Upload thumbnail if provided
    if args.thumbnail:
        print(f"\n🖼️  Uploading custom thumbnail: {args.thumbnail}...")
        thumb_res = youtube_client.update_video_thumbnail(
            video_id=video_id,
            image_file_path=args.thumbnail
        )
        if thumb_res.get("error"):
            print(f"❌ Thumbnail upload failed: {thumb_res['error']}")
            sys.exit(1)
        print("✅ Thumbnail uploaded and set successfully!")

    print("\n🎉 Done!")


if __name__ == "__main__":
    main()

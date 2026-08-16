#!/usr/bin/env python3
"""
CLI Utility to fetch and extract clean transcripts from any YouTube video URL or Video ID.

Usage:
  ./venv/bin/python fetch_transcript.py https://www.youtube.com/watch?v=l7bc8KTOyMo
  ./venv/bin/python fetch_transcript.py l7bc8KTOyMo --output transcripts/l7bc8KTOyMo.txt
"""

import argparse
import os
import re
import subprocess
import sys
import glob

TRANSCRIPTS_DIR = "transcripts"

def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube 11-char video ID from various URL formats or raw ID."""
    if len(url_or_id) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    match = re.search(r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)
    return url_or_id


def parse_vtt_to_clean_text(vtt_file_path: str) -> str:
    """Parses a WebVTT file, strips cues/tags/duplicates, and returns clean transcript text."""
    with open(vtt_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all subtitle cue bodies
    cues = re.findall(
        r'(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n)(.*?)(?=\n\d{2}:\d{2}:\d{2}\.\d{3}|\Z)',
        content,
        re.DOTALL
    )

    full_text_pieces = []
    last_text = ""
    for time_header, cue_body in cues:
        clean = re.sub(r'<[^>]+>', '', cue_body).strip()
        lines = [line.strip() for line in clean.split('\n') if line.strip()]
        for line in lines:
            if line != last_text:
                full_text_pieces.append(line)
                last_text = line

    return " ".join(full_text_pieces)


def fetch_transcript(video_input: str, output_file: str = None) -> str:
    """Fetches auto-subs or manual captions for a video and returns clean text."""
    video_id = extract_video_id(video_input)
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    temp_prefix = os.path.join(TRANSCRIPTS_DIR, f"temp_{video_id}")

    print(f"🎬 Fetching transcript for video ID: {video_id} ({video_url})...")

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--write-auto-subs",
        "--write-subs",
        "--skip-download",
        "--sub-lang", "en,en-GB,en-US",
        "-o", f"{temp_prefix}.%(ext)s",
        video_url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check for downloaded vtt files
    vtt_candidates = glob.glob(f"{temp_prefix}*.vtt")
    if not vtt_candidates:
        print(f"⚠️  No subtitles found or yt-dlp error: {result.stderr}")
        return ""

    vtt_file = vtt_candidates[0]
    clean_text = parse_vtt_to_clean_text(vtt_file)

    # Clean up temp vtt
    for f in vtt_candidates:
        try:
            os.remove(f)
        except OSError:
            pass

    out_path = output_file or os.path.join(TRANSCRIPTS_DIR, f"{video_id}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"✅ Clean transcript saved to: {out_path}\n")
    return clean_text


def main():
    parser = argparse.ArgumentParser(description="Fetch and extract YouTube video transcripts.")
    parser.add_argument("video", help="YouTube video URL or Video ID")
    parser.add_argument("--output", "-o", default=None, help="Optional output text file path")
    args = parser.parse_args()

    text = fetch_transcript(args.video, args.output)
    if text:
        print("=" * 60)
        print("📜 EXTRACTED TRANSCRIPT:")
        print("=" * 60)
        print(text)
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

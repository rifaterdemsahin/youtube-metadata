---
name: youtube-thumbnails
description: >-
  Create, edit, upload, and preview YouTube thumbnails for @RifatErdemSahin.
  Use when generating or updating a video thumbnail, custom thumb, Shorts cover,
  or running thumbnail-tester.html.
---

# YouTube thumbnails

## Always show the image

When you **create** or **update** a thumbnail, display it in the chat in that same turn.

1. Save the file under `thumbnails/thumbnail_<VIDEO_ID>.jpg`.
2. **Archive in this repo, then commit and push.** Add the custom jpg plus any first-frame still (`frame_<VIDEO_ID>.jpg`) and live verify copy (`live_<VIDEO_ID>.jpg`). Update `thumbnails/archive.json`. Do not commit per-second dumps (`frame_<id>_01.jpg` …) or 404 stub JPEGs.
3. `read_file` that path so the image renders for the user.
4. Upload: `./venv/bin/python update_video_metadata_cli.py <id> --thumbnail thumbnails/thumbnail_<id>.jpg`
5. **Verify on YouTube.** Download the live `maxresdefault` (cache-bust with `?t=`) to `thumbnails/live_<VIDEO_ID>.jpg` and `read_file` it. Compare to the local jpg. API `thumbnails.set` returning success is not enough — Shorts often keep an auto frame.
6. If the live image is not the custom thumb, **ask the user to upload it in Studio** and give the file path plus `https://studio.youtube.com/video/<id>/editing`. Do not claim the cover is live.

Do not only report a path. The user must see the actual frame (local, then live). Always leave the custom jpg in git.

## Shorts layout

YouTube Shorts **center-crops** 16:9 thumbs to 9:16. Put hook type in the **center third** (stacked, on a dark plate). Do not park titles on the left or right edge.

Preview crops in `thumbnail-tester.html` (`open -a "Google Chrome"`).

## Upload

```bash
./venv/bin/python update_video_metadata_cli.py VIDEO_ID --thumbnail thumbnails/thumbnail_VIDEO_ID.jpg
```

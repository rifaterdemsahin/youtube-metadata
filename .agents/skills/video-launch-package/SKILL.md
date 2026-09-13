---
name: video-launch-package
description: >-
  Builds and ships a full YouTube video launch package: title, description, pinned comment,
  and 3 thumbnail variants (for A/B testing), then pushes them live via the YouTube Data API
  and publishes a shareable review page with copy-to-clipboard buttons.
  Use when the user gives a video URL/ID + script and asks for a title, description,
  thumbnail, and/or pinned comment, or asks to "package"/"launch" a video.
---

# Skill: YouTube Video Launch Package

End-to-end workflow for turning a video script into a published, ready-to-review metadata
package for `@RifatErdemSahin`.

## 🎯 What it produces
1. **Title** — punchy, names the hook, matches channel's contrarian-but-substantiated tone.
2. **Description** — follows the existing convention in `descriptions/*.txt`:
   Skool link at top → hook paragraphs → `WHAT THIS VIDEO COVERS` bullets →
   `KEY TAKEAWAY` → `RESOURCES` → hashtags → Skool link again at bottom.
3. **Pinned comment** — restates the core hook as a question to drive replies, ends with the
   Skool community link. Note: the YouTube Data API cannot programmatically *pin* a comment —
   it can only create/update it. Actual pinning is a manual Studio action.
4. **3 thumbnail variants** (always 3, for A/B testing — see [[thumbnail_ab_testing_rule]] memory):
   distinct compositions/hooks, not near-duplicates. Never depict a real, identifiable person
   (e.g. a specific public figure) — use silhouettes/anonymous figures/abstracted concepts instead.

## 🔑 Getting API keys

Prefer pulling secrets from Azure Key Vault over asking the user to paste them
(see [[azure_keyvault_secrets]] memory):

```bash
# fal.ai key for thumbnail generation
export FAL_KEY=$(az keyvault secret show --vault-name dp-kv-deliverypilot --name FAL-AI-KEY --query value -o tsv)
```

YouTube OAuth (`client_secret.json` / `token.json`) — usually already present in the repo root;
if missing, fetch from Key Vault:
```bash
./venv/bin/python fetch_azure_secrets.py --vault dp-kv-deliverypilot
```

## 🚀 Execution steps

### 1. Generate thumbnails (3 variants)
```bash
python3 /Users/rifaterdemsahin/.claude/skills/image-generation/generate_image.py \
  --prompt "<variant prompt>" --model nano-banana-pro \
  --width 1280 --height 720 \
  --output thumbnails/<VIDEO_ID>_thumb_a.png
# repeat for _b and _c with genuinely different hooks/compositions
```
Review each generated image before shipping — check for accidental real-person likeness.

### 2. Write the description file
Save to `descriptions/<VIDEO_ID>.txt` following the format above (see any existing file in
`descriptions/` for the exact template).

### 3. Push title, description, and thumbnail A live
```bash
./venv/bin/python update_video_metadata_cli.py <VIDEO_ID> \
  --title "<title>" \
  --description-file descriptions/<VIDEO_ID>.txt \
  --thumbnail thumbnails/<VIDEO_ID>_thumb_a.png
```

### 4. Post the pinned comment
```bash
./venv/bin/python -c "
import youtube_client
res = youtube_client.create_or_update_video_comment('<VIDEO_ID>', '''<comment text>''')
print(res)
"
```
If this fails with `commentsDisabled`, tell the user comments are off for the video — enabling
them is a manual Studio setting, not an API call.

### 5. Publish the review page
Build one HTML page (via the Artifact tool) that shows: title, description, pinned comment
(with a note if posting failed), and all 3 thumbnails side by side, each with a **Copy** button
next to Title/Description/Pinned Comment for manual pasting. Load `artifact-design` first.
Pass the 3 thumbnail PNGs via the `files` param so they render inline. Include a note that
YouTube's thumbnail A/B test itself must be started manually in Studio (Content → video →
Details → thumbnail test icon) since the Data API doesn't expose it.

### 6. Archive a local copy and open it
Also save a standalone copy to `archive/<VIDEO_ID>_video_package.html` — see
[[archive_page_and_local_server_rule]] memory. This is a full `<!doctype html>` document
(the Artifact is a body-only fragment), with image paths fixed to `../thumbnails/...` and a
link back to the live Artifact URL. Then serve and open it:
```bash
(python3 -m http.server 8765 > /tmp/yt_archive_server.log 2>&1 &)
open -a "Google Chrome" "http://localhost:8765/archive/<VIDEO_ID>_video_package.html"
```

## 📌 Conventions to reuse
- Skool link: `https://www.skool.com/delivery-pilot-8938`
- Description template lives implicitly in `descriptions/*.txt` — read 1-2 existing files
  before writing a new one to match tone/structure.
- `youtube_client.py` has all the API primitives (`update_video_metadata`,
  `update_video_thumbnail`, `create_or_update_video_comment`, `list_video_comments`).
  `update_video_metadata_cli.py` wraps title/description/thumbnail/playlist in one call.

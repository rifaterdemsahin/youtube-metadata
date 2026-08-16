# YouTube Studio MCP & Metadata Manager — Operations Guide

This guide explains how the system works end-to-end and the steps to execute live updates or use the MCP server in Claude Desktop / Cursor.

---

## 🏗️ Architecture & How It Works

```
Google Cloud OAuth (Desktop) ──► Azure Key Vault (dp-kv-deliverypilot)
                                             │
                                             ▼
                       Local Workspace (/youtube-metadata)
                       ├── token.json (Auto-refreshing OAuth)
                       ├── client_secret.json
                       ├── server.py (FastMCP stdio server)
                       └── append_skool_link.py (Bulk updater)
                                             │
                                             ▼
                                  YouTube Data API v3
```

---

## 📋 Steps to Complete & Operate

### Step 1: Run Live Description Updates
To apply your Skool community link (`https://www.skool.com/delivery-pilot-8938`) to all video descriptions:

```bash
cd /Users/rifaterdemsahin/projects/youtube-metadata
./venv/bin/python append_skool_link.py --apply
```
- The script checks each video description.
- If the Skool link is already present, it skips it safely.
- If not present, it appends the link and updates the video on YouTube.

---

### Step 2: Enable MCP Server in Claude Desktop / Cursor

Add this block to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "/Users/rifaterdemsahin/projects/youtube-metadata/venv/bin/python3",
      "args": [
        "/Users/rifaterdemsahin/projects/youtube-metadata/server.py"
      ],
      "env": {
        "YOUTUBE_CLIENT_SECRET_FILE": "/Users/rifaterdemsahin/projects/youtube-metadata/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "/Users/rifaterdemsahin/projects/youtube-metadata/token.json"
      }
    }
  }
}
```

#### Available MCP Tools in Claude / Cursor:
- `check_auth_status`: Check connection to your channel.
- `list_videos`: Fetch uploaded videos, view counts, and metadata.
- `update_video`: Edit titles, tags, descriptions, and privacy.
- `set_thumbnail`: Upload custom thumbnails.
- `append_link_to_all_descriptions`: Batch add links across descriptions with dry-run support.

---

### Step 3: Restore or Deploy on Any New Machine

All credentials and tokens are securely stored in Azure Key Vault. On any fresh machine, run:

```bash
git clone https://github.com/rifaterdemsahin/youtube-metadata.git
cd youtube-metadata
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python fetch_azure_secrets.py --vault dp-kv-deliverypilot
```
No re-authentication or Google sign-in required.

### Step 4: Extract Video Transcripts
To extract and clean captions/subtitles from any YouTube video URL or ID:

```bash
./venv/bin/python fetch_transcript.py <VIDEO_URL_OR_ID>
# Example:
./venv/bin/python fetch_transcript.py https://www.youtube.com/watch?v=l7bc8KTOyMo
```
This saves the clean, timestamp-free transcript in `transcripts/<VIDEO_ID>.txt`.

---

### Step 5: Update Video Title, Description, Tags & Upload Custom Thumbnail
To update a single video's metadata and apply a custom 16:9 thumbnail while setting/preserving privacy:

```bash
./venv/bin/python update_video_metadata_cli.py <VIDEO_ID> \
  --title "Your Video Title" \
  --description "Your Description" \
  --tags "Obsidian,AI,Claude" \
  --privacy unlisted \
  --thumbnail thumbnails/your_thumbnail.jpg \
  --append-skool
```

---

## 🌐 Live Operations Dashboard & Pages
- **Operations Dashboard**: [http://localhost:8888/index.html](http://localhost:8888/index.html)
- **Thumbnails & Video Studio**: [http://localhost:8888/thumbnails.html](http://localhost:8888/thumbnails.html)
- **Video Catalog & Notes**: [http://localhost:8888/catalog.html](http://localhost:8888/catalog.html)
- **Applied Updates Log**: [http://localhost:8888/updates.html](http://localhost:8888/updates.html)
- **GitHub Pages**: [https://rifaterdemsahin.github.io/youtube-metadata/](https://rifaterdemsahin.github.io/youtube-metadata/)

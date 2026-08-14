# YouTube Studio MCP Server & Metadata Manager

A Python-based **Model Context Protocol (MCP)** server and automated metadata updater for YouTube Studio, built using the official `google-api-python-client` with YouTube Data API v3 and FastMCP.

---

## 🌟 Features

- **MCP Tools for Claude Desktop & Cursor**:
  - `check_auth_status`: Validate OAuth2 authentication and channel access.
  - `list_videos`: Fetch all uploaded videos, metadata, statistics, and thumbnails.
  - `update_video`: Edit video title, description, tags, category, and privacy status.
  - `set_thumbnail`: Upload custom high-res video thumbnails.
  - `append_link_to_all_descriptions`: Batch append community/promotional links (such as Skool) across all channel videos with dry-run support.
- **Local OAuth 2.0 Management**: Supports `client_secret.json` and persistent `token.json` token refresh.
- **Bulk Metadata CLI Script**: `append_skool_link.py` to batch-append your [Skool Community link](https://www.skool.com/delivery-pilot-8938) to all videos with simulation and report generation.
- **Visual Operations Dashboard**: `index.html` for tracking server configuration and update reports.

---

## 📦 Reference Repositories

- **Recommended MCP Base**: [i1s-abhishek/youtube-studio-mcp](https://github.com/i1s-abhishek/youtube-studio-mcp)
- **Official YouTube API Client**: [googleapis/google-api-python-client](https://github.com/googleapis/google-api-python-client)
- **FastMCP Protocol**: [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

---

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Google Cloud OAuth Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **YouTube Data API v3**.
3. Create OAuth 2.0 Credentials:
   - Application type: **Desktop App**
4. Download the JSON credential file and save it as **`client_secret.json`** in this project directory.

---

## 🔌 MCP Configuration (Claude Desktop & Cursor)

Add the following block to your MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "python3",
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

---

## 🎯 Batch Update: Append Skool Link to All Videos

To append `https://www.skool.com/delivery-pilot-8938` to all video descriptions:

### Dry-run (Preview without modifying):
```bash
python append_skool_link.py --dry-run
```

### Apply Live Changes:
```bash
python append_skool_link.py --apply
```

---

## 📊 Operations Dashboard

View the local reporting page:
- [index.html](file:///Users/rifaterdemsahin/projects/youtube-metadata/index.html)

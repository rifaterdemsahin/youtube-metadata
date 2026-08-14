# YouTube Studio MCP Server & Metadata Manager

A Python-based **Model Context Protocol (MCP)** server and automated metadata updater for YouTube Studio, built using the official `google-api-python-client` with YouTube Data API v3 and FastMCP.

---

## 📺 Configured YouTube Channel

- **Channel URL**: [https://www.youtube.com/@RifatErdemSahin](https://www.youtube.com/@RifatErdemSahin)
- **Channel Handle**: `@RifatErdemSahin`
- **Target Skool Community**: [https://www.skool.com/delivery-pilot-8938](https://www.skool.com/delivery-pilot-8938)

---

## 🌟 Features

- **MCP Tools for Claude Desktop & Cursor**:
  - `check_auth_status`: Validate OAuth2 authentication and channel access for `@RifatErdemSahin`.
  - `list_videos`: Fetch all uploaded videos, metadata, statistics, and thumbnails.
  - `update_video`: Edit video title, description, tags, category, and privacy status.
  - `set_thumbnail`: Upload custom high-res video thumbnails.
  - `append_link_to_all_descriptions`: Batch append community/promotional links (such as Skool) across all channel videos with dry-run support.
- **Local OAuth 2.0 Management**: Supports `client_secret.json` and persistent `token.json` token refresh with Azure Key Vault sync.
- **Bulk Metadata CLI Script**: `append_skool_link.py` to batch-append your Skool Community link to all videos with simulation and report generation.
- **Visual Operations Dashboard**: `index.html` for tracking server configuration and update reports.

---

## 📦 Reference Repositories

- **Recommended MCP Base**: [i1s-abhishek/youtube-studio-mcp](https://github.com/i1s-abhishek/youtube-studio-mcp)
- **Official YouTube API Client**: [googleapis/google-api-python-client](https://github.com/googleapis/google-api-python-client)
- **FastMCP Protocol**: [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

---

## 🔌 MCP Configuration (Claude Desktop & Cursor)

Add the following block to your MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

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

---

## 🎯 Batch Update: Append Skool Link to All Videos

Target Link: `https://www.skool.com/delivery-pilot-8938`

### Dry-run (Preview without modifying):
```bash
./venv/bin/python append_skool_link.py --dry-run
```

### Apply Live Changes:
```bash
./venv/bin/python append_skool_link.py --apply
```

---

## 📊 Operations Dashboard

View the local reporting page:
- [index.html](http://localhost:8080/index.html)

# Antigravity Operating Principles & Project Blueprint

## 🌌 Core Mandate
1. **Always Backup Before Changes**:
   - Before executing live metadata updates or structural codebase modifications, generate snapshot backups (e.g. JSON snapshots of channel videos, Git commits).
   - Maintain authorized OAuth token and client secret backups in Azure Key Vault (`dp-kv-deliverypilot`).

2. **Visual & Verification Protocol**:
   - Always open updated pages or modified YouTube videos in the default browser (Google Chrome) for visual/functional confirmation.
   - Display clickable links at the end of every response.

---

## 🛠️ YouTube Studio MCP & Metadata Ecosystem

- **Target Channel**: [https://www.youtube.com/@RifatErdemSahin](https://www.youtube.com/@RifatErdemSahin) (`@RifatErdemSahin`)
- **Target Skool Community**: [https://www.skool.com/delivery-pilot-8938](https://www.skool.com/delivery-pilot-8938)
- **Azure Key Vault**: `dp-kv-deliverypilot` (`youtube-client-secret`, `youtube-token`)
- **FastMCP Server**: [`server.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/server.py) (stdio transport for Claude Desktop & Cursor)
- **Bulk Metadata CLI**: [`append_skool_link.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/append_skool_link.py)
- **Azure Secrets Fetcher**: [`fetch_azure_secrets.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/fetch_azure_secrets.py)

---

## 📄 Application Pages
- **Operations Dashboard**: [`index.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/index.html)
- **End Video Closing Strategy**: [`endvideo.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/endvideo.html)
- **Live Execution Reports**: [`reports.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/reports.html)
- **Skills Studio & Automation**: [`skills.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/skills.html)
- **Video Catalog & Notes Editor**: [`catalog.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/catalog.html)
- **Playlists & Learning Paths**: [`playlists.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/playlists.html)
- **Thumbnails Studio**: [`thumbnails.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/thumbnails.html)
- **Analytics & Performance**: [`analytics.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/analytics.html)
- **Applied Updates Log**: [`updates.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/updates.html)
- **Live GitHub Pages**: [https://rifaterdemsahin.github.io/youtube-metadata/](https://rifaterdemsahin.github.io/youtube-metadata/)

---

## ⚡ Antigravity Skills & CLI Runbooks
- **Skill 1: Pinned Comments Promoter**: [`sync_pinned_comments.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/sync_pinned_comments.py) · [`.agents/skills/sync-pinned-comments-skool/SKILL.md`](file:///Users/rifaterdemsahin/projects/youtube-metadata/.agents/skills/sync-pinned-comments-skool/SKILL.md)
- **Skill 2: Top 2 Lines Skool CTA Syncer**: [`update_first_lines_skool.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/update_first_lines_skool.py) · [`.agents/skills/sync-first-lines-skool-cta/SKILL.md`](file:///Users/rifaterdemsahin/projects/youtube-metadata/.agents/skills/sync-first-lines-skool-cta/SKILL.md)
- **Skill 3: End Cards & Skool Video Promoter**: [`sync_end_cards.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/sync_end_cards.py) · [`.agents/skills/sync-end-cards-skool/SKILL.md`](file:///Users/rifaterdemsahin/projects/youtube-metadata/.agents/skills/sync-end-cards-skool/SKILL.md)
- **Skill 4: Skool Link Description Appender**: [`append_skool_link.py`](file:///Users/rifaterdemsahin/projects/youtube-metadata/append_skool_link.py) · [`.agents/skills/append-skool-link/SKILL.md`](file:///Users/rifaterdemsahin/projects/youtube-metadata/.agents/skills/append-skool-link/SKILL.md)

---

## 🔄 Backup & Execution Workflow
Before applying any description/title updates:
```bash
# 1. Take a snapshot of current channel metadata
./venv/bin/python -c "import youtube_client, json; json.dump(youtube_client.list_channel_videos(max_results=50), open('backup_channel_snapshot.json', 'w'), indent=2)"

# 2. Sync Pinned Comments across all channel videos
./venv/bin/python sync_pinned_comments.py --apply

# 3. Optimize top 2 lines of video descriptions with Skool CTA
./venv/bin/python update_first_lines_skool.py --apply
```


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
- **Video Catalog & Notes Editor**: [`catalog.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/catalog.html)
- **Applied Updates Log**: [`updates.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/updates.html)
- **Live GitHub Pages**: [https://rifaterdemsahin.github.io/youtube-metadata/](https://rifaterdemsahin.github.io/youtube-metadata/)

---

## 🔄 Backup Workflow
Before applying any description/title updates:
```bash
# 1. Take a snapshot of current channel metadata
python3 -c "import youtube_client, json; json.dump(youtube_client.list_channel_videos(max_results=50), open('backup_channel_snapshot.json', 'w'), indent=2)"

# 2. Backup secrets to Key Vault
az keyvault secret set --vault-name dp-kv-deliverypilot --name youtube-token --file token.json

# 3. Apply changes
./venv/bin/python append_skool_link.py --apply
```

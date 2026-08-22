# YouTube Studio MCP Server & Metadata Manager

A Python-based **Model Context Protocol (MCP)** server and automated metadata updater for YouTube Studio, built using the official `google-api-python-client` with YouTube Data API v3 and FastMCP.

---

## 🌐 Live Operations Dashboard & Links

- **GitHub Pages Dashboard**: [https://rifaterdemsahin.github.io/youtube-metadata/](https://rifaterdemsahin.github.io/youtube-metadata/)
- **Video Catalog & Notes**: [https://rifaterdemsahin.github.io/youtube-metadata/catalog.html](https://rifaterdemsahin.github.io/youtube-metadata/catalog.html)
- **Audience Retention**: [https://rifaterdemsahin.github.io/youtube-metadata/retention.html](https://rifaterdemsahin.github.io/youtube-metadata/retention.html)
- **Impressions CTR**: [https://rifaterdemsahin.github.io/youtube-metadata/ctr.html](https://rifaterdemsahin.github.io/youtube-metadata/ctr.html)
- **August 2026 Analytics**: [https://rifaterdemsahin.github.io/youtube-metadata/august.html](https://rifaterdemsahin.github.io/youtube-metadata/august.html)
- **Year briefing (365d + today)**: [https://rifaterdemsahin.github.io/youtube-metadata/year.html](https://rifaterdemsahin.github.io/youtube-metadata/year.html)
- **Google Flow vs live-action retention**: [https://rifaterdemsahin.github.io/youtube-metadata/flow.html](https://rifaterdemsahin.github.io/youtube-metadata/flow.html)
- **Applied Updates Log**: [https://rifaterdemsahin.github.io/youtube-metadata/updates.html](https://rifaterdemsahin.github.io/youtube-metadata/updates.html)
- **Target YouTube Channel**: [https://www.youtube.com/@RifatErdemSahin](https://www.youtube.com/@RifatErdemSahin) (`@RifatErdemSahin`)
- **Target Skool Community**: [https://www.skool.com/delivery-pilot-8938](https://www.skool.com/delivery-pilot-8938)
- **Google Cloud OAuth Test Users Page**: [https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419](https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419)

---

## 🌟 Features

- **MCP Tools for Claude Desktop & Cursor**:
  - `check_auth_status`: Validate OAuth2 authentication and channel access for `@RifatErdemSahin`.
  - `list_videos`: Fetch all uploaded videos, metadata, statistics, and thumbnails.
  - `update_video`: Edit video title, description, tags, category, and privacy status.
  - `set_thumbnail`: Upload custom high-res video thumbnails.
  - `append_link_to_all_descriptions`: Batch append community/promotional links (such as Skool) across all channel videos with dry-run support.
- **Local OAuth 2.0 Management**: Supports `client_secret.json` and persistent `token.json` token refresh with Azure Key Vault sync (`dp-kv-deliverypilot`).
- **Bulk Metadata CLI Script**: `append_skool_link.py` to batch-append your Skool Community link to all videos with simulation and report generation.
- **Visual Operations Dashboard**: grouped top nav (Operate / Library / Performance / Logs / Channel) across `index.html`, `catalog.html`, `analytics.html`, `retention.html`, `ctr.html`, `august.html`, `year.html`, and `updates.html`.

---

## 🔑 OAuth Setup & Test Users Configuration

- **Direct Link to Add Test Users**:  
  👉 [Google Cloud OAuth Audience & Test Users (Project: `gen-lang-client-0369583419`)](https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419)
- **Detailed Guides**:
  - [`AUTHENTICATION_GUIDE.md`](AUTHENTICATION_GUIDE.md): 4-step Google Cloud + Azure Key Vault setup.
  - [`OAUTH_TEST_USERS_FIX.md`](OAUTH_TEST_USERS_FIX.md): Resolving Error 403 by configuring test users.
  - [`LIMITATIONS.md`](LIMITATIONS.md): What the API cannot do (End Screens & Info Cards are Studio-only).
  - [`antigravity.md`](antigravity.md): Backup protocols and operating principles.

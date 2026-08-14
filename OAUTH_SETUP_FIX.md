# Fixing Google OAuth Error 400: `redirect_uri_mismatch`

## Why this happens
The Google Cloud OAuth Client ID was created as a **Web application** rather than a **Desktop App** (Installed App), or the dynamic localhost port isn't permitted by Web application redirect URI rules.

Desktop App client IDs allow dynamic ports (e.g. `http://localhost:<port>/`) automatically without explicit URI registration.

---

## 🛠️ Solution 1: Create a Desktop App OAuth Client ID (Recommended)

1. Go to **[Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials)**.
2. Select your project: `deliverypilot`.
3. Click **+ CREATE CREDENTIALS** -> **OAuth client ID**.
4. Set **Application type** to:
   👉 **Desktop App** (Desktop application)
5. Name it: `YouTube Studio MCP Desktop`
6. Click **CREATE**.
7. Click **DOWNLOAD JSON** on the created credential.
8. Save the file directly as:
   `/Users/rifaterdemsahin/projects/youtube-metadata/client_secret.json`
9. Upload it to your Azure Key Vault for safe storage:
   ```bash
   az keyvault secret set --vault-name dp-kv-deliverypilot --name youtube-client-secret --file client_secret.json
   ```

---

## 🛠️ Solution 2: Add Redirect URIs if using Existing Web App Client

If you want to keep using the existing OAuth Client ID (`616339871325-kjkviiai3iubd1pegip1heedddperv68.apps.googleusercontent.com`):

1. Open **[Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials)**.
2. Under **OAuth 2.0 Client IDs**, click your client ID to edit.
3. Under **Authorized redirect URIs**, click **+ ADD URI** and add:
   - `http://localhost:8080/`
   - `http://localhost:8080`
   - `http://127.0.0.1:8080/`
   - `http://127.0.0.1:8080`
   - `http://localhost`
4. Click **SAVE**.
5. When running the local scripts, fixed port `8080` can be used.

---

## 🚀 Re-run after Updating Credentials

Once `client_secret.json` is replaced, run the dry run again:
```bash
./venv/bin/python append_skool_link.py --dry-run
```

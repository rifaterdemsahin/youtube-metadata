# YouTube OAuth Authentication & Azure Key Vault Guide

Step-by-step guide to create your Desktop OAuth credential in Google Cloud, authenticate your channel (`@RifatErdemSahin`), and securely persist both the client secrets and authorized token in Azure Key Vault (`dp-kv-deliverypilot`).

---

## 📌 Step 1: Create Desktop App OAuth Credentials (Google Cloud)

1. Open **[Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials)** in your browser.
2. Ensure project **`deliverypilot`** is selected at the top.
3. Click **+ CREATE CREDENTIALS** ➔ **OAuth client ID**.
4. Configure the credential:
   - **Application type**: `Desktop App`
   - **Name**: `YouTube Studio MCP Desktop`
5. Click **CREATE**.
6. On the confirmation modal, click **DOWNLOAD JSON**.
7. Rename or move the downloaded file to:
   ```bash
   /Users/rifaterdemsahin/projects/youtube-metadata/client_secret.json
   ```

---

## 📌 Step 2: Upload Client Secret to Azure Key Vault

Store your newly downloaded `client_secret.json` into Azure Key Vault `dp-kv-deliverypilot`:

```bash
az keyvault secret set \
  --vault-name dp-kv-deliverypilot \
  --name youtube-client-secret \
  --file /Users/rifaterdemsahin/projects/youtube-metadata/client_secret.json
```

---

## 📌 Step 3: Authenticate & Authorize Access

Run the dry-run CLI command from your project directory:

```bash
cd /Users/rifaterdemsahin/projects/youtube-metadata
./venv/bin/python append_skool_link.py --dry-run
```

### What happens next:
1. Google will automatically open your Chrome browser to the OAuth consent page.
2. Sign in with the Google Account that manages **`@RifatErdemSahin`**.
3. If presented with *"Google hasn't verified this app"*, click **Advanced** ➔ **Go to YouTube Studio MCP (unsafe)**.
4. Check the box to grant YouTube manage permissions and click **Continue**.
5. The terminal will output `Connected to channel: 'Rifat Erdem Sahin' (@RifatErdemSahin)` and generate a persistent **`token.json`** file.

---

## 📌 Step 4: Backup the Authorized `token.json` to Azure Key Vault

Once authenticated, upload the generated `token.json` to Azure Key Vault so you can restore or deploy it anywhere without re-prompting:

```bash
az keyvault secret set \
  --vault-name dp-kv-deliverypilot \
  --name youtube-token \
  --file /Users/rifaterdemsahin/projects/youtube-metadata/token.json
```

---

## 📌 Step 5: Verify & Pull Anytime

Whenever you set up a new environment or MCP instance, run:

```bash
./venv/bin/python fetch_azure_secrets.py --vault dp-kv-deliverypilot
```

This automatically downloads both `client_secret.json` and `token.json` from Azure Key Vault.

---

## 📌 Step 6: Apply the Live Description Update

To apply `https://www.skool.com/delivery-pilot-8938` to all 25 video descriptions:

```bash
./venv/bin/python append_skool_link.py --apply
```

# How to Fix `Error 403: access_denied` (Google OAuth Test User)

## Why this happens:
Your Google Cloud project (`deliverypilot` or `n8n`) is in **"Testing"** mode. In Testing mode, only email addresses explicitly added as **Test Users** are allowed to sign in.

---

## 🛠️ Quick 1-Minute Fix: Add Your Email as a Test User

1. Open **[Google Cloud Console OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)** in Chrome.
2. Ensure you have the right project selected in the top bar (e.g. `deliverypilot`).
3. Scroll down to the **Test users** section.
4. Click **+ ADD USERS**.
5. Enter the email address you are trying to sign in with (e.g. your personal Google account or `info@pexabo.com` / `info@deliverypilot.net`).
6. Click **SAVE**.

---

## 🚀 Re-run the Auth Flow

After adding your email as a test user, rerun the dry-run command:

```bash
./venv/bin/python append_skool_link.py --dry-run
```

When signing in:
- Click **Continue** when prompted with the unverified app warning.
- Check the box to grant YouTube management access.

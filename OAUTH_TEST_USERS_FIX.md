# Google Cloud OAuth Consent & Test Users Configuration

Direct links and instructions to manage OAuth audience settings and authorized test users for the project.

---

## 🔗 Direct Google Cloud Console Links

- **OAuth Audience & Test Users Page (Project: `gen-lang-client-0369583419`)**:  
  👉 **[https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419](https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419)**

- **Credentials & OAuth Client IDs**:  
  👉 **[https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0369583419](https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0369583419)**

---

## 🛠️ How to Add or Manage Test Users

When an OAuth 2.0 app is in **Testing** mode in Google Cloud:
1. Open the [OAuth Audience / Test Users link](https://console.cloud.google.com/auth/audience?project=gen-lang-client-0369583419).
2. Under the **Test users** section, click **+ ADD USERS**.
3. Enter the email address of the account you want to authenticate (e.g. `info@pexabo.com`, `info@deliverypilot.net`, or your personal Google account).
4. Click **SAVE**.

---

## 🚀 Re-authenticating

Once added as a test user, run:
```bash
./venv/bin/python append_skool_link.py --dry-run
```
Sign in with the test user email to authorize channel metadata access without encountering `Error 403: access_denied`.

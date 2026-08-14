#!/usr/bin/env python3
"""
Fetch YouTube OAuth secrets from Azure Key Vault and export locally as client_secret.json / token.json
Usage:
  python fetch_azure_secrets.py --vault dp-kv-deliverypilot --secret-name youtube-client-secret
"""

import argparse
import subprocess
import json
import os
import sys

def get_secret_from_vault(vault_name, secret_name):
    print(f"Fetching '{secret_name}' from Key Vault '{vault_name}'...")
    try:
        res = subprocess.run(
            ["az", "keyvault", "secret", "show", "--vault-name", vault_name, "--name", secret_name, "--query", "value", "-o", "tsv"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving secret {secret_name}: {e.stderr}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube credentials from Azure Key Vault")
    parser.add_argument("--vault", default="dp-kv-deliverypilot", help="Key Vault name")
    parser.add_argument("--client-secret-name", default="youtube-client-secret", help="Secret name for client_secret.json")
    parser.add_argument("--token-name", default="youtube-token", help="Secret name for token.json (optional)")
    args = parser.parse_args()

    client_secret_val = get_secret_from_vault(args.vault, args.client_secret_name)
    if client_secret_val:
        with open("client_secret.json", "w") as f:
            f.write(client_secret_val)
        print("Successfully saved 'client_secret.json' from Azure Key Vault!")
    else:
        print(f"Could not find secret '{args.client_secret_name}'.")
        print(f"To store it into Azure Key Vault, run:")
        print(f"  az keyvault secret set --vault-name {args.vault} --name {args.client_secret_name} --file client_secret.json")

    # Optional: fetch token.json if already stored
    token_val = get_secret_from_vault(args.vault, args.token_name)
    if token_val:
        with open("token.json", "w") as f:
            f.write(token_val)
        print("Successfully saved 'token.json' from Azure Key Vault!")

if __name__ == "__main__":
    main()

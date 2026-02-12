import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_DIR.mkdir(exist_ok=True)

def create_dummy_files():
    # Headers
    headers_file = CONFIG_DIR / "headers.json"
    if not headers_file.exists():
        with open(headers_file, "w") as f:
            json.dump({
                "blinkit": {"note": "Add real headers here"},
                "zepto": {"note": "Add real headers here"},
                "flipkart_minutes": {"note": "Add real headers here"}
            }, f, indent=4)
        print(f"Created {headers_file}")

    # Credentials
    creds_file = CONFIG_DIR / "credentials.json"
    if not creds_file.exists():
        with open(creds_file, "w") as f:
            json.dump({
                "type": "service_account",
                "project_id": "dummy",
                "private_key_id": "dummy",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDwy...\n-----END PRIVATE KEY-----\n",
                "client_email": "dummy@dummy.iam.gserviceaccount.com",
                "client_id": "123",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy"
            }, f, indent=4)
        print(f"Created {creds_file}")

if __name__ == "__main__":
    create_dummy_files()

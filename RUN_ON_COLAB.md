# 🚀 Run Price Intelligence Engine on Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1cKtREWWbUqYDuB3x8PVoXHkF38l8k7Sq?usp=sharing)

Follow these exact steps to run the engine in a Google Colab notebook.

### 1️⃣ Step 1: Install Dependencies

Copy and paste this into the **first code cell** and run it.

```python
# Clone the repository (if you haven't already uploaded it)
!git clone https://github.com/heavens7above/ProjectMarlboro.git
%cd ProjectMarlboro/price-intel-engine

# Install required libraries
!pip install -r requirements.txt
!pip install --upgrade curl_cffi tenacity loguru gspread oauth2client pydantic-settings
```

### 2️⃣ Step 2: Setup Configuration (Crucial!)

Copy and paste this into the **second code cell**.
**Replace headers with real values for best results**.

```python
import json
import os

# Create config directory
os.makedirs("config", exist_ok=True)

# ---------------------------------------------------------
# PASTE YOUR REAL HEADERS BELOW
# ---------------------------------------------------------
headers_config = {
    "blinkit": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        "auth_token": "YOUR_REAL_BLINKIT_AUTH_TOKEN",
        "location_id": "YOUR_REAL_LOCATION_ID"
    },
    "zepto": {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
        "app_version": "YOUR_ZEPTO_APP_VERSION",
        "auth_token": "YOUR_ZEPTO_AUTH_TOKEN"
    },
    "flipkart_minutes": {
         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
    }
}

# Write headers.json
with open("config/headers.json", "w") as f:
    json.dump(headers_config, f, indent=4)

print("✅ Configuration set up! Don't forget to replace placeholders!")
```

### 3️⃣ Step 3: Run the Engine 🏎️

Copy and paste this into the **third code cell**.

```python
import sys
import os

# Create a dummy credentials file to bypass GSheet error if you don't use it
if not os.path.exists("config/credentials.json"):
    with open("config/credentials.json", "w") as f:
        f.write("{}")

# Set PYTHONPATH so python can find the 'src' module
os.environ['PYTHONPATH'] = os.getcwd()

# Run the Scraper for "Marlboro Red"
# --dry-run : Skips attempting to upload to Google Sheets
!python src/main.py --term "Marlboro Red" --dry-run
```

### 4️⃣ Troubleshooting

- **"Request failed" / 401 Unauthorized**: Your headers in Step 2 are wrong or expired.
- **ModuleNotFoundError**: Make sure you ran `%cd ProjectMarlboro/price-intel-engine` in Step 1.

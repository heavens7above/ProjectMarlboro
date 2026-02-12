# 🚀 Run Price Intelligence Engine on Google Colab

This guide will help you run the scraping engine directly in Google Colab.

## Option A: Quick Upload (Easiest)

1.  **Download Code**: Zip your local `price-intel-engine` folder.
2.  **Open Colab**: Go to [colab.research.google.com](https://colab.research.google.com).
3.  **Upload**: Click the "Files" icon (folder) on the left sidebar -> Upload -> Select your zip file.
4.  **Unzip**: Run this in a code cell:
    ```python
    !unzip price-intel-engine.zip
    %cd price-intel-engine
    ```
5.  **Install**:
    ```python
    !pip install -r requirements.txt
    ```
6.  **Configure**:
    - Right-click `config/headers.json` in the sidebar and edit it to add your real Blinkit/Zepto headers.
    - (Optional) Upload `credentials.json` to the `config/` folder for Google Sheets.
7.  **Run**:
    ```python
    !python src/main.py --term "Amul Butter"
    ```

## Option B: Git Clone (Best for Updates)

1.  **Push Code**: Push your code to a public/private GitHub repo.
2.  **Clone in Colab**:
    ```python
    !git clone https://github.com/YOUR_USERNAME/price-intel-engine.git
    %cd price-intel-engine
    ```
3.  **Install**:
    ```python
    !pip install -r requirements.txt
    ```
4.  **Setup Config**:
    Since `config/` files are gitignored, you must create them.

    ```python
    import json

    # PASTE YOUR REAL HEADERS HERE
    headers = {
        "blinkit": {"auth_token": "...", "location_id": "..."},
        "zepto": {"app_version": "...", "platform": "web"}
    }

    with open("config/headers.json", "w") as f:
        json.dump(headers, f)
    ```

5.  **Run**:
    ```python
    !python src/main.py --term "Coke"
    ```

## ⚠️ Notes for Colab Users

- **IP Rotation**: Colab IPs are datacenter IPs (Google). You might get flagged faster than on residential wifi.
- **Persistent Storage**: Files are deleted when the runtime disconnects. Use Google Drive mounting if you need to save data permanently not using GSheets.
  ```python
  from google.colab import drive
  drive.mount('/content/drive')
  ```

# Price Intelligence Engine 🛒📊

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1cKtREWWbUqYDuB3x8PVoXHkF38l8k7Sq?usp=sharing)

A sophisticated, modular scraping engine for Quick Commerce platforms (Blinkit, Zepto, Flipkart Minutes). Built for reliability, stealth, and actionable data extraction.

## 🚀 Features

- **Multi-Platform Support**: Modular scrapers for Blinkit, Zepto, and Flipkart.
- **Robustness**:
  - 🔄 User-Agent Rotation
  - 🛡️ TLS Fingerprint Evasion (`curl_cffi`)
  - 🔁 Exponential Backoff & Retry Logic
- **Data Normalization**: Standardized `Product` model across all sources.
- **Price Intelligence**: Automatic calculation of "Cheapest Deal" and price spread.
- **Export**: Built-in Google Sheets integration.
- **Production Ready**: Dockerized and CI/CD ready (GitHub Actions).

## 🛠️ Setup

### 1. Prerequisites

- Python 3.9+
- Docker (optional)
- Google Cloud Service Account (for Sheets export)

### 2. Installation

```bash
# Clone the repo
git clone <repo-url>
cd price-intel-engine

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

**A. Headers (Crucial)**
The scrapers require real session headers (Auth tokens, Location IDs) to work against live APIs.

1. Open Blinkit/Zepto in your browser.
2. Inspect Network traffic for search requests.
3. Copy headers to `config/headers.json`:

```json
{
  "blinkit": {
    "auth_token": "...",
    "location_id": "..."
  },
  "zepto": {
    "app_version": "..."
  }
}
```

**B. Google Sheets**

1. Place your Service Account JSON key at `config/credentials.json`.
2. Share your target Google Sheet with the Service Account email.

## 🏃 Usage

**Dry Run (Console Output Only)**

```bash
python src/main.py --term "Amul Butter 500g" --dry-run
```

**Live Run (Export to Sheets)**

```bash
python src/main.py --term "Amul Butter 500g"
```

## 🐳 Docker Usage

```bash
docker build -t price-intel .
docker run -v $(pwd)/config:/app/config price-intel --term "Milk"
```

## 🧪 Development

We use `pytest` for testing and `make` for automation.

```bash
# Install dependencies & setup config
make install

# Run all tests
make test

# Run a dry-run search
make run

# Build Docker image
make docker-build
```

## ⚠️ Disclaimer

This tool is for educational purposes only. Scraping private APIs may violate Terms of Service. Use responsibly and at your own risk.

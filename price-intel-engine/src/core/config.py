from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Dict, Any, Optional
import json

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Price Intelligence Engine"
    DEBUG: bool = False
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    CONFIG_DIR: Path = BASE_DIR / "config"
    HEADERS_FILE: Path = CONFIG_DIR / "headers.json"
    CREDS_FILE: Path = CONFIG_DIR / "credentials.json"

    # Google
    GOOGLE_CREDS_JSON: Optional[str] = None
    GSHEET_NAME: str = "PriceTracker"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def load_headers(self) -> Dict[str, Any]:
        if not self.HEADERS_FILE.exists():
            return {}
        try:
            with open(self.HEADERS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_platform_headers(self, platform: str) -> Dict[str, str]:
        all_headers = self.load_headers()
        return all_headers.get(platform, {})

# Singleton instance
settings = Settings()

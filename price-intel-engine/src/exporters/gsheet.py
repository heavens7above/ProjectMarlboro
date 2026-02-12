import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.core.models import Product
from src.core.config import settings
from typing import List
from loguru import logger
import os

class GSheetExporter:
    SCOPE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    def __init__(self, sheet_name: str = "PriceTracker"):
        self.sheet_name = sheet_name
        self.client = self._authenticate()
        self.sheet = None

    def _authenticate(self):
        try:
            # Check for credentials file first
            if settings.CREDS_FILE.exists():
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    str(settings.CREDS_FILE), self.SCOPE
                )
            # Fallback to environment variable (good for CI/CD/Lambda)
            elif os.getenv("GOOGLE_CREDS_JSON"):
                import json
                creds_dict = json.loads(os.getenv("GOOGLE_CREDS_JSON"))
                creds = ServiceAccountCredentials.from_json_keyfile_dict(
                    creds_dict, self.SCOPE
                )
            else:
                logger.warning("No Google Sheets credentials found. Export will fail.")
                return None

            return gspread.authorize(creds)
        except Exception as e:
            logger.error(f"Google Sheets authentication failed: {e}")
            return None

    def export(self, products: List[Product]):
        if not self.client:
            logger.warning("Skipping Google Sheets export due to missing credentials.")
            return

        try:
            # Open the spreadsheet
            # Note: The service account must be invited to edit the sheet.
            try:
                sheet = self.client.open(self.sheet_name).sheet1
            except gspread.SpreadsheetNotFound:
                logger.error(f"Spreadsheet '{self.sheet_name}' not found. Make sure to share it with the service account.")
                return

            # Prepare rows
            rows = [
                [
                    p.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    p.platform,
                    p.name,
                    p.price,
                    p.mrp,
                    "In Stock" if p.availability else "OOS",
                    p.location or "N/A"
                ]
                for p in products
            ]

            # Append to sheet
            if rows:
                sheet.append_rows(rows)
                logger.success(f"Successfully exported {len(rows)} items to Google Sheets.")

        except Exception as e:
            logger.error(f"Failed to export to Google Sheets: {e}")

from typing import List, Dict
from src.core.models import SearchQuery, Product
from src.scrapers.base_scraper import BaseScraper
from loguru import logger
from datetime import datetime

class FlipkartMinutesScraper(BaseScraper):
    # Flipkart Minutes is often integrated into the main Flipkart API with specific 'marketPlaceId' or tags.
    # This is a placeholder endpoint.
    SEARCH_URL = "https://1.rome.api.flipkart.com/api/4/page/fetch" 

    def search(self, query: SearchQuery) -> List[Product]:
        if not self.headers:
            logger.warning("No headers found for Flipkart Minutes. Returning mock data.")
            return self._get_mock_data(query)

        # Flipkart often uses a complex POST payload with 'pageUri', 'locationContext', etc.
        payload = {
            "pageUri": f"/search?q={query.term}&sid=search",
            "locationContext": {
                "pincode": query.pincode or "110001"
            },
            "marketPlaceId": "FLIPKART_MINUTES" # Hypothetical ID
        }

        try:
            response = self._make_request("POST", self.SEARCH_URL, json=payload)
            data = response.json()
            return self.parse(data)
        except Exception as e:
            logger.error(f"Flipkart Minutes search failed: {e}")
            return []

    def parse(self, response: Dict) -> List[Product]:
        products = []
        try:
            # Flipkart's response structure is notoriously deep and widget-based (slots, widgets, data).
            # This is a simplified extraction logic.
            slots = response.get("RESPONSE", {}).get("slots", [])
            for slot in slots:
                widget = slot.get("widget", {})
                if widget.get("type") == "PRODUCT_SUMMARY":
                    data = widget.get("data", {})
                    product = Product(
                        platform="flipkart_minutes",
                        name=data.get("titles", {}).get("title", "Unknown"),
                        price=float(data.get("pricing", {}).get("finalPrice", {}).get("value", 0)),
                        mrp=float(data.get("pricing", {}).get("mrp", {}).get("value", 0)),
                        availability=data.get("availability", {}).get("status") == "IN_STOCK",
                        image_url=data.get("images", [{}])[0].get("url"),
                        timestamp=datetime.now()
                    )
                    products.append(product)
        except Exception as e:
            logger.error(f"Error parsing Flipkart response: {e}")
        
        return products

    def _get_mock_data(self, query: SearchQuery) -> List[Product]:
        return [
            Product(
                platform="flipkart_minutes",
                name=f"{query.term} (Mock Flipkart)",
                price=105.0,
                mrp=115.0,
                availability=True,
                location="Mock Location",
                timestamp=datetime.now()
            )
        ]

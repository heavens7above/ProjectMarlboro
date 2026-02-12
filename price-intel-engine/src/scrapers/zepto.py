from typing import List, Dict
from src.core.models import SearchQuery, Product
from src.scrapers.base_scraper import BaseScraper
from loguru import logger
from datetime import datetime

class ZeptoScraper(BaseScraper):
    # Zepto often uses a different API structure, sometimes GraphQL or strictly mobile APIs.
    SEARCH_URL = "https://api.zepto.co.in/api/v1/search" # Try .co.in

    async def search(self, query: SearchQuery) -> List[Product]:
        if not self.headers:
            logger.warning("No headers found for Zepto. Returning mock data.")
            return self._get_mock_data(query)

        payload = {
            "query": query.term,
            "page": 1,
            "limit": 20
        }

        try:
            # Zepto usually requires specific headers like 'app-version', 'platform', etc.
            response = await self._make_request("POST", self.SEARCH_URL, json=payload)
            data = response.json()
            return self.parse(data)
        except Exception as e:
            logger.error(f"Zepto search failed: {e}")
            return []

    def parse(self, response: Dict) -> List[Product]:
        products = []
        try:
            items = response.get("results", [])
            for item in items:
                product = Product(
                    platform="zepto",
                    name=item.get("product_name", "Unknown"),
                    price=float(item.get("selling_price", 0)),
                    mrp=float(item.get("mrp", 0)),
                    availability=item.get("is_available", False),
                    image_url=item.get("image", {}).get("url"),
                    weight=item.get("quantity", {}).get("value"),
                    timestamp=datetime.now()
                )
                products.append(product)
        except Exception as e:
            logger.error(f"Error parsing Zepto response: {e}")
        
        return products

    def _get_mock_data(self, query: SearchQuery) -> List[Product]:
        return [
            Product(
                platform="zepto",
                name=f"{query.term} (Mock Zepto)",
                price=110.0,
                mrp=120.0,
                availability=True,
                location="Mock Location",
                timestamp=datetime.now()
            )
        ]

from typing import List, Dict
from src.core.models import SearchQuery, Product
from src.scrapers.base_scraper import BaseScraper
from loguru import logger
from datetime import datetime

class BlinkitScraper(BaseScraper):
    # This is a likely endpoint, but it might change.
    # Users should verify this in their Network tab.
    SEARCH_URL = "https://blinkit.com/v1/search/products" 
    
    def search(self, query: SearchQuery) -> List[Product]:
        if not self.headers:
            logger.warning("No headers found for Blinkit. Returning mock data.")
            return self._get_mock_data(query)

        params = {
            "q": query.term,
            "start": 0,
            "size": 20,
            "location_id": self.headers.get("location_id", "") # Custom header often needed
        }

        try:
            # Note: Blinkit often uses query params or a POST body. 
            # This is a best-guess structure based on common patterns.
            response = self._make_request("GET", self.SEARCH_URL, params=params)
            data = response.json()
            return self.parse(data)
        except Exception as e:
            logger.error(f"Blinkit search failed: {e}")
            return []

    def parse(self, response: Dict) -> List[Product]:
        products = []
        # This parsing logic depends 100% on the response structure.
        # We will need to adjust this once we have real JSON.
        # For now, this is a schematic parser.
        try:
            items = response.get("products", [])
            for item in items:
                product = Product(
                    platform="blinkit",
                    name=item.get("name", "Unknown"),
                    price=float(item.get("price", 0)),
                    mrp=float(item.get("mrp", 0)),
                    availability=item.get("inventory", {}).get("available", False),
                    image_url=item.get("image_url"),
                    weight=item.get("weight"),
                    timestamp=datetime.now()
                )
                products.append(product)
        except Exception as e:
            logger.error(f"Error parsing Blinkit response: {e}")
        
        return products

    def _get_mock_data(self, query: SearchQuery) -> List[Product]:
        """
        Returns fake data for testing the pipeline when no headers are present.
        """
        return [
            Product(
                platform="blinkit",
                name=f"{query.term} (Mock)",
                price=10.0,
                mrp=12.0,
                availability=True,
                location="Mock Location",
                timestamp=datetime.now()
            ),
             Product(
                platform="blinkit",
                name=f"Premium {query.term} (Mock)",
                price=150.0,
                mrp=200.0,
                availability=True,
                location="Mock Location",
                timestamp=datetime.now()
            )
        ]

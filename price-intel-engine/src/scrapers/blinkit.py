from typing import List, Dict
from src.core.models import SearchQuery, Product
from src.scrapers.base_scraper import BaseScraper
from loguru import logger
from datetime import datetime

class BlinkitScraper(BaseScraper):
    # This is a likely endpoint, but it might change.
    # Users should verify this in their Network tab.
    SEARCH_URL = "https://blinkit.com/v1/layout/search" 
    
    async def search(self, query: SearchQuery) -> List[Product]:
        if not self.headers:
            logger.warning("No headers found for Blinkit. Returning mock data.")
            return self._get_mock_data(query)

        params = {
            "q": query.term,
            "start": 0,
            "size": 20,
            # Use 'lat' & 'lon' if provided in headers (often easier to find), else use 'location_id'
            "lat": self.headers.get("lat", ""), 
            "lon": self.headers.get("lon", ""),
            "location_id": self.headers.get("location_id", "") 
        }

        try:
            # Note: Blinkit often uses query params or a POST body. 
            # This is a best-guess structure based on common patterns.
            response = await self._make_request("GET", self.SEARCH_URL, params=params)
            data = response.json()
            return self.parse(data)
        except Exception as e:
            if "404" in str(e):
                logger.error(f"Blinkit 404 Error: The API Endpoint '{self.SEARCH_URL}' is likely invalid. Please check your browser's Network Tab for the correct 'search' URL and update src/scrapers/blinkit.py.")
            else:
                logger.error(f"Blinkit search failed: {e}")
            return []

    def parse(self, response: Dict) -> List[Product]:
        products = []
        try:
            # Blinkit response often wraps data in 'response' -> 'snippets'
            # We look for widgets that contain 'cart_item' data
            root = response.get("response", {})
            snippets = root.get("snippets", [])
            
            for snippet in snippets:
                try:
                    data = snippet.get("data", {})
                    
                    # Look for the cart_item which has the clean data
                    atc_action = data.get("atc_action", {})
                    cart_item = atc_action.get("add_to_cart", {}).get("cart_item")
                    
                    if cart_item:
                        product = Product(
                            platform="blinkit",
                            name=cart_item.get("product_name", "Unknown"),
                            price=float(cart_item.get("price", 0)),
                            mrp=float(cart_item.get("mrp", 0)),
                            availability=bool(cart_item.get("inventory", 0) > 0),
                            image_url=cart_item.get("image_url"),
                            weight=cart_item.get("unit"),
                            timestamp=datetime.now()
                        )
                        products.append(product)
                except Exception:
                    continue
                    
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

from typing import List, Dict, Optional, Any
from src.core.models import Product
from loguru import logger

class PriceNormalizer:
    @staticmethod
    def compare_products(products: List[Product]) -> Dict[str, Any]:
        """
        Analyzes a list of products and returns a comparison summary.
        """
        if not products:
            return {"cheapest": None, "all": []}

        # Filter out unavailable products for 'cheapest' calculation
        available_products = [p for p in products if p.availability]
        
        cheapest = None
        if available_products:
            cheapest = min(available_products, key=lambda p: p.price)

        # Sort all products by price for display
        sorted_products = sorted(products, key=lambda p: p.price)

        return {
            "cheapest": cheapest,
            "all": sorted_products,
            "price_spread": _calculate_spread(available_products)
        }

def _calculate_spread(products: List[Product]) -> float:
    if not products or len(products) < 2:
        return 0.0
    prices = [p.price for p in products]
    return max(prices) - min(prices)

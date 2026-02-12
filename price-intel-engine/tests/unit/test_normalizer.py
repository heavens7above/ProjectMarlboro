from src.core.normalizer import PriceNormalizer
from src.core.models import Product

def test_compare_products_empty():
    result = PriceNormalizer.compare_products([])
    assert result["cheapest"] is None
    assert result["all"] == []

def test_compare_products_logic():
    p1 = Product(platform="a", name="A", price=100, availability=True)
    p2 = Product(platform="b", name="B", price=50, availability=True)
    p3 = Product(platform="c", name="C", price=200, availability=False) # Unavailable

    products = [p1, p2, p3]
    result = PriceNormalizer.compare_products(products)

    assert result["cheapest"] == p2
    assert len(result["all"]) == 3
    assert result["price_spread"] == 50.0 # 100 - 50 (ignoring unavailable for spread? implementation check needed)

def test_compare_products_all_unavailable():
    p1 = Product(platform="a", name="A", price=100, availability=False)
    p2 = Product(platform="b", name="B", price=50, availability=False)
    
    result = PriceNormalizer.compare_products([p1, p2])
    assert result["cheapest"] is None

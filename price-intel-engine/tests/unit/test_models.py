from src.core.models import Product, SearchQuery
from datetime import datetime

def test_product_model_creation():
    p = Product(
        platform="amazon",
        name="Test Item",
        price=50.0,
        mrp=100.0,
        availability=True
    )
    assert p.platform == "amazon"
    assert p.price == 50.0
    assert isinstance(p.timestamp, datetime)

def test_search_query_creation():
    q = SearchQuery(term="Milk", pincode="110001")
    assert q.term == "Milk"
    assert q.pincode == "110001"

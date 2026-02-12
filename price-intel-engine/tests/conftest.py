import pytest
import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture
def sample_product():
    from src.core.models import Product
    return Product(
        platform="test_platform",
        name="Test Product",
        price=100.0,
        mrp=120.0,
        availability=True
    )

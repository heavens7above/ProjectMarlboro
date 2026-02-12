from unittest.mock import MagicMock, patch
from src.main import run_pipeline
from src.core.models import Product

@patch("src.main.BlinkitScraper")
@patch("src.main.ZeptoScraper")
@patch("src.main.FlipkartMinutesScraper")
def test_pipeline_dry_run(MockFlipkart, MockZepto, MockBlinkit):
    # Setup Mocks
    mock_product = Product(platform="mock", name="Test", price=10, availability=True)
    
    # Configure instances
    MockBlinkit.return_value.search.return_value = [mock_product]
    MockZepto.return_value.search.return_value = []
    MockFlipkart.return_value.search.return_value = []

    # Run Pipeline in dry-run mode (no GSheet export)
    run_pipeline("Test Term", dry_run=True)

    # Verify scrapers were called
    MockBlinkit.return_value.search.assert_called_once()
    MockZepto.return_value.search.assert_called_once()
    MockFlipkart.return_value.search.assert_called_once()

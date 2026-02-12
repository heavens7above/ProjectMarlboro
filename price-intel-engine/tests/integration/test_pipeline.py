import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from src.main import run_pipeline
from src.core.models import Product

@pytest.mark.asyncio
@patch("src.main.BlinkitScraper")
@patch("src.main.ZeptoScraper")
@patch("src.main.FlipkartMinutesScraper")
async def test_pipeline_dry_run(MockFlipkart, MockZepto, MockBlinkit):
    # Setup Mocks
    mock_product = Product(platform="mock", name="Test", price=10, availability=True)
    
    # Configure instances to return AsyncMocks
    # When scraper_instance.search() is called, it should return an awaitable list
    MockBlinkit.return_value.search = AsyncMock(return_value=[mock_product])
    MockZepto.return_value.search = AsyncMock(return_value=[])
    MockFlipkart.return_value.search = AsyncMock(return_value=[])
    
    # Mock close methods
    MockBlinkit.return_value.close = AsyncMock()
    MockZepto.return_value.close = AsyncMock()
    MockFlipkart.return_value.close = AsyncMock()

    # Run Pipeline in dry-run mode (no GSheet export)
    await run_pipeline("Test Term", dry_run=True)

    # Verify scrapers were called
    MockBlinkit.return_value.search.assert_called_once()
    MockZepto.return_value.search.assert_called_once()
    MockFlipkart.return_value.search.assert_called_once()
    
    # Verify cleanup
    MockBlinkit.return_value.close.assert_called_once()

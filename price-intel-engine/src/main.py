import sys
import argparse
from typing import List
from src.core.logger_config import logger # Import configured logger
from src.core.models import SearchQuery, Product
from src.core.config import settings
from src.scrapers.blinkit import BlinkitScraper
from src.scrapers.zepto import ZeptoScraper
from src.scrapers.flipkart_minutes import FlipkartMinutesScraper
from src.core.normalizer import PriceNormalizer

def run_pipeline(term: str, dry_run: bool = False):
    logger.info(f"Starting Price Intelligence Engine query='{term}'")
    
    # Load configuration
    query = SearchQuery(term=term)
    products: List[Product] = []

    # Initialize Scrapers
    scrapers = [
        BlinkitScraper("blinkit", headers=settings.get_platform_headers("blinkit")),
        ZeptoScraper("zepto", headers=settings.get_platform_headers("zepto")),
        FlipkartMinutesScraper("flipkart_minutes", headers=settings.get_platform_headers("flipkart_minutes"))
    ]

    # Run Scrapers
    for scraper in scrapers:
        logger.info(f"Scraping {scraper.platform_name}...")
        try:
            results = scraper.search(query)
            logger.info(f"Found {len(results)} items on {scraper.platform_name}")
            products.extend(results)
        except Exception as e:
            logger.error(f"Failed to scrape {scraper.platform_name}: {e}")

    # Process Results
    if not products:
        logger.warning("No products found.")
        return

    # Normalize and Compare
    comparison = PriceNormalizer.compare_products(products)
    cheapest = comparison.get("cheapest")
    all_sorted = comparison.get("all")

    logger.info("\n" + "="*50)
    logger.info(f"RESULTS FOR '{term}'")
    logger.info("="*50)
    
    if cheapest:
        logger.success(f"🏆 CHEAPEST DEAL: [{cheapest.platform.upper()}] {cheapest.name} @ ₹{cheapest.price}")
    else:
        logger.warning("No products currently available in stock.")

    logger.info("\n--- Full List ---")
    for p in all_sorted:
        status_icon = "✅" if p.availability else "mj"
        logger.info(f"{status_icon} [{p.platform.upper()}] {p.name} | ₹{p.price} (MRP: ₹{p.mrp})")

    # Need GSheet export logic here later
    if not dry_run:
        from src.exporters.gsheet import GSheetExporter
        exporter = GSheetExporter(sheet_name="PriceTracker")
        exporter.export(all_sorted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quick Commerce Price Tracker")
    parser.add_argument("--term", type=str, required=True, help="Search term (e.g. 'Amul Butter')")
    parser.add_argument("--dry-run", action="store_true", help="Print to console only, skip DB/Sheet write")
    
    args = parser.parse_args()
    run_pipeline(args.term, args.dry_run)

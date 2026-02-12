import sys
import argparse
import asyncio
from typing import List
from src.core.logger_config import logger # Import configured logger
from src.core.models import SearchQuery, Product
from src.core.config import settings
from src.scrapers.blinkit import BlinkitScraper
from src.scrapers.zepto import ZeptoScraper
from src.scrapers.flipkart_minutes import FlipkartMinutesScraper
from src.core.normalizer import PriceNormalizer

async def run_pipeline(term: str, dry_run: bool = False) -> None:
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

    try:
        # Run Scrapers in Parallel
        logger.info("Scraping all platforms in parallel...")
        tasks = [scraper.search(query) for scraper in scrapers]
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results_list):
            scraper_name = scrapers[i].platform_name
            if isinstance(result, Exception):
                logger.error(f"Failed to scrape {scraper_name}: {result}")
            elif isinstance(result, list):
                logger.info(f"Found {len(result)} items on {scraper_name}")
                products.extend(result)
            else:
                 logger.error(f"Unexpected result type from {scraper_name}: {type(result)}")


    finally:
        # Cleanup sessions
        for scraper in scrapers:
            await scraper.close()

    if not products:
        logger.warning("No products found.")
        return

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

    if all_sorted:
        logger.info("\n--- Full List ---")
        for p in all_sorted:
            status_icon = "✅" if p.availability else "mj"
            logger.info(f"{status_icon} [{p.platform.upper()}] {p.name} | ₹{p.price} (MRP: ₹{p.mrp})")

        if not dry_run:
            from src.exporters.gsheet import GSheetExporter
            exporter = GSheetExporter(sheet_name=settings.GSHEET_NAME)
            exporter.export(all_sorted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quick Commerce Price Tracker")
    parser.add_argument("--term", type=str, required=True, help="Search term (e.g., 'Amul Butter')")
    parser.add_argument("--dry-run", action="store_true", help="Skip export to Google Sheets")
    
    args = parser.parse_args()
    try:
        asyncio.run(run_pipeline(args.term, args.dry_run))
    except Exception as e:
        logger.error(f"Fatal error: {e}")

from sqlalchemy.orm import Session

from app.models.maker_product import MakerProduct, MakerScrapeConfig


async def scrape_maker_products(config: MakerScrapeConfig, db: Session) -> int:
    """Scrape products from a maker's website.

    TODO: Implement actual scraping logic.
    This would use httpx + BeautifulSoup or similar to extract product listings.

    Returns the number of products found.
    """
    # Placeholder implementation
    return 0

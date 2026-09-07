from app.scrapers.base.base_rss_scraper import BaseRSSScraper
from app.config.settings import ANTHROPIC_RSS_URLS

class AnthropicScraper(BaseRSSScraper):

    def __init__(self):
        super().__init__(rss_urls=ANTHROPIC_RSS_URLS)
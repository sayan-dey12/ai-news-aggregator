from app.scrapers.base.base_rss_scraper import BaseRSSScraper
from app.config.sources import OPENAI_RSS_URLS

class OpenAIScraper(BaseRSSScraper):

    def __init__(self):
        super().__init__(rss_urls=OPENAI_RSS_URLS)
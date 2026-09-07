from app.scrapers.base.base_rss_scraper import BaseRSSScraper


class OpenAIScraper(BaseRSSScraper):

    def __init__(self):
        super().__init__(
            rss_urls=[
                "https://openai.com/news/rss.xml"
            ]
        )
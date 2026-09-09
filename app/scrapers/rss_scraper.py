from app.scrapers.base.base_rss_scraper import BaseRSSScraper


class RSSScraper(BaseRSSScraper):

    def __init__(
        self,
        rss_urls: list[str],
        source_name: str,
    ):
        super().__init__(
            rss_urls=rss_urls,
            source_name=source_name,
        )
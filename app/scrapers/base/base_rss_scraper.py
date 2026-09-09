from datetime import datetime, timedelta, timezone
from typing import List, Optional

import feedparser

#from docling.document_converter import DocumentConverter

from app.database.models import RSSArticle
from app.services.content_converter import ContentConverter


class BaseRSSScraper:

    def __init__(
        self,
        rss_urls: List[str],
        source_name: str,
    ):
        self.rss_urls = rss_urls
        self.source_name = source_name
        #self.converter = DocumentConverter()
        self.content_converter = ContentConverter()

    def get_articles(
        self,
        hours: int = 240,
    ) -> List[RSSArticle]:

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)

        articles = []
        seen_guids = set()

        for rss_url in self.rss_urls:

            feed = feedparser.parse(rss_url)

            if not feed.entries:
                continue

            for entry in feed.entries:

                published_parsed = entry.get(
                    "published_parsed"
                )

                if not published_parsed:
                    published_parsed = entry.get(
                        "updated_parsed"
                    )

                if not published_parsed:
                    continue

                published_time = datetime(
                    *published_parsed[:6],
                    tzinfo=timezone.utc,
                )

                if published_time < cutoff_time:
                    continue

                guid = entry.get(
                    "id",
                    entry.get("link", ""),
                )

                if not guid:
                    continue

                if guid in seen_guids:
                    continue

                seen_guids.add(guid)

                articles.append(
                    RSSArticle(
                        guid=guid,
                        source=self.source_name,
                        title=entry.get("title", ""),
                        url=entry.get("link", ""),
                        description=entry.get(
                            "description",
                            "",
                        ),
                        published_at=published_time,
                        category=self._get_category(entry),
                    )
                )

        return articles

    def _get_category(
        self,
        entry,
    ) -> Optional[str]:

        tags = entry.get("tags", [])

        if not tags:
            return None

        return tags[0].get("term")

    def url_to_markdown(
        self,
        url: str,
    ) -> Optional[str]:

        try:
            # result = self.converter.convert(url)
            # return result.document.export_to_markdown()
            
            return self.content_converter.url_to_markdown(url)
        except Exception:
            return None
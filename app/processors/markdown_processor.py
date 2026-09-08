from typing import Optional

from app.config.sources import RSS_SOURCES
from app.database.repository import Repository
from app.processors.content_processor import process_missing_content
from app.scrapers.rss_scraper import RSSScraper


def process_markdown(
    source_name: str,
    limit: Optional[int] = None,
) -> dict:

    source = next(
        (
            source
            for source in RSS_SOURCES
            if source.name == source_name
        ),
        None,
    )

    if source is None:
        raise ValueError(
            f"Unknown RSS source: {source_name}"
        )

    repo = Repository()

    scraper = source.scraper_class(
        rss_urls=list(source.rss_urls),
        source_name=source.name,
    )

    return process_missing_content(
        get_items=lambda limit: repo.get_without_content(
            model=source.model,
            content_field="markdown",
            limit=limit,
        ),

        generate_content=lambda article: (
            scraper.url_to_markdown(article.url)
        ),

        save_content=lambda article, content: (
            repo.update_content(
                model=source.model,
                unique_field=source.unique_field,
                unique_value=getattr(
                    article,
                    source.unique_field,
                ),
                content_field="markdown",
                content=content,
            )
        ),

        limit=limit,
    )
from typing import Optional

from app.database.repository import Repository
from app.processors.content_processor import process_missing_content
from app.config.content_sources import MARKDOWN_SOURCES


def process_markdown(
    source_name: str,
    limit: Optional[int] = None,
) -> dict:

    source = next(
        source
        for source in MARKDOWN_SOURCES
        if source.name == source_name
    )

    repo = Repository()
    scraper = source.scraper_class()

    return process_missing_content(
        get_items=lambda limit: repo.get_without_content(
            model=source.model,
            content_field=source.content_field,
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
                content_field=source.content_field,
                content=content,
            )
        ),

        limit=limit,
    )
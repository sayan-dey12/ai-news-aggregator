from typing import Optional

from app.config.content_sources import MARKDOWN_SOURCES
from app.database.repository import Repository
from app.processors.content_processor import process_missing_content


def process_markdown(
    source_name: str,
    limit: Optional[int] = None,
) -> dict:

    source = next(
        (
            source
            for source in MARKDOWN_SOURCES
            if source.name == source_name
        ),
        None,
    )

    if source is None:
        raise ValueError(
            f"Unknown markdown source: {source_name}"
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
    
    
    
if __name__ == "__main__":
    from app.config.content_sources import MARKDOWN_SOURCES

    test_urls = {
        "openai": "https://openai.com/index/an-alien-mind",
        "anthropic": "https://www.anthropic.com/news/model-hardware-standard-research-preview",
    }

    for source_name, url in test_urls.items():
        print("\n" + "=" * 70)
        print(f"TESTING {source_name.upper()}")
        print("=" * 70)
        print(f"URL: {url}")

        source = next(
            (
                source
                for source in MARKDOWN_SOURCES
                if source.name == source_name
            ),
            None,
        )

        if source is None:
            print(f"ERROR: Unknown source: {source_name}")
            continue

        scraper = source.scraper_class()

        try:
            content = scraper.url_to_markdown(url)

            if content:
                print("\nSUCCESS")
                print(f"Content length: {len(content)} characters")
                print("\n--- CONTENT PREVIEW ---\n")
                print(content[:3000])
            else:
                print("\nFAILED")
                print("url_to_markdown() returned None.")

        except Exception as e:
            print("\nERROR")
            print(f"{type(e).__name__}: {e}")
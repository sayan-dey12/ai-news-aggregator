from typing import Any

from app.config.sources import (
    RSS_SOURCES,
    YOUTUBE_SOURCE,
)
from app.database.repository import Repository


def run_scrapers(hours: int = 24) -> dict[str, Any]:
    """
    Run all configured scrapers and persist new records.

    RSS sources and YouTube sources are handled according
    to their source configuration.
    """

    repo = Repository()

    results = {}

    # ==========================================================
    # RSS sources
    # ==========================================================

    for source in RSS_SOURCES:

        scraper = source.scraper_class()

        articles = scraper.get_articles(hours=hours)

        article_dicts = [
            article.model_dump()
            for article in articles
        ]

        created = repo.bulk_create(
            model=source.model,
            items=article_dicts,
            unique_field=source.unique_field,
        )

        results[source.name] = {
            "scraped": len(articles),
            "created": created,
        }

    # ==========================================================
    # YouTube
    # ==========================================================

    youtube_scraper = YOUTUBE_SOURCE.scraper_class()

    videos = youtube_scraper.scrape_channels(
        channel_ids=YOUTUBE_SOURCE.channel_ids,
        hours=hours,
    )

    video_dicts = [
        video.model_dump()
        for video in videos
    ]

    created = repo.bulk_create(
        model=YOUTUBE_SOURCE.model,
        items=video_dicts,
        unique_field=YOUTUBE_SOURCE.unique_field,
    )

    results[YOUTUBE_SOURCE.name] = {
        "scraped": len(videos),
        "created": created,
    }

    return results


if __name__ == "__main__":

    result = run_scrapers(hours=48)

    for source, stats in result.items():
        print(
            f"{source}: "
            f"{stats['scraped']} scraped, "
            f"{stats['created']} created"
        )
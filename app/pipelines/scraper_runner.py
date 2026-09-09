from typing import Any

from app.config.sources import (
    RSS_SOURCES,
    YOUTUBE_SOURCE,
)

from app.scrapers.base.base_rss_scraper import BaseRSSScraper

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

        scraper = source.scraper_class(
            rss_urls=list(source.rss_urls),
            source_name=source.name,
        )

        articles = scraper.get_articles(hours=hours)

        article_dicts = [
            {
                "guid": article.guid,
                "source": article.source,
                "title": article.title,
                "url": article.url,
                "description": article.description,
                "published_at": article.published_at,
                "category": article.category,
            }
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

    youtube_scraped = 0
    youtube_created = 0

    for channel_id in YOUTUBE_SOURCE.channel_ids:

        videos = youtube_scraper.get_latest_videos(
            channel_id=channel_id,
            hours=hours,
        )

        youtube_scraped += len(videos)

        video_dicts = [
            {
                **video.model_dump(),
                "channel_id": channel_id,
            }
            for video in videos
        ]

        created = repo.bulk_create(
            model=YOUTUBE_SOURCE.model,
            items=video_dicts,
            unique_field=YOUTUBE_SOURCE.unique_field,
        )

        youtube_created += created

    results[YOUTUBE_SOURCE.name] = {
        "scraped": youtube_scraped,
        "created": youtube_created,
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
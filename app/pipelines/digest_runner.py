import logging

from typing import Optional

from app.agents.digest_agent import DigestAgent
from app.database.repository import Repository


logger = logging.getLogger(__name__)


def process_digests(
    limit: Optional[int] = None,
) -> dict:

    agent = DigestAgent()
    repo = Repository()

    articles = repo.get_articles_without_digest(
        limit=limit
    )

    total = len(articles)
    processed = 0
    failed = 0

    logger.info(
        "Starting digest processing for %d articles",
        total,
    )

    for index, article in enumerate(
        articles,
        start=1,
    ):
        article_type = article["type"]
        article_id = article["id"]
        content_source = article.get(
            "content_source",
            "unknown",
        )

        article_title = article["title"]

        if len(article_title) > 60:
            article_title = (
                article_title[:60] + "..."
            )

        logger.info(
            "[%d/%d] Processing %s (%s): %s",
            index,
            total,
            article_type,
            content_source,
            article_title,
        )

        try:
            digest_result = agent.generate_digest(
                title=article["title"],
                content=article["content"],
                article_type=article_type,
            )

            if not digest_result:
                failed += 1

                logger.warning(
                    "Failed to generate digest for "
                    "%s %s",
                    article_type,
                    article_id,
                )

                continue

            digest = repo.create_digest(
                article_type=article_type,
                article_id=article_id,
                url=article["url"],
                title=digest_result.title,
                summary=digest_result.summary,
                published_at=article.get(
                    "published_at"
                ),
            )

            if digest:
                processed += 1

                logger.info(
                    "Successfully created digest for "
                    "%s %s",
                    article_type,
                    article_id,
                )

            else:
                failed += 1

                logger.warning(
                    "Digest already exists for "
                    "%s %s",
                    article_type,
                    article_id,
                )

        except Exception as exc:
            failed += 1

            logger.exception(
                "Error processing %s %s: %s",
                article_type,
                article_id,
                exc,
            )

    return {
        "total": total,
        "processed": processed,
        "failed": failed,
    }


if __name__ == "__main__":

    result = process_digests()

    print(
        f"Total articles: {result['total']}"
    )

    print(
        f"Processed: {result['processed']}"
    )

    print(
        f"Failed: {result['failed']}"
    )
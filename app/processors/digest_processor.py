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

        display_title = article_title

        if len(display_title) > 60:
            display_title = (
                display_title[:60] + "..."
            )

        logger.info(
            "[%d/%d] Processing %s (%s): %s",
            index,
            total,
            article_type,
            content_source,
            display_title,
        )

        try:

            # --------------------------------------------------
            # Generate digest
            # --------------------------------------------------

            digest_result = agent.generate_digest(
                title=article["title"],
                content=article["content"],
                article_type=article_type,
            )

            # --------------------------------------------------
            # LLM failed
            # --------------------------------------------------

            if digest_result is None:

                failed += 1

                logger.warning(
                    "[%d/%d] Digest generation failed for "
                    "%s %s: %s",
                    index,
                    total,
                    article_type,
                    article_id,
                    display_title,
                )

                continue

            # --------------------------------------------------
            # Persist digest
            # --------------------------------------------------

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

            # --------------------------------------------------
            # Database result
            # --------------------------------------------------

            if digest:

                processed += 1

                logger.info(
                    "[%d/%d] Successfully created digest "
                    "for %s %s",
                    index,
                    total,
                    article_type,
                    article_id,
                )

            else:

                failed += 1

                logger.warning(
                    "[%d/%d] Digest was not created "
                    "for %s %s "
                    "(possibly already exists)",
                    index,
                    total,
                    article_type,
                    article_id,
                )

        except Exception as exc:

            failed += 1

            logger.exception(
                "[%d/%d] Error processing %s %s: %s",
                index,
                total,
                article_type,
                article_id,
                exc,
            )

    logger.info(
        "Digest processing complete: "
        "%d processed, %d failed",
        processed,
        failed,
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
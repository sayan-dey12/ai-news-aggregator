import logging
from typing import Any

from dotenv import load_dotenv

from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def curate_digests(hours: int = 240) -> dict[str, Any]:
    """
    Fetch recent digests and rank them according to the user's profile.

    This function is responsible for orchestration.
    The CuratorAgent is responsible only for LLM-based ranking.
    """

    repo = Repository()
    curator = CuratorAgent(USER_PROFILE)

    # --------------------------------------------------
    # 1. Get recent digests from the database
    # --------------------------------------------------

    digests = repo.get_recent_digests(hours=hours)

    total = len(digests)

    if total == 0:
        logger.warning(
            "No digests found from the last %s hours",
            hours,
        )

        return {
            "total": 0,
            "ranked": 0,
            "articles": [],
        }

    logger.info(
        "Found %d digests from the last %d hours",
        total,
        hours,
    )

    # --------------------------------------------------
    # 2. Send digests to Curator Agent
    # --------------------------------------------------

    ranked_articles = curator.rank_digests(digests)

    if not ranked_articles:
        logger.error("Curator agent returned no ranked articles")

        return {
            "total": total,
            "ranked": 0,
            "articles": [],
        }

    # --------------------------------------------------
    # 3. Validate the result
    # --------------------------------------------------

    ranked_ids = {article.digest_id for article in ranked_articles}
    digest_ids = {digest["id"] for digest in digests}

    missing_ids = digest_ids - ranked_ids

    if missing_ids:
        logger.warning(
            "Curator did not rank %d digest(s)",
            len(missing_ids),
        )

    # --------------------------------------------------
    # 4. Sort by rank
    # --------------------------------------------------

    ranked_articles = sorted(
        ranked_articles,
        key=lambda article: article.rank,
    )

    # --------------------------------------------------
    # 5. Log the top articles
    # --------------------------------------------------

    logger.info("Successfully ranked %d articles", len(ranked_articles))

    logger.info("=== Top 10 Ranked Articles ===")

    digest_lookup = {
        digest["id"]: digest
        for digest in digests
    }

    for article in ranked_articles[:10]:

        digest = digest_lookup.get(article.digest_id)

        if not digest:
            continue

        logger.info(
            "Rank %d | Score %.1f/10.0",
            article.rank,
            article.relevance_score,
        )

        logger.info(
            "Title: %s",
            digest["title"],
        )

        logger.info(
            "Type: %s",
            digest["article_type"],
        )

        logger.info(
            "Reasoning: %s",
            article.reasoning,
        )

    # --------------------------------------------------
    # 6. Return structured result
    # --------------------------------------------------

    return {
        "total": total,
        "ranked": len(ranked_articles),
        "articles": [
            {
                "digest_id": article.digest_id,
                "rank": article.rank,
                "relevance_score": article.relevance_score,
                "reasoning": article.reasoning,
            }
            for article in ranked_articles
        ],
    }


if __name__ == "__main__":

    result = curate_digests(hours=240)

    print("\n=== Curation Results ===")
    print(f"Total digests: {result['total']}")
    print(f"Ranked: {result['ranked']}")

    for article in result["articles"][:10]:
        print(
            f"Rank {article['rank']} | "
            f"Score: {article['relevance_score']:.1f} | "
            f"ID: {article['digest_id']}"
        )
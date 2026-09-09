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


def validate_ranking(
    digests: list[dict],
    ranked_articles: list,
) -> tuple[bool, str]:

    expected_ids = [digest["id"] for digest in digests]
    returned_ids = [article.digest_id for article in ranked_articles]

    expected_id_set = set(expected_ids)
    returned_id_set = set(returned_ids)

    # --------------------------------------------------
    # Check number of results
    # --------------------------------------------------

    if len(ranked_articles) != len(digests):
        return (
            False,
            f"Expected {len(digests)} ranked articles, "
            f"but received {len(ranked_articles)}",
        )

    # --------------------------------------------------
    # Check missing IDs
    # --------------------------------------------------

    missing_ids = expected_id_set - returned_id_set

    if missing_ids:
        return (
            False,
            f"Missing digest IDs: {missing_ids}",
        )

    # --------------------------------------------------
    # Check unexpected IDs
    # --------------------------------------------------

    extra_ids = returned_id_set - expected_id_set

    if extra_ids:
        return (
            False,
            f"Unexpected digest IDs: {extra_ids}",
        )

    # --------------------------------------------------
    # Check duplicate IDs
    # --------------------------------------------------

    if len(returned_ids) != len(set(returned_ids)):
        duplicates = {
            digest_id
            for digest_id in returned_ids
            if returned_ids.count(digest_id) > 1
        }

        return (
            False,
            f"Duplicate digest IDs: {duplicates}",
        )

    # --------------------------------------------------
    # Check ranks
    # --------------------------------------------------

    expected_ranks = set(range(1, len(digests) + 1))
    returned_ranks = [article.rank for article in ranked_articles]

    # Duplicate ranks
    if len(returned_ranks) != len(set(returned_ranks)):
        duplicates = {
            rank
            for rank in returned_ranks
            if returned_ranks.count(rank) > 1
        }

        return (
            False,
            f"Duplicate ranks: {duplicates}",
        )

    # Missing / invalid ranks
    if set(returned_ranks) != expected_ranks:
        return (
            False,
            f"Invalid ranks. "
            f"Expected {expected_ranks}, "
            f"received {set(returned_ranks)}",
        )

    return True, "Ranking is valid"


def curate_digests(
    hours: int = 240,
) -> dict[str, Any]:

    """
    Fetch recent digests and rank them according to
    the user's profile.

    Curator results are intentionally NOT stored in the
    database. They are returned in memory for the next
    pipeline stage, such as the email agent.
    """

    repo = Repository()
    curator = CuratorAgent(USER_PROFILE)

    # --------------------------------------------------
    # 1. Get recent digests
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

        logger.error(
            "Curator agent returned no ranked articles"
        )

        return {
            "total": total,
            "ranked": 0,
            "articles": [],
        }

    # --------------------------------------------------
    # 3. Strict validation
    # --------------------------------------------------

    is_valid, validation_message = validate_ranking(
        digests,
        ranked_articles,
    )

    if not is_valid:

        logger.error(
            "Invalid curator result: %s",
            validation_message,
        )

        return {
            "total": total,
            "ranked": 0,
            "articles": [],
        }

    logger.info(
        "Curator validation successful: %s",
        validation_message,
    )

    # --------------------------------------------------
    # 4. Sort by rank
    # --------------------------------------------------

    ranked_articles = sorted(
        ranked_articles,
        key=lambda article: article.rank,
    )

    # --------------------------------------------------
    # 5. Log ranked articles
    # --------------------------------------------------

    logger.info(
        "Successfully ranked %d articles",
        len(ranked_articles),
    )

    logger.info("=== Top 10 Ranked Articles ===")

    digest_lookup = {
        digest["id"]: digest
        for digest in digests
    }

    for article in ranked_articles[:10]:

        digest = digest_lookup.get(
            article.digest_id
        )

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

    print(
        f"Total digests: {result['total']}"
    )

    print(
        f"Ranked: {result['ranked']}"
    )

    for article in result["articles"][:10]:

        print(
            f"Rank {article['rank']} | "
            f"Score: {article['relevance_score']:.1f} | "
            f"ID: {article['digest_id']}"
        )
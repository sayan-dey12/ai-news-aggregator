import logging
from typing import Any, Optional

from app.pipelines.scraper_runner import run_scrapers
from app.pipelines.content_runner import run_content_processing
from app.pipelines.digest_runner import process_digests
from app.processes.email_process import send_digest_email


logger = logging.getLogger(__name__)


def run_full_pipeline(
    hours: int = 72,
    content_limit: Optional[int] = None,
    digest_limit: Optional[int] = None,
    digest_hours: int = 72,
    top_n: int = 10,
    send_email: bool = True,
) -> dict[str, Any]:

    results: dict[str, Any] = {}

    # ==========================================================
    # 1. Scrape sources
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 1: SCRAPING SOURCES")
    logger.info("=" * 70)

    results["scraping"] = run_scrapers(
        hours=hours
    )

    # ==========================================================
    # 2. Process content
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 2: PROCESSING CONTENT")
    logger.info("=" * 70)

    results["content"] = run_content_processing()

    # ==========================================================
    # 3. Generate digests
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 3: GENERATING DIGESTS")
    logger.info("=" * 70)

    results["digests"] = process_digests(
        limit=digest_limit
    )

    # ==========================================================
    # 4. Generate and send email
    #
    # Email process internally:
    #     - gets recent digests
    #     - calls CuratorAgent
    #     - matches ranked results with DB data
    #     - calls EmailAgent
    #     - sends through Resend
    #
    # Curation is NOT persisted.
    # ==========================================================

    if send_email:

        logger.info("=" * 70)
        logger.info("STAGE 4: GENERATING AND SENDING EMAIL")
        logger.info("=" * 70)

        results["email"] = send_digest_email(
            hours=digest_hours,
            top_n=top_n,
        )

    else:
        logger.info(
            "Email sending disabled."
        )

    # ==========================================================
    # Complete
    # ==========================================================

    logger.info("=" * 70)
    logger.info("FULL PIPELINE COMPLETE")
    logger.info("=" * 70)

    return results


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    result = run_full_pipeline(
        hours=72,
        content_limit=None,
        digest_limit=None,
        digest_hours=72,
        top_n=10,
        send_email=True,
    )

    print("\n=== PIPELINE RESULT ===")

    for stage, value in result.items():
        print(f"\n{stage}:")
        print(value)
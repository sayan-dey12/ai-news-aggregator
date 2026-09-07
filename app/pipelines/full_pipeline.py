import logging
from typing import Any, Optional

from app.pipelines.scraper_runner import run_scrapers
from app.processors.markdown_processor import process_markdown
from app.processors.transcript_processor import process_youtube_transcripts
from app.processors.digest_processor import process_digests
from app.processors.curation_processor import curate_digests
from app.processes.email_process import send_digest_email


logger = logging.getLogger(__name__)


def run_full_pipeline(
    hours: int = 24,
    content_limit: Optional[int] = None,
    digest_limit: Optional[int] = None,
    digest_hours: int = 24,
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
    # 2. Process OpenAI Markdown
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 2A: PROCESSING OPENAI MARKDOWN")
    logger.info("=" * 70)

    results["openai_markdown"] = process_markdown(
        source_name="openai",
        limit=content_limit,
    )

    # ==========================================================
    # 3. Process Anthropic Markdown
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 2B: PROCESSING ANTHROPIC MARKDOWN")
    logger.info("=" * 70)

    results["anthropic_markdown"] = process_markdown(
        source_name="anthropic",
        limit=content_limit,
    )

    # ==========================================================
    # 4. Process YouTube transcripts
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 2C: PROCESSING YOUTUBE TRANSCRIPTS")
    logger.info("=" * 70)

    results["youtube_transcripts"] = (
        process_youtube_transcripts(
            limit=content_limit
        )
    )

    # ==========================================================
    # 5. Generate digests
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 3: GENERATING DIGESTS")
    logger.info("=" * 70)

    results["digests"] = process_digests(
        limit=digest_limit
    )

    # ==========================================================
    # 6. Curate
    # ==========================================================

    logger.info("=" * 70)
    logger.info("STAGE 4: CURATING DIGESTS")
    logger.info("=" * 70)

    results["curation"] = curate_digests(
        hours=digest_hours
    )

    # ==========================================================
    # 7. Send email
    # ==========================================================

    if send_email:

        logger.info("=" * 70)
        logger.info("STAGE 5: SENDING EMAIL")
        logger.info("=" * 70)

        results["email"] = send_digest_email(
            hours=digest_hours,
            top_n=top_n,
        )

    else:
        logger.info(
            "Email sending disabled."
        )

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
        hours=15,
        content_limit=None,
        digest_limit=None,
        digest_hours=24,
        top_n=10,
        send_email=True,
    )

    print("\n=== PIPELINE RESULT ===")

    for stage, value in result.items():
        print(f"\n{stage}:")
        print(value)

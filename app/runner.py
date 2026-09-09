import logging
import time

from app.database.reset_data import reset_database
from app.pipelines.full_pipeline import run_full_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


RUN_INTERVAL_SECONDS = 24 * 60 * 60


def run_once() -> None:
    """
    Reset the database and run the complete daily pipeline.
    """

    logger.info("=" * 70)
    logger.info("STARTING DAILY NEWS PIPELINE")
    logger.info("=" * 70)

    # ==========================================================
    # 1. Reset previous data
    # ==========================================================

    logger.info("Resetting database data...")

    reset_database()

    logger.info("Database reset complete.")

    # ==========================================================
    # 2. Run full pipeline
    # ==========================================================

    logger.info("Starting full pipeline...")

    result = run_full_pipeline(
        hours=24,
        content_limit=None,
        digest_limit=None,
        digest_hours=24,
        top_n=10,
        send_email=True,
    )

    # ==========================================================
    # 3. Log results
    # ==========================================================

    logger.info("Daily pipeline completed.")

    logger.info("Pipeline result:")

    for stage, value in result.items():
        logger.info("%s: %s", stage, value)

    logger.info("=" * 70)
    logger.info("DAILY NEWS PIPELINE FINISHED")
    logger.info("=" * 70)


def main() -> None:
    """
    Run the complete pipeline once every 24 hours.
    """

    logger.info("Daily runner started.")

    logger.info(
        "Pipeline will run once every %s hours.",
        RUN_INTERVAL_SECONDS // 3600,
    )

    while True:

        try:
            run_once()

        except Exception:
            logger.exception(
                "Daily pipeline failed."
            )

        logger.info(
            "Sleeping for 24 hours before the next run..."
        )

        time.sleep(RUN_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
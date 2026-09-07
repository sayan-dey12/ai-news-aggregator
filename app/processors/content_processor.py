import logging
from typing import Callable, Optional, Any

logger = logging.getLogger(__name__)


def process_missing_content(
    *,
    get_items: Callable,
    generate_content: Callable,
    save_content: Callable,
    limit: Optional[int] = None,
    unavailable_marker: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generic processor for filling missing content.

    Flow:

        fetch missing content
            ↓
        generate content
            ↓
        save content
    """

    items = get_items(limit=limit)

    total = len(items)
    processed = 0
    unavailable = 0
    failed = 0

    logger.info(
        "Starting content processing for %d items",
        total,
    )

    for index, item in enumerate(items, start=1):

        try:
            content = generate_content(item)

            if content:

                save_content(item, content)

                processed += 1

                logger.info(
                    "[%d/%d] Successfully processed",
                    index,
                    total,
                )

            elif unavailable_marker is not None:

                save_content(
                    item,
                    unavailable_marker,
                )

                unavailable += 1

                logger.warning(
                    "[%d/%d] Content unavailable",
                    index,
                    total,
                )

            else:

                failed += 1

                logger.warning(
                    "[%d/%d] Failed to generate content",
                    index,
                    total,
                )

        except Exception as exc:

            failed += 1

            logger.exception(
                "[%d/%d] Error processing item: %s",
                index,
                total,
                exc,
            )

    logger.info(
        "Content processing complete: "
        "%d processed, %d unavailable, %d failed",
        processed,
        unavailable,
        failed,
    )

    return {
        "total": total,
        "processed": processed,
        "unavailable": unavailable,
        "failed": failed,
    }
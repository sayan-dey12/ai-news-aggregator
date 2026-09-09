from typing import Any

from app.config.sources import RSS_SOURCES
from app.processors.markdown_processor import process_markdown
from app.processors.transcript_processor import (
    process_youtube_transcripts,
)


def run_content_processing() -> dict[str, Any]:
    """
    Process all missing RSS article markdown and
    YouTube video transcripts.
    """

    results: dict[str, Any] = {}

    # ==========================================================
    # RSS Markdown
    # ==========================================================

    for source in RSS_SOURCES:

        print(f"\nProcessing Markdown: {source.name}")

        result = process_markdown(
            source_name=source.name,
            limit=None,
        )

        results[source.name] = result

        print(
            f"{source.name}: {result}"
        )

    # ==========================================================
    # YouTube Transcripts
    # ==========================================================

    print("\nProcessing YouTube transcripts...")

    youtube_result = process_youtube_transcripts(
        limit=None,
    )

    results["youtube"] = youtube_result

    print(
        f"youtube: {youtube_result}"
    )

    return results


if __name__ == "__main__":

    results = run_content_processing()

    print("\n" + "=" * 60)
    print("CONTENT PROCESSING COMPLETE")
    print("=" * 60)

    for source, result in results.items():
        print(f"{source}: {result}")
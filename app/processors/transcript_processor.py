from typing import Optional

from app.config.sources import YOUTUBE_SOURCE
from app.database.repository import Repository
from app.processors.content_processor import process_missing_content


TRANSCRIPT_UNAVAILABLE_MARKER = "__UNAVAILABLE__"


def process_youtube_transcripts(
    limit: Optional[int] = None,
) -> dict:

    repo = Repository()
    scraper = YOUTUBE_SOURCE.scraper_class()

    return process_missing_content(
        get_items=lambda limit: repo.get_without_content(
            model=YOUTUBE_SOURCE.model,
            content_field="transcript",
            limit=limit,
        ),

        generate_content=lambda video: (
            transcript.text
            if (
                transcript := scraper.get_transcript(
                    video.video_id
                )
            )
            else None
        ),

        save_content=lambda video, content: (
            repo.update_content(
                model=YOUTUBE_SOURCE.model,
                unique_field=YOUTUBE_SOURCE.unique_field,
                unique_value=video.video_id,
                content_field="transcript",
                content=content,
            )
        ),

        limit=limit,

        unavailable_marker=TRANSCRIPT_UNAVAILABLE_MARKER,
    )
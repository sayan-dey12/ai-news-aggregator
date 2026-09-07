from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm import Session

from .connection import get_session
from .models import (
    YouTubeVideo,
    OpenAIArticle,
    AnthropicArticle,
    Digest,
)


class Repository:

    def __init__(self, session: Optional[Session] = None):
        self.session = session or get_session()

    # ==========================================================
    # Generic creation
    # ==========================================================

    def bulk_create(
        self,
        model: Type,
        items: List[dict],
        unique_field: str,
    ) -> int:
        """
        Generic bulk creation for any model.

        Args:
            model: SQLAlchemy model class.
            items: List of dictionaries containing model fields.
            unique_field: Field used to detect duplicates.

        Returns:
            Number of newly created records.
        """

        if not items:
            return 0

        new_items = []

        for item in items:
            unique_value = item.get(unique_field)

            if unique_value is None:
                continue

            existing = (
                self.session
                .query(model)
                .filter_by(**{unique_field: unique_value})
                .first()
            )

            if existing:
                continue

            new_items.append(model(**item))

        if new_items:
            self.session.add_all(new_items)
            self.session.commit()

        return len(new_items)

    # ==========================================================
    # Missing content
    # ==========================================================

    def get_without_content(
        self,
        model: Type,
        content_field: str,
        limit: Optional[int] = None,
    ) -> list:
        """
        Generic query for records whose content field is NULL.
        """

        field = getattr(model, content_field)

        query = (
            self.session
            .query(model)
            .filter(field.is_(None))
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def update_content(
        self,
        model: Type,
        unique_field: str,
        unique_value: str,
        content_field: str,
        content: str,
    ) -> bool:
        """
        Generic update for a content field.
        """

        record = (
            self.session
            .query(model)
            .filter_by(**{unique_field: unique_value})
            .first()
        )

        if not record:
            return False

        setattr(record, content_field, content)
        self.session.commit()

        return True

    # ==========================================================
    # YouTube compatibility methods
    # ==========================================================

    def get_youtube_videos_without_transcript(
        self,
        limit: Optional[int] = None,
    ) -> List[YouTubeVideo]:

        return self.get_without_content(
            model=YouTubeVideo,
            content_field="transcript",
            limit=limit,
        )

    def update_youtube_video_transcript(
        self,
        video_id: str,
        transcript: str,
    ) -> bool:

        return self.update_content(
            model=YouTubeVideo,
            unique_field="video_id",
            unique_value=video_id,
            content_field="transcript",
            content=transcript,
        )

    # ==========================================================
    # RSS compatibility methods
    # ==========================================================

    def get_anthropic_articles_without_markdown(
        self,
        limit: Optional[int] = None,
    ) -> List[AnthropicArticle]:

        return self.get_without_content(
            model=AnthropicArticle,
            content_field="markdown",
            limit=limit,
        )

    def update_anthropic_article_markdown(
        self,
        guid: str,
        markdown: str,
    ) -> bool:

        return self.update_content(
            model=AnthropicArticle,
            unique_field="guid",
            unique_value=guid,
            content_field="markdown",
            content=markdown,
        )

    def get_openai_articles_without_markdown(
        self,
        limit: Optional[int] = None,
    ) -> List[OpenAIArticle]:

        return self.get_without_content(
            model=OpenAIArticle,
            content_field="markdown",
            limit=limit,
        )

    def update_openai_article_markdown(
        self,
        guid: str,
        markdown: str,
    ) -> bool:

        return self.update_content(
            model=OpenAIArticle,
            unique_field="guid",
            unique_value=guid,
            content_field="markdown",
            content=markdown,
        )

    # ==========================================================
    # Articles without digest
    # ==========================================================

    def get_articles_without_digest(
        self,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:

        articles = []
        seen_ids = set()

        # Existing digests
        digests = self.session.query(Digest).all()

        for digest in digests:
            seen_ids.add(
                f"{digest.article_type}:{digest.article_id}"
            )

        # ------------------------------------------------------
        # YouTube
        # ------------------------------------------------------

        youtube_videos = self.session.query(YouTubeVideo).all()

        for video in youtube_videos:

            key = f"youtube:{video.video_id}"

            if key in seen_ids:
                continue

            if (
                video.transcript
                and video.transcript != "__UNAVAILABLE__"
            ):
                content = video.transcript
                content_source = "transcript"

            elif video.transcript == "__UNAVAILABLE__":
                content = f"""
Title: {video.title}

Transcript not available.

Description:
{video.description or "No description available."}
"""
                content_source = "description"

            else:
                continue

            articles.append({
                "type": "youtube",
                "id": video.video_id,
                "title": video.title,
                "url": video.url,
                "content": content,
                "content_source": content_source,
                "published_at": video.published_at,
            })

        # ------------------------------------------------------
        # OpenAI
        # ------------------------------------------------------

        openai_articles = self.session.query(OpenAIArticle).all()

        for article in openai_articles:

            key = f"openai:{article.guid}"

            if key in seen_ids:
                continue

            content = (
                article.markdown
                or article.description
                or ""
            )

            if not content:
                continue

            articles.append({
                "type": "openai",
                "id": article.guid,
                "title": article.title,
                "url": article.url,
                "content": content,
                "content_source": (
                    "markdown"
                    if article.markdown
                    else "description"
                ),
                "published_at": article.published_at,
            })

        # ------------------------------------------------------
        # Anthropic
        # ------------------------------------------------------

        anthropic_articles = (
            self.session
            .query(AnthropicArticle)
            .all()
        )

        for article in anthropic_articles:

            key = f"anthropic:{article.guid}"

            if key in seen_ids:
                continue

            content = (
                article.markdown
                or article.description
                or ""
            )

            if not content:
                continue

            articles.append({
                "type": "anthropic",
                "id": article.guid,
                "title": article.title,
                "url": article.url,
                "content": content,
                "content_source": (
                    "markdown"
                    if article.markdown
                    else "description"
                ),
                "published_at": article.published_at,
            })

        if limit is not None:
            articles = articles[:limit]

        return articles

    # ==========================================================
    # Digest
    # ==========================================================

    def create_digest(
        self,
        article_type: str,
        article_id: str,
        url: str,
        title: str,
        summary: str,
        published_at: Optional[datetime] = None,
    ) -> Optional[Digest]:

        digest_id = f"{article_type}:{article_id}"

        existing = (
            self.session
            .query(Digest)
            .filter_by(id=digest_id)
            .first()
        )

        if existing:
            return None

        if published_at:

            if published_at.tzinfo is None:
                published_at = published_at.replace(
                    tzinfo=timezone.utc
                )

            created_at = published_at

        else:
            created_at = datetime.now(timezone.utc)

        digest = Digest(
            id=digest_id,
            article_type=article_type,
            article_id=article_id,
            url=url,
            title=title,
            summary=summary,
            created_at=created_at,
        )

        self.session.add(digest)
        self.session.commit()

        return digest

    def get_recent_digests(
        self,
        hours: int = 24,
    ) -> List[Dict[str, Any]]:

        cutoff_time = (
            datetime.now(timezone.utc)
            - timedelta(hours=hours)
        )

        digests = (
            self.session
            .query(Digest)
            .filter(Digest.created_at >= cutoff_time)
            .order_by(Digest.created_at.desc())
            .all()
        )

        return [
            {
                "id": digest.id,
                "article_type": digest.article_type,
                "article_id": digest.article_id,
                "url": digest.url,
                "title": digest.title,
                "summary": digest.summary,
                "created_at": digest.created_at,
            }
            for digest in digests
        ]
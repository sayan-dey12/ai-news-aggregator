from dataclasses import dataclass
from typing import Type

from app.config.settings import YOUTUBE_CHANNELS

from app.database.models import (
    AnthropicArticle,
    OpenAIArticle,
    YouTubeVideo,
)

from app.scrapers.anthropic_sources import AnthropicScraper
from app.scrapers.openai_sources import OpenAIScraper
from app.scrapers.youtube_sources import YouTubeScraper


@dataclass(frozen=True)
class RSSSource:
    name: str
    scraper_class: Type
    model: Type
    unique_field: str


@dataclass(frozen=True)
class YouTubeSource:
    name: str
    scraper_class: Type
    model: Type
    unique_field: str
    channel_ids: tuple[str, ...]


RSS_SOURCES = (
    RSSSource(
        name="openai",
        scraper_class=OpenAIScraper,
        model=OpenAIArticle,
        unique_field="guid",
    ),
    RSSSource(
        name="anthropic",
        scraper_class=AnthropicScraper,
        model=AnthropicArticle,
        unique_field="guid",
    ),
)


YOUTUBE_SOURCE = YouTubeSource(
    name="youtube",
    scraper_class=YouTubeScraper,
    model=YouTubeVideo,
    unique_field="video_id",
    channel_ids=tuple(YOUTUBE_CHANNELS),
)

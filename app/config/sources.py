from dataclasses import dataclass
from typing import Type

from app.config.settings import (
    ANTHROPIC_RSS_URLS,
    OPENAI_RSS_URLS,
    HUGGING_FACE_RSS_URLS,
    GOOGLE_RSS_URLS,
    META_AI_RSS_URLS,
    MISTRAL_URLS,
    XAI_URLS,
    OLLAMA_URLS,
    THE_BATCH_BY_DEEPLEARNING_AI_URLS,
    SIMON_WILLISONS_URLS,
    COHER_URLS,
)

from app.database.models import (
    RSSArticle,
    YouTubeVideo,
)

from app.scrapers.base.base_rss_scraper import BaseRSSScraper
from app.scrapers.youtube_sources import YouTubeScraper

from app.config.settings import YOUTUBE_CHANNELS

from app.scrapers.rss_scraper import RSSScraper


@dataclass(frozen=True)
class RSSSource:

    name: str
    rss_urls: tuple[str, ...]
    model: Type
    unique_field: str
    markdown: bool = True
    scraper_class: Type = RSSScraper

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
        rss_urls=tuple(OPENAI_RSS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="anthropic",
        rss_urls=tuple(ANTHROPIC_RSS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="huggingface",
        rss_urls=tuple(HUGGING_FACE_RSS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="google",
        rss_urls=tuple(GOOGLE_RSS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="meta_ai",
        rss_urls=tuple(META_AI_RSS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="mistral",
        rss_urls=tuple(MISTRAL_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="xai",
        rss_urls=tuple(XAI_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="ollama",
        rss_urls=tuple(OLLAMA_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="the_batch",
        rss_urls=tuple(THE_BATCH_BY_DEEPLEARNING_AI_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="simon_willison",
        rss_urls=tuple(SIMON_WILLISONS_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),

    RSSSource(
        name="cohere",
        rss_urls=tuple(COHER_URLS),
        model=RSSArticle,
        unique_field="guid",
        markdown=True,
    ),
)


YOUTUBE_SOURCE = YouTubeSource(
    name="youtube",
    scraper_class=YouTubeScraper,
    model=YouTubeVideo,
    unique_field="video_id",
    channel_ids=tuple(YOUTUBE_CHANNELS),
)

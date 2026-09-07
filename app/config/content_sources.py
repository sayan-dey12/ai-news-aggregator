from dataclasses import dataclass
from typing import Type

from app.database.models import (
    AnthropicArticle,
    OpenAIArticle,
)

from app.scrapers.anthropic_sources import AnthropicScraper
from app.scrapers.openai_sources import OpenAIScraper


@dataclass(frozen=True)
class ContentSource:
    name: str
    model: Type
    unique_field: str
    content_field: str
    scraper_class: Type


MARKDOWN_SOURCES = (
    ContentSource(
        name="openai",
        model=OpenAIArticle,
        unique_field="guid",
        content_field="markdown",
        scraper_class=OpenAIScraper,
    ),
    ContentSource(
        name="anthropic",
        model=AnthropicArticle,
        unique_field="guid",
        content_field="markdown",
        scraper_class=AnthropicScraper,
    ),
)
from dataclasses import dataclass
from typing import Callable, Type

from app.database.models import (
    OpenAIArticle,
    AnthropicArticle,
)

from app.scrapers.openai_sources import OpenAIScraper
from app.scrapers.anthropic_sources import AnthropicScraper


@dataclass(frozen=True)
class MarkdownSource:
    name: str
    model: Type
    unique_field: str
    content_field: str
    scraper_class: Type


MARKDOWN_SOURCES = (
    MarkdownSource(
        name="openai",
        model=OpenAIArticle,
        unique_field="guid",
        content_field="markdown",
        scraper_class=OpenAIScraper,
    ),

    MarkdownSource(
        name="anthropic",
        model=AnthropicArticle,
        unique_field="guid",
        content_field="markdown",
        scraper_class=AnthropicScraper,
    ),
)
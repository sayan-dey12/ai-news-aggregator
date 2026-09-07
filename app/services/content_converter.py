import logging
import requests
from html_to_markdown import convert

logger = logging.getLogger(__name__)


class ContentConverter:

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def url_to_markdown(self, url: str) -> str | None:
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0 Safari/537.36"
                    )
                },
            )

            response.raise_for_status()

            result = convert(response.text)

            markdown = result["content"]

            if not markdown or not markdown.strip():
                logger.warning(
                    "HTML to Markdown returned empty content: %s",
                    url,
                )
                return None

            return markdown.strip()

        except Exception as exc:
            logger.exception(
                "Failed to convert URL to Markdown: %s | %s",
                url,
                exc,
            )
            return None
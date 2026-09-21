import json
import logging
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from app.agents.base.base_llm_agent import BaseLLMAgent


load_dotenv()

logger = logging.getLogger(__name__)


class DigestOutput(BaseModel):
    title: str
    summary: str


PROMPT = """
You are an expert AI news analyst specializing in
summarizing technical articles, research papers, and video content
about artificial intelligence.

Your role is to create concise, informative digests that help readers
quickly understand the key points and significance of AI-related content.

Guidelines:

- Create a compelling title of 5-10 words that captures the essence
  of the content.
- Write a 2-3 sentence summary that highlights the main points and why
  they matter.
- Focus on actionable insights and implications.
- Use clear, accessible language while maintaining technical accuracy.
- Avoid marketing fluff and focus on substance.

The provided Markdown may contain additional webpage elements such as:

- navigation menus
- headers and footers
- cookie notices
- subscription prompts
- author information
- social sharing links
- related articles
- recommended content
- legal/privacy text
- website metadata
- repeated headings or navigation elements

Ignore these elements.

Use only the actual article content when generating the digest.

Do not summarize navigation, promotional content, related articles,
website chrome, or other non-article material.

If the Markdown contains multiple sections, identify the main article
and base the digest primarily on that article.

YouTube-specific instructions:

- Some YouTube videos may not have a transcript.
- When the content says "Transcript not available", do not treat that
  statement as part of the video's subject matter.
- In that situation, use the video's title and the meaningful parts of
  its description to understand what the video is about.
- Ignore promotional or navigational content such as course links,
  playlist links, social-media links, newsletter links, affiliate links,
  sponsorships, calls to subscribe, calls to follow, and similar
  promotional material.
- Do not summarize the links themselves.
- If the description contains both useful information and promotional
  material, use only the useful information.
- The video title is an important source of context when no transcript
  is available.
- Do not invent technical details that are not supported by the title
  or description.

OUTPUT REQUIREMENTS:

- Return ONLY a valid JSON object.
- Do NOT return Markdown.
- Do NOT use ```json code fences.
- Do NOT include any explanation before or after the JSON.
- The JSON must contain exactly these fields:

{
  "title": "string",
  "summary": "string"
}
"""


class DigestAgent(BaseLLMAgent):

    def __init__(self):
        super().__init__()
        self.system_prompt = PROMPT

    def generate_digest(
        self,
        title: str,
        content: str,
        article_type: str,
    ) -> Optional[DigestOutput]:

        user_prompt = (
            f"Create a digest for this {article_type}:\n\n"
            f"Title: {title}\n\n"
            f"Content:\n{content[:8000]}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.7,
                response_format={
                    "type": "json_object",
                },
            )

            # --------------------------------------------------
            # 1. Validate response object
            # --------------------------------------------------

            if response is None:
                logger.error(
                    "LLM returned None response for article: %s",
                    title,
                )
                return None

            if not response.choices:
                logger.error(
                    "LLM returned no choices for article: %s",
                    title,
                )
                return None

            # --------------------------------------------------
            # 2. Get message safely
            # --------------------------------------------------

            message = response.choices[0].message

            if message is None:
                logger.error(
                    "LLM returned None message for article: %s",
                    title,
                )
                return None

            # --------------------------------------------------
            # 3. Get content safely
            # --------------------------------------------------

            raw_content = message.content

            if raw_content is None:
                logger.error(
                    "LLM returned None content for article: %s",
                    title,
                )

                logger.debug(
                    "Raw LLM message: %r",
                    message,
                )

                return None

            if not isinstance(raw_content, str):
                logger.error(
                    "Unexpected content type %s for article: %s",
                    type(raw_content).__name__,
                    title,
                )
                return None

            raw_content = raw_content.strip()

            if not raw_content:
                logger.error(
                    "LLM returned empty content for article: %s",
                    title,
                )
                return None

            # --------------------------------------------------
            # 4. Parse JSON
            # --------------------------------------------------

            try:
                data = json.loads(raw_content)
            except json.JSONDecodeError as exc:
                logger.error(
                    "Invalid JSON returned for article '%s': %s",
                    title,
                    exc,
                )

                logger.debug(
                    "Raw model output: %r",
                    raw_content,
                )

                return None

            # --------------------------------------------------
            # 5. Validate expected structure
            # --------------------------------------------------

            try:
                digest = DigestOutput.model_validate(data)
            except ValidationError as exc:
                logger.error(
                    "Invalid digest structure for article '%s': %s",
                    title,
                    exc,
                )

                logger.debug(
                    "Parsed model output: %r",
                    data,
                )

                return None

            # --------------------------------------------------
            # 6. Final validation
            # --------------------------------------------------

            if not digest.title.strip():
                logger.error(
                    "Digest title is empty for article: %s",
                    title,
                )
                return None

            if not digest.summary.strip():
                logger.error(
                    "Digest summary is empty for article: %s",
                    title,
                )
                return None

            return digest

        except Exception as exc:
            logger.exception(
                "Error generating digest for '%s': %s",
                title,
                exc,
            )
            return None
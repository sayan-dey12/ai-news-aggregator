import os
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from app.agents.base.base_llm_agent import BaseLLMAgent


load_dotenv()


class DigestOutput(BaseModel):
    title: str
    summary: str

PROMPT = """You are an expert AI news analyst specializing in
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

  "title": string
  "summary": string
"""
class DigestAgent(BaseLLMAgent):
    def __init__(self):
        super().__init__()
        
        self.model = "minimax/minimax-m3:free"
        self.system_prompt = PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        try:
            user_prompt = f"Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:8000]}"

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
                    "type": "json_object"
                },
            )

            content = response.choices[0].message.content


            # print("\n========== RAW MODEL RESPONSE ==========")
            # print(content)
            # print("========================================\n")

            if not content:
                return None

            return DigestOutput.model_validate_json(content)

        except Exception as e:
            print(f"Error generating digest: {e}")
            return None
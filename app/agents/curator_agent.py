import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from app.agents.base.base_llm_agent import BaseLLMAgent


load_dotenv()


class RankedArticle(BaseModel):
    digest_id: str = Field(
        description="The ID of the digest (article_type:article_id)"
    )
    relevance_score: float = Field(
        description="Relevance score from 0.0 to 10.0",
        ge=0.0,
        le=10.0,
    )
    rank: int = Field(
        description="Rank position (1 = most relevant)",
        ge=1,
    )
    reasoning: str = Field(
        description="Brief explanation of why this article is relevant"
    )


class RankedDigestList(BaseModel):
    articles: List[RankedArticle]


CURATOR_PROMPT = """
You are an expert AI news curator specializing in personalized
content ranking for AI professionals.

Your task is to analyze AI news digests and rank them according
to the user's profile.

Ranking Criteria:
1. Relevance to the user's interests and background
2. Technical depth and practical value
3. Novelty and significance
4. Alignment with the user's expertise level
5. Actionability and real-world applicability

Scoring Guidelines:
- 9.0-10.0: Extremely relevant and directly aligned with the user's interests
- 7.0-8.9: Highly relevant with strong alignment
- 5.0-6.9: Moderately relevant with some alignment
- 3.0-4.9: Somewhat relevant with limited alignment
- 0.0-2.9: Low relevance

Important:
- Rank every article.
- Rank 1 must be the most relevant article.
- Each article must have a unique rank.
- Do not omit any article.
- Base the ranking on the user's profile rather than general popularity.
- Avoid giving higher scores simply because a topic is popular or
  comes from a well-known company.
"""


class CuratorAgent:
    def __init__(self, user_profile: dict):
        super().__init__()

        self.user_profile = user_profile
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        interests = "\n".join(
            f"- {interest}"
            for interest in self.user_profile["interests"]
        )

        preferences = self.user_profile["preferences"]

        preferences_text = "\n".join(
            f"- {key}: {value}"
            for key, value in preferences.items()
        )

        return f"""
{CURATOR_PROMPT}

USER PROFILE

Name:
{self.user_profile["name"]}

Title:
{self.user_profile.get("title", "")}

Background:
{self.user_profile["background"]}

Expertise Level:
{self.user_profile["expertise_level"]}

Interests:
{interests}

Preferences:
{preferences_text}

OUTPUT REQUIREMENTS:

Return ONLY a valid JSON object.

DO NOT return Markdown.
DO NOT use headings.
DO NOT use bullet points.
DO NOT use tables.
DO NOT use ```json code fences.
DO NOT include any explanation before or after the JSON.

ID RULES:

- The "digest_id" MUST exactly match one of the IDs provided in the input.
- Copy the digest ID exactly as provided.
- Do NOT modify, reconstruct, shorten, or generate digest IDs.
- Do NOT change the article_type prefix.
- Every input digest must appear exactly once.
- Do NOT create IDs that are not present in the input.

RANKING RULES:

- Rank every digest.
- Rank 1 is the most relevant.
- Rank {{len(digests)}} is the least relevant.
- Every rank must be unique.
- Use exactly one rank from 1 to {{len(digests)}} for each digest.

SCORING RULES:

- relevance_score must be between 0.0 and 10.0.
- The score represents absolute relevance to the user's profile, not relative position.
- Use the following scale:
  9.0-10.0: Extremely relevant and directly aligned
  7.0-8.9: Highly relevant
  5.0-6.9: Moderately relevant
  3.0-4.9: Somewhat relevant
  0.0-2.9: Low relevance
- Do not assign scores based on article rank alone.
- Articles with similar relevance may have similar scores.

OUTPUT STRUCTURE:

{{
  "articles": [
    {{
      "digest_id": "exact-id-from-input",
      "relevance_score": 0.0,
      "rank": 1,
      "reasoning": "Brief explanation of relevance."
    }}
  ]
}}

The "articles" array MUST contain exactly one item for every digest provided.
"""

    def rank_digests(
        self,
        digests: List[dict],
    ) -> List[RankedArticle]:

        if not digests:
            return []

        digest_list = "\n\n".join(
            [
                f"""
ID: {digest["id"]}
Title: {digest["title"]}
Summary: {digest["summary"]}
Type: {digest["article_type"]}
"""
                for digest in digests
            ]
        )

        user_prompt = f"""
Rank the following {len(digests)} AI news digests
according to the user profile.

{digest_list}

Return one ranking result for every digest.

The rank must be between 1 and {len(digests)}.

Rank the articles from most relevant to least relevant.
"""

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
                temperature=0.3,
                response_format={
                    "type": "json_object"
                },
            )

            content = response.choices[0].message.content
            
            # print("\n========== RAW CURATOR RESPONSE ==========")
            # print(repr(content))
            # print("==========================================\n")

            if not content:
                return []

            # Parse the JSON returned by the model
            import json

            data = json.loads(content)

            ranked_list = RankedDigestList.model_validate(data)

            return ranked_list.articles

        except Exception as e:
            print(f"Error ranking digests: {e}")
            return []
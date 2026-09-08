import json
from typing import List

from pydantic import BaseModel, Field
from app.agents.base.base_llm_agent import BaseLLMAgent


class RankedArticle(BaseModel):
    digest_id: str = Field(
        description="The exact ID of the digest provided in the input"
    )

    relevance_score: float = Field(
        description="Absolute relevance score from 0.0 to 10.0",
        ge=0.0,
        le=10.0,
    )

    rank: int = Field(
        description="Rank position, where 1 is the most relevant",
        ge=1,
    )

    reasoning: str = Field(
        description="Brief explanation of why the article is relevant"
    )


class RankedDigestList(BaseModel):
    articles: List[RankedArticle]


CURATOR_PROMPT = """
You are an expert AI news curator specializing in personalized
content ranking for AI professionals.

Your task is to analyze AI news digests and rank them according
to the user's profile.

RANKING CRITERIA

Evaluate each article using these factors:

1. Relevance to the user's interests and background
2. Technical depth and practical value
3. Novelty and significance
4. Alignment with the user's expertise level
5. Actionability and real-world applicability

PRIORITY ORDER

For this user, prioritize topics approximately in this order:

1. AI engineering implementation
2. LLM application development
3. AI agents and agentic workflows
4. Agent architectures, tools, memory, and orchestration
5. RAG and retrieval systems
6. Generative AI applications
7. Prompt engineering and structured LLM outputs
8. AI APIs and model providers
9. Python backend development and FastAPI
10. PostgreSQL, SQLAlchemy, and database-backed AI systems
11. Docker, deployment, MLOps, and production AI systems
12. Multimodal AI
13. Practical AI tutorials and implementation guides
14. General AI model/product news
15. AI business, social, policy, or other general AI news

IMPORTANT

A technically useful article should generally rank higher than
a popular but superficial announcement.

Do NOT give a high score merely because:

- the company is famous
- the model is popular
- the announcement is trending
- the article is widely discussed
- the article mentions AI
- the article comes from OpenAI, Google, Anthropic, Meta, etc.

Prefer substance over popularity.

USER PROFILE ALIGNMENT

The user is an intermediate-level aspiring AI engineer and
backend developer who prefers:

- practical content
- technical depth
- hands-on projects
- production-focused engineering
- understanding system architecture
- learning by building
- real-world AI applications

The user prefers to avoid:

- marketing hype
- surface-level AI news
- content with little technical or practical value

SCORING GUIDELINES

9.0-10.0:
Extremely relevant and directly aligned with the user's core
interests. Strong technical or practical value.

7.0-8.9:
Highly relevant with strong alignment to the user's interests.

5.0-6.9:
Moderately relevant with some useful connection to the user's
interests.

3.0-4.9:
Somewhat relevant but outside the user's primary focus.

0.0-2.9:
Low relevance with little connection to the user's goals.

The score represents ABSOLUTE relevance to the user.
Do not assign scores simply based on relative ranking.

ID RULES

- Copy every digest ID EXACTLY.
- Do not modify any character of a digest ID.
- Do not create a new digest ID.
- Do not reconstruct a digest ID.
- Do not shorten a digest ID.
- Do not change the article_type prefix.
- Every input digest must appear exactly once.
- Do not omit any digest.

RANKING RULES

- Rank every digest.
- Rank 1 is the most relevant.
- The final rank must equal the number of input digests.
- Every rank must be unique.
- Use exactly one rank from 1 through N.
- Do not skip ranks.
- Do not duplicate ranks.

OUTPUT REQUIREMENTS

Return ONLY a valid JSON object.

Do NOT return Markdown.
Do NOT use headings.
Do NOT use bullet points.
Do NOT use tables.
Do NOT use ```json code fences.
Do NOT include any explanation before or after the JSON.

The output must contain exactly one object for every input digest.

OUTPUT STRUCTURE

{
  "articles": [
    {
      "digest_id": "exact-id-from-input",
      "relevance_score": 0.0,
      "rank": 1,
      "reasoning": "Brief explanation of relevance."
    }
  ]
}
"""


class CuratorAgent(BaseLLMAgent):

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
"""

    def rank_digests(
        self,
        digests: List[dict],
    ) -> List[RankedArticle]:

        if not digests:
            return []

        digest_list = "\n\n".join(
            f"""
ID: {digest["id"]}
Title: {digest["title"]}
Summary: {digest["summary"]}
Type: {digest["article_type"]}
"""
            for digest in digests
        )

        count = len(digests)

        user_prompt = f"""
Rank all {count} AI news digests according to the user profile.

INPUT DIGESTS

{digest_list}

STRICT REQUIREMENTS

Return exactly {count} ranking objects.

Every input digest ID must appear exactly once.

Ranks must contain every number from 1 to {count}
exactly once.

Rank 1 must be the most relevant article.

Rank {count} must be the least relevant article.

Do not omit, duplicate, modify, or invent any digest ID.

Return ONLY the JSON object.
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
                temperature=0.2,
                response_format={
                    "type": "json_object"
                },
            )

            content = response.choices[0].message.content

            if not content:
                return []

            data = json.loads(content)

            ranked_list = RankedDigestList.model_validate(data)

            return ranked_list.articles

        except Exception as e:
            print(f"Error ranking digests: {e}")
            return []
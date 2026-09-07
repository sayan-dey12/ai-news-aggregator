import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class EmailIntroduction(BaseModel):
    greeting: str = Field(
        description="Personalized greeting containing the user's name and current date."
    )
    introduction: str = Field(
        description="A concise 2-3 sentence overview of the articles included in the email."
    )


class RankedArticleDetail(BaseModel):
    digest_id: str
    rank: int
    relevance_score: float
    title: str
    summary: str
    url: str
    article_type: str
    reasoning: Optional[str] = None


class EmailDigestResponse(BaseModel):
    introduction: EmailIntroduction
    articles: List[RankedArticleDetail]
    total_ranked: int
    top_n: int

    def to_markdown(self) -> str:
        markdown = f"{self.introduction.greeting}\n\n"
        markdown += f"{self.introduction.introduction}\n\n"
        markdown += "---\n\n"

        for article in self.articles:
            markdown += f"## {article.title}\n\n"
            markdown += f"{article.summary}\n\n"
            markdown += f"[Read more →]({article.url})\n\n"
            markdown += "---\n\n"

        return markdown


class EmailDigest(BaseModel):
    introduction: EmailIntroduction
    ranked_articles: List[dict] = Field(
        description="The ranked articles included in the email."
    )


EMAIL_PROMPT = """You are an expert email writer specializing in personalized AI news digests.

Your role is to write a warm, concise, professional introduction for a personalized AI news digest.

The introduction should:
- Greet the user by name.
- Mention the current date.
- State how many articles are included.
- Briefly preview the main themes or interesting topics.
- Match the number of articles actually provided.
- Never claim that there are 10 articles unless 10 articles are actually provided.

Keep the introduction to 2-3 sentences.
Do not write the individual article summaries.
Do not use markdown.
"""


class EmailAgent:
    def __init__(self, user_profile: dict):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = "minimax/minimax-m3:free"
        self.user_profile = user_profile

    def generate_introduction(
        self,
        ranked_articles: List[RankedArticleDetail],
    ) -> EmailIntroduction:

        current_date = datetime.now().strftime("%B %d, %Y")
        article_count = len(ranked_articles)

        # No articles
        if article_count == 0:
            return EmailIntroduction(
                greeting=(
                    f"Hey {self.user_profile['name']}, "
                    f"here is your AI news digest for {current_date}."
                ),
                introduction="No relevant articles were found for this digest.",
            )

        # Extract only the information the LLM needs
        article_summaries = "\n".join(
            [
                (
                    f"{idx}. {article.title} "
                    f"(Relevance: {article.relevance_score:.1f}/10)\n"
                    f"Summary: {article.summary}"
                )
                for idx, article in enumerate(ranked_articles, start=1)
            ]
        )

        user_prompt = f"""
Create an email introduction for {self.user_profile['name']}.

Date: {current_date}

Number of articles included: {article_count}

Articles:

{article_summaries}

Write a short introduction that accurately previews these {article_count} articles.
"""

        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=EMAIL_PROMPT,
                temperature=0.7,
                input=user_prompt,
                text_format=EmailIntroduction,
            )

            intro = response.output_parsed

            if intro is None:
                raise ValueError("Model returned no structured output.")

            # We control the greeting ourselves so that the model
            # cannot accidentally use the wrong name/date.
            intro.greeting = (
                f"Hey {self.user_profile['name']}, "
                f"here is your AI news digest for {current_date}."
            )

            return intro

        except Exception as e:
            print(f"Error generating email introduction: {e}")

            return EmailIntroduction(
                greeting=(
                    f"Hey {self.user_profile['name']}, "
                    f"here is your AI news digest for {current_date}."
                ),
                introduction=(
                    f"Here are {article_count} AI news articles "
                    f"ranked by relevance to your interests."
                ),
            )

    def create_email_digest(
        self,
        ranked_articles: List[RankedArticleDetail],
        limit: int = 10,
    ) -> EmailDigest:

        # Never return more articles than actually exist.
        top_articles = ranked_articles[:limit]

        introduction = self.generate_introduction(top_articles)

        return EmailDigest(
            introduction=introduction,
            ranked_articles=[
                article.model_dump()
                if isinstance(article, RankedArticleDetail)
                else article
                for article in top_articles
            ],
        )

    def create_email_digest_response(
        self,
        ranked_articles: List[RankedArticleDetail],
        total_ranked: int,
        limit: int = 10,
    ) -> EmailDigestResponse:

        # If there are only 5 articles, this produces 5.
        # If there are 10, it produces 10.
        # If there are 20, it produces the top 10.
        top_articles = ranked_articles[:limit]

        introduction = self.generate_introduction(top_articles)

        return EmailDigestResponse(
            introduction=introduction,
            articles=top_articles,
            total_ranked=total_ranked,
            top_n=len(top_articles),
        )
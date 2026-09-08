from openai import OpenAI

# from app.config.settings import (
#     OPENROUTER_API_KEY,
#     OPENROUTER_BASE_URL,
#     LLM_MODEL,
# )

from app.config.settings import (
    GEMINI_API_KEY,
    GEMINI_BASE_URL,
    LLM_MODEL
)

from .base_agent import BaseAgent


class BaseLLMAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url=GEMINI_BASE_URL,
        )

        self.model = LLM_MODEL
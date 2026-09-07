from openai import OpenAI

from app.config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    LLM_MODEL,
)

from .base_agent import BaseAgent


class BaseLLMAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

        self.model = LLM_MODEL
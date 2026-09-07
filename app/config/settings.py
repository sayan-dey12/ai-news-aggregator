import os

from dotenv import load_dotenv

load_dotenv()


# -------------------------
# LLM Configuration
# -------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

LLM_MODEL = "minimax/minimax-m3:free"


# -------------------------
# YouTube Configuration
# -------------------------

YOUTUBE_CHANNELS = [
    "UCn8ujwUInbJkBhffxqAPBVQ",  # Dave Ebbelaar
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
    "UChpleBmo18P08aKCIgti38g",  # Matt Wolfe
]
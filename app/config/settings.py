import os

from dotenv import load_dotenv

load_dotenv()


# -------------------------
# LLM Configuration
# -------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

LLM_MODEL = "google/gemma-4-31b-it:free"


# -------------------------
# YouTube Configuration
# -------------------------

YOUTUBE_CHANNELS = [
    "UCn8ujwUInbJkBhffxqAPBVQ",  # Dave Ebbelaar
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
    "UChpleBmo18P08aKCIgti38g",  # Matt Wolfe
    "UCKelCK4ZaO6HeEI1KQjqzWA",  # The AI Daily Brief: Artificial Intelligence News
    "UCNJ1Ymd5yFuUPtn21xtRbbw",  # AI Explained
    "UCbfYPyITQ-7l4upoX8nvctg",  # Two Minute Papers
]


# ========================================================== 
# RSS Configuration 
# ==========================================================
ANTHROPIC_RSS_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
]

OPENAI_RSS_URLS = [
    "https://openai.com/news/rss.xml",
]
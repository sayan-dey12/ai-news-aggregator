import os

from dotenv import load_dotenv

load_dotenv()


# -------------------------
# LLM Configuration
# -------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

#-------------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

LLM_MODEL = "gemini-2.5-flash-lite"


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
    "https://openai.com/news/engineering/rss.xml",
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_openai_developer.xml",
    
]

HUGGING_FACE_RSS_URLS = [
    "https://huggingface.co/blog/feed.xml",
]

GOOGLE_RSS_URLS = [
    "https://deepmind.google/blog/rss.xml",                                               # google deepmind
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_google_ai.xml", # google developer blog - ai
]

META_AI_RSS_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_meta_ai.xml",
]

MISTRAL_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_mistral.xml",
]

XAI_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_xainews.xml",
]

OLLAMA_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_ollama.xml",
]

THE_BATCH_BY_DEEPLEARNING_AI_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_the_batch.xml",
]

SIMON_WILLISONS_URLS = [
    "https://simonwillison.net/atom/beats/tool/",
]

COHER_URLS = [
    "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_cohere.xml",
]


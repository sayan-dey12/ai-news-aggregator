
from app.scrapers.anthropic import AnthropicScraper
from app.scrapers.openai import OpenAIScraper
from app.scrapers.youtube import YouTubeScraper
from app.config import YOUTUBE_CHANNELS

from typing import List

def run_scrapers(hours: int = 24) -> dict:
    
    anthropic_scraper = AnthropicScraper()
    openai_scraper = OpenAIScraper()
    youtube_scraper = YouTubeScraper()    
    
    youtube_videos = []
    
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours)
        youtube_videos.extend(videos)
        
    openai_articles = openai_scraper.get_articles(hours=hours)
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    
    return{
        "anthropic" : anthropic_articles,
        "openai" : openai_articles,
        "youtube" : youtube_videos,
    }
    
    
    
    
if __name__ == "__main__":
    
    result = run_scrapers(hours=150)
    print(f"Anthropic articles: {len(result['anthropic'])}")
    print(f"OpenAI articles: {len(result['openai'])}")
    print(f"YouTube videos: {len(result['youtube'])}")

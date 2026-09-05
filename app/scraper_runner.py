
from app.scrapers.anthropic import AnthropicScraper
from app.scrapers.openai import OpenAIScraper
from app.scrapers.youtube import YouTubeScraper
from app.config import YOUTUBE_CHANNELS
from app.database.repository import Repository


def run_scrapers(hours: int = 24) -> dict:
    
    anthropic_scraper = AnthropicScraper()
    openai_scraper = OpenAIScraper()
    youtube_scraper = YouTubeScraper() 
    repo = Repository()
    
    youtube_videos = []
    video_dicts = []
    
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
        youtube_videos.extend(videos)
        
        video_dicts.extend([
            {
                "video_id": v.video_id,
                "title": v.title,
                "url": v.url,
                "channel_id": channel_id,
                "published_at": v.published_at,
                "description": v.description,
                "transcript": v.transcript
            }
            for v in videos
        ])
        
        if video_dicts:
            repo.bulk_create_youtube_videos(video_dicts)
        
    openai_articles = openai_scraper.get_articles(hours=hours)
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    
    
    if openai_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in openai_articles
        ]
        repo.bulk_create_openai_articles(article_dicts)
        
        
        
    if anthropic_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in anthropic_articles
        ]
        repo.bulk_create_anthropic_articles(article_dicts)
        
        
        
    
    return{
        "anthropic" : anthropic_articles,
        "openai" : openai_articles,
        "youtube" : youtube_videos,
    }
    
    
    
    
if __name__ == "__main__":
    
    result = run_scrapers(hours=48)
    print(f"Anthropic articles: {len(result['anthropic'])}")
    print(f"OpenAI articles: {len(result['openai'])}")
    print(f"YouTube videos: {len(result['youtube'])}")

from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import time
import logging

import feedparser
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
)
from youtube_transcript_api.proxies import WebshareProxyConfig

logger = logging.getLogger(__name__)

class Transcript(BaseModel):
    text: str


class ChannelVideo(BaseModel):
    title: str
    url: str
    video_id: str
    published_at: datetime
    description: str
    transcript: Optional[str] = None
    
    
class YouTubeScraper:
    
    def __init__(self):
        proxy_config = None
        proxy_username = os.getenv("PROXY_USERNAME")
        proxy_password = os.getenv("PROXY_PASSWORD")
        
        if proxy_username and proxy_password:
            proxy_config = WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_password
            )
        
        self.transcript_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        
        
    def _extract_video_id(self, video_url: str) -> str:
        if "youtube.com/watch?v=" in video_url:
            return video_url.split("v=")[1].split("&")[0]

        if "youtube.com/shorts/" in video_url:
            return video_url.split("shorts/")[1].split("?")[0]

        if "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]

        return video_url
        
        
    def _get_rss_url(self, channel_id: str) -> str:
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    
    def get_transcript(
        self,
        video_id: str,
    ) -> Optional[Transcript]:

        max_retries = 3
        delay = 2

        for attempt in range(1, max_retries + 1):
            try:
                transcript = self.transcript_api.fetch(video_id)

                text = " ".join(
                    snippet.text
                    for snippet in transcript.snippets
                )

                return Transcript(text=text)

            except (TranscriptsDisabled, NoTranscriptFound):
                return None

            except Exception as exc:
                logger.warning(
                    "Transcript attempt %d/%d failed for %s: %s",
                    attempt,
                    max_retries,
                    video_id,
                    exc,
                )

                if attempt == max_retries:
                    logger.exception(
                        "Failed to fetch transcript for %s after %d attempts",
                        video_id,
                        max_retries,
                    )
                    return None

                time.sleep(delay)
                delay *= 2

        return None
        
    def get_latest_videos(
        self,
        channel_id: str,
        hours: int = 24,
    ) -> list[ChannelVideo]:

        feed = feedparser.parse(
            self._get_rss_url(channel_id)
        )

        if not feed.entries:
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        videos = []

        for entry in feed.entries:

            published_time = datetime(
                *entry.published_parsed[:6],
                tzinfo=timezone.utc,
            )

            if published_time >= cutoff_time:

                video_id = self._extract_video_id(
                    entry.link
                )

                videos.append(
                    ChannelVideo(
                        title=entry.title,
                        url=entry.link,
                        video_id=video_id,
                        published_at=published_time,
                        description=entry.get(
                            "summary",
                            "",
                        ),
                    )
                )

        return videos
    
    
    def scrape_channel(self, channel_id: str, hours: int = 150) -> list[ChannelVideo]:
        videos = self.get_latest_videos(channel_id, hours)
        result = []
        for video in videos:
            transcript = self.get_transcript(video.video_id)
            result.append(
                video.model_copy(
                    update={"transcript": transcript.text if transcript else None}
                )
            )
        return result


if __name__ == "__main__":
    scraper = YouTubeScraper()

    # videos = scraper.get_latest_videos(
    #     "UCNQ6FEtztATuaVhZKCY28Yw"
    # )

    # transcript: Transcript = scraper.get_transcript("jqd6_bbjhS8")
    # print(transcript)
    
    #print(videos)
    # UCNQ6FEtztATuaVhZKCY28Yw
    #result = scraper.scrape_channel("UCn8ujwUInbJkBhffxqAPBVQ")
    #result = scraper.scrape_channel("UCawZsQWqfGSbCI5yjkdVkTA")
    
    # result = scraper.get_latest_videos("UCawZsQWqfGSbCI5yjkdVkTA" , hours=80)
    # print(len(result))
    # print(result)
    
    # result_transcript = scraper.get_transcript("xdXLzFzxA9Q")
    # print(result_transcript)
    
    # for video in result:
    #     print("=" * 80)
    #     print(f"Title       : {video.title}")
    #     print(f"Video ID    : {video.video_id}")
    #     print(f"URL         : {video.url}")
    #     print(f"Published   : {video.published_at}")
    #     # print(f"Description : {video.description}")
    #     print(f"Transcript  : {video.transcript}")
        
    
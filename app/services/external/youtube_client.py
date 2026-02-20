"""YouTube API client for searching weather-related videos."""

import httpx
from typing import List, Optional, Dict
from app.config import settings
from app.schemas import YouTubeVideo
import logging

logger = logging.getLogger(__name__)


class YouTubeClient:
    """Client for YouTube Data API v3 integration."""

    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self):
        """Initialize YouTube client with API key."""
        self.api_key = settings.YOUTUBE_API_KEY
        self.client = httpx.AsyncClient()

    async def search_videos(
        self,
        query: str,
        max_results: int = 5
    ) -> List[YouTubeVideo]:
        """Search for videos on YouTube.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of YouTubeVideo objects
        """
        try:
            params = {
                "q": query,
                "part": "snippet",
                "type": "video",
                "key": self.api_key,
                "maxResults": max_results,
                "order": "relevance"
            }
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_results(data.get("items", []))
        except Exception as e:
            logger.error(f"YouTube search error: {str(e)}")
            return []

    def _parse_results(self, items: List[Dict]) -> List[YouTubeVideo]:
        """Parse YouTube API response into YouTubeVideo objects.
        
        Args:
            items: List of search results from YouTube API
            
        Returns:
            List of YouTubeVideo objects
        """
        videos = []
        for item in items:
            try:
                video = YouTubeVideo(
                    video_id=item["id"]["videoId"],
                    title=item["snippet"]["title"],
                    description=item["snippet"]["description"],
                    thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"]
                )
                videos.append(video)
            except (KeyError, IndexError) as e:
                logger.warning(f"Error parsing video item: {str(e)}")
                continue
        return videos

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

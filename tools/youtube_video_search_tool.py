from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
from datetime import datetime, timezone
import os
import requests
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

#Basically we are creating a tool that will search for youtube videos based on a keyword and return a list of video search results
#What we expect to get from the tool is a list of video search results
class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int

#Creating the input schema for the tool
class YouTubeVideoSearchToolInput(BaseModel):
    """Input for YouTubeVideoSearchTool"""
    keyword: str = Field(...,description="The keyword to search for YouTube videos")
    max_results: int = Field(10, description="The maximum number of search results to return")

class YoutubeVideoSearchTool(BaseTool):
    name: str = "Youtube Video Search Tool"
    description: str = "Searches YouTube videos based on a keyword and returns a list of video search results"
    args_schema: Type[BaseModel] = YouTubeVideoSearchToolInput #Basically it tells the tool what kind of input to expect
    #Whenever we are creating a tool we have to define a _run file that will be executed when the tool is run

    def _run(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        api_key = YOUTUBE_API_KEY
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "maxResults": max_results,
            "type": "video",
            "key": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        results = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel_id = item["snippet"]["channelId"]
            channel_title = item["snippet"]["channelTitle"]
            publish_date = datetime.fromisoformat(
                item["snippet"]["publishedAt"].replace('Z', '+00:00')).astimezone(timezone.utc)
            days_since_published = (datetime.now(
                timezone.utc) - publish_date).days
            
            results.append(VideoSearchResult(
                video_id=video_id,
                title=title,
                channel_id=channel_id,
                channel_title=channel_title,
                days_since_published=days_since_published
            ))

        return results
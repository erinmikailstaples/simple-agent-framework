import aiohttp
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from agent_framework.tools.base import BaseTool
from agent_framework.models import ToolMetadata
from .schemas import YoutubeWeatherVibesInput, YoutubeWeatherVibesOutput
from pydantic import BaseModel

class YoutubeWeatherVibesTool(BaseTool):
    """Tool for finding YouTube videos that match weather vibes"""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        """Get tool metadata"""
        return ToolMetadata(
            name="youtube_weather_vibes",
            description="Finds YouTube videos that match the vibe of the current weather",
            tags=["weather", "youtube", "vibes", "entertainment"],
            input_schema=YoutubeWeatherVibesInput.model_json_schema(),
            output_schema=YoutubeWeatherVibesOutput.model_json_schema(),
        )

    async def execute(self, weather_condition: str = None, temperature: float = None, weather_data: Optional[Dict[str, Any]] = None, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Find YouTube videos that match the weather vibe
        
        Args:
            weather_condition: The current weather condition (e.g., "Cloudy", "Rainy")
            temperature: The current temperature in degrees Celsius
            weather_data: Output from the weather_retriever tool containing weather_condition and temperature
            input_data: Optional dictionary containing weather_condition and temperature
            
        Returns:
            Dictionary containing weather information and matching YouTube videos
        """
        load_dotenv()
        
        # First priority: check if individual parameters were provided
        if weather_condition is None or temperature is None:
            # Second priority: extract from weather_data parameter
            if weather_data:
                weather_condition = weather_data.get('weather_condition', weather_condition)
                temperature = weather_data.get('temperature', temperature)
            
            # Third priority: check if input_data has the required fields
            if input_data and (weather_condition is None or temperature is None):
                weather_condition = input_data.get('weather_condition', weather_condition)
                temperature = input_data.get('temperature', temperature)
        
        # Validate that we have the required data
        if weather_condition is None or temperature is None:
            missing = []
            if weather_condition is None:
                missing.append("weather_condition")
            if temperature is None:
                missing.append("temperature")
            raise ValueError(f"Missing required weather data: {', '.join(missing)}")
            
        # Check API key
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            self.logger.warning("YOUTUBE_API_KEY environment variable is not set - using mock data")
            print("WARNING: YOUTUBE_API_KEY is missing. Using mock YouTube video data.")
            # Generate mock video data
            search_query = self._generate_search_query(weather_condition, temperature)
            
            # Create mock videos with appropriate themes based on the weather
            mock_videos = [
                {
                    "title": f"[MOCK DATA] Relaxing {weather_condition} Day Music Mix | {temperature}°C Vibes",
                    "channel_title": "Weather Vibes Music",
                    "description": f"[MOCK DATA - YOUTUBE_API_KEY missing] The perfect playlist for a {weather_condition} day with temperatures around {temperature}°C. Enjoy these carefully selected tracks to match your weather mood.",
                    "thumbnail_url": "https://i.ytimg.com/vi/mock_id_1/hqdefault.jpg",
                    "video_id": "mock_id_1",
                    "video_url": "https://www.youtube.com/watch?v=mock_id_1"
                },
                {
                    "title": f"[MOCK DATA] Study/Work Music for {weather_condition} Weather | Ambient Focus Playlist",
                    "channel_title": "Focus Flow",
                    "description": f"[MOCK DATA - YOUTUBE_API_KEY missing] Boost your productivity during {weather_condition} weather with this ambient music mix designed for focus and concentration.",
                    "thumbnail_url": "https://i.ytimg.com/vi/mock_id_2/hqdefault.jpg",
                    "video_id": "mock_id_2",
                    "video_url": "https://www.youtube.com/watch?v=mock_id_2"
                },
                {
                    "title": f"[MOCK DATA] {temperature}°C Weather Beats | Lofi Hip Hop Mix",
                    "channel_title": "Chill Beats Studio",
                    "description": "[MOCK DATA - YOUTUBE_API_KEY missing] Lofi hip hop beats perfect for relaxing, studying, or working while enjoying the current weather conditions.",
                    "thumbnail_url": "https://i.ytimg.com/vi/mock_id_3/hqdefault.jpg",
                    "video_id": "mock_id_3",
                    "video_url": "https://www.youtube.com/watch?v=mock_id_3"
                },
                {
                    "title": f"[MOCK DATA] Epic {weather_condition} Soundtrack | Cinematic Music Collection",
                    "channel_title": "Epic Music World",
                    "description": f"[MOCK DATA - YOUTUBE_API_KEY missing] Experience the majesty of {weather_condition} weather with this epic cinematic soundtrack collection.",
                    "thumbnail_url": "https://i.ytimg.com/vi/mock_id_4/hqdefault.jpg",
                    "video_id": "mock_id_4",
                    "video_url": "https://www.youtube.com/watch?v=mock_id_4"
                },
                {
                    "title": f"[MOCK DATA] Acoustic Covers for {weather_condition} Days | Relaxing Playlist",
                    "channel_title": "Acoustic Treasures",
                    "description": "[MOCK DATA - YOUTUBE_API_KEY missing] Beautiful acoustic covers of popular songs that perfectly match the mood of today's weather.",
                    "thumbnail_url": "https://i.ytimg.com/vi/mock_id_5/hqdefault.jpg",
                    "video_id": "mock_id_5",
                    "video_url": "https://www.youtube.com/watch?v=mock_id_5"
                }
            ]
            
            return {
                "weather_condition": weather_condition,
                "temperature": temperature,
                "search_query": search_query,
                "videos": mock_videos,
                "mock_data": True,
                "missing_api_key": "YOUTUBE_API_KEY"
            }

        # Determine search query based on weather condition and temperature
        search_query = self._generate_search_query(weather_condition, temperature)
        
        # API endpoint
        url = "https://www.googleapis.com/youtube/v3/search"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params={
                    "key": api_key,
                    "part": "snippet",
                    "q": search_query,
                    "type": "video",
                    "maxResults": 5,
                    "videoEmbeddable": "true"
                }
            ) as response:
                if response.status != 200:
                    raise Exception(f"YouTube API error: {await response.text()}")
                    
                data = await response.json()
                
                videos = []
                for item in data.get("items", []):
                    video_id = item.get("id", {}).get("videoId")
                    if video_id:
                        videos.append({
                            "title": item.get("snippet", {}).get("title", ""),
                            "channel_title": item.get("snippet", {}).get("channelTitle", ""),
                            "description": item.get("snippet", {}).get("description", ""),
                            "thumbnail_url": item.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url", ""),
                            "video_id": video_id,
                            "video_url": f"https://www.youtube.com/watch?v={video_id}"
                        })
                
                return {
                    "weather_condition": weather_condition,
                    "temperature": temperature,
                    "search_query": search_query,
                    "videos": videos,
                    "mock_data": False
                }
    
    def _generate_search_query(self, weather_condition: str, temperature: float) -> str:
        """Generate a search query based on weather condition and temperature"""
        # Base query components
        base_query = "music playlist"
        
        # Temperature-based modifiers
        temp_modifier = ""
        if temperature < 0:
            temp_modifier = "freezing cold winter"
        elif temperature < 10:
            temp_modifier = "cold winter"
        elif temperature < 15:
            temp_modifier = "cool spring"
        elif temperature < 22:
            temp_modifier = "mild pleasant"
        elif temperature < 28:
            temp_modifier = "warm summer"
        else:
            temp_modifier = "hot summer"
            
        # Weather condition modifiers
        condition_modifier = ""
        condition_lower = weather_condition.lower()
        
        if "rain" in condition_lower or "shower" in condition_lower or "drizzle" in condition_lower:
            condition_modifier = "rainy day relaxing"
        elif "snow" in condition_lower:
            condition_modifier = "snowy day cozy"
        elif "cloud" in condition_lower or "overcast" in condition_lower:
            condition_modifier = "cloudy day chill"
        elif "sun" in condition_lower or "clear" in condition_lower:
            condition_modifier = "sunny day upbeat"
        elif "fog" in condition_lower or "mist" in condition_lower:
            condition_modifier = "foggy atmospheric"
        elif "thunder" in condition_lower or "storm" in condition_lower:
            condition_modifier = "thunderstorm dramatic"
        elif "wind" in condition_lower:
            condition_modifier = "windy day ambient"
        else:
            # Default to the actual weather condition if no specific mapping
            condition_modifier = f"{weather_condition} vibes"
            
        # Combine all components into a search query
        search_query = f"{condition_modifier} {temp_modifier} {base_query}"
        return search_query 
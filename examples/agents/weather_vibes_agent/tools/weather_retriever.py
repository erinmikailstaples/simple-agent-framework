import aiohttp
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from agent_framework.tools.base import BaseTool
from agent_framework.models import ToolMetadata
from .schemas import WeatherRetrieverInput, WeatherRetrieverOutput, WeatherRetrieverMetadata

class WeatherRetrieverTool(BaseTool):
    """Tool for retrieving weather data"""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        """Get tool metadata"""
        return ToolMetadata(
            name="weather_retriever",
            description="Retrieves current weather data for a given location",
            tags=["weather", "location"],
            input_schema=WeatherRetrieverInput.model_json_schema(),
            output_schema=WeatherRetrieverOutput.model_json_schema(),
        )

    async def execute(self, location: str) -> Dict[str, Any]:
        """Get weather data for location"""
        load_dotenv()
        api_key = os.getenv("WEATHER_API_KEY") or os.getenv("WEATHERAPI_KEY")
        if not api_key:
            # Determine which API key is missing
            weather_api_key = os.getenv("WEATHER_API_KEY")
            weatherapi_key = os.getenv("WEATHERAPI_KEY")
            missing_keys = []
            if not weather_api_key:
                missing_keys.append("WEATHER_API_KEY")
            if not weatherapi_key:
                missing_keys.append("WEATHERAPI_KEY")
            
            missing_keys_str = " and ".join(missing_keys)
            self.logger.warning("Missing API key(s): %s. Using mock weather data for location: %s", missing_keys_str, location)
            
            return {
                "location": location,
                "temperature": 22.5,  # Pleasant temperature in Celsius
                "weather_condition": "[MOCK DATA] Partly cloudy",
                "precipitation_chance": 20.0,  # 20% chance of precipitation
                "mock_data": True,
                "missing_api_keys": missing_keys_str
            }

        # API endpoint
        url = "http://api.weatherapi.com/v1/current.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params={
                    "key": api_key,
                    "q": location,
                    "aqi": "no"
                }
            ) as response:
                if response.status != 200:
                    raise Exception(f"Weather API error: {await response.text()}")
                    
                data = await response.json()
                
                return {
                    "location": data["location"]["name"],
                    "temperature": data["current"]["temp_c"],
                    "weather_condition": data["current"]["condition"]["text"],
                    "precipitation_chance": data["current"].get("precip_mm", 0) * 100,  # Convert to percentage
                    "mock_data": False
                } 

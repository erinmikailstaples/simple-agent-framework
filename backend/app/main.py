from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Add the project root to the path so we can import from examples
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import the WeatherVibesAgent
try:
    from examples.agents.weather_vibes_agent.agent import WeatherVibesAgent
except ImportError:
    raise ImportError("Could not import WeatherVibesAgent. Make sure the examples directory is in your PYTHONPATH.")

app = FastAPI(title="Weather Vibes API", description="API for getting weather information and recommended videos")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the WeatherVibesAgent
weather_vibes_agent = WeatherVibesAgent()

class LocationRequest(BaseModel):
    location: str

class WeatherResponse(BaseModel):
    location: str
    temperature: Optional[float] = None
    conditions: Optional[str] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    additional_info: Optional[Dict[str, Any]] = None

class VideoResponse(BaseModel):
    location: str
    weather_summary: str
    video_title: Optional[str] = None
    video_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Weather Vibes API. Use /weather/{location} to get weather info and /recommend-video/{location} to get video recommendations."}

@app.get("/weather/{location}", response_model=WeatherResponse)
async def get_weather(location: str):
    """
    Get weather information for a specific location.
    """
    try:
        # Use the WeatherVibesAgent to get weather information
        weather_info = weather_vibes_agent.get_weather_information(location)
        
        # Construct a structured response
        response = WeatherResponse(
            location=location,
            additional_info={}
        )
        
        # Parse the weather_info and populate the response
        # This will depend on the exact structure returned by the agent
        if isinstance(weather_info, dict):
            response.temperature = weather_info.get("temperature")
            response.conditions = weather_info.get("conditions")
            response.humidity = weather_info.get("humidity")
            response.wind_speed = weather_info.get("wind_speed")
            # Store any additional fields
            for key, value in weather_info.items():
                if key not in ["temperature", "conditions", "humidity", "wind_speed"]:
                    response.additional_info[key] = value
        else:
            # If it's not a dictionary, just store the raw data
            response.additional_info = {"raw_data": weather_info}
            
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting weather information: {str(e)}")

@app.get("/recommend-video/{location}", response_model=VideoResponse)
async def recommend_video(location: str):
    """
    Get a recommended YouTube video based on the weather in the specified location.
    """
    try:
        # First get the weather information
        weather_info = weather_vibes_agent.get_weather_information(location)
        
        # Now get a video recommendation based on the weather
        video_recommendation = weather_vibes_agent.recommend_video_for_weather(location)
        
        # Construct a structured response
        response = VideoResponse(
            location=location,
            weather_summary="",  # This will be populated based on weather_info
            additional_info={}
        )
        
        # Extract weather summary
        if isinstance(weather_info, dict):
            conditions = weather_info.get("conditions", "")
            temp = weather_info.get("temperature", "")
            response.weather_summary = f"{conditions}, {temp}°C" if temp else conditions
        else:
            response.weather_summary = str(weather_info)
        
        # Parse the video recommendation
        if isinstance(video_recommendation, dict):
            response.video_title = video_recommendation.get("title")
            response.video_url = video_recommendation.get("url")
            # Store any additional fields
            for key, value in video_recommendation.items():
                if key not in ["title", "url"]:
                    response.additional_info[key] = value
        else:
            # If it's not a dictionary, just store the raw data
            response.additional_info = {"raw_data": video_recommendation}
            
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting video recommendation: {str(e)}")

@app.post("/weather", response_model=WeatherResponse)
async def post_weather(request: LocationRequest):
    """
    Get weather information for a location using POST method.
    """
    return await get_weather(request.location)

@app.post("/recommend-video", response_model=VideoResponse)
async def post_recommend_video(request: LocationRequest):
    """
    Get a recommended YouTube video based on weather using POST method.
    """
    return await recommend_video(request.location)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)


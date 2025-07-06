import requests
import json
from typing import Dict, Any, Optional
import config
from models.schema import Tool

async def get_geo_location(city: str) -> Dict[str, Any]:
    """
    Get geolocation data for a city using OpenWeatherMap's Geocoding API
    
    Args:
        city: City name
        
    Returns:
        Dictionary containing geolocation information
    """
    try:
        # Using OpenWeatherMap Geocoding API
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config.WEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we have results
        if not data:
            return {"error": "Location not found"}
        
        # Extract relevant information from the first result
        location = data[0]
        
        # Format the response according to requested format
        geo_info = {
            "name": location.get("name"),
            "lat": location.get("lat"),
            "lon": location.get("lon"),
            "country": location.get("country"),
            "zip": location.get("zip")
        }
        
        return geo_info
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching geolocation data: {str(e)}"}

async def get_weather(city: str, country: str = None) -> Dict[str, Any]:
    """
    Get current weather for a given city
    
    Args:
        city: City name
        country: Country code (optional)
        
    Returns:
        Dictionary containing weather information
    """
    location = city if not country else f"{city},{country}"
    
    try:
        geo_location = await get_geo_location(location)
        lat = geo_location.get("lat")
        lon = geo_location.get("lon")
        
        # Using OpenWeatherMap API (replace with your preferred weather API)
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={config.WEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        weather_info = {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temperature": f"{data['main']['temp']}°C",
            "feels_like": f"{data['main']['feels_like']}°C",
            "description": data['weather'][0]['description'],
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s",
            "timestamp": data['dt']
        }
        
        return weather_info
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching weather data: {str(e)}"}
    except (KeyError, IndexError) as e:
        return {"error": f"Error parsing weather data: {str(e)}"}

def register_weather_tool(mcp_server):
    """Register the weather tool with the MCP server"""
    weather_tool = Tool(
        name="get_weather",
        description="Get current weather information for a city",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g., 'New York'"
                },
                "country": {
                    "type": "string",
                    "description": "Country code (optional), e.g., 'US'"
                }
            },
            "required": ["city"]
        },
        function=get_weather
    )
    
    geo_location_tool = Tool(
        name="get_geo_location",
        description="Get geolocation data for a city",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g., 'New York'"
                }
            },
            "required": ["city"]
        },
        function=get_geo_location
    )
    
    mcp_server.register_tool(weather_tool)

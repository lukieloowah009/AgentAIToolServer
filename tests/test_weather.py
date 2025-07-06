import unittest
from unittest.mock import patch, MagicMock
import json
import asyncio
from tools.weather import get_weather, get_geo_location

class TestWeatherTool(unittest.TestCase):
    """Test cases for weather tools"""
    
    @patch('tools.weather.requests.get')
    async def test_get_geo_location_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "name": "London",
            "lat": 51.5074,
            "lon": -0.1278,
            "country": "GB"
        }]
        mock_get.return_value = mock_response
        
        # Call the function
        result = await get_geo_location("London")
        
        # Assertions
        self.assertEqual(result["name"], "London")
        self.assertEqual(result["lat"], 51.5074)
        self.assertEqual(result["lon"], -0.1278)
        self.assertEqual(result["country"], "GB")
        
    @patch('tools.weather.requests.get')
    async def test_get_geo_location_no_results(self, mock_get):
        # Mock an empty response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Call the function
        result = await get_geo_location("NonExistentCity")
        
        # Assertions
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Location not found")
    
    @patch('tools.weather.requests.get')
    async def test_get_geo_location_api_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        # Call the function
        result = await get_geo_location("London")
        
        # Assertions
        self.assertIn("error", result)
        self.assertTrue(result["error"].startswith("Error fetching geolocation data"))

    @patch('tools.weather.get_geo_location')
    @patch('tools.weather.requests.get')
    async def test_get_weather_success(self, mock_weather_get, mock_geo):
        # Mock the geo location response
        mock_geo.return_value = {
            "name": "London",
            "lat": 51.5074,
            "lon": -0.1278,
            "country": "GB"
        }
        
        # Mock the weather API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {
                "temp": 15.5,
                "feels_like": 14.8,
                "humidity": 76
            },
            "weather": [{"description": "cloudy"}],
            "wind": {"speed": 5.2},
            "dt": 1625050000
        }
        mock_weather_get.return_value = mock_response
        
        # Call the function
        result = await get_weather("London")
        
        # Assertions
        self.assertEqual(result["location"], "London, GB")
        self.assertEqual(result["temperature"], "15.5°C")
        self.assertEqual(result["description"], "cloudy")

    @patch('tools.weather.get_geo_location')
    async def test_get_weather_geo_error(self, mock_geo):
        # Mock geo location error
        mock_geo.return_value = {"error": "Location not found"}
        
        # Call the function with error from geo location
        result = await get_weather("NonExistentCity")
        
        # Should have error from geo location
        self.assertIn("error", result)

# Allow running the tests directly
if __name__ == "__main__":
    unittest.main()

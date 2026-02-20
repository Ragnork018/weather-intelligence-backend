"""Weather service for fetching and processing weather data."""

import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.schemas import WeatherResponse, WeatherData, ExternalAPIError
from app.config import settings
from app.database import get_db
from app.models import WeatherRecord
from app.crud import weather_crud
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """Service class for weather operations and external API integrations."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        """Initialize the weather service with API key."""
        self.api_key = settings.OPENWEATHER_API_KEY
        self.client = httpx.AsyncClient()

    async def get_weather_by_coordinates(
        self, lat: float, lon: float
    ) -> WeatherResponse:
        """Fetch weather data by latitude and longitude.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            WeatherResponse with current weather data
            
        Raises:
            ExternalAPIError: If API call fails
        """
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_weather_response(data)
        except Exception as e:
            logger.error(f"Error fetching weather: {str(e)}")
            raise ExternalAPIError(f"Failed to fetch weather data: {str(e)}")

    async def get_weather_by_zip_code(self, zip_code: str) -> WeatherResponse:
        """Fetch weather data by zip code.
        
        Args:
            zip_code: Zip code string
            
        Returns:
            WeatherResponse with current weather data
        """
        try:
            params = {
                "zip": zip_code,
                "appid": self.api_key,
                "units": "metric"
            }
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_weather_response(data)
        except Exception as e:
            logger.error(f"Error fetching weather by zip: {str(e)}")
            raise ExternalAPIError(f"Failed to fetch weather data: {str(e)}")

    def _parse_weather_response(self, data: Dict) -> WeatherResponse:
        """Parse OpenWeatherMap API response into WeatherResponse.
        
        Args:
            data: Raw API response
            
        Returns:
            Parsed WeatherResponse object
        """
        weather_data = WeatherData(
            location=data.get("name", ""),
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"],
            timestamp=datetime.utcnow()
        )
        return WeatherResponse(
            status="success",
            data=weather_data,
            timestamp=datetime.utcnow()
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

"""Pydantic request and response schemas.

Defines validation schemas for API requests and responses,
ensuring data integrity and type safety.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Any
from datetime import date


class WeatherRequestCreate(BaseModel):
    """Schema for creating a new weather request."""
    location: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Location name, city, ZIP code, or coordinates"
    )
    start_date: date = Field(..., description="Query start date (YYYY-MM-DD)")
    end_date: date = Field(..., description="Query end date (YYYY-MM-DD)")

    @validator("end_date")
    def validate_date_range(cls, v, values):
        """Ensure end_date is not before start_date."""
        start = values.get("start_date")
        if start and v < start:
            raise ValueError("end_date must be on or after start_date")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "location": "San Francisco",
                "start_date": "2025-02-20",
                "end_date": "2025-02-25"
            }
        }


class WeatherRequestUpdate(BaseModel):
    """Schema for updating an existing weather request."""
    start_date: Optional[date] = Field(None, description="New start date")
    end_date: Optional[date] = Field(None, description="New end date")

    @validator("end_date")
    def validate_update_date_range(cls, v, values):
        """Ensure end_date is not before start_date on update."""
        start = values.get("start_date")
        if start and v and v < start:
            raise ValueError("end_date must be on or after start_date")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2025-02-20",
                "end_date": "2025-02-25"
            }
        }


class WeatherRequestBase(BaseModel):
    """Schema for weather request responses (all fields populated)."""
    id: int = Field(..., description="Unique request identifier")
    raw_location: str = Field(..., description="Original location input")
    resolved_location: str = Field(..., description="Validated location")
    latitude: Optional[float] = Field(None, description="Geographic latitude")
    longitude: Optional[float] = Field(None, description="Geographic longitude")
    start_date: str = Field(..., description="Query start date")
    end_date: str = Field(..., description="Query end date")
    weather_payload: Any = Field(..., description="OpenWeatherMap API response")
    extra_payload: Optional[Any] = Field(None, description="Extra API data")
    source: str = Field(..., description="Data source identifier")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "raw_location": "San Francisco",
                "resolved_location": "San Francisco, US",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "start_date": "2025-02-20",
                "end_date": "2025-02-25",
                "weather_payload": {},
                "extra_payload": {"youtube_videos": []},
                "source": "openweathermap",
                "created_at": "2025-02-20T10:30:00",
                "updated_at": "2025-02-20T10:30:00"
            }
        }

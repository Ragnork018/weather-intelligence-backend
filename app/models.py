"""Database ORM models for Weather Intelligence API.

This module defines the SQLAlchemy models for storing weather requests
and related data in the database.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func
from .database import Base


class WeatherRequest(Base):
    """ORM model for weather request data.
    
    Stores user queries, API responses, and metadata about weather requests.
    """
    __tablename__ = "weather_requests"

    # Primary identifier
    id = Column(Integer, primary_key=True, index=True)
    
    # User input and location resolution
    raw_location = Column(String, index=True, nullable=False, comment="Raw location input from user")
    resolved_location = Column(String, index=True, nullable=False, comment="Validated location (city, country)")
    latitude = Column(Float, nullable=True, comment="Geographic latitude")
    longitude = Column(Float, nullable=True, comment="Geographic longitude")
    
    # Date range for weather query
    start_date = Column(String, nullable=False, comment="Query start date (ISO format)")
    end_date = Column(String, nullable=False, comment="Query end date (ISO format)")
    
    # API response data
    weather_payload = Column(JSON, nullable=False, comment="Full OpenWeatherMap API response")
    extra_payload = Column(JSON, nullable=True, comment="Extra data (YouTube videos, maps, etc)")
    
    # Metadata
    source = Column(String, default="openweathermap", comment="Weather data source")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="Record update timestamp")
    
    def __repr__(self) -> str:
        return f"<WeatherRequest(id={self.id}, location={self.resolved_location}, dates={self.start_date}..{self.end_date})>"

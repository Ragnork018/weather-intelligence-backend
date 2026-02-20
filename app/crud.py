"""CRUD (Create, Read, Update, Delete) operations for weather requests.

Database interaction layer using SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional


def create_weather_request(
    db: Session,
    raw_location: str,
    resolved_location: str,
    latitude: Optional[float],
    longitude: Optional[float],
    payload: dict,
    extra_payload: Optional[dict],
    start_date: str,
    end_date: str,
) -> models.WeatherRequest:
    """Create a new weather request record in the database."""
    obj = models.WeatherRequest(
        raw_location=raw_location,
        resolved_location=resolved_location,
        latitude=latitude,
        longitude=longitude,
        weather_payload=payload,
        extra_payload=extra_payload,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_weather_requests(
    db: Session, skip: int = 0, limit: int = 50
) -> List[models.WeatherRequest]:
    """Retrieve all weather requests with pagination."""
    return db.query(models.WeatherRequest).offset(skip).limit(limit).all()


def get_weather_request(
    db: Session, request_id: int
) -> Optional[models.WeatherRequest]:
    """Retrieve a single weather request by ID."""
    return db.query(models.WeatherRequest).filter(
        models.WeatherRequest.id == request_id
    ).first()


def update_weather_request(
    db: Session, request_id: int, update: schemas.WeatherRequestUpdate
) -> Optional[models.WeatherRequest]:
    """Update an existing weather request."""
    obj = get_weather_request(db, request_id)
    if not obj:
        return None
    data = update.dict(exclude_unset=True)
    for field, value in data.items():
        if field == "start_date" and value:
            obj.start_date = value.isoformat()
        elif field == "end_date" and value:
            obj.end_date = value.isoformat()
    db.commit()
    db.refresh(obj)
    return obj


def delete_weather_request(db: Session, request_id: int) -> bool:
    """Delete a weather request by ID."""
    obj = get_weather_request(db, request_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

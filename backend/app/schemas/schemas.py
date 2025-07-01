from datetime import date
from typing import Optional

from pydantic import BaseModel


class CircuitBase(BaseModel):
    circuit_id: int
    circuit_ref: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: Optional[int] = None  # Optional for nullable fields
    url: str

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models


class DriverBase(BaseModel):
    driver_id: int
    driver_ref: str
    number: Optional[int] = None  # Optional for nullable fields
    code: Optional[str] = None  # Optional for nullable fields
    forename: str
    surname: str
    dob: date
    nationality: str
    url: str

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models


class CircuitSummary(CircuitBase):
    fastest_lap_ms: Optional[int] = None  # Optional for nullable fields
    total_races: int


class DriverSummary(DriverBase):
    podiums: int
    total_races: int

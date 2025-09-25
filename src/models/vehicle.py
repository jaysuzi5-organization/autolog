"""
Autolog Vehicle Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Vehicle data.
- The Pydantic schema for validating API requests when creating a Vehicle.

Other models (insurance, registration, maintenance, gas, etc.)
will be defined separately and related back to this Vehicle.
"""

from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional, List
from .base import Base
from .gas import GasRead


class Vehicle(Base):
    """
    SQLAlchemy ORM model representing a Vehicle in the AutoLog system.
    """

    __tablename__ = "autolog_vehicle"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    color = Column(String(30), nullable=True)
    vin_number = Column(String(50), nullable=True, unique=True)
    license_plate_number = Column(String(20), nullable=True)
    registration_number = Column(String(50), nullable=True)
    state = Column(String(20), nullable=True)

    purchased_date = Column(Date, nullable=True)
    purchased_price = Column(Float, nullable=True)
    purchased_odometer = Column(Integer, nullable=True)

    dealer_name = Column(String(100), nullable=True)

    sold_date = Column(Date, nullable=True)
    sold_price = Column(Float, nullable=True)
    sold_odometer = Column(Integer, nullable=True)

    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    def __repr__(self):
        return f"<Vehicle(id={self.id}, year={self.year}, make='{self.make}', model='{self.model}')>"


# ---------- Pydantic Schemas ----------

class VehicleCreate(BaseModel):
    year: int
    make: str
    model: str
    color: Optional[str] = None
    vin_number: Optional[str] = None
    license_plate_number: Optional[str] = None
    registration_number: Optional[str] = None
    state: Optional[str] = None
    purchased_date: Optional[datetime] = None
    purchased_price: Optional[float] = None
    purchased_odometer: Optional[int] = None
    dealer_name: Optional[str] = None
    sold_date: Optional[datetime] = None
    sold_price: Optional[float] = None
    sold_odometer: Optional[int] = None

    class Config:
        orm_mode = True


class VehicleRead(BaseModel):
    id: int
    year: int
    make: str
    model: str
    color: Optional[str]
    vin_number: Optional[str]
    license_plate_number: Optional[str]
    registration_number: Optional[str]
    state: Optional[str]
    purchased_date: Optional[datetime]
    purchased_price: Optional[float]
    purchased_odometer: Optional[int]
    dealer_name: Optional[str]
    sold_date: Optional[datetime]
    sold_price: Optional[float]
    sold_odometer: Optional[int]

    # 🔹 Related entries (optional)
    gas: List[GasRead] = []  # only returned when explicitly included

    class Config:
        orm_mode = True

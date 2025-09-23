"""
Autolog Vehicle Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Vehicle data.
- The Pydantic schema for validating API requests when creating a Vehicle.

Other models (insurance, registration, maintenance, gas, etc.)
will be defined separately and related back to this Vehicle.
"""

from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from framework.db import Base
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional, List


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

# Lightweight references to related models
class InsuranceEntry(BaseModel):
    date: datetime
    cost: float
    notes: Optional[str] = None


class RegistrationEntry(BaseModel):
    date: datetime
    cost: float
    notes: Optional[str] = None


class MaintenanceEntry(BaseModel):
    date: datetime
    odometer: int
    cost: float
    notes: Optional[str] = None


class GasEntry(BaseModel):
    date: datetime
    odometer: int
    gallons: Optional[float] = None
    cost: Optional[float] = None
    mpg: Optional[float] = None
    milesDriven: Optional[int] = None
    costPerGallon: Optional[float] = None


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

    # Lists of related entries
    insurance: List[InsuranceEntry] = []
    registration: List[RegistrationEntry] = []
    maintenance: List[MaintenanceEntry] = []
    gas: List[GasEntry] = []

    class Config:
        orm_mode = True

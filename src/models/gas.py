"""
Autolog Gas Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Gas/EV charging data.
- The Pydantic schema for validating API requests when creating Gas entries.

Each Gas entry belongs to a Vehicle (FK to autolog_vehicle).
"""

from sqlalchemy import Column, Date, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional
from .base import Base


class Gas(Base):
    """
    SQLAlchemy ORM model representing a Gas/EV charging record in AutoLog.
    """

    __tablename__ = "autolog_gas"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("autolog_vehicle.id"), nullable=False)

    # Core fields
    date = Column(Date, nullable=False)
    odometer = Column(Integer, nullable=False)

    # Fuel-related fields (perhaps null for EVs)
    gallons = Column(Float, nullable=True)
    cost = Column(Float, nullable=True)
    mpg = Column(Float, nullable=True)
    miles_driven = Column(Integer, nullable=True)
    cost_per_gallon = Column(Float, nullable=True)

    # EV-related fields (perhaps null for gas vehicles)
    kwh_per_mile = Column(Float, nullable=True)
    miles_per_kwh = Column(Float, nullable=True)
    cost_per_kwh = Column(Float, nullable=True)

    # Metadata
    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    # Relationship back to Vehicle
    vehicle = relationship("Vehicle", backref="gas_entries")

    def __repr__(self):
        return (
            f"<Gas(id={self.id}, vehicle_id={self.vehicle_id}, date={self.date}, "
            f"odometer={self.odometer}, gallons={self.gallons}, cost={self.cost}, "
            f"kWhPerMile={self.kwh_per_mile}, milesPerKWh={self.miles_per_kwh})>"
        )


# ---------- Pydantic Schemas ----------

class GasBase(BaseModel):
    date: datetime
    odometer: int
    gallons: Optional[float] = None
    cost: Optional[float] = None
    mpg: Optional[float] = None
    miles_driven: Optional[int] = None
    cost_per_gallon: Optional[float] = None
    kwh_per_mile: Optional[float] = None
    miles_per_kwh: Optional[float] = None
    cost_per_kwh: Optional[float] = None


class GasCreate(GasBase):
    """Schema for creating a gas entry"""
    pass


class GasUpdate(GasBase):
    """Schema for updating a gas entry (partial or full)"""
    pass


class GasRead(GasBase):
    id: int
    vehicle_id: int

    class Config:
        orm_mode = True

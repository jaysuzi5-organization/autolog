"""
Autolog Insure Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Insurance data.
- The Pydantic schema for validating API requests when creating Insurance entries.

Each Insurance entry belongs to a Vehicle (FK to autolog_vehicle).
"""

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from pydantic import BaseModel
from .base import Base


class Insurance(Base):
    """
    SQLAlchemy ORM model representing a Insurance record in AutoLog.
    """

    __tablename__ = "autolog_insurance"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("autolog_vehicle.id"), nullable=False)

    # Core fields
    date = Column(Date, nullable=False)
    cost = Column(Float, nullable=False)
    notes = Column(String(500), nullable=True)

    # Metadata
    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    # Relationship back to Vehicle
    vehicle = relationship("Vehicle", backref="insurance_entries")

    def __repr__(self):
        return (
            f"<Insurance(id={self.id}, vehicle_id={self.vehicle_id}, date={self.date}, "
            f"cost={self.cost}, "
            f"notes={self.notes})>"
        )


# ---------- Pydantic Schemas ----------

class InsuranceBase(BaseModel):
    date: datetime
    cost: float
    notes: str = ""

class InsuranceCreate(InsuranceBase):
    """Schema for creating a insurance entry"""
    pass


class InsuranceUpdate(InsuranceBase):
    """Schema for updating a insurance entry (partial or full)"""
    pass


class InsuranceRead(InsuranceBase):
    id: int
    vehicle_id: int

    class Config:
        orm_mode = True

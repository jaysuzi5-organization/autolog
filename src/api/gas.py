from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from ..app import get_db
from models.gas import Gas, GasCreate
from models.vehicle import Vehicle
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """Convert SQLAlchemy ORM model instance into a dict."""
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


# ---------- Endpoints ----------

@router.get("/api/v1/autolog/vehicle/{vehicle_id}/gas")
def list_gas(
    vehicle_id: int,
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of Gas records for a vehicle.
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")

        offset = (page - 1) * limit
        records = (
            db.query(Gas)
            .filter(Gas.vehicle_id == vehicle_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [serialize_sqlalchemy_obj(item) for item in records]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/autolog/vehicle/{vehicle_id}/gas/{gas_id}")
def get_gas_by_id(vehicle_id: int, gas_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Gas record by ID for a vehicle.
    """
    try:
        record = (
            db.query(Gas)
            .filter(Gas.vehicle_id == vehicle_id, Gas.id == gas_id)
            .first()
        )
        if not record:
            raise HTTPException(status_code=404, detail=f"Gas {gas_id} not found for vehicle {vehicle_id}")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/autolog/vehicle/{vehicle_id}/gas")
def create_gas(
    vehicle_id: int,
    gas_data: GasCreate = Body(..., description="Data for the new gas record"),
    db: Session = Depends(get_db)
):
    """
    Create a new Gas record for a vehicle.
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")

        data = gas_data.model_dump(exclude_unset=True)
        new_record = Gas(vehicle_id=vehicle_id, **data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/autolog/vehicle/{vehicle_id}/gas/{gas_id}")
def update_gas_full(
    vehicle_id: int,
    gas_id: int,
    gas_data: GasCreate = Body(..., description="Updated data for the gas record"),
    db: Session = Depends(get_db)
):
    """
    Fully update a Gas record (all fields required).
    """
    try:
        record = (
            db.query(Gas)
            .filter(Gas.vehicle_id == vehicle_id, Gas.id == gas_id)
            .first()
        )
        if not record:
            raise HTTPException(status_code=404, detail=f"Gas {gas_id} not found for vehicle {vehicle_id}")

        data = gas_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/autolog/vehicle/{vehicle_id}/gas/{gas_id}")
def update_gas_partial(
    vehicle_id: int,
    gas_id: int,
    gas_data: GasCreate = Body(..., description="Partial updated data for the gas record"),
    db: Session = Depends(get_db)
):
    """
    Partially update a Gas record (only provided fields updated).
    """
    try:
        record = (
            db.query(Gas)
            .filter(Gas.vehicle_id == vehicle_id, Gas.id == gas_id)
            .first()
        )
        if not record:
            raise HTTPException(status_code=404, detail=f"Gas {gas_id} not found for vehicle {vehicle_id}")

        data = gas_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/autolog/vehicle/{vehicle_id}/gas/{gas_id}")
def delete_gas(vehicle_id: int, gas_id: int, db: Session = Depends(get_db)):
    """
    Delete a Gas record by ID for a vehicle.
    """
    try:
        record = (
            db.query(Gas)
            .filter(Gas.vehicle_id == vehicle_id, Gas.id == gas_id)
            .first()
        )
        if not record:
            raise HTTPException(status_code=404, detail=f"Gas {gas_id} not found for vehicle {vehicle_id}")

        db.delete(record)
        db.commit()
        return {"detail": f"Gas {gas_id} for vehicle {vehicle_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

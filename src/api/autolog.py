from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from framework.db import get_db
from models.autolog import Autolog, AutologCreate
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/autolog")
def list_autolog(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of Autolog records.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized Autolog records.
    """
    try:
        offset = (page - 1) * limit
        autolog_records = db.query(Autolog).offset(offset).limit(limit).all()
        return [serialize_sqlalchemy_obj(item) for item in autolog_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/autolog")
def create_record(
    autolog_data: AutologCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new Autolog record.

    Args:
        autolog_data (AutologCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created Autolog record.
    """
    try:
        data = autolog_data.model_dump(exclude_unset=True)
        new_record = Autolog(**data)
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


@router.get("/api/v1/autolog/{id}")
def get_autolog_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Autolog record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching Autolog record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Autolog).filter(Autolog.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Autolog with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/autolog/{id}")
def update_autolog_full(
    id: int,
    autolog_data: AutologCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing Autolog record (all fields required).

    Args:
        id (int): The ID of the record to update.
        autolog_data (AutologCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Autolog record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Autolog).filter(Autolog.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Autolog with id {id} not found")

        data = autolog_data.model_dump(exclude_unset=False)
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


@router.patch("/api/v1/autolog/{id}")
def update_autolog_partial(
    id: int,
    autolog_data: AutologCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing Autolog record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        Autolog_data (AutologCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Autolog record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Autolog).filter(Autolog.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Autolog with id {id} not found")

        data = autolog_data.model_dump(exclude_unset=True)
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


@router.delete("/api/v1/autolog/{id}")
def delete_autolog(id: int, db: Session = Depends(get_db)):
    """
    Delete a Autolog record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Autolog).filter(Autolog.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Autolog with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"Autolog with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

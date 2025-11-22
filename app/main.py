# app/main.py

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .db import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Test Asset Manager API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def read_health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}


# ----- Testbed endpoints ----- #

@app.post("/testbeds", response_model=schemas.TestbedRead, status_code=status.HTTP_201_CREATED)
def create_testbed(testbed: schemas.TestbedCreate, db: Session = Depends(get_db)):
    """
    Create a new Testbed.
    """
    existing = db.query(models.Testbed).filter(models.Testbed.name == testbed.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Testbed with this name already exists.",
        )

    db_testbed = models.Testbed(
        name=testbed.name,
        location=testbed.location,
        description=testbed.description,
    )
    db.add(db_testbed)
    db.commit()
    db.refresh(db_testbed)
    return db_testbed


@app.get("/testbeds", response_model=List[schemas.TestbedRead])
def list_testbeds(db: Session = Depends(get_db)):
    """
    List all Testbeds.
    """
    testbeds = db.query(models.Testbed).all()
    return testbeds

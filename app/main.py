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

# ----- SimulationConfig Endpoints ----- #

@app.post("/configs", response_model=schemas.SimulationConfigRead, status_code=status.HTTP_201_CREATED)
def create_simulation_config(config: schemas.SimulationConfigCreate, db: Session = Depends(get_db)):
    """
    Create a new SimulationConfig associated with a specific Testbed.
    """
    
    # Do not want to create a SimulationConfig that points to a non-existent testbed right now.
    # This might change later, if we want to track configs that have not been tested.
    parent_testbed = db.get(models.Testbed, config.testbed_id)
    if parent_testbed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Testbed with id {config.testbed_id} not found.",
        )

    # Could unpack it with db_config = models.SimulationConfig(**config.dict())
    # Right now doing this style for practice
    db_config = models.SimulationConfig(
        testbed_id=config.testbed_id,
        name=config.name,
        sim_version=config.sim_version,
        os=config.os,
        notes=config.notes,
        is_current_config=(
            config.is_current_config
            if config.is_current_config is not None
            else False
        ),
    )

    db.add(db_config)
    db.commit()
    db.refresh(db_config)

    return db_config


@app.get("/configs", response_model=List[schemas.SimulationConfigRead])
def list_simulation_configs( testbed_id: int | None = None, db: Session = Depends(get_db)):
    """
    List SimulationConfigs.

    If 'testbed_id' query parameter is provided, only return configs for that testbed.
    Otherwise, return all configs.
    """

    query = db.query(models.SimulationConfig)

    if testbed_id is not None:
        query = query.filter(models.SimulationConfig.testbed_id == testbed_id)

    configs = query.all()
    return configs

# ---- TestRun Endpoints ---- #
@app.post("/runs", response_model=schemas.TestRunRead, status_code=status.HTTP_201_CREATED)
def create_test_run(run: schemas.TestRunCreate, db: Session = Depends(get_db)):
    """
    Create a new TestRun for a specific SimulationConfig.
    """

    parent_config = db.get(models.SimulationConfig, run.simulation_config_id)
    if parent_config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SimulationConfig with id {run.simulation_config_id} not found.",
        )

    db_run = models.TestRun(
        simulation_config_id=run.simulation_config_id,
        operator=run.operator,
        result=run.result,
        notes=run.notes,
    )

    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    return db_run


@app.get("/runs", response_model=List[schemas.TestRunRead])
def list_test_runs(simulation_config_id: int | None = None, db: Session = Depends(get_db)):
    """
    List TestRuns.

    If 'simulation_config_id' is provided as a query parameter,
    only return runs for that configuration.
    Otherwise, return all runs.
    """

    query = db.query(models.TestRun)

    if simulation_config_id is not None:
        query = query.filter(
            models.TestRun.simulation_config_id == simulation_config_id
        )

    runs = query.all()
    return runs
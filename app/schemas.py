# app/schemas.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .models import RunResult


class TestbedBase(BaseModel):
    name: str
    location: str | None = None
    description: str | None = None


class TestbedCreate(TestbedBase):
    """
    Schema for creating a new Testbed.
    """
    pass


class TestbedRead(TestbedBase):
    """
    Schema for reading a Testbed from the API.
    """
    id: int

    class Config:
        orm_mode = True


class SimulationConfigBase(BaseModel):
    """
    Common fields shared by SimulationConfig input/output models
    """
    testbed_id: int
    name: str
    software_version: Optional[str] = None
    os: Optional[str] = None
    notes: Optional[str] = None 


class SimulationConfigCreate(SimulationConfigBase):
    """
    Schema for creating a new SimulationCOnfig.
    """
    pass 


class SimulationConfigRead(SimulationConfigBase):
    """
    Schema for reading a SimulationConfig from the API
    """
    id: int

    class Config:
        orm_mode = True


class TestRunBase(BaseModel):
    """
    Common fields shared by TestRun input/output models.
    """
    simulation_config_id: int
    operator: Optional[str] = None
    result: RunResult = RunResult.IN_PROGRESS
    notes: Optional[str] = None


class TestRunCreate(TestRunBase):
    """
    Schema for creating a new TestRun.
    """
    pass


class TestRunRead(TestRunBase):
    """
    Schema for reading a TestRun from the API.
    """
    id: int
    run_date: datetime

    class Config:
        orm_mode = True
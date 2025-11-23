# app/schemas.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from .models import RunResult


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
        from_attributes = True

        
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
        from_attributes = True

class SimulationConfigBase(BaseModel):
    """
    Common fields shared by SimulationConfig input/output models
    """
    testbed_id: int
    name: str
    sim_version: Optional[str] = None
    os: Optional[str] = None
    notes: Optional[str] = None 
    is_current_config: bool | None = None


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
        from_attributes = True
class SimulationConfigWithRuns(BaseModel):
    """
    A SimulationConfig plus its associated TestRuns.
    """
    id: int
    testbed_id: int
    name: str
    sim_version: Optional[str] = None
    os: Optional[str] = None
    notes: Optional[str] = None
    is_current_config: bool
    runs: List[TestRunRead] = []

    class Config:
        from_attributes = True

class TestbedSummary(BaseModel):
    """
    Summary view of a Testbed with its configs and runs.
    """
    id: int
    name: str
    location: Optional[str] = None
    description: Optional[str] = None
    configs: List[SimulationConfigWithRuns] = []

    class Config:
        from_attributes = True
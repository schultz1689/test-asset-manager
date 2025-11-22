# app/models.py

from datetime import datetime
import enum

from sqlalchemy import ( 
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship

from .db import Base

class Testbed(Base):
    """
    ORM model for testbeds. 

    Each Testbed is at least the hardware required to run a sim. This includes devices that run remotely.
    """

    __tablename__ = "testbeds"

    id = Column(Integer, primary_key=True, index=True)
    # The hostname of the device. If dual host, use the first hostname and clarify in the description
    name = Column(String(100), nullable=False, unique=True, index=True)
    location = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    configs = relationship(
        "SimulationConfig",
        back_populates="testbed",
        cascade="all, delete-orphan",
    )

class SimulationConfig(Base):

    """
    ORM model for the simulation_configs table

    Represents the current configuration that a Testbed is supporting, and has supported in the past.
    """

    __tablename__ = "simulation_configs"

    id = Column(Integer, primary_key=True, index=True)

    testbed_id = Column(
        Integer,
        ForeignKey("testbeds.id"),
        nullable=False,
        index=True,
    )

    # Right now the idea is that we can track every single SimulationConfig ran on a specific device, and what its current configuration is.
    # As of making this, I belive this will change a lot. For now lets get this prototype off the ground.
    name = Column(String(100), nullable=False)
    sim_version = Column(String(50), nullable=True)
    os = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_current_config = Column(bool, nullable=True)

    testbed = relationship(
        "Testbed",
        back_populates="configs",
    )

    runs = relationship(
        "TestRun",
        back_populates="config",
        cascade="all, delete-orphan",
    )

class RunResult(str, enum.Enum):
    """
    Enum of allowed run results.
    """
    PASS = "PASS"
    FAIL = "FAIL"
    IN_PROGRESS = "IN_PROGRESS"
class TestRun(Base):
    """
    ORM model for the test_runs tablee

    Represents a single execution of a SimulationConfig
    """

    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)

    simulation_config_id = Column(
        DateTime,
        nullable=False,
        default=datetime.timezone.utc,
    )

    operator = Column(String(100), nullable=True)

    result = Column(
        Enum(RunResult),
        nullable=False,
        default=RunResult.IN_PROGRESS,
    )

    notes = Column(Text, nullable = True)

    config = relationship(
        "SimulationConfig",
        back_populates="runs",
        cascade="all, delete-orphan",
    )
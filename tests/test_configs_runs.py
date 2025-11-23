# tests/test_configs_runs.py

import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.db import Base
from app import models

TEST_DB_PATH = "test_asset_manager_configs_runs.db"

if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, 
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_full_flow_testbed_config_run():
    """
    End-to-end test of:
      1) Creating a Testbed
      2) Creating a SimulationConfig for that Testbed
      3) Creating a TestRun for that SimulationConfig
      4) Listing configs and runs and verifying the data
    """

    new_testbed = {
        "name": "Integration Rig 1",
        "location": "Lab A",
        "description": "Main integration rig for configs and runs",
    }

    response = client.post("/testbeds", json=new_testbed)
    assert response.status_code == 201

    testbed_data = response.json()
    assert testbed_data["name"] == new_testbed["name"]
    assert testbed_data["location"] == new_testbed["location"]
    assert testbed_data["description"] == new_testbed["description"]
    assert "id" in testbed_data

    testbed_id = testbed_data["id"]


    new_config = {
        "testbed_id": testbed_id,
        "name": "Baseline Config v1",
        "sim_version": "1.0.0",
        "os": "Linux",
        "notes": "Baseline configuration for regression testing",
        "is_current_config": True,
    }

    response = client.post("/configs", json=new_config)
    assert response.status_code == 201

    config_data = response.json()
    assert config_data["testbed_id"] == testbed_id
    assert config_data["name"] == new_config["name"]
    assert config_data["sim_version"] == new_config["sim_version"]
    assert config_data["os"] == new_config["os"]
    assert config_data["notes"] == new_config["notes"]
    assert config_data["is_current_config"] is True
    assert "id" in config_data

    config_id = config_data["id"]


    new_run = {
        "simulation_config_id": config_id,
        "operator": "Eric",
        "result": "PASS",
        "notes": "Initial smoke test run",
    }

    response = client.post("/runs", json=new_run)
    assert response.status_code == 201

    run_data = response.json()
    assert run_data["simulation_config_id"] == config_id
    assert run_data["operator"] == new_run["operator"]
    assert run_data["result"] == new_run["result"]
    assert run_data["notes"] == new_run["notes"]
    assert "id" in run_data
    assert "run_date" in run_data  

    response = client.get(f"/configs?testbed_id={testbed_id}")
    assert response.status_code == 200

    configs_list = response.json()
    assert len(configs_list) == 1
    assert configs_list[0]["id"] == config_id
    assert configs_list[0]["name"] == new_config["name"]

    response = client.get(f"/runs?simulation_config_id={config_id}")
    assert response.status_code == 200

    runs_list = response.json()
    assert len(runs_list) == 1
    assert runs_list[0]["id"] == run_data["id"]
    assert runs_list[0]["result"] == "PASS"
    assert runs_list[0]["operator"] == "Eric"


def test_create_config_for_nonexistent_testbed_returns_404():
    """
    If we try to create a SimulationConfig for a testbed_id that doesn't exist,
    the API should return 404 Not Found.
    """

    # Use an ID that we are confident doesn't exist yet.
    # Since we freshly create the DB for this module, 9999 is safe.
    new_config = {
        "testbed_id": 9999,
        "name": "Config pointing to nowhere",
        "software_version": "0.0.1",
        "os": "Linux",
        "notes": "This should fail because the testbed doesn't exist",
        "is_current_config": True,
    }

    response = client.post("/configs", json=new_config)

    assert response.status_code == 404

    data = response.json()
    assert "not found" in data["detail"].lower()


def test_create_run_for_nonexistent_config_returns_404():
    """
    If we try to create a TestRun for a simulation_config_id that doesn't exist,
    the API should return 404 Not Found.
    """

    new_run = {
        "simulation_config_id": 9999,
        "operator": "Eric",
        "result": "PASS",
        "notes": "This should fail because the config doesn't exist",
    }

    response = client.post("/runs", json=new_run)

    assert response.status_code == 404

    data = response.json()
    assert "not found" in data["detail"].lower()

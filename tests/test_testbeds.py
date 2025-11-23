# tests/test_testbeds.py

import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db 
from app.db import Base
from app import models

TEST_DB_PATH = "test_asset_manager_test.db"

if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

SQLALCHEMY_TEST_DATABASE_URL = f"sqlite:///./{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
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


def test_create_and_list_testbeds():
    response = client.get("/testbeds")
    assert response.status_code == 200
    initial_testbeds = response.json()
    initial_count = len(initial_testbeds)

    new_testbed = {
        "name": "Testbed 1",
        "location": "Lab A",
        "description": "First testbed",
    }
    response = client.post("/testbeds", json=new_testbed)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Testbed 1"
    assert data["location"] == "Lab A"
    assert data["description"] == "First testbed"
    assert "id" in data

    response = client.get("/testbeds")
    assert response.status_code == 200
    testbeds = response.json()
    assert len(testbeds) == initial_count + 1

    names = [tb["name"] for tb in testbeds]
    assert "Testbed 1" in names
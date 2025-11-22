# app/schemas.py

from pydantic import BaseModel

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

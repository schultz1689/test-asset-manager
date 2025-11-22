# app/models.py

from sqlalchemy import Column, Integer, String, Text
from .db import Base

class Testbed(Base):

    __tablename__ = "testbeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    location = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
# src/models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = 'pokemon'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    types = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    abilities = Column(String)
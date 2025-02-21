# src/database.py
import os
from sqlite3 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_DIR = "./data"
DATABASE_URL = "sqlite:///./data/pokemon.db"

# Ensure data directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except OperationalError as e:
        print(f"Error initializing database: {e}")
        # Create data directory if it doesn't exist
        os.makedirs(DATABASE_DIR, exist_ok=True)
        # Retry database initialization
        Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
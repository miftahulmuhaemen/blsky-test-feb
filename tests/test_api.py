import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api import app
from src.database import Base, get_db
from src.models import Pokemon

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def sample_pokemon(test_db):
    db = TestingSessionLocal()
    pokemon = Pokemon(
        id=1,
        name="bulbasaur",
        types="grass,poison",
        height=7,
        weight=69,
        abilities="overgrow,chlorophyll"
    )
    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)
    db.close()
    return pokemon

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_read_pokemon(sample_pokemon):
    response = client.get("/api/pokemon/1")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["type"] == "pokemon"
    assert data["data"]["id"] == "1"
    assert data["data"]["attributes"]["name"] == "bulbasaur"
    assert "grass" in data["data"]["attributes"]["types"]

def test_read_pokemon_not_found():
    response = client.get("/api/pokemon/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pokemon not found"

def test_read_all_pokemon(sample_pokemon):
    response = client.get("/api/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["type"] == "pokemon"
    assert data["data"][0]["id"] == "1"

def test_pokemon_json_format(sample_pokemon):
    response = client.get("/api/pokemon/1")
    data = response.json()
    
    # Check JSON:API format
    assert "data" in data
    assert "type" in data["data"]
    assert "id" in data["data"]
    assert "attributes" in data["data"]
    
    # Check attributes
    attributes = data["data"]["attributes"]
    assert "name" in attributes
    assert "types" in attributes
    assert "height" in attributes
    assert "weight" in attributes
    assert "abilities" in attributes
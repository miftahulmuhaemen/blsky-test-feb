import pytest
import responses
from src.scraper import PokemonScraper
from src.models import Pokemon
from src.database import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_scraper.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def scraper(test_db):
    scraper = PokemonScraper()
    # Override the session to use test database
    scraper.session = TestingSessionLocal()
    return scraper

@responses.activate
def test_scrape_single_pokemon(scraper):
    
    # Test scraping
    scraper.scrape_pokemon(limit=1)

    # Verify database entry
    db = TestingSessionLocal()
    pokemon = db.query(Pokemon).first()
    assert pokemon.name == "Bulbasaur"
    assert pokemon.types == "Grass,Poison"
    assert pokemon.height == "0.7 m (2′04″)"
    assert pokemon.weight == "6.9 kg (15.2 lbs)"
    assert pokemon.abilities == "Overgrow,Chlorophyll"
    db.close()

def test_database_connection(test_db):
    db = TestingSessionLocal()
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        db.close()
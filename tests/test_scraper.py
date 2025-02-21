import pytest
import responses
from src.scraper import PokemonScraper
from src.models import Pokemon
from src.database import Base, get_db
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
    # Mock PokeAPI responses
    pokemon_list_response = {
        "results": [
            {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon/1"
            }
        ]
    }
    
    pokemon_detail_response = {
        "id": 1,
        "name": "bulbasaur",
        "types": [
            {"type": {"name": "grass"}},
            {"type": {"name": "poison"}}
        ],
        "height": 7,
        "weight": 69,
        "abilities": [
            {"ability": {"name": "overgrow"}},
            {"ability": {"name": "chlorophyll"}}
        ]
    }

    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon?limit=1",
        json=pokemon_list_response,
        status=200
    )

    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/1",
        json=pokemon_detail_response,
        status=200
    )

    # Test scraping
    scraper.scrape_pokemon(limit=1)

    # Verify database entry
    db = TestingSessionLocal()
    pokemon = db.query(Pokemon).first()
    assert pokemon.name == "bulbasaur"
    assert pokemon.types == "grass,poison"
    assert pokemon.height == 7
    assert pokemon.weight == 69
    assert pokemon.abilities == "overgrow,chlorophyll"
    db.close()

@responses.activate
def test_scrape_error_handling(scraper):
    # Mock failed API response
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon?limit=1",
        status=500
    )

    # Test error handling
    with pytest.raises(Exception):
        scraper.scrape_pokemon(limit=1)

def test_database_connection(test_db):
    db = TestingSessionLocal()
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        db.close()
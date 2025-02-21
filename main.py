# main.py
import os
import uvicorn
from src.database import init_db
from src.scraper import PokemonScraper
from src.api import app

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Scrape Pokemon data
    scraper = PokemonScraper()
    scraper.scrape_pokemon()
    
    # Run API server
    uvicorn.run(app, host=HOST, port=PORT)
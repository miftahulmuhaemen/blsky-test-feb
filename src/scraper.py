# src/scraper.py
import requests
from .models import Pokemon
from .database import SessionLocal

class PokemonScraper:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.session = SessionLocal()

    def scrape_pokemon(self, limit=151):  # Starting with original 151 Pokemon
        pokemon_list = requests.get(f"{self.base_url}/pokemon?limit={limit}").json()
        
        for pokemon in pokemon_list['results']:
            pokemon_data = requests.get(pokemon['url']).json()
            
            # Extract relevant data
            pokemon_entry = Pokemon(
                id=pokemon_data['id'],
                name=pokemon_data['name'],
                types=','.join([t['type']['name'] for t in pokemon_data['types']]),
                height=pokemon_data['height'],
                weight=pokemon_data['weight'],
                abilities=','.join([a['ability']['name'] for a in pokemon_data['abilities']])
            )
            
            self.session.merge(pokemon_entry)
        
        self.session.commit()
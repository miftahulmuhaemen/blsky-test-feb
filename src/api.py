# src/api.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Pokemon

app = FastAPI()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/pokemon")
def get_all_pokemon(db: Session = Depends(get_db)):
    pokemon_list = db.query(Pokemon).all()
    return {
        "data": [
            {
                "type": "pokemon",
                "id": str(pokemon.id),
                "attributes": {
                    "name": pokemon.name,
                    "types": pokemon.types.split(','),
                    "height": pokemon.height,
                    "weight": pokemon.weight,
                    "abilities": pokemon.abilities.split(',')
                }
            }
            for pokemon in pokemon_list
        ]
    }

@app.get("/api/pokemon/{pokemon_id}")
def get_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return {
        "data": {
            "type": "pokemon",
            "id": str(pokemon.id),
            "attributes": {
                "name": pokemon.name,
                "types": pokemon.types.split(','),
                "height": pokemon.height,
                "weight": pokemon.weight,
                "abilities": pokemon.abilities.split(',')
            }
        }
    }
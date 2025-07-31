from pydantic import BaseModel
from typing import List

class PokemonBase(BaseModel):
    id_pokemon: int

class TimeCompletoCreate(BaseModel):
    id_time: int
    id_usuario: int
    nivel_combate: int
    pokemons: List[PokemonBase]

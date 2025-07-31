from pydantic import BaseModel
from typing import Optional
from datetime import date

# ---------- USUÁRIO ----------
class Usuario(BaseModel):
    nome: str
    email: str
    data_cadastro: date
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

# ---------- POKÉMON ----------
class PokemonCreate(BaseModel):
    nome: str
    popularidade: int
    nivel: int
    raridade: str

class PokemonUpdate(BaseModel):
    nome: Optional[str] = None
    popularidade: Optional[int] = None
    nivel: Optional[int] = None
    raridade: Optional[str] = None

class Pokemon(BaseModel):
    id_pokemon: int
    nome: str
    popularidade: int
    nivel: int
    raridade: str

# ---------- TIME ----------
class Time(BaseModel):
    id_time: int
    id_usuario: int
    nivel_combate: int

class TimeUpdate(BaseModel):
    nivel_combate: Optional[int] = None

# ---------- SORTEIO ----------
class Sorteio(BaseModel):
    id_sorteio: int
    tipo_sorteio: str
    id_usuario: int

class SorteioUpdate(BaseModel):
    tipo_sorteio: Optional[str] = None

# ---------- BATALHA ----------
class Batalha(BaseModel):
    id_batalha: int
    id_time_1: int
    id_time_2: int
    resultado: str

class BatalhaUpdate(BaseModel):
    resultado: Optional[str] = None

# ---------- RELACIONAMENTOS ----------
class TimePokemon(BaseModel):
    id_time: int
    id_pokemon: int

class SorteioPokemon(BaseModel):
    id_sorteio: int
    id_pokemon: int


#-------------visões-------------------
class QtdPokemonsPorTreinador(BaseModel):
    id_usuario: int
    treinador: str
    qtd_pokemons: int

class QtdPokemonsPorTipo(BaseModel):
    nome_tipo: str
    qtd_pokemons: int

class PokemonsPorTreinador(BaseModel):
    treinador: str
    pokemon: str
    nivel_combate: int

class PokemonComTipo(BaseModel):
    id_pokemon: int
    nome: str
    raridade: str
    nome_tipo: str
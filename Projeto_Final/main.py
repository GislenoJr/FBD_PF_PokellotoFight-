from fastapi import FastAPI

from pokemon_router import router as pokemon_router
from usuario_router import router as usuario_router
from time_router import router as time_router
from sorteio_router import router as sorteio_router
from batalha_router import router as batalha_router
from time_pokemon_router import router as time_pokemon_router
from sorteio_pokemon_router import router as sorteio_pokemon_router
from completo import router as completo_router
from view_router import router as view_router  




app = FastAPI(
    title="API Pokémon",
    version="1.0"
)

app.include_router(pokemon_router, prefix="/pokemons", tags=["Pokémons"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(time_router, prefix="/times", tags=["Times"])
app.include_router(sorteio_router, prefix="/sorteios", tags=["Sorteios"])
app.include_router(batalha_router, prefix="/batalhas", tags=["Batalhas"])
app.include_router(time_pokemon_router, prefix="/relacoes/time-pokemon", tags=["Time × Pokémon"])
app.include_router(sorteio_pokemon_router, prefix="/relacoes/sorteio-pokemon", tags=["Sorteio × Pokémon"])
app.include_router(completo_router, prefix="/completo", tags=["Operações Completas"])
app.include_router(view_router, prefix="/api/views")
from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Pokemon, PokemonUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Pokemon])
async def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_pokemon, nome, popularidade, nivel, raridade FROM pokemon")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Pokemon(id_pokemon=r[0], nome=r[1], popularidade=r[2], nivel=r[3], raridade=r[4]) for r in rows]

@router.post("/")
async def criar(pokemon: Pokemon):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO pokemon (id_pokemon, nome, popularidade, nivel, raridade) VALUES (%s, %s, %s, %s, %s)",
            (pokemon.id_pokemon, pokemon.nome, pokemon.popularidade, pokemon.nivel, pokemon.raridade)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao inserir Pokémon: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pokémon criado com sucesso"}

@router.patch("/pokemon/{id_pokemon}")
async def atualizar(id_pokemon: int, dados: PokemonUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_pokemon FROM pokemon WHERE id_pokemon = %s", (id_pokemon,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Pokémon não encontrado")

    campos = []
    valores = []
    for campo, valor in dados.dict(exclude_unset=True).items():
        campos.append(f"{campo} = %s")
        valores.append(valor)

    if not campos:
        raise HTTPException(400, "Nenhum campo para atualizar")

    valores.append(id_pokemon)
    try:
        cur.execute(f"UPDATE pokemon SET {', '.join(campos)} WHERE id_pokemon = %s", valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar Pokémon: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pokémon atualizado com sucesso"}

@router.delete("/pokemon/{id_pokemon}")
async def deletar(id_pokemon: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM pokemon WHERE id_pokemon = %s", (id_pokemon,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Pokémon não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao deletar Pokémon: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pokémon deletado com sucesso"}
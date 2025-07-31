from fastapi import APIRouter, HTTPException
from db import get_connection
from models import TimePokemon
from typing import List

router = APIRouter()

@router.get("/", response_model=List[TimePokemon])
async def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_time, id_pokemon FROM time_pokemon")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [TimePokemon(id_time=r[0], id_pokemon=r[1]) for r in rows]

@router.post("/")
async def inserir(rel: TimePokemon):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO time_pokemon (id_time, id_pokemon) VALUES (%s, %s)",
            (rel.id_time, rel.id_pokemon)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao inserir relação: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Relacionamento criado com sucesso"}

@router.delete("/")
async def deletar(rel: TimePokemon):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM time_pokemon WHERE id_time = %s AND id_pokemon = %s",
            (rel.id_time, rel.id_pokemon)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Relacionamento não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao deletar relacionamento: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Relacionamento deletado com sucesso"}

# 🔍 NOVO ENDPOINT: Listar todos os Pokémon de um usuário no time
@router.get("/usuario/{id_usuario}")
async def listar_pokemons_do_usuario(id_usuario: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id_pokemon, p.nome, p.nivel, p.raridade, p.popularidade
            FROM pokemon p
            JOIN time_pokemon tp ON p.id_pokemon = tp.id_pokemon
            JOIN time t ON tp.id_time = t.id_time
            WHERE t.id_usuario = %s
        """, (id_usuario,))
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar pokémons: {e}")
    finally:
        cur.close()
        conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Nenhum Pokémon encontrado para esse usuário")

    return [
        {
            "id_pokemon": r[0],
            "nome": r[1],
            "nivel": r[2],
            "raridade": r[3],
            "popularidade": r[4]
        }
        for r in rows
    ]

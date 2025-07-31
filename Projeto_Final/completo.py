from fastapi import APIRouter, HTTPException
from db import get_connection
from models2 import TimeCompletoCreate

router = APIRouter()

@router.post("/time")
async def criar_time_completo(time: TimeCompletoCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN;")
        cur.execute(
            "INSERT INTO time (id_time, id_usuario, nivel_combate) VALUES (%s, %s, %s)",
            (time.id_time, time.id_usuario, time.nivel_combate)
        )
        for poke in time.pokemons:
            cur.execute(
                "INSERT INTO time_pokemon (id_time, id_pokemon) VALUES (%s, %s)",
                (time.id_time, poke.id_pokemon)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar time completo: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Time completo criado com sucesso"}

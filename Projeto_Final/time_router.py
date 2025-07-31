from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Time, TimeUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Time])
async def listar_times():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_time, id_usuario, nivel_combate FROM time")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Time(id_time=r[0], id_usuario=r[1], nivel_combate=r[2]) for r in rows]

@router.get("/{id_time}", response_model=Time)
async def get_time(id_time: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_time, id_usuario, nivel_combate FROM time WHERE id_time=%s", (id_time,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Time(id_time=row[0], id_usuario=row[1], nivel_combate=row[2])
    raise HTTPException(404, "Time não encontrado")

@router.post("/")
async def criar_time(time: Time):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO time (id_time, id_usuario, nivel_combate) VALUES (%s, %s, %s)",
            (time.id_time, time.id_usuario, time.nivel_combate)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar time: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Time criado com sucesso"}

@router.patch("/{id_time}")
async def atualizar_time(id_time: int, time_update: TimeUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE time SET id_usuario = %s, nivel_combate = %s WHERE id_time = %s",
            (time_update.id_usuario, time_update.nivel_combate, id_time)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar time: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Time atualizado com sucesso"}

@router.delete("/{id_time}")
async def deletar_time(id_time: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM time WHERE id_time = %s", (id_time,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar time: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Time deletado com sucesso"}

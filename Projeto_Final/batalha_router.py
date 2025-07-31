from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Batalha, BatalhaUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Batalha])
async def listar_batalhas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_batalha, id_time_1, id_time_2, resultado FROM batalha")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Batalha(id_batalha=r[0], id_time_1=r[1], id_time_2=r[2], resultado=r[3]) for r in rows]

@router.get("/{id_batalha}", response_model=Batalha)
async def get_batalha(id_batalha: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_batalha, id_time_1, id_time_2, resultado FROM batalha WHERE id_batalha = %s", (id_batalha,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Batalha(id_batalha=row[0], id_time_1=row[1], id_time_2=row[2], resultado=row[3])
    raise HTTPException(404, "Batalha não encontrada")

@router.post("/")
async def criar_batalha(batalha: Batalha):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO batalha (id_batalha, id_time_1, id_time_2, resultado) VALUES (%s, %s, %s, %s)",
            (batalha.id_batalha, batalha.id_time_1, batalha.id_time_2, batalha.resultado)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar batalha: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Batalha criada com sucesso"}

@router.patch("/{id_batalha}")
async def atualizar_batalha(id_batalha: int, batalha_update: BatalhaUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        campos = []
        valores = []

        if batalha_update.resultado is not None:
            campos.append("resultado = %s")
            valores.append(batalha_update.resultado)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        valores.append(id_batalha)
        sql = f"UPDATE batalha SET {', '.join(campos)} WHERE id_batalha = %s"

        cur.execute(sql, tuple(valores))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Batalha não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar batalha: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Batalha atualizada com sucesso"}

@router.delete("/{id_batalha}")
async def deletar_batalha(id_batalha: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM batalha WHERE id_batalha = %s", (id_batalha,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Batalha não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao deletar batalha: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Batalha deletada com sucesso"}
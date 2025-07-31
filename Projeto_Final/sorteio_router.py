from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Sorteio, SorteioUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Sorteio])
async def listar_sorteios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_sorteio, tipo_sorteio, id_usuario FROM sorteio")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Sorteio(id_sorteio=r[0], tipo_sorteio=r[1], id_usuario=r[2]) for r in rows]

@router.get("/{id_sorteio}", response_model=Sorteio)
async def get_sorteio(id_sorteio: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_sorteio, tipo_sorteio, id_usuario FROM sorteio WHERE id_sorteio=%s", (id_sorteio,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Sorteio(id_sorteio=row[0], tipo_sorteio=row[1], id_usuario=row[2])
    raise HTTPException(404, "Sorteio não encontrado")

@router.post("/")
async def criar_sorteio(sorteio: Sorteio):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO sorteio (id_sorteio, tipo_sorteio, id_usuario) VALUES (%s, %s, %s)",
            (sorteio.id_sorteio, sorteio.tipo_sorteio, sorteio.id_usuario)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar sorteio: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Sorteio criado com sucesso"}

@router.patch("/{id_sorteio}")
async def atualizar_sorteio(id_sorteio: int, sorteio_update: SorteioUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        campos = []
        valores = []

        if sorteio_update.tipo_sorteio is not None:
            campos.append("tipo_sorteio = %s")
            valores.append(sorteio_update.tipo_sorteio)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        valores.append(id_sorteio)
        sql = f"UPDATE sorteio SET {', '.join(campos)} WHERE id_sorteio = %s"

        cur.execute(sql, tuple(valores))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Sorteio não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar sorteio: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Sorteio atualizado com sucesso"}

@router.delete("/{id_sorteio}")
async def deletar_sorteio(id_sorteio: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM sorteio WHERE id_sorteio = %s", (id_sorteio,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Sorteio não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao deletar sorteio: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Sorteio deletado com sucesso"}
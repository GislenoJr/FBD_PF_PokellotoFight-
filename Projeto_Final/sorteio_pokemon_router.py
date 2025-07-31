from fastapi import APIRouter, HTTPException
from db import get_connection
from models import SorteioPokemon
from typing import List

router = APIRouter()

@router.get("/", response_model=List[SorteioPokemon])
async def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_sorteio, id_pokemon FROM sorteio_pokemon")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [SorteioPokemon(id_sorteio=r[0], id_pokemon=r[1]) for r in rows]

@router.get("/{id_sorteio}", response_model=List[SorteioPokemon])
async def listar_por_sorteio(id_sorteio: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_sorteio, id_pokemon FROM sorteio_pokemon WHERE id_sorteio = %s", (id_sorteio,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Nenhum relacionamento encontrado para esse sorteio")
    return [SorteioPokemon(id_sorteio=r[0], id_pokemon=r[1]) for r in rows]

@router.post("/")
async def inserir(rel: SorteioPokemon):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO sorteio_pokemon (id_sorteio, id_pokemon) VALUES (%s, %s)",
            (rel.id_sorteio, rel.id_pokemon)
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
async def deletar(rel: SorteioPokemon):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM sorteio_pokemon WHERE id_sorteio = %s AND id_pokemon = %s",
            (rel.id_sorteio, rel.id_pokemon)
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

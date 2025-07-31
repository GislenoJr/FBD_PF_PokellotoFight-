from fastapi import APIRouter, HTTPException
from db import get_connection
from models import PokemonsPorTreinador, QtdPokemonsPorTipo, PokemonComTipo, QtdPokemonsPorTipo
from typing import List

router = APIRouter()

@router.get("/vw_pokemons_por_treinador", response_model=List[PokemonsPorTreinador])
async def listar_pokemons_por_treinador():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT treinador, pokemon, nivel_combate FROM vw_pokemons_por_treinador")
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(500, f"Erro ao consultar vw_pokemons_por_treinador: {e}")
    finally:
        cur.close()
        conn.close()

    return [
        PokemonsPorTreinador(treinador=r[0], pokemon=r[1], nivel_combate=r[2])
        for r in rows
    ]


@router.get("/vw_qtd_pokemons_por_tipo", response_model=List[QtdPokemonsPorTipo])
async def listar_qtd_pokemons_por_tipo():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nome_tipo, qtd_pokemons FROM vw_qtd_pokemons_por_tipo")
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(500, f"Erro ao consultar vw_qtd_pokemons_por_tipo: {e}")
    finally:
        cur.close()
        conn.close()

    return [
        QtdPokemonsPorTipo(nome_tipo=r[0], qtd_pokemons=r[1])
        for r in rows
    ]

@router.get("/vw_pokemons_por_treinador", response_model=List[PokemonsPorTreinador])
async def listar_pokemons_por_treinador():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT treinador, pokemon, nivel_combate FROM vw_pokemons_por_treinador")
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(500, f"Erro ao consultar vw_pokemons_por_treinador: {e}")
    finally:
        cur.close()
        conn.close()

    return [
        PokemonsPorTreinador(treinador=r[0], pokemon=r[1], nivel_combate=r[2])
        for r in rows
    ]


@router.get("/vw_qtd_pokemons_por_tipo", response_model=List[QtdPokemonsPorTipo])
async def listar_qtd_pokemons_por_tipo():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nome_tipo, qtd_pokemons FROM vw_qtd_pokemons_por_tipo")
        rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(500, f"Erro ao consultar vw_qtd_pokemons_por_tipo: {e}")
    finally:
        cur.close()
        conn.close()

    return [
        QtdPokemonsPorTipo(nome_tipo=r[0], qtd_pokemons=r[1])
        for r in rows
    ]

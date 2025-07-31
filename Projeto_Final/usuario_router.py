from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Usuario, UsuarioUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Usuario])
async def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome, email, data_cadastro, senha FROM usuario")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Usuario(id_usuario=r[0], nome=r[1], email=r[2], data_cadastro=r[3], senha=r[4]) for r in rows]

@router.get("/{id_usuario}", response_model=Usuario)
async def get_usuario(id_usuario: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome, email, data_cadastro, senha FROM usuario WHERE id_usuario=%s", (id_usuario,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Usuario(id_usuario=row[0], nome=row[1], email=row[2], data_cadastro=row[3], senha=row[4])
    raise HTTPException(404, "Usuário não encontrado")

@router.post("/")
async def criar_usuario(usuario: Usuario):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuario ( nome, email, data_cadastro, senha) VALUES ( %s, %s, %s, %s)",
            (usuario.nome, usuario.email, usuario.data_cadastro, usuario.senha)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar usuário: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuário criado com sucesso"}

@router.patch("/{id_usuario}")
async def atualizar_usuario(id_usuario: int, dados: UsuarioUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s", (id_usuario,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Usuário não encontrado")

    campos = []
    valores = []
    for campo, valor in dados.dict(exclude_unset=True).items():
        campos.append(f"{campo} = %s")
        valores.append(valor)

    if not campos:
        raise HTTPException(400, "Nenhum campo para atualizar")

    valores.append(id_usuario)

    try:
        cur.execute(f"UPDATE usuario SET {', '.join(campos)} WHERE id_usuario = %s", valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar usuário: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuário atualizado com sucesso"}

@router.delete("/{id_usuario}")
async def deletar_usuario(id_usuario: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Usuário não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao deletar usuário: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuário deletado com sucesso"}

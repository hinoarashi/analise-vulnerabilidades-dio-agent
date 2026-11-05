#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 03 DIO - app.py VULNERÁVEL (SQL Injection intencional)

⚠️  ESTE ARQUIVO É INTENCIONALMENTE VULNERÁVEL — apenas para laboratório.
    Monte um banco SQLite em memória, crie a tabela `usuarios` e faça um
    login que monta a consulta SQL juntando diretamente o que a pessoa
    digitou (concatenação de strings). É exatamente esse padrão que
    permite SQL Injection.

    NÃO execute fora de ambiente de laboratório controlado.
    NÃO conecte a nenhum banco real ou de terceiros.

Uso (somente laboratório):
    python app.py <usuario> <senha>
    python app.py admin "' OR '1'='1"        # exemplo de tentativa de bypass
    python app.py --demo                     # demonstra login legítimo e bypass

O código vulnerável está marcado com:  # <- VULNERÁVEL
"""

from __future__ import annotations

import sqlite3
import sys

# ---------------------------------------------------------------------------
# Banco de laboratório (SQLite em memória — nada sai da máquina)
# ---------------------------------------------------------------------------

def banco_de_laboratorio() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY,"
        "usuario TEXT NOT NULL UNIQUE,"
        "senha TEXT NOT NULL"
        ")"
    )
    # Credenciais de laboratorio (ficticias, sem valor real)
    cur.executemany(
        "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
        [("admin", "admin123"), ("usuario_lab", "lab123456")],
    )
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Login VULNERÁVEL — monta o SQL concatenando a entrada do usuário
# ---------------------------------------------------------------------------

def login(conn: sqlite3.Connection, usuario: str, senha: str) -> tuple | None:
    cur = conn.cursor()
    # <- CORRIGIDO: consulta parametrizada. A entrada nunca é interpreta como SQL.
    query = "SELECT id, usuario FROM usuarios WHERE usuario = ? AND senha = ?"
    cur.execute(query, (usuario, senha))
    resultado = cur.fetchone()
    return resultado


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        conn = banco_de_laboratorio()
        print("[demo] Login legítimo: admin / admin123")
        print("  ->", login(conn, "admin", "admin123"))
        print("[demo] Bypass com senha fictícia (laboratório):")
        print("  ->", login(conn, "admin", "' OR '1'='1"))
        conn.close()
        return 0

    if len(sys.argv) != 3:
        print("Uso: python app.py <usuario> <senha>")
        print("     python app.py --demo")
        return 2

    conn = banco_de_laboratorio()
    resultado = login(conn, sys.argv[1], sys.argv[2])
    if resultado:
        print(f"[login] OK — usuário autenticado: {resultado[1]} (id={resultado[0]})")
    else:
        print("[login] FALHA — credenciais inválidas.")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

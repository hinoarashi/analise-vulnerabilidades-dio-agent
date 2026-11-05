#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 03 DIO - app.py CORRIGIDO (SQL Injection mitigado)

Versão defensiva do mesmo login: usa consulta parametrizada (placeholders
"?" do sqlite3), nunca concatenando entrada do usuário na query.

Uso:
    python app.py <usuario> <senha>
    python app.py --demo     # demonstra login legítimo e que o bypass falha
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
# Login SEGURO — consulta parametrizada, entrada nunca vira SQL
# ---------------------------------------------------------------------------

def login(conn: sqlite3.Connection, usuario: str, senha: str) -> tuple | None:
    cur = conn.cursor()
    # SEGURO: parâmetros passados separadamente, sem interpolação
    cur.execute(
        "SELECT id, usuario FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha),
    )
    return cur.fetchone()


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        conn = banco_de_laboratorio()
        print("[demo] Login legítimo: admin / admin123")
        print("  ->", login(conn, "admin", "admin123"))
        print("[demo] Mesma tentativa de bypass (deve FALHAR):")
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

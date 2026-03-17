from __future__ import annotations

import sqlite3
from pathlib import Path

from schema import SCHEMA_SQL

DB_DIR = Path.home() / ".zeit"
DB_PATH = DB_DIR / "zeit.db"


def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    initialize_database(connection)
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)
    connection.commit()

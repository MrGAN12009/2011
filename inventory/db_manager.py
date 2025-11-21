from __future__ import annotations

import sqlite3
from typing import Any


class DatabaseManager:
    def __init__(self):
        self._TABLE_NAME = "inventory"
        self.db_path = "db.db"
        self.connection: sqlite3.Connection | None = None
        self._connect()
        self._init_tables()

    def _connect(self) -> None:
        if self.connection:
            return
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Cursor | None:
        if not self.connection:
            raise RuntimeError("Database connection is not connected")
        cursor = self.connection.execute(query, params)
        self.connection.commit()
        return cursor

    def query(self, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def _init_tables(self) -> None:
        self.execute(f"""CREATE TABLE IF NOT EXISTS {self._TABLE_NAME} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL,
                            quantity INTEGER NOT NULL,
                            description TEXT);""")

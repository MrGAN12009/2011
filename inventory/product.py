from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """Описание продукта"""
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def from_row(cls, sqlite_row: sqlite3.Row) -> Product:
        return cls(
            id = sqlite_row['id'],
            name = sqlite_row['name'],
            price = sqlite_row['price'],
            quantity = sqlite_row['quantity'],
            description = sqlite_row['description'],
        )


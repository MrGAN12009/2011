"""CRUD OPS"""
from __future__ import annotations

from typing import Optional

from .db_manager import DatabaseManager
from .product import Product


class ProductManager:
    """CRUD OPERATIONS"""
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def add_product(self, product: Product) -> Product:
        cursor = self.db.execute(
            "INSERT INTO inventory(name, price, quantity, description) "
            "VALUES (?, ?, ?, ?)",
            (product.name, product.price, product.quantity, product.description))

        product.id = cursor.lastrowid
        return product

    def list_products(self) -> list[Product]:
        rows = self.db.execute(
            "SELECT * FROM inventory ORDER BY name"
        )
        return [Product.from_row(row) for row in rows]

    def get_product_by_id(self, id: int) -> Optional[Product]:
        row = self.db.execute("SELECT * FROM inventory WHERE id = ?", (id,))
        return Product.from_row(row[0]) if row else None

    def update_product(self, product: Product) -> bool:
        if not product.id:
            raise ValueError("Product ID is required")
        cursor = self.db.execute("UPDATE inventory SET name = ?, price = ?, quantity = ?, description = ? "
                                 "WHERE id = ? ",
                                 (product.name, product.price, product.quantity,
                                  product.description, product.id))

        return cursor.rowcount > 0

    def delete_product(self, id: int) -> bool:
        cursor = self.db.execute("DELETE FROM inventory WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def search_product(self, query: str) -> list[Product]:
        like_query = f"%{query}%"

        rows = self.db.execute("SELECT * FROM inventory "
                               "WHERE name LIKE ? OR description LIKE ? "
                               "ORDER BY name",
                               (like_query, like_query))

        return [Product.from_row(row) for row in rows]













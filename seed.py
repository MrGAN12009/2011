from __future__ import annotations

import argparse
import random
from pydoc import describe
from typing import List

from inventory.db_manager import DatabaseManager
from inventory.product import Product
from inventory.repository import ProductManager

ADJECTIVES = [
    "Ультра", "Премиум", "Профессиональный", "Компактный", "Бюджетный", "Беспроводной",
]
ITEMS = [
    "набор инструментов", "дисплей", "гарнитура", "проектор", "брендовый аксессуар",
    "смарт-колонка", "оперативная память", "SSD", "внешний накопитель", "адаптер",
]
DESCRIPTIONS = [
    "Надежный выбор для ежедневного использования.",
    "Оптимальное сочетание цены и качества.",
    "Тестовый товар из автоматической выборки.",
    "Отличный вариант для подарка.",
    "Поддерживается на всех платформах.",
]


def _generate_random_product(index: int) -> Product:
    name = f"{random.choice(ADJECTIVES)} {random.choice(ITEMS)} #{index+1}"
    price = round(random.uniform(10.0, 450.0), 2)
    quantity = random.randint(1, 10)
    description = random.choice(DESCRIPTIONS)
    print(f"Товар #{index} добавлен!")
    return Product(name, price, quantity, description)

def _seed_products(count: int) -> List[Product]:
    return [_generate_random_product(i) for i in range(count)]

def seed_database(count: int = 10) -> None:
    manager = DatabaseManager()
    repo = ProductManager(manager)

    try:
        manager.execute("DELETE FROM inventory;")
        products = _seed_products(count)
        for product in products:
            repo.add_product(product)
        print(f"В базу добавлено: {len(products)} товаров.")
    finally:
        manager.close()

def main() -> None:
    parser = argparse.ArgumentParser(description="Генерирует случанйю демо базу товаров.")
    parser.add_argument("--count", type=int, default=10, help="Количество записей.")
    args = parser.parse_args()
    seed_database(args.count)

if __name__ == "__main__":
    main()



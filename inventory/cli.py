"""CLI for inventory management"""
import argparse
from collections.abc import Sequence

from .product import Product
from .repository import ProductManager


def _print_products(products: list[Product]) -> None:
    print(f"{len(products)} найдено:")
    for product in products:
        description = f" - {product.description}" if product.description else ""
        print(f"[{product.id}] {product.name} | Цена: {product.price} | Кол-во: {product.quantity} | {description}")


class InventoryCLI:
    """CLI for inventory management"""
    def __init__(self, repository: ProductManager) -> None:
        self.repository = repository
        self.parser = argparse.ArgumentParser(description='CLI для управления товарами.')
        self._configure_subcommands()


    def _configure_subcommands(self):
        subparser = self.parser.add_subparsers(dest='command')

        subparser.add_parser("list", help="Показать все товары.")

        add_parser = subparser.add_parser("add", help="Добавление нового товара.")
        add_parser.add_argument("--name", required=True, help="Название товара.")
        add_parser.add_argument("--price", type=float, required=True, help="Стоимость товара.")
        add_parser.add_argument("--quantity", type=int, required=True, help="Количество.")
        add_parser.add_argument("--description", help="Описание.")

        update_parser = subparser.add_parser("update", help="Обновление товара по ID.")
        update_parser.add_argument("--id", type=int, required=True, help="ID товара")
        update_parser.add_argument("--name", required=True, help="Название товара/новое название.")
        update_parser.add_argument("--price", type=float, required=True, help="Новая цена.")
        update_parser.add_argument("--quantity", type=int, required=True, help="Обновлённое количество.")
        update_parser.add_argument("--description", required=True, help="Описание/новое описание.")

        delete_parser = subparser.add_parser("delete", help="Удаление товара по ID.")
        delete_parser.add_argument("--id", type=int, required=True, help="ID товара")

        search_parser = subparser.add_parser("search", help="Поиск товара по ключевой фразе.")
        search_parser.add_argument("--query", required=True, help="Строка поиска.")

    def run(self, args: Sequence[str] | None = None) -> int:
        parser = self.parser.parse_args(args=args)
        command = parser.command
        if command == "list":
            self._handle_list()
        elif command == "add":
            self._handle_add(parser)
        elif command == "update":
            self._handle_update(parser)
        elif command == "delete":
            self._handle_delete(parser)
        elif command == "search":
            self._handle_search(parser)
        else:
            self.parser.print_help()
            return 1
        return 0

    def _handle_list(self) -> None:
        products = self.repository.list_products()
        if products:
            _print_products(products)
        else:
            print("Список пуст!")

    def _handle_add(self, parsed: argparse.Namespace) -> None:
        product = Product(
            name=parsed.name,
            price=parsed.price,
            quantity=parsed.quantity,
            description=parsed.description
        )
        saved = self.repository.add_product(product)
        print(f"Товар сохранён #{saved.id}: {saved.name}")

    def _handle_update(self, parsed: argparse.Namespace) -> None:
        product = Product(
            id=parsed.id,
            name=parsed.name,
            price=parsed.price,
            quantity=parsed.quantity,
            description=parsed.description
        )
        success = self.repository.update_product(product)
        message = "Обновлён" if success else "Товар не найден"
        print(f"{message}: {product.id}")

    def _handle_delete(self, parsed: argparse.Namespace) -> None:
        success = self.repository.delete_product(parsed.id)
        message = "Удалён" if success else "Товар не найден"
        print(f"{message}: {parsed.id}")

    def _handle_search(self, parsed: argparse.Namespace) -> None:
        products = self.repository.search_product(parsed.query)
        if products:
            _print_products(products)
        else:
            print(f"Товаров по даному описанию не было найдено.")













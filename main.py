from inventory.cli import InventoryCLI
from inventory.db_manager import DatabaseManager
from inventory.repository import ProductManager

def main() -> None:
    database_manager = DatabaseManager()
    repo = ProductManager(database_manager)

    try:
        cli = InventoryCLI(repo)
        cli.run()
    finally:
        database_manager.close()

if __name__ == '__main__':
    main()
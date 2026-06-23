# Author: Ahmet Aksoy
# Date: 22.05.2026
# Python3.12 Ubuntu 24.04

"""
Advanced SQLite Database Management Example
Demonstrates secure relational CRUD procedures, automated transaction management 
via context utilities, and strict query parameterization to block SQL Injection.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Generator


class DatabaseManager:
    """Manages the lifecycle and connection configurations for SQLite."""
    
    def __init__(self, db_name: str = "inventory.db") -> None:
        # Changed default target to a local file database to persist tables 
        # seamlessly across sequential context blocks.
        self.db_name = db_name

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager that guarantees connection safety, auto-commits 
        successful transactions, and auto-rolls back if exceptions hit.
        """
        conn = sqlite3.connect(self.db_name)
        # Return rows as dictionary-like objects instead of flat tuples
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[Database Error] Transaction aborted & rolled back: {e}")
            raise e
        finally:
            conn.close()


def initialize_database(db: DatabaseManager) -> None:
    """Creates the structural schema tables required for the application."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS inventory_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        quantity INTEGER DEFAULT 0,
        price REAL NOT NULL
    );
    """
    with db.connection() as conn:
        conn.execute(create_table_query)
    print("Database schema tables initialized successfully.")


# =====================================================================
# SECURE CRUD IMPLEMENTATIONS (Using Parameterized Queries)
# =====================================================================

def create_item(db: DatabaseManager, sku: str, name: str, qty: int, price: float) -> bool:
    """Inserts a new product track safely using safe variable tuple binding."""
    query = "INSERT INTO inventory_items (sku, name, quantity, price) VALUES (?, ?, ?, ?);"
    try:
        with db.connection() as conn:
            conn.execute(query, (sku, name, qty, price))
        return True
    except sqlite3.IntegrityError:
        print(f"[Warning] Failed to insert: SKU '{sku}' already exists.")
        return False


def read_all_items(db: DatabaseManager) -> list[sqlite3.Row]:
    """Retrieves all rows out of the asset catalog."""
    query = "SELECT id, sku, name, quantity, price FROM inventory_items;"
    with db.connection() as conn:
        cursor = conn.execute(query)
        return cursor.fetchall()


def update_item_stock(db: DatabaseManager, sku: str, new_qty: int) -> bool:
    """Updates stock metrics safely based on specific matching SKUs."""
    query = "UPDATE inventory_items SET quantity = ? WHERE sku = ?;"
    with db.connection() as conn:
        cursor = conn.execute(query, (new_qty, sku))
        return cursor.rowcount > 0


def delete_item(db: DatabaseManager, sku: str) -> bool:
    """Removes a product row completely from the catalog data tables."""
    query = "DELETE FROM inventory_items WHERE sku = ?;"
    with db.connection() as conn:
        cursor = conn.execute(query, (sku,))
        return cursor.rowcount > 0


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Advanced SQLite Transaction Engine Started ---\n")

    db_filename = "inventory.db"
    
    # Clean up any leftover database file from previous broken runs
    if os.path.exists(db_filename):
        os.remove(db_filename)

    # Instantiate manager targeting our local file
    db_manager = DatabaseManager(db_filename)
    initialize_database(db_manager)
    print("-" * 55)

    print("=== 1. Populating Data (Create) ===")
    create_item(db_manager, "SKU-MECH-01", "Mechanical Keyboard", 45, 89.99)
    create_item(db_manager, "SKU-MOUS-02", "Ergonomic Wireless Mouse", 120, 49.50)
    # Attempting a duplicate SKU transaction to test integrity constraints
    create_item(db_manager, "SKU-MECH-01", "Duplicate Keyboard Entry", 10, 15.00)
    print("-" * 55)

    print("\n=== 2. Fetching Catalog Inventory (Read) ===")
    items = read_all_items(db_manager)
    for row in items:
        print(f"Item #{row['id']} | SKU: {row['sku']} | {row['name']} | Stock: {row['quantity']} | Price: ${row['price']:.2f}")
    print("-" * 55)

    print("\n=== 3. Adjusting Asset Configurations (Update) ===")
    if update_item_stock(db_manager, "SKU-MECH-01", 50):
        print("Stock updated successfully for item 'SKU-MECH-01'.")
    print("-" * 55)

    print("\n=== 4. Deleting Records (Delete) ===")
    if delete_item(db_manager, "SKU-MOUS-02"):
        print("Item 'SKU-MOUS-02' removed from the active database system.")
    print("-" * 55)

    print("\n=== Final Active Database State ===")
    remaining_items = read_all_items(db_manager)
    for row in remaining_items:
        print(f"Remaining -> {row['name']} | Current Stock: {row['quantity']}")
        
    # Clean up file after run execution ends cleanly
    if os.path.exists(db_filename):
        os.remove(db_filename)

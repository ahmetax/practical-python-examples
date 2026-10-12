# Project 29: SQLite CRUD with a Transaction Context Manager

A small inventory example built on the standard `sqlite3` module. It shows:
- a `@contextmanager` that opens a connection, commits on success, rolls back on an exception and always closes the connection,
- `sqlite3.Row` as `row_factory`, so columns can be read by name (`row['sku']`),
- parameterized queries (`?` placeholders) for every value, which keeps user input out of the SQL text and prevents SQL injection,
- a `UNIQUE` constraint on `sku` that turns a duplicate insert into `sqlite3.IntegrityError`.

## How It Works
- `DatabaseManager.connection()` opens a **new** connection for every `with` block. This is why the demo uses a file (`inventory.db`): with `":memory:"` each block would get its own empty database, and the second block would fail with `no such table: inventory_items`.
- `initialize_database()` creates the `inventory_items` table (`id`, `sku`, `name`, `quantity`, `price`).
- `create_item()`, `read_all_items()`, `update_item_stock()` and `delete_item()` each run one statement inside their own `with db.connection()` block. `create_item()` catches `IntegrityError` and returns `False`.
- The script deletes `inventory.db` at start and at the end, so it leaves no file behind after a normal run. If it stops with an error, `inventory.db` stays in the current directory.

The manager is not thread-safe in any special way; it just opens a separate connection per block.

## Project Structure
```text
29_sqlite_advanced/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (the `list[sqlite3.Row]` type hint needs 3.9). Tested on Python 3.12.3 with SQLite 3.45.1 (Ubuntu 24.04) and on the `python:3.12-slim` Docker image (Python 3.12.15, SQLite 3.46.1); the output was identical.
- No third-party packages.

## Running
```bash
python3 main.py
```
The script creates and then deletes `inventory.db` in the current directory.

## Sample Output (Python 3.12.3)
```text
--- Advanced SQLite Transaction Engine Started ---

Database schema tables initialized successfully.
-------------------------------------------------------
=== 1. Populating Data (Create) ===
[Database Error] Transaction aborted & rolled back: UNIQUE constraint failed: inventory_items.sku
[Warning] Failed to insert: SKU 'SKU-MECH-01' already exists.
-------------------------------------------------------

=== 2. Fetching Catalog Inventory (Read) ===
Item #1 | SKU: SKU-MECH-01 | Mechanical Keyboard | Stock: 45 | Price: $89.99
Item #2 | SKU: SKU-MOUS-02 | Ergonomic Wireless Mouse | Stock: 120 | Price: $49.50
-------------------------------------------------------

=== 3. Adjusting Asset Configurations (Update) ===
Stock updated successfully for item 'SKU-MECH-01'.
-------------------------------------------------------

=== 4. Deleting Records (Delete) ===
Item 'SKU-MOUS-02' removed from the active database system.
-------------------------------------------------------

=== Final Active Database State ===
Remaining -> Mechanical Keyboard | Current Stock: 50
```

## Note: Rollback and the Turkish Locale
In its default (legacy) transaction mode, Python's `sqlite3` opens a transaction implicitly before `INSERT`, `UPDATE`, `DELETE` and `REPLACE`. Up to Python 3.12 it detects these keywords with a C-level case-insensitive comparison that depends on the locale. With a Turkish locale (`LC_CTYPE=tr_TR.UTF-8`), `I` does not lowercase to `i`, so a statement written as `INSERT` is not recognized: no transaction is opened, the row is committed immediately, and a later `rollback()` cannot undo it. `insert` in lowercase, `UPDATE` and `DELETE` are not affected.

The demo itself is not affected, because every block runs a single statement. It matters as soon as you put two statements in one `with db.connection()` block: a test that inserted one row and then a duplicate SKU in the same block gave these results:

| Environment | `in_transaction` after `INSERT` | Rows after the failed block |
|-------------|----------------------------------|-----------------------------|
| Python 3.12.3, `LC_CTYPE=tr_TR.UTF-8` | `False` | 2 (first insert kept, although `rolled back` is printed) |
| Python 3.12.3, `LC_ALL=C.UTF-8` | `True` | 1 (rolled back) |
| Docker Python 3.12.15, `tr_TR.UTF-8` | `False` | 2 |
| Docker Python 3.13.16, `tr_TR.UTF-8` | `True` | (not affected) |

Fixes on Python 3.12: connect with `sqlite3.connect(..., autocommit=False)` (new in 3.12; a transaction is always open and `commit()`/`rollback()` behave as expected), start the transaction yourself with `conn.execute("BEGIN")`, or run the program with a non-Turkish `LC_CTYPE`. Python 3.13 no longer has the problem.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/25/python-ve-sqlite-guvenli-ve-profesyonel-veritabani-yonetimi/
- `sqlite3` documentation: https://docs.python.org/3/library/sqlite3.html
- Transaction control in `sqlite3`: https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions

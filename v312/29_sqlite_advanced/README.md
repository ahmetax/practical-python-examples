# Project 29: Advanced SQLite Database Management

A production-grade sample project demonstrating robust relational database interactions using Python's native `sqlite3` driver. This implementation covers custom transactional context management, explicit entity constraints, dict-like record decoding, and strict SQL Injection prevention through parameterization.

## Architectural Goal
The application provides a resilient, thread-safe persistence management module tailored for local file storage or fast in-memory staging caches. It automates database connection workflows, ensuring transactions commit automatically on success and rollback cleanly when operational anomalies or integrity constraint errors occur.

## Project Structure
```text
29_sqlite_advanced/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Set up an isolated directory for this specific project inside your repository workspace:

```bash
mkdir 29_sqlite_advanced
cd 29_sqlite_advanced

### Step 2: Formulate the Persistence Layer
Create a file named main.py. Build your relational wrapper system step-by-step:

Build a Connection Context Utility: Leverage @contextmanager from the contextlib library to manage database lifecycles safely. Inside your generator context block, establish connections using sqlite3.connect(). Set conn.row_factory = sqlite3.Row to convert flat index tuples into readable, dictionary-like key mapping instances.

Handle Transactions and Errors: Implement an explicit try/except/finally sequence inside the manager. Use a yield statement to pass database connections to your operations. If operations run successfully, call conn.commit(). If an exception occurs, catch it and force a conn.rollback() to preserve database integrity before closing connections in the finally block.

Draft the Base Database Schema: Define an initialization function (e.g., initialize_database(db)) that builds a core reference table with auto-incrementing primary keys, unique SKU tags, strings, integer tallies, and precision float fields.

Implement Secure Parameterized CRUD Blocks: Create dedicated data pipeline methods (create_item, read_all_items, update_item_stock, delete_item). Never string-interpolate raw variables into SQL lines. Instead, pass clean query statements using placeholder symbols (?) and pass your variables inside matching argument tuples. This ensures the database engine escapes input data safely and blocks malicious SQL injection strings.

### Step 3: Run and Verify
Configure a quick trial run inside your execution block (if __name__ == "__main__":). Initialize an in-memory database using the special filename ":memory:", invoke creation procedures, trigger record variations, intercept constraint limits, and log results out to the console. Run the script:

```bash
python main.py



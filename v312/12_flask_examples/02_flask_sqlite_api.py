"""
Author: Ahmet Aksoy
Date: 2026-04-22
Python 3.12 - Ubuntu 24.04

Description:
    A simple REST API built with Python + Flask + SQLite.

    Python handles application startup, database initialization,
    and Flask server configuration. Route handlers are defined
    in flask_sqlite_helpers.py.

    The API uses the library.db database created by sqlite_file.py.
    If the database does not exist, it is created and seeded automatically.

    Endpoints:
      GET    /api/books              -> list all books
      GET    /api/books/<id>         -> get one book
      GET    /api/books?genre=Sci-Fi -> filter by genre
      GET    /api/authors            -> list all authors
      POST   /api/books              -> add a new book
      PUT    /api/books/<id>         -> update a book
      DELETE /api/books/<id>         -> delete a book
      GET    /api/stats              -> summary statistics

    Run:
      python 02_flask_sqlite_api.py
    Test:
      curl http://localhost:8117/api/books
      curl http://localhost:8117/api/stats
      curl http://localhost:8117/api/books?genre=Sci-Fi

Requirements:
    pip install flask
"""

import flask, sqlite3, os
import flask_sqlite_helpers

def ensure_db():
    """
    Create and seed the database if it does not exist yet.
    Safe to call on every startup — uses INSERT OR IGNORE.
    """
    db_path = os.getcwd() + "/library.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    _ = conn.execute("PRAGMA journal_mode=WAL")

    # Authors table
    _ = conn.execute(
        "CREATE TABLE IF NOT EXISTS authors ("
        "  id    INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  name  TEXT    NOT NULL UNIQUE"
        ")"
    )

    # Books table
    _ = conn.execute(
        "CREATE TABLE IF NOT EXISTS books ("
        "  id        INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  title     TEXT    NOT NULL,"
        "  author_id INTEGER NOT NULL,"
        "  year      INTEGER NOT NULL,"
        "  genre     TEXT    NOT NULL,"
        "  rating    REAL    DEFAULT 0.0,"
        "  FOREIGN KEY (author_id) REFERENCES authors(id)"
        ")"
    )
    conn.commit()

    # Seed authors
    make_t1 = lambda a: (a,)
    authors = list()
    authors.append(make_t1("George Orwell"))
    authors.append(make_t1("Frank Herbert"))
    authors.append(make_t1("Isaac Asimov"))
    authors.append(make_t1("Ursula K. Le Guin"))
    authors.append(make_t1("Philip K. Dick"))
    _ = conn.executemany(
        "INSERT OR IGNORE INTO authors (name) VALUES (?)", authors
    )
    conn.commit()

    # Helper to get author id
    get_id = lambda conn, name: conn.execute('SELECT id FROM authors WHERE name=?', (name,)).fetchone()[0]

    # Seed books
    make_t5 = lambda a,b,c,d,e: (a,b,c,d,e)
    books = list()

    orwell_id  = get_id(conn, "George Orwell")
    herbert_id = get_id(conn, "Frank Herbert")
    asimov_id  = get_id(conn, "Isaac Asimov")
    leguin_id  = get_id(conn, "Ursula K. Le Guin")
    dick_id    = get_id(conn, "Philip K. Dick")

    books.append(make_t5("1984",                       orwell_id,  1949, "Dystopia",   4.7))
    books.append(make_t5("Animal Farm",                orwell_id,  1945, "Satire",     4.5))
    books.append(make_t5("Dune",                       herbert_id, 1965, "Sci-Fi",     4.8))
    books.append(make_t5("Dune Messiah",               herbert_id, 1969, "Sci-Fi",     4.4))
    books.append(make_t5("Foundation",                 asimov_id,  1951, "Sci-Fi",     4.6))
    books.append(make_t5("I, Robot",                   asimov_id,  1950, "Sci-Fi",     4.5))
    books.append(make_t5("The Left Hand of Darkness",  leguin_id,  1969, "Sci-Fi",     4.6))
    books.append(make_t5("The Dispossessed",           leguin_id,  1974, "Sci-Fi",     4.5))
    books.append(make_t5("Do Androids Dream",          dick_id,    1968, "Sci-Fi",     4.4))
    books.append(make_t5("The Man in the High Castle", dick_id,    1962, "Alt-History", 4.2))

    _ = conn.executemany(
        "INSERT OR IGNORE INTO books (title, author_id, year, genre, rating)"
        " VALUES (?, ?, ?, ?, ?)",
        books
    )
    conn.commit()
    conn.close()
    print("✓ Database ready: " + db_path)


def main():

    # Ensure database exists and is seeded
    ensure_db()

    # Create Flask app
    app = flask.Flask("__main__")

    flask_sqlite_helpers.setup_routes(app)

    print("=" * 50)
    print("  Flask + SQLite API starting on port 8117")
    print("  Endpoints:")
    print("    GET  /api/books")
    print("    GET  /api/books/<id>")
    print("    GET  /api/books?genre=Sci-Fi")
    print("    GET  /api/authors")
    print("    POST /api/books")
    print("    PUT  /api/books/<id>")
    print("    DELETE /api/books/<id>")
    print("    GET  /api/stats")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    _ = app.run(host="0.0.0.0", port=8117, debug=False)

main()
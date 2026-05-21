# 🚀 Flask Examples with Python

This project contains two practical Flask applications demonstrating different levels of complexity: a minimal "Hello World" server and a fully functional REST API backed by SQLite. These examples are perfect for learning Flask fundamentals and building web services with database integration.

---

## 📁 Project Structure

```text
12_flask_examples/
├── 01_flask_hello.py           # Minimal Flask server
├── flask_helpers.py           # Routes for the minimal app
├── 02_flask_sqlite_api.py     # REST API with SQLite database
├── flask_sqlite_helpers.py    # API route handlers and DB logic
├── library.db                 # SQLite database (auto-created)
└── flask_sqlite_api_guide.md  # Additional API documentation
```

---

## 🛠️ Step-by-Step Implementation Guide

### Prerequisites
Install Flask:
```bash
pip install flask
```

---

## Part 1: Minimal Flask Server (`01_flask_hello.py`)

**Goal**: Create a simple Flask web server that responds with text and JSON.

### Step 1: Create the Helper Module (`flask_helpers.py`)
This file contains the route definitions, keeping the main app clean.

1. Import `jsonify` from `flask`.
2. Define a function `setup_routes(app)` that takes the Flask app as a parameter.
3. **Define the index route**:
   - Use `@app.route('/')` decorator.
   - Return the string `'Hello from Python + Flask!'`.
4. **Define the ping route**:
   - Use `@app.route('/ping')` decorator.
   - Use `jsonify({'status': 'ok', 'message': 'Python + Flask is running!'})` to return JSON.
5. Save the file.

### Step 2: Create the Main Application (`01_flask_hello.py`)
This file initializes and runs the Flask server.

1. Import `flask` and the `flask_helpers` module.
2. Define a `main()` function.
3. Create a Flask application: `app = flask.Flask("__main__")`.
4. Call `flask_helpers.setup_routes(app)` to register routes.
5. Print startup information (URL, port).
6. Run the app: `app.run(host="0.0.0.0", port=8117, debug=False)`.
7. Call `main()` at the end of the file.

### Step 3: Run the Server
```bash
python 01_flask_hello.py
```
- Visit `http://localhost:8117` to see the hello message.
- Visit `http://localhost:8117/ping` to see the JSON response.

---

## Part 2: REST API with SQLite (`02_flask_sqlite_api.py`)

**Goal**: Build a complete REST API for managing a library of books and authors, with full CRUD operations and statistics.

### Step 1: Create the Database Setup (`02_flask_sqlite_api.py`)
This file ensures the database exists and is seeded with sample data.

1. Import `flask`, `sqlite3`, and `os`. Import `flask_sqlite_helpers`.
2. Define `ensure_db()` function:
   - Set `db_path` to `library.db` in the current directory.
   - Connect to SQLite and set `row_factory = sqlite3.Row` for column access.
   - Execute `PRAGMA journal_mode=WAL` for better concurrency.
   - **Create `authors` table**: id (PK), name (TEXT, UNIQUE).
   - **Create `books` table**: id (PK), title, author_id (FK), year, genre, rating.
   - **Seed authors**: Insert "George Orwell", "Frank Herbert", "Isaac Asimov", etc. using `INSERT OR IGNORE`.
   - **Seed books**: Get author IDs using a helper, then insert book records with titles like "1984", "Dune", "Foundation", etc.
   - Commit and close the connection.
3. Define `main()` function:
   - Call `ensure_db()` to initialize the DB.
   - Create Flask app: `app = flask.Flask("__main__")`.
   - Call `flask_sqlite_helpers.setup_routes(app)` to register API routes.
   - Print API endpoint information.
   - Run the app on port 8117.

### Step 2: Create the API Helpers (`flask_sqlite_helpers.py`)
This file contains all the route handlers and database logic.

1. Import `sqlite3`, `Flask`, `jsonify`, and `request`.
2. Define `DB_PATH = "library.db"`.
3. **Database Helper Functions**:
   - `get_conn()`: Returns a sqlite3 connection with `row_factory = sqlite3.Row`.
   - `row_to_dict(row)`: Converts a sqlite3 Row to a Python dictionary.
4. **Define `setup_routes(app)`** and implement the following endpoints:

   #### GET `/api/books`
   - Accept optional query param `?genre=Sci-Fi`.
   - If genre is provided, filter by genre; otherwise, return all books.
   - Join `books` and `authors` tables to get author name.
   - Return JSON list of books.

   #### GET `/api/books/<id>`
   - Fetch a single book by ID.
   - Return 404 if not found, otherwise return JSON book object.

   #### GET `/api/authors`
   - Select all authors with a LEFT JOIN to count their books.
   - Group by author and order by book count descending.
   - Return JSON list of authors with book counts.

   #### POST `/api/books`
   - Expect JSON body: `{"title": "...", "author": "...", "year": 1984, "genre": "...", "rating": 4.5}`.
   - Validate required fields.
   - **Author Logic**: Check if author exists; if not, insert them.
   - Insert the new book and return 201 Created with the new ID.

   #### PUT `/api/books/<id>`
   - Expect JSON body with any subset of fields: title, year, genre, rating.
   - Validate allowed fields.
   - Build dynamic SQL: `UPDATE books SET field1=?, field2=? WHERE id=?`.
   - Return success message or 404 if not found.

   #### DELETE `/api/books/<id>`
   - Delete the book by ID.
   - Return success message or 404 if not found.

   #### GET `/api/stats`
   - Calculate: total number of books, average rating.
   - Group by genre to get count per genre.
   - Return JSON with summary statistics.

5. Save the file.

### Step 3: Run the API Server
```bash
python 02_flask_sqlite_api.py
```

### Step 4: Test the API
You can test using `curl`:

```bash
# Get all books
curl http://localhost:8117/api/books

# Get books filtered by genre
curl "http://localhost:8117/api/books?genre=Sci-Fi"

# Get a single book
curl http://localhost:8117/api/books/1

# Get all authors
curl http://localhost:8117/api/authors

# Get statistics
curl http://localhost:8117/api/stats

# Add a new book
curl -X POST http://localhost:8117/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "New Author", "year": 2024, "genre": "Fiction", "rating": 4.0}'

# Update a book
curl -X PUT http://localhost:8117/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"rating": 4.8}'

# Delete a book
curl -X DELETE http://localhost:8117/api/books/1
```

---

## 📖 Key Concepts Demonstrated

- **Flask App Initialization**: Creating a Flask app and running the development server.
- **Route Definition**: Using decorators (`@app.route`) to map URLs to Python functions.
- **JSON Responses**: Using `jsonify` to return JSON-formatted data.
- **SQLite Integration**: Connecting to a database, executing queries, and handling rows.
- **Database Seeding**: Automatically creating tables and inserting sample data on startup.
- **REST API Design**: Following REST principles (GET, POST, PUT, DELETE) for CRUD operations.
- **Dynamic SQL**: Building SQL queries dynamically for partial updates (PUT).
- **Error Handling**: Returning appropriate HTTP status codes (404, 400, 201).

---

## 🏃 Running Both Examples

1. Navigate to the project folder.
2. Run the minimal Flask server:
   ```bash
   python 01_flask_hello.py
   ```
   Then open `http://localhost:8117` in your browser.

3. Stop the server (Ctrl+C) and run the REST API:
   ```bash
   python 02_flask_sqlite_api.py
   ```
   Test the endpoints using curl or a tool like Postman.

---

## 🔧 Extension Ideas

- Add **authentication** to the API using Bearer tokens.
- Add **pagination** to the `/api/books` endpoint.
- Create a **frontend** using HTML/JS to consume this API.
- Add **search functionality** with SQL `LIKE` queries.
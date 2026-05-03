"""
Author: Ahmet Aksoy
Date: 2026-05-03
Python version: 3.12 | Ubuntu

Description:
    A To-Do List web application built with Python + Flask + SQLite.

    Python handles application startup and database initialization.
    Flask route handlers and Jinja2 templates are managed on the
    Python side via todo_helpers.py and the todo_templates/ directory.

    Features:
      - Add tasks with priority (high / medium / low)
      - Mark tasks as done / undone
      - Edit task title and priority
      - Delete individual tasks
      - Clear all completed tasks
      - Filter by: all / pending / done / high priority
      - Live stats (total, pending, done, high priority)

    File structure:
      todo_app.py           <- this file
      todo_helpers.py       <- Flask routes
      todo.db               <- SQLite database (auto-created)
      todo_templates/
        base.html           <- shared layout
        index.html          <- task list
        edit.html           <- edit form

    Run:
      python todo_app.py
    Then open http://localhost:8117 in your browser.

Requirements:
    pip install flask
"""

import flask
import sqlite3
import os


def ensure_db():
    """Create the tasks table if it does not exist."""
    db_path = os.getcwd() + "/todo.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tasks ("
        "  id         INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  title      TEXT    NOT NULL,"
        "  priority   TEXT    NOT NULL DEFAULT 'medium',"
        "  done       INTEGER NOT NULL DEFAULT 0,"
        "  created_at TEXT    NOT NULL"
        ")"
    )
    conn.commit()
    conn.close()
    print("✓ Database ready: " + db_path)


if __name__ == "__main__":
    ensure_db()

    app = flask.Flask(
        __name__,
        template_folder="todo_templates"
    )

    # Secret key required for flash messages
    app.secret_key = "mojo-todo-secret-key"

    # Register routes
    import todo_helpers
    todo_helpers.setup_routes(app)

    print("=" * 45)
    print("  To-Do App starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 45)

    app.run(host="0.0.0.0", port=8117, debug=False)
"""
Author: Ahmet Aksoy
Date: 2026-04-17
Python 3.12 - Ubuntu 24.04

Description:
    Blog / Content Management System built with Flask + SQLite.

    Python handles application startup and database initialization.
    Flask routes and authentication logic are in blog_helpers.py.
    HTML templates are in the blog_templates/ directory.

    Authentication features:
      - User registration with input validation
      - Password hashing with bcrypt
      - Login / logout with Flask session
      - login_required decorator for protected routes
      - Change password (verifies current password first)
      - Delete account (cascades to posts)

    Blog features:
      - Public: home page (all posts), single post view
      - Protected: dashboard, new post, edit post, delete post
      - Authors can only edit/delete their own posts

    File structure:
      blog_app.py              <- this file
      blog_helpers.py            <- Flask routes + auth logic
      blog.db                    <- SQLite database (auto-created)
      blog_templates/
        base.html
        index.html               <- public home
        post.html                <- public single post
        login.html
        register.html
        dashboard.html           <- protected
        post_form.html           <- protected (new + edit)
        profile.html             <- protected

    Run:
      python blog_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask bcrypt sqlite3
"""

import os
import sqlite3
import flask

def ensure_db():
    """Create users and posts tables if they do not exist."""
    db_path = os.getcwd() + "/blog.db"
    conn = sqlite3.connect(db_path)

    _ = conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "  id         INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  username   TEXT    NOT NULL UNIQUE,"
        "  email      TEXT    NOT NULL UNIQUE,"
        "  password   TEXT    NOT NULL,"
        "  created_at TEXT    NOT NULL"
        ")"
    )

    _ = conn.execute(
        "CREATE TABLE IF NOT EXISTS posts ("
        "  id         INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  user_id    INTEGER NOT NULL,"
        "  title      TEXT    NOT NULL,"
        "  body       TEXT    NOT NULL,"
        "  created_at TEXT    NOT NULL,"
        "  updated_at TEXT    NOT NULL,"
        "  FOREIGN KEY (user_id) REFERENCES users(id)"
        ")"
    )

    conn.commit()
    conn.close()
    print("✓ Database ready: " + db_path)

import blog_helpers

def main():

    ensure_db()

    app= flask.Flask(
        str("__main__"),
        template_folder=str("blog_templates")
    )

    app.secret_key = str("python-blog-secret-key-change-in-production")

    
    blog_helpers.setup_routes(app)

    print("=" * 50)
    print("  PythonBlog starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    _ = app.run(host="0.0.0.0", port=8117, debug=False)

main()    

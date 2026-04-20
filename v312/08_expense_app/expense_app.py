"""
Author: Ahmet Aksoy
Date: 2026-04-19
Python 3.12 - Ubuntu 24.04

Description:
    Expense Tracker web application built with Python + Flask + SQLite.

    Mojo handles application startup and database initialization.
    Flask routes are defined in expense_helpers.py.
    HTML templates are in the expense_templates/ directory.

    Features:
      - Add expenses with description, amount, category and date
      - Dashboard with total / monthly / weekly spending stats
      - Doughnut chart: spending by category
      - Delete individual expenses
      - Monthly report with:
          - Daily spending bar chart (Chart.js)
          - Category breakdown table
          - Month navigation (prev / next)
          - Daily average and top category

    File structure:
      expense_app.py             <- this file
      expense_helpers.py         <- Flask routes
      expense.db                 <- SQLite database (auto-created)
      expense_templates/
        base.html
        index.html               <- dashboard
        add.html                 <- add expense form
        report.html              <- monthly report

    Run:
      python expense_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask
"""

import os
import flask
import sqlite3

def ensure_db():
    """Create the expenses table if it does not exist."""
    db_path = os.getcwd() + "/expense.db"
    conn = sqlite3.connect(db_path)
    _ = conn.execute(
        "CREATE TABLE IF NOT EXISTS expenses ("
        "  id          INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  description TEXT    NOT NULL,"
        "  amount      REAL    NOT NULL,"
        "  category    TEXT    NOT NULL DEFAULT 'Other',"
        "  date        TEXT    NOT NULL"
        ")"
    )
    conn.commit()
    conn.close()
    print("✓ Database ready: " + db_path)


def main():
    ensure_db()

    app = flask.Flask(
        "__main__",
        template_folder="expense_templates"
    )

    app.secret_key = "python-expense-secret-key"

    import expense_helpers
    
    expense_helpers.setup_routes(app)

    print("=" * 48)
    print("  Expense Tracker starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 48)

    _ = app.run(host="0.0.0.0", port=8117, debug=False)

# call main()
main()
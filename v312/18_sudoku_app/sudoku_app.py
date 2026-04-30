"""
Author: Ahmet Aksoy
Author: Ahmet Aksoy
Date: 2026-04-30
Python 3.12 - Ubuntu 24.04

Description:
    Sudoku Creator / Solver web application.
    Built with Python + Flask.

    Features:
      - Puzzle generation (Easy / Medium / Hard)
      - Optional random seed for reproducible puzzles
      - Python backtracking solver with step recording
      - Python backtracking solver via subprocess
      - Step-by-step animation with play/pause/step controls
      - Variable animation speed
      - User input via numpad or keyboard
      - Board validation (conflict detection)
      - Reset to given / Clear all

    File structure:
      sudoku_app.py         <- this file (Flask startup)
      sudoku_solver.py      <- Python solver (subprocess)
      sudoku_engine.py      <- Creator + Python solver
      sudoku_helpers.py     <- Flask routes
      sudoku_templates/
        base.html
        index.html

    Run:
      python sudoku_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask
"""

import flask
import sudoku_helpers

app = flask.Flask(__name__, template_folder="sudoku_templates")
app.secret_key = "python-sudoku-secret-key"

sudoku_helpers.setup_routes(app)

if __name__ == "__main__":
    print("=" * 50)
    print("  Sudoku App starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    app.run(host="0.0.0.0", port=8117, debug=False)

"""
Author: Ahmet Aksoy
Date: 2026-04-22
Python 3.12 - Ubuntu 24.04

Description:
    Minimal Flask web server started from Python.
    Tests whether Flask's application loop can be launched from Python.

    Endpoints:
      GET /          -> "Hello from Python + Flask!"
      GET /ping      -> JSON {"status": "ok"}

    Run:
      python flask_hello.py
    Then open http://localhost:8117 in your browser.
"""

import flask
import flask_helpers

def main():


    # Create Flask app
    app = flask.Flask("__main__")

    flask_helpers.setup_routes(app)

    print("=" * 45)
    print("  Flask server starting on port 8117")
    print("  http://localhost:8117")
    print("  http://localhost:8117/ping")
    print("  Press Ctrl+C to stop.")
    print("=" * 45)

    # Start the Flask development server
    _ = app.run(
        host="0.0.0.0",
        port=8117,
        debug=False
    )

main()
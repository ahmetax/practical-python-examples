"""
Author: Ahmet Aksoy
Date: 2026-04-17
Python 3.12 - Ubuntu 24.04

Description:
    Ollama Chat Web Application built with Python + Flask.

    Python handles application startup and Flask configuration.
    Ollama API calls and streaming are handled in ollama_helpers.py.

    Features:
      - Automatic model discovery (lists all installed Ollama models)
      - Streaming responses (tokens appear as generated)
      - Multi-turn conversation with history
      - System prompt configuration
      - Temperature and max token controls
      - Session stats (message count, response time, tokens/sec)
      - Clear conversation

    Architecture:
      Browser  →  POST /chat (SSE stream)
               →  ollama_helpers.py
               →  Ollama API (localhost:11434)
               →  SSE tokens back to browser

    File structure:
      ollama_chat_app.py      <- this file
      ollama_helpers.py         <- Flask routes + Ollama API
      ollama_templates/
        base.html
        index.html              <- chat UI

    Run:
      1. Make sure Ollama is running: ollama serve
      2. Pull a model if needed: ollama pull llama3.2
      3. python ollama_chat_app.py
      4. Open http://localhost:8117

Requirements:
    pip install flask requests
"""

import flask
import ollama_helpers

def main():
    app = flask.Flask(
        "__main__",
        template_folder="ollama_templates"
    )
    app.secret_key = "mojo-ollama-secret-key"

    ollama_helpers.setup_routes(app)

    print("=" * 52)
    print("  Ollama Chat App starting on port 8117")
    print("  http://localhost:8117")
    print("  Make sure Ollama is running: ollama serve")
    print("  Press Ctrl+C to stop.")
    print("=" * 52)

    _ = app.run(host="0.0.0.0", port=8117, debug=False)

if __name__ == "__main__":
    main()
    
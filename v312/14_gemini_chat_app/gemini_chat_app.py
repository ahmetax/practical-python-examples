"""
Author: Ahmet Aksoy
Date: 2026-04-25
Python 3.12 - Ubuntu 24.04

Gemini Chat Web Application — Python + Flask + Google AI Studio
=============================================================

Features:
  - Google Gemini API (free tier, no credit card needed)
  - Streaming responses token by token
  - Multi-turn conversation with history
  - Tool calling: web search (Tavily) + crypto prices (CoinGecko)
  - System prompt, temperature, max token controls
  - Session stats (response time, tokens/sec)
  - Model selection (gemini-2.0-flash, gemini-1.5-flash, etc.)

File structure:
  gemini_chat_app.py    <- this file
  gemini_helpers.py       <- Flask routes + Gemini API
  .env                    <- API keys (never commit this)
  .env.example            <- template
  gemini_templates/
    base.html
    index.html

Setup:
  1. Get free API key: https://aistudio.google.com
  2. cp .env.example .env
  3. Add GEMINI_API_KEY and TAVILY_API_KEY to .env
  4. pip install flask requests
  5. mojo gemini_chat_app.mojo
  6. Open http://localhost:8118

Requirements:
  pip install flask requests
"""

import flask
import gemini_helpers

def main():
    app = flask.Flask(
        "__main__",
        template_folder="gemini_templates"
    )
    app.secret_key = "gemini-chat-secret-key"

    gemini_helpers.setup_routes(app)

    print("=" * 54)
    print("  Gemini Chat App starting on port 8118")
    print("  http://localhost:8118")
    print("  Press Ctrl+C to stop.")
    print("=" * 54)

    _ = app.run(host="0.0.0.0", port=8118, debug=False)

if __name__ == "__main__":
    main()
    
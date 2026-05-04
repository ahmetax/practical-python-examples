"""
Author: Ahmet Aksoy
Date: 2026-05-04
Python 3.12 | Ubuntu

Description:
    General-purpose Web Scraper built with Python + Flask + BeautifulSoup.

    scraper_app.py handles application startup and Flask configuration.
    Scraping logic and route handlers are in scraper_helpers.py.
    HTML templates are in the scraper_templates/ directory.

    Features:
      - Scrape any public URL
      - Selectable data types:
          Meta tags (title, description, og:*, charset...)
          Headings (h1-h6 with tag labels)
          Links (href + anchor text, absolute URLs)
          Images (src + alt, absolute URLs)
          Page text (cleaned, script/style removed)
          Tables (headers + rows)
      - Advanced options:
          Timeout, max links, max images, User-Agent selection
      - Results displayed inline with stats
      - Download results as JSON
      - Scrape history (in-memory, current session)
      - History view with re-open and download

    File structure:
      scraper_app.py             <- this file
      scraper_helpers.py         <- Flask routes + scraping logic
      scraper_templates/
        base.html
        index.html               <- scrape form
        result.html              <- scrape results
        history.html             <- past scrapes

    Run:
      python scraper_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask requests beautifulsoup4
"""

from flask import Flask
from scraper_helpers import setup_routes


def main():
    app = Flask(
        "__main__",
        template_folder="scraper_templates"
    )
    
    app.secret_key = "mojo-scraper-secret-key"
    
    setup_routes(app)
    
    print("=" * 50)
    print("  Web Scraper starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=8117, debug=False)


if __name__ == "__main__":
    main()

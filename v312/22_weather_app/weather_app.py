"""
Author: Ahmet Aksoy
Date: 2026-05-12
Python3.12 Ubuntu 24.04

Description:
    Weather App built with Python + Flask + OpenWeatherMap API.

    API calls and route handlers are in weather_helpers.py.
    HTML templates are in the weather_templates/ directory.

    Features:
      - Search any city worldwide
      - Current weather: temperature, feels like, humidity,
        wind speed, pressure, visibility, sunrise/sunset
      - 5-day forecast with daily min/max temperatures
      - Weather condition emoji icons
      - Recent searches (stored in session)

    File structure:
      weather_app.py           <- this file
      weather_helpers.py       <- Flask routes + API calls
      weather_templates/
        base.html
        index.html               <- search + current + forecast

    Run:
      python weather_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask requests
"""

from flask import Flask
import weather_helpers

def main():
    app = Flask(__name__, template_folder="weather_templates")
    app.secret_key = "python-weather-secret-key"

    weather_helpers.setup_routes(app)

    print("=" * 48)
    print("  Weather App starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 48)

    app.run(host="0.0.0.0", port=8117, debug=False)

if __name__ == "__main__":
    main()

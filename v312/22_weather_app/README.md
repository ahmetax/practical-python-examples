# 🌤️ Weather App - Python/Flask Edition

A lightweight, elegant weather application built with **Python** and **Flask**. This app allows users to search for any city worldwide to get real-time current weather data and a 5-day forecast using the **OpenWeatherMap API**.

## 🚀 Features
- **Global Search**: Get weather data for any city in the world.
- **Current Weather**: Displays temperature, feels-like temp, humidity, wind speed, pressure, visibility, and local sunrise/sunset times.
- **5-Day Forecast**: Aggregated daily min/max temperatures and conditions.
- **Visual Cues**: Weather conditions are represented by intuitive emoji icons.
- **Session History**: Keeps track of your most recent searches during the session.

---

## 📁 Project Structure
```text
weather_app/
├── .env                   # API Key storage (Secret)
├── weather_app.py         # Application entry point & Flask config
├── weather_helpers.py     # API logic and route handlers
└── weather_templates/      # HTML UI templates
    ├── base.html          # Shared layout
    └── index.html         # Main search and display page
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.12+ installed on your system.

### 2. Get an API Key
This app uses the OpenWeatherMap API.
1. Go to [openweathermap.org/api](https://openweathermap.org/api).
2. Sign up for a free account.
3. Generate an **API Key** (AppID) from your dashboard.

### 3. Installation
Clone the project and install the required dependencies:
```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install flask requests
```

### 4. Configuration
Create a file named `.env` in the root directory of the project and add your API key:
```text
OPENWEATHERMAP_API_KEY=your_api_key_here
```
You can copy the .env.example file .env and fill it with your actual API_KEY.
---

## 🏃 Running the App

Start the application by running:
```bash
python weather_app.py
```
Once started, open your browser and go to:
**`http://localhost:8117`**

---

## 📖 Technical Explanation

### `weather_app.py`
This is the **Entry Point**. It initializes the Flask application, sets the secret key for session management, and tells Flask where to find the HTML templates. It then calls `setup_routes` from the helper file to register the URL endpoints.

### `weather_helpers.py`
This file contains the **Business Logic**:
- **API Integration**: Uses the `requests` library to fetch data from OpenWeatherMap.
- **Data Processing**: 
    - `fetch_current()`: Cleans the raw JSON response into a simple dictionary. It also calculates local sunrise/sunset times based on the city's timezone offset.
    - `fetch_forecast()`: Processes 40 segments of 3-hour forecasts, grouping them by date to find the daily high, low, and most frequent weather condition.
- **Emoji Mapper**: A helper function maps OpenWeatherMap condition codes to specific emojis (e.g., `800` $\rightarrow$ ☀️).
- **Route Handling**: Defines the `/` route, manages the search query, and handles the "Recent Searches" list using Flask's `session` object.

### `weather_templates/`
- **`base.html`**: Provides a consistent shell (navbar, footer, CSS) so that other pages don't need to repeat the same HTML.
- **`index.html`**: The dynamic heart of the UI. It uses Jinja2 templating to conditionally display the search bar, current weather cards, and the forecast grid based on whether a city was searched.

---

## ⚠️ Troubleshooting
- **City Not Found**: Ensure the city name is spelled correctly.
- **Invalid API Key**: Check your `.env` file and ensure the key is active (new keys can take a few hours to activate).
- **Port Conflict**: If port 8117 is taken, you can change the port in `weather_app.py`.


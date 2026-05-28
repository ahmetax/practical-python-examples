# 🕷️ General-Purpose Web Scraper

A powerful and flexible web scraping application built with **Python**, **Flask**, and **BeautifulSoup**. This tool allows users to extract structured data from any public URL, offering a wide range of selectable data types and advanced scraping options.

## 🚀 Features

- **Flexible Data Extraction**: Choose what to extract from a page:
  - **Meta Tags**: Page title, description, OpenGraph tags, and charset.
  - **Headings**: All h1-h6 tags with their labels.
  - **Links**: All `<a>` tags with absolute URLs and anchor text.
  - **Images**: All `<img>` tags with absolute source URLs and alt text.
  - **Page Text**: Cleaned-up textual content (removing scripts, styles, and nav elements).
  - **Tables**: Structured data from `<table>` elements, including headers and rows.
- **Advanced Request Options**:
  - **User-Agent Selection**: Switch between Chrome, Firefox, Googlebot, or default agents to bypass simple bot detection.
  - **Timeout Control**: Set custom timeouts to handle slow-responding servers.
  - **Limiters**: Define the maximum number of links and images to extract.
- **Result Management**:
  - **Inline Preview**: View all extracted data immediately on a results page.
  - **Session History**: Keep track of past scrapes during the current session.
  - **JSON Export**: Download any scrape result as a formatted JSON file.

---

## 📁 Project Structure

```text
scraper_app/
├── scraper_app.py             # Application entry point & Flask configuration
├── scraper_helpers.py         # Scraping logic and route handlers
└── scraper_templates/          # HTML UI templates
    ├── base.html               # Shared layout and CSS
    ├── index.html              # Scraper input form
    ├── result.html             # Data display page
    └── history.html            # List of past scrapes
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install the required libraries:
```bash
pip install flask requests beautifulsoup4
```

### 2. Implementing the Scraping Logic (`scraper_helpers.py`)

The core of the app is the extraction engine.

#### A. Page Fetching
Create a `fetch_page(url, timeout, user_agent)` function:
- Use `requests.get()` to fetch the page.
- Apply a `User-Agent` header from a predefined dictionary (Chrome, Firefox, etc.).
- Use `allow_redirects=True` and a custom timeout.
- Call `raise_for_status()` to handle HTTP errors.

#### B. Data Extraction Helpers
Use **BeautifulSoup** (`bs4`) to parse the HTML:
- **Meta**: Search for `<meta>` tags and extract `name`/`property` and `content`.
- **Headings**: Find all tags in `['h1', 'h2', 'h3', 'h4', 'h5', 'h6']` and extract their text.
- **Links**: Find all `<a>` tags with `href`. Use `urllib.parse.urljoin` to convert relative URLs into absolute ones.
- **Images**: Find all `<img>` tags with `src`. Use `urljoin` for absolute URLs and extract `alt` text.
- **Text**: Remove noise tags like `<script>`, `<style>`, `<nav>`, and `<footer>` using `tag.decompose()`, then use `soup.get_text()` with a newline separator.
- **Tables**: Find all `<table>` tags. Iterate through `<th>` for headers and `<td>` within `<tr>` for row data.

#### C. The Main Scrape Orchestrator
Implement a `scrape(url, options)` function:
- Call `fetch_page()`.
- Initialize a `result` dictionary with basic info: `id` (uuid), `url`, `status_code`, `elapsed` time, and `scraped_at` timestamp.
- Based on the `options` provided by the user (via checkboxes), call the corresponding extraction helpers and add the data to the `result` dictionary.

### 3. Implementing Flask Routes (`scraper_helpers.py`)

- **Index (`GET /`)**: Render the input form.
- **Scrape (`POST /scrape`)**: 
  - Collect the URL and options (meta, headings, links, etc.) from the form.
  - Handle common exceptions (`Timeout`, `ConnectionError`, `HTTPError`).
  - Store the result in a global `history` dictionary and render the `result.html` page.
- **View Result (`GET /result/<id>`)**: Retrieve a result from `history` by its ID and render it.
- **Download (`GET /download/<id>`)**: Convert the `result` dictionary to a JSON string and use `send_file()` to provide it as a downloadable `.json` file.
- **History (`GET /history`)**: Display all entries in the `history` dictionary, sorted by date.
- **Clear History (`POST /history/clear`)**: Empty the `history` dictionary.

### 4. Application Entry (`scraper_app.py`)
- Initialize the Flask app with `template_folder="scraper_templates"`.
- Register the routes via `setup_routes(app)`.
- Run the server on port 8117.

### 5. Frontend Implementation (`scraper_templates/`)

- **`base.html`**: Provide a responsive layout and include a navigation bar.
- **`index.html`**: 
  - A URL input field.
  - A group of checkboxes for selecting data types (Meta, Headings, Links, Images, Text, Tables).
  - Input fields for timeout, max links, and a dropdown for User-Agent.
- **`result.html`**: 
  - Display a summary card (Title, Status Code, Response Time).
  - Use conditional rendering (Jinja2 `{% if %}`) to display only the extracted data types that were requested.
  - Format tables using HTML `<table>` tags and list links/images with their metadata.
- **`history.html`**: A simple list of previous scrapes with links to view the full result or download the JSON.

---

## 🏃 How to Run

1. Run the application:
   ```bash
   python scraper_app.py
   ```
2. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **HTTP Requests**: Using the `requests` library to interact with web servers.
- **HTML Parsing**: Using `BeautifulSoup` to navigate and extract data from the DOM.
- **URL Normalization**: Converting relative paths to absolute URLs using `urljoin`.
- **Data Serialization**: Exporting structured data to JSON.
- **User-Agent Spoofing**: Mimicking different browsers to avoid basic anti-scraping blocks.
- **Error Handling**: Implementing robust try-except blocks for network-related failures.
- **State Management**: Using a simple in-memory dictionary to manage a session-based history of results.

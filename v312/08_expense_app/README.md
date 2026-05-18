# 💰 Expense Tracker Web App

A lightweight, user-friendly Flask application for tracking personal expenses. It allows users to record spending, view summary statistics on a dashboard, and generate detailed monthly reports with visual charts.

## 🚀 Features

- **Add Expenses**: Record transactions with description, amount, category, and date.
- **Dashboard Overview**: View total spending, monthly spending, and weekly spending at a glance.
- **Visual Analytics**: A doughnut chart displaying spending breakdown by category.
- **Delete Expenses**: Remove individual entries easily.
- **Monthly Reports**: Navigate between months to view:
  - Daily spending bar chart (using Chart.js)
  - Category breakdown table
  - Daily average spending
  - Top spending category

---

## 📁 Project Structure

```text
expense_app/
├── expense_app.py          # Application entry point & DB initialization
├── expense_helpers.py      # Flask routes, logic, and DB helpers
├── expense.db              # SQLite database (auto-generated)
└── expense_templates/      # HTML UI templates
    ├── base.html           # Common layout (Navbar, CSS, Flash messages)
    ├── index.html         # Dashboard with stats, chart, recent expenses
    ├── add.html           # Form to add new expense
    └── report.html        # Monthly report with charts
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install the necessary library:
```bash
pip install flask
```

### 2. Database Setup
Create an `ensure_db()` function in your entry point script. This function will:
- Connect to a SQLite database file named `expense.db`.
- Create an `expenses` table if it doesn't exist with the following schema:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - `description` (TEXT, NOT NULL)
  - `amount` (REAL, NOT NULL)
  - `category` (TEXT, DEFAULT 'Other')
  - `date` (TEXT, NOT NULL)
- Commit the changes and close the connection.

### 3. Application Entry (`expense_app.py`)
- Initialize a Flask application object.
- Set a `secret_key` for session management.
- Call the database setup function.
- Import and call `setup_routes()` from your helpers module.
- Run the Flask app on host `0.0.0.0` and port `8117`.

### 4. Core Logic (`expense_helpers.py`)
Create a helper module to handle all route logic and database operations.

#### Database Helpers
- **`get_conn()`**: Returns a sqlite3 connection with `row_factory = sqlite3.Row` to access columns by name.
- **`row_to_dict(row)`**: Converts a sqlite3 Row object into a standard Python dictionary.
- **`get_stats(conn)`**: Executes SQL queries to compute:
  - Total spending (sum of all expenses).
  - This month's spending (using `LIKE` query on current year-month).
  - This week's spending (filtering by date >= start of week).
  - Total count of expenses.
- **`get_cat_data(conn, year, month)`**: Returns aggregated data grouping expenses by category with sums and counts.

#### Route Handlers

1. **`index` (GET `/`)**:
   - Fetches all stats and recent expenses (LIMIT 20, ordered by date DESC).
   - Gets category breakdown data.
   - Passes labels and values for the doughnut chart to the template.

2. **`add_expense` (GET/POST `/add`)**:
   - **GET**: Renders the form with today's date pre-filled.
   - **POST**: Validates that description, amount, and date are provided. Ensures amount is a positive number. Inserts the new record into the database and flashes a success message.

3. **`delete_expense` (POST `/delete/<id>`)**:
   - Deletes the expense with the given ID.
   - Redirects back to the referring page (the dashboard or report).

4. **`report` (GET `/report`)**:
   - Accepts optional `year` and `month` query parameters (defaults to current date).
   - Calculates previous and next month for navigation links.
   - Fetches all expenses for the selected month.
   - Aggregates data into a daily map (day -> total amount).
   - Generates arrays for Chart.js: days of the month (labels) and daily totals (values).
   - Calculates monthly total, entry count, daily average, and top category.
   - Passes all this data to the report template.

### 5. UI Templates (`expense_templates/`)

- **`base.html`**: Define the HTML skeleton, include Chart.js via CDN for the charts, and create a navbar with links to "Dashboard" and "Add Expense". Include a section for flash messages.
- **`index.html`**: Display four stat cards (Total, This Month, This Week, Total Entries). Add a canvas element for the doughnut chart. Below that, list recent expenses in a table with a delete button for each row.
- **`add.html`**: Create a form with fields: Description (text), Amount (number), Category (select dropdown with options like Food, Transport, Utilities, Entertainment, Other), and Date (date input). Use POST to submit to `/add`.
- **`report.html`**: Add navigation arrows to go to the previous/next month. Display a title showing "Month Year". Add a canvas for a bar chart (daily spending). Below, show a table of category breakdown. At the bottom, display summary stats (Monthly Total, Daily Average, Top Category).

---

## 🏃 How to Run

1. Ensure you have Flask installed:
   ```bash
   pip install flask
   ```
2. Run the application:
   ```bash
   python expense_app.py
   ```
3. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📖 Key Concepts Demonstrated

- **Flask Web Development**: Routing, templates (Jinja2), and form handling.
- **SQLite Integration**: Creating databases, running queries, and aggregating data.
- **Data Visualization**: Integrating **Chart.js** to render doughnut and bar charts from Python data.
- **Date Handling**: Using Python's `datetime` and `calendar` modules to manage monthly views and calculations.
- **Session Flash Messages**: Providing user feedback for actions (success/error messages).
# ✅ To-Do List Web Application

A clean and functional To-Do List application built with **Python**, **Flask**, and **SQLite**. This app helps users manage their daily tasks with priority levels, filtering, and real-time progress statistics.

## 🚀 Features

- **Task Management**: Full CRUD (Create, Read, Update, Delete) capabilities for tasks.
- **Priority Levels**: Assign priorities (High, Medium, Low) to organize tasks by importance.
- **Quick Toggles**: Mark tasks as completed or pending with a single click.
- **Smart Filtering**: View tasks based on their state:
  - **All**: View everything.
  - **Pending**: Only show incomplete tasks (sorted by priority).
  - **Done**: View only completed tasks.
  - **High Priority**: Focus on critical pending tasks.
- **Live Statistics**: A dashboard showing the total number of tasks, pending count, completed count, and high-priority pending tasks.
- **Bulk Actions**: Ability to clear all completed tasks with one click.

---

## 📁 Project Structure

```text
19_todo_app/
├── todo_app.py           # Application entry point & DB initialization
├── todo_helpers.py       # Flask routes and DB logic
├── todo.db               # SQLite database (auto-created)
└── todo_templates/       # UI templates
    ├── base.html         # Shared layout and CSS
    ├── index.html        # Main task list and dashboard
    └── edit.html         # Task modification form
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install the required library:
```bash
pip install flask
```

### 2. Database Setup (`todo_app.py`)
Implement an `ensure_db()` function that runs at startup to initialize the SQLite database.
- **Database File**: `todo.db`.
- **Table Schema**: Create a `tasks` table with the following columns:
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT.
  - `title`: TEXT NOT NULL.
  - `priority`: TEXT (e.g., 'high', 'medium', 'low') with a default of 'medium'.
  - `done`: INTEGER (0 for pending, 1 for done) with a default of 0.
  - `created_at`: TEXT (timestamp of creation).

### 3. Core Logic (`todo_helpers.py`)

Implement the following helpers and route handlers:

#### A. Database Helpers
- **`get_conn()`**: Returns a connection to `todo.db` with `row_factory = sqlite3.Row` to allow accessing columns by name.
- **`row_to_dict(row)`**: A utility to convert SQLite rows into Python dictionaries for easier use in templates.
- **`get_stats(conn)`**: Executes counts for total, done, pending, and high-priority tasks.

#### B. Route Handlers
- **Index (`GET /`)**:
  - Read the `filter` query parameter.
  - Use a `CASE` statement in SQL to sort tasks by priority (`high` $\rightarrow$ `medium` $\rightarrow$ `low`).
  - Fetch the corresponding tasks and the current stats.
  - Render the `index.html` template.
- **Add Task (`POST /add`)**:
  - Extract `title` and `priority` from the form.
  - Validate that the title is not empty.
  - Insert a new record into the `tasks` table with the current timestamp.
- **Toggle Status (`POST /toggle/<id>`)**:
  - Update the `done` column by flipping its value (`done = 1 - done`).
- **Edit Task (`GET` and `POST /edit/<id>`)**:
  - **GET**: Fetch the specific task by ID and show it in the edit form.
  - **POST**: Update the `title` and `priority` of the task.
- **Delete Task (`POST /delete/<id>`)**:
  - Remove the specific task from the database.
- **Clear Done (`POST /clear_done`)**:
  - Run a `DELETE` query where `done = 1`.

### 4. Application Entry (`todo_app.py`)
- Initialize the Flask app.
- Set a `secret_key` (essential for using `flash()` messages).
- Call `ensure_db()` to prepare the database.
- Call `todo_helpers.setup_routes(app)` to register all endpoints.
- Run the server on port 8117.

### 5. Frontend Implementation (`todo_templates/`)

- **`base.html`**: Define the global style, including a clean typography and a navigation bar. Create a block for flash messages to show "Task added!" or "Task deleted!" alerts.
- **`index.html`**:
  - **Stats Bar**: Display the summary counts (Total, Pending, Done, High).
  - **Filter Bar**: Create links to filter by All, Pending, Done, and High.
  - **Input Form**: A simple form to enter a task title and select a priority from a dropdown.
  - **Task List**: A table or list of tasks. Each item should show the priority (with color coding), a toggle checkbox for completion, and buttons for editing and deleting.
- **`edit.html`**: A simple form allowing the user to change the task's title and priority.

---

## 🏃 How to Run

1. Run the server:
   ```bash
   python todo_app.py
   ```
2. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **CRUD Application**: A classic implementation of Create, Read, Update, and Delete operations.
- **SQLite Integration**: Using a relational database for persistent storage of simple application data.
- **Dynamic Filtering**: Using SQL query parameters to filter data on the server side.
- **Flask Sessions & Flashing**: Providing immediate user feedback through flash messages.
- **State Management**: Managing the "Done/Undone" state of a task.
- **Priority-Based Sorting**: Implementing custom sort orders in SQL.

# ✍️ Flask Blog App (Mini CMS)

A fully functional, lightweight Content Management System (CMS) built with **Python**, **Flask**, and **SQLite**. This application implements a complete user-to-content workflow, including user authentication, profile management, and a full CRUD (Create, Read, Update, Delete) system for blog posts.

## 🚀 Features

### 🌍 Public Access
- **Home Page**: A feed of all published blog posts from all users, sorted by most recent.
- **Post View**: A dedicated page to read the full content of a specific post.

### 🔐 User Authentication
- **Registration**: Create a new account with validation for usernames, emails, and password matching.
- **Security**: Passwords are securely hashed using `bcrypt`.
- **Session Management**: Secure login/logout using Flask sessions.
- **Protected Routes**: A custom `login_required` decorator ensures private pages are only accessible to authenticated users.

### 🛠️ User Dashboard & Management
- **Personal Dashboard**: A private area where users can see and manage only their own posts.
- **Post Management**: Full CRUD capabilities (Create new posts, Edit existing ones, Delete posts).
- **Profile Settings**: Change passwords (with current password verification) and the option to permanently delete the account.

---

## 📁 Project Structure

To build this project, organize your files as follows:

```text
blog_app/
├── blog_app.py          # Application entry point & DB initialization
├── blog_helpers.py      # Route handlers, auth logic, and DB helpers
├── blog.db              # SQLite database file (auto-generated)
└── blog_templates/      # UI Folder
    ├── base.html        # Common layout (Navbar, Flash messages)
    ├── index.html       # Public feed
    ├── post.html        # Single post view
    ├── login.html       # Login form
    ├── register.html    # Registration form
    ├── dashboard.html   # User's private post list
    ├── post_form.html    # Form for creating/editing posts
    └── profile.html      # Account settings
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Environment Setup
Install the necessary libraries:
```bash
pip install flask bcrypt
```

### 2. Database Design
Implement a helper function in your entry point to ensure the SQLite database exists. You need two tables:
- **`users`**: Stores `id` (PK), `username` (Unique), `email` (Unique), `password` (Hashed), and `created_at`.
- **`posts`**: Stores `id` (PK), `user_id` (FK to users), `title`, `body`, `created_at`, and `updated_at`.

### 3. Core Logic (`blog_helpers.py`)
Create a helper module to keep the main app clean. Implement the following:
- **Database Connection**: A function to return a `sqlite3` connection with `row_factory = sqlite3.Row` (to access columns by name).
- **Auth Helpers**:
    - `hash_password(password)`: Uses `bcrypt.hashpw`.
    - `check_password(password, hashed)`: Uses `bcrypt.checkpw`.
    - `login_required(f)`: A wrapper that checks if `user_id` exists in the session; if not, redirects to login.
- **Route Handlers**:
    - **Public Routes**: Use `SELECT` queries with `JOIN` to link posts to their authors.
    - **Auth Routes**: Handle `POST` requests for registration (with regex validation) and login.
    - **Private Routes**: Implement logic to ensure users can only edit or delete posts where the `user_id` matches the session's `user_id`.

### 4. Application Entry (`blog_app.py`)
- Initialize the Flask app.
- Set a `secret_key` for session security.
- Call the database initialization function.
- Call the `setup_routes` function from your helpers module to register all endpoints.

### 5. UI Templates (`blog_templates/`)
Build your frontend using **Jinja2** templates:
- Use `base.html` to define the HTML skeleton and a navigation bar that changes based on whether a user is logged in.
- Use `flash` messages in the base template to show success/error alerts.
- Use forms in `post_form.html` that work for both creating and editing (by passing the `post` object).

---

## 🏃 How to Run

1. Place all files in the structure described above.
2. Run the application:
   ```bash
   python blog_app.py
   ```
3. Navigate to `http://localhost:8117` in your web browser.

## 📈 Complexity & Security Notes
- **Time Complexity**: Most database operations are $O(1)$ or $O(N)$ where $N$ is the number of posts, which is efficient for small-to-medium blogs.
- **Security**: This app uses **Bcrypt** for passwords, preventing plain-text leaks, and **Server-side Sessions** to prevent unauthorized access to the dashboard.

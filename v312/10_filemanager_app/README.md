# 📁 File Manager Web Application

A full-featured web-based file manager built with **Python** and **Flask**. It allows users to upload, view, preview, download, and delete files directly from a web browser. The application includes type detection, inline previews for various file formats, and a dashboard with storage statistics.

## 🚀 Features

- **Multi-File Upload**: Upload multiple files at once via a form or drag-and-drop.
- **File Type Detection**: Automatically identifies and assigns icons to images, PDFs, text files, archives, videos, audio, spreadsheets, and documents.
- **Inline Preview**: 
  - **Images**: Displayed directly in the browser.
  - **PDFs**: Viewed inline.
  - **Text/Code**: Shows the first 20KB of content for quick inspection.
- **File Information**: Displays file size (human-readable), upload/modification date, and MIME type.
- **Download**: Download any file from the manager.
- **Delete**: Remove files from the storage.
- **Filtering**: Filter files by category (All, Images, PDFs, Other).
- **Statistics Dashboard**: Shows total file count, total storage used, and counts per category.
- **Duplicate Handling**: If a file with the same name exists, appends a timestamp to the filename to avoid overwriting.

---

## 📁 Project Structure

```text
filemanager_app/
├── filemanager_app.py          # Application entry point
├── filemanager_helpers.py      # Flask routes and file logic
├── uploads/                    # Directory where uploaded files are stored
└── filemanager_templates/      # HTML UI templates
    ├── base.html               # Common layout (Navbar, CSS, Flash messages)
    ├── index.html              # File list, upload form, stats, filters
    └── preview.html            # File preview page
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install the required libraries:
```bash
pip install flask werkzeug
```

### 2. Application Entry (`filemanager_app.py`)
- Import `flask`.
- Create a `main()` function.
- Initialize a Flask application object, specifying `template_folder="filemanager_templates"`.
- Set a `secret_key` for session management.
- Import `filemanager_helpers` and call `setup_routes(app)` to register routes.
- Run the Flask app on host `0.0.0.0` and port `8117`.

### 3. Core Logic (`filemanager_helpers.py`)

#### Configuration Constants
- Define `UPLOAD_FOLDER = "uploads"` and `MAX_MB = 16`.
- Create sets for file extensions: `IMAGE_EXTS`, `PDF_EXTS`, `TEXT_EXTS` to categorize files.

#### Helper Functions

1. **`file_icon(ext)`**:
   - Returns an emoji string based on the file extension (e.g., 🖼 for images, 📄 for PDFs, 📝 for text).

2. **`human_size(nbytes)`**:
   - Converts raw byte size to a human-readable string (B, KB, MB, GB).

3. **`file_info(filename)`**:
   - Takes a filename and returns a dictionary containing:
     - `filename`, `ext` (lowercase extension), `icon`, `is_image`, `is_pdf`
     - `size` (formatted), `size_raw` (bytes), `date` (formatted timestamp)

4. **`get_all_files(filter_type='all')`**:
   - Scans the `UPLOAD_FOLDER`.
   - If `filter_type` is 'image', 'pdf', or 'other', filters accordingly.
   - Returns a list of file info dictionaries, sorted by newest first.

5. **`get_stats()`**:
   - Calls `get_all_files()` and calculates:
     - Total count, total size, number of images, number of PDFs, number of others.

#### Route Handlers

1. **Index (GET `/`)**:
   - Gets the `filter` query parameter (default 'all').
   - Retrieves filtered file list and statistics.
   - Renders `index.html` passing `files`, `stats`, `filter`, and `max_mb`.

2. **Upload (POST `/upload`)**:
   - Handles multi-file upload via `request.files.getlist('files')`.
   - Uses `secure_filename()` from Werkzeug to sanitize filenames.
   - **Duplicate Handling**: If the destination file exists, renames the new file by appending a timestamp (e.g., `file_20260516_143022.txt`).
   - Saves the file to the `uploads` directory.
   - Flashes success or error messages.

3. **Preview (GET `/preview/<filename>`)**:
   - Secures the filename and checks existence.
   - Determines the file type:
     - **Image**: Sets `file_type = 'image'`.
     - **PDF**: Sets `file_type = 'pdf'`.
     - **Text**: Reads up to 20KB of content for preview.
     - **Other**: Just shows metadata.
   - Renders `preview.html` with file details and content (if applicable).

4. **Download (GET `/download/<filename>`)**:
   - Uses Flask's `send_from_directory` with `as_attachment=True`.

5. **Serve File (GET `/uploads/<filename>`)**:
   - Serves files inline (for displaying images/PDFs in the browser without downloading).

6. **Delete (POST `/delete/<filename>`)**:
   - Secures the filename and removes the file from the filesystem.
   - Redirects back to the referring page.

### 4. UI Templates (`filemanager_templates/`)

#### `base.html`
- HTML5 skeleton.
- Include a navigation bar with links to "File Manager".
- Add a section for flash messages (success/error).
- Add basic CSS for layout, tables, cards, and responsiveness.

#### `index.html`
- **Stats Section**: Display 5 cards showing Total Files, Total Size, Images, PDFs, Others.
- **Upload Section**: A form with `enctype="multipart/form-data"`, a file input with `multiple` attribute, and an upload button.
- **Filter Links**: Buttons or links to filter by All, Images, PDFs, Other.
- **File Table**: A table listing files with columns: Icon, Filename, Size, Date, Actions (Preview, Download, Delete).
- Use Jinja2 loops to iterate over the `files` list.

#### `preview.html`
- Display file icon and name prominently.
- Show metadata: Size, Date, MIME type.
- **Content Area**:
  - If image: `<img src="{{ url_for('serve_file', filename=filename) }}">`
  - If PDF: `<embed src="...">` or a download link.
  - If text: Display the content in a `<pre>` block.
- Add action buttons: Download, Delete.
- Add a "Back to List" link.

---

## 🏃 How to Run

1. Install dependencies:
   ```bash
   pip install flask werkzeug
   ```
2. Run the application:
   ```bash
   python filemanager_app.py
   ```
3. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **Flask Web Development**: Routing, request handling, template rendering (Jinja2).
- **File Handling**: Uploading, saving, deleting, and serving files securely using `werkzeug.utils.secure_filename`.
- **MIME Type Detection**: Using Python's `mimetypes` module.
- **Static File Serving**: Using `send_from_directory` for both downloads and inline display.
- **User Feedback**: Using Flask's `flash` system to show success and error messages.
- **Filtering & Aggregation**: Processing file lists to generate statistics and category-based filters.
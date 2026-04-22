"""
Author: Ahmet Aksoy
Date: 2026-04-17
Python 3.12 - Ubuntu 24.04

Description:
    General File Manager web application built with Python + Flask.

    Python handles application startup and Flask configuration.
    Route handlers and file operations are in filemanager_helpers.py.
    HTML templates are in the filemanager_templates/ directory.
    Uploaded files are stored in the uploads/ directory.

    Features:
      - Multi-file upload with drag & drop support
      - File type detection (image, PDF, text, archive, video, audio...)
      - Thumbnail preview for images
      - Inline preview for images, PDFs and text/code files
      - File info: size, upload date, MIME type
      - Download any file
      - Delete files
      - Filter by type: all / images / PDFs / other
      - Stats: total count, total size, per-type counts
      - Duplicate filename handling (timestamp suffix)

    File structure:
      filemanager_app.py          <- this file
      filemanager_helpers.py        <- Flask routes + file logic
      uploads/                      <- uploaded files stored here
      filemanager_templates/
        base.html
        index.html                  <- file list + upload
        preview.html                <- file preview

    Run:
      python filemanager_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask werkzeug
"""

import flask

def main():

    app = flask.Flask(
        str("__main__"),
        template_folder="filemanager_templates"
    )

    app.secret_key = "python-filemanager-secret-key"

    import filemanager_helpers

    filemanager_helpers.setup_routes(app)

    print("=" * 50)
    print("  File Manager starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    _ = app.run(host="0.0.0.0", port=8117, debug=False)

main()
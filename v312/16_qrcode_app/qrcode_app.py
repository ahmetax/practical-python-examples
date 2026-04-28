"""
Author: Ahmet Aksoy
Date: 2026-04-26
Python 3.12 - Ubuntu 24.04

Description:
    QR Code Creator & Reader web application built with Python + Flask.

    Python handles application startup and Flask configuration.
    QR generation, decoding and route handlers are in qrcode_helpers.py.
    HTML templates are in the qrcode_templates/ directory.

    Features:
      Creator:
        - Text / URL / vCard / WiFi QR code generation
        - Size selection: 200 / 300 / 400 / 600 px
        - Error correction: L / M / Q / H
        - Color themes: Black on White / Blue on White / White on Dark
        - Inline PNG preview
        - PNG download

      Reader:
        - Upload image (PNG, JPG, GIF, BMP, WebP) with drag & drop
        - Webcam live scanning via jsQR (browser-side, no server round-trip)
        - Auto-open URLs from decoded content
        - Copy to clipboard

    File structure:
      qrcode_app.py            <- this file
      qrcode_helpers.py          <- Flask routes + QR logic
      qrcode_templates/
        base.html
        create.html              <- QR code generator
        read.html                <- image upload + webcam reader

    Run:
      python qrcode_app.py
    Then open http://localhost:8117

Requirements:
    pip install flask qrcode[pil] pyzbar pillow numpy opencv-python
    
    Note: pyzbar also requires the zbar shared library:
      Ubuntu/Debian: sudo apt-get install libzbar0
      macOS:         brew install zbar
"""

from flask import Flask
import qrcode_helpers

app = Flask(__name__, template_folder="qrcode_templates", static_folder="static", static_url_path="/static")
app.secret_key = "python-qrcode-secret-key"

qrcode_helpers.setup_routes(app)

if __name__ == "__main__":
    print("=" * 50)
    print("  QR Code App starting on port 8117")
    print("  http://localhost:8117")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    app.run(host="0.0.0.0", port=8117, debug=False)

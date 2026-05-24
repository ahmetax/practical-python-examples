# 📱 QR Code Creator & Reader

A comprehensive web application built with **Python** and **Flask** that allows users to both generate customized QR codes and decode existing ones from images or via a live webcam stream.

## 🚀 Features

### 🎨 QR Code Creator
- **Multiple Formats**: Generate QR codes for:
  - Simple Text or URLs.
  - **vCards**: Digital business cards (Name, Phone, Email, Org, URL).
  - **WiFi**: Automatic network connection/login (SSID, Password, Security).
- **Customization**:
  - **Size**: Choose from various resolutions (e.g., 200px to 600px).
  - **Error Correction**: Adjust the level (L, M, Q, H) to handle damage or noise.
  - **Themes**: Select from different color palettes (e.g., Black on White, Blue on White, White on Dark).
- **Fast Preview**: View the generated QR code instantly as a base64 image.
- **Download**: Save the resulting QR code as a high-quality PNG file.

### 🔍 QR Code Reader
- **Image Upload**: Upload an image (PNG, JPG, GIF, BMP, WebP) and decode the content.
- **Multi-Strategy Decoding**: Uses a combination of `pyzbar` and `OpenCV` with preprocessing (grayscale, thresholding, sharpening, and upscaling) to ensure high accuracy even with low-quality images.
- **Webcam Scanning**: Integrates a live scanning feature via the browser (utilizing `jsQR` on the client side and a server-side `/scan_frame` endpoint).
- **Smart Actions**: Automatically detects URLs in the decoded content for easy navigation.

---

## 📁 Project Structure

```text
16_qrcode_app/
├── qrcode_app.py          # Main entry point and Flask configuration
├── qrcode_helpers.py       # QR generation, decoding logic, and route handlers
├── qrcode_templates/       # HTML UI templates
│   ├── base.html           # Common layout and CSS
│   ├── create.html         # Generator interface
│   └── read.html           # Reader and uploader interface
└── static/                 # (Optional) CSS/JS files
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install the required Python libraries:
```bash
pip install flask qrcode[pil] pyzbar pillow numpy opencv-python
```
*Note: `pyzbar` requires the zbar shared library on your system.*
- **Ubuntu/Debian**: `sudo apt-get install libzbar0`
- **macOS**: `brew install zbar`

### 2. Implementation Logic (`qrcode_helpers.py`)

#### A. QR Content Builders
Create functions to format data according to standards:
- **vCard**: Format as `BEGIN:VCARD...END:VCARD`.
- **WiFi**: Format as `WIFI:T:[Security];S:[SSID];P:[Password];H:[Hidden];;`.

#### B. QR Generation (`generate_qr`)
- Use the `qrcode` library to create a `QRCode` object.
- Set `box_size` (calculated from total pixels), `error_correction`, and `border`.
- Add data and generate the image.
- Use `PIL` (Pillow) to apply the chosen `fill_color` and `back_color`.
- Resize the image to the requested dimensions using `Image.NEAREST` to keep pixels sharp.
- Save the image to a `BytesIO` buffer and return a **base64-encoded string** for inline HTML display.

#### C. QR Decoding Strategy (`read_qr_from_image`)
Implement a robust decoding pipeline to handle various image qualities:
1. **Standard**: Run `pyzbar.decode` on the original image.
2. **OpenCV Detection**: Use `cv2.QRCodeDetector().detectAndDecode()`.
3. **Preprocessing**:
   - Convert to grayscale $\rightarrow$ Apply Otsu's thresholding $\rightarrow$ Decode.
   - Apply a sharpening filter (Laplacian/custom kernel) $\rightarrow$ Decode.
   - Upscale the image $2\times$ using cubic interpolation $\rightarrow$ Decode.

#### D. Flask Route Handlers
- **`/create`**:
  - **GET**: Show the generator form.
  - **POST**: Collect form data (type, size, color, content), build the appropriate string (Text/WiFi/vCard), generate the QR image, and render the preview.
- **`/download`**: Serve the last generated QR image bytes as a `send_file` PNG attachment.
- **`/read`**:
  - **GET**: Show the upload form.
  - **POST**: Receive an uploaded image, pass it to the decoding pipeline, and display the result.
- **`/scan_frame`**: A specialized endpoint for webcam scanning. It receives a base64 image from the browser, decodes it, and returns the result as JSON.

### 3. Application Entry (`qrcode_app.py`)
- Initialize the Flask app with the `qrcode_templates` folder.
- Import `qrcode_helpers` and call `setup_routes(app)`.
- Start the server on port 8117.

### 4. Frontend Implementation (`qrcode_templates/`)

- **`base.html`**: Define the overall look and feel, including navigation and flash messages.
- **`create.html`**:
  - A form with a dropdown to select QR type (Text, URL, vCard, WiFi).
  - Dynamic input fields that appear based on the selected type.
  - Options for size, error correction, and color.
  - A preview area to show the generated QR code.
- **`read.html`**:
  - An upload area with drag-and-drop support.
  - A webcam view area (using a `<video>` element and a `<canvas>` for frame capture).
  - JavaScript to capture frames and send them to `/scan_frame` via `fetch`.

---

## 🏃 How to Run

1. Ensure all dependencies and the `zbar` library are installed.
2. Run the application:
   ```bash
   python qrcode_app.py
   ```
3. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **QR Standard Implementation**: Handling specific formats for vCards and WiFi.
- **Image Processing**: Using `Pillow` for resizing and coloring, and `OpenCV` for advanced image preprocessing (thresholding, sharpening).
- **Computer Vision**: Utilizing `pyzbar` and `cv2` for QR code detection and decoding.
- **Binary Data Handling**: Working with `io.BytesIO` and `base64` to serve images without saving them to disk.
- **Real-time Interaction**: Combining Python backend decoding with JavaScript webcam frame capture.
- **Web Frameworks**: Using Flask to build a multi-functional tool with dynamic routing and file serving.

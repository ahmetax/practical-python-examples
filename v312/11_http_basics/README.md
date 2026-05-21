# 🌐 HTTP Basics with Python

A comprehensive collection of examples demonstrating core HTTP operations using Python's `requests` library. This project covers essential topics like fetching JSON data, posting data to APIs, managing sessions, handling authentication, downloading files, and implementing retry logic.

## 🚀 Features

### 1. GET Requests (JSON API)
- Fetching a list of resources from a REST API
- Filtering results using query parameters
- Fetching a single resource by ID
- Error handling for failed requests

### 2. POST/PUT Requests
- Creating new resources with POST
- Updating existing resources with PUT
- Sending JSON payloads
- Handling response status codes (201 Created, 200 OK)

### 3. Session Management
- Reusing TCP connections for multiple requests
- Setting session-level headers (applied to all requests)
- Automatic cookie persistence across requests

### 4. Authentication Methods
- Bearer Token authentication (OAuth2, JWT)
- API Key authentication (custom headers like X-Api-Key)
- Basic Authentication (Base64 encoded username:password)

### 5. File Downloads
- Simple download (loads entire file into memory)
- Streaming download (constant memory usage for large files)
- Download with progress indicator

### 6. Timeout and Retry Logic
- Setting connect and read timeouts
- Manual retry with fixed delay
- Exponential backoff (doubling wait time after each failure)

---

## 📁 Project Structure

```text
11_http_basics/
├── http_get_json_api.py       # GET requests and JSON parsing
├── http_post_json.py          # POST and PUT requests
├── http_session.py            # Session management
├── http_auth_headers.py       # Authentication patterns
├── http_download_streaming.py # File downloading techniques
└── http_timeout_retry.py     # Timeouts and retry strategies
```

---

## 🛠️ Step-by-Step Implementation Guide

### Prerequisites
Install the required library:
```bash
pip install requests
```

---

### 1. HTTP GET Requests — `http_get_json_api.py`

**Goal**: Fetch data from a public REST API (JSONPlaceholder) and display it.

**Implementation Steps**:

1. **Import modules**: Import `requests` and `json`.
2. **Define fetch function**:
   - Build the API URL (e.g., `https://jsonplaceholder.typicode.com/posts`).
   - Use query parameters dict to filter by `userId`.
   - Call `requests.get(url, params=params, timeout=10)`.
3. **Handle response**:
   - Check if `response.status_code == 200`.
   - Parse JSON using `response.json()`.
   - Loop through results and print selected fields (id, title, body preview).
4. **Handle errors**: Wrap in try/except and print connection error messages.
5. **Single resource fetch**:
   - Construct URL with ID appended (e.g., `/posts/7`).
   - Handle 404 status for missing resources.
6. **Main function**: Call both examples to demonstrate.

---

### 2. HTTP POST/PUT Requests — `http_post_json.py`

**Goal**: Send data to a REST API to create or update resources.

**Implementation Steps**:

1. **Create post function**:
   - Define API URL (POST endpoint).
   - Build payload dict with `userId`, `title`, `body`.
   - Set custom headers (`Content-Type`, `Accept`).
   - Use `requests.post(url, json=payload, headers=headers)`.
2. **Check status**: Expect 201 Created on success.
3. **Parse response**: The API echoes back the created object with an assigned ID.
4. **Update function** (PUT):
   - Use `requests.put()` with the full resource URL.
   - Include all fields in the payload (PUT replaces the entire record).
5. **Main**: Call create_post() and update_post() to demonstrate.

---

### 3. Session Management — `http_session.py`

**Goal**: Reuse connections, share headers, and manage cookies automatically.

**Implementation Steps**:

1. **Basic session**:
   - Create `session = requests.Session()`.
   - Use `session.get(url)` instead of `requests.get(url)`.
   - Call `session.close()` when done to release resources.
2. **Session headers**:
   - Set `session.headers["Authorization"] = "Bearer ..."` once.
   - This header is automatically included in every request made through the session.
3. **Cookie handling**:
   - Make a request to set a cookie (e.g., `/cookies/set/session_id/...`).
   - Make a second request — the session automatically sends the stored cookie.
   - Use httpbin.org to verify cookie echo-back.
4. **Main**: Call all three functions to show different session patterns.

---

### 4. Authentication — `http_auth_headers.py`

**Goal**: Access protected APIs using various auth methods.

**Implementation Steps**:

1. **Bearer Token**:
   - Build headers dict: `{"Authorization": "Bearer " + token}`.
   - Send GET request to protected endpoint.
   - Handle 401 Unauthorized if token is invalid.
2. **API Key**:
   - Use custom header name (commonly `X-Api-Key`).
   - Send request and verify echoed headers from httpbin.org.
3. **Basic Auth**:
   - Use `requests.get(url, auth=(username, password))`.
   - The `auth` parameter automatically Base64 encodes credentials.
   - Test with httpbin.org's `/basic-auth/{user}/{pass}` endpoint.
4. **Best Practice Note**: Emphasize using environment variables instead of hardcoding credentials.

---

### 5. File Downloading — `http_download_streaming.py`

**Goal**: Download files efficiently, handling large files without memory issues.

**Implementation Steps**:

1. **Simple download**:
   - Use `requests.get(url)`.
   - Write `response.content` directly to a file in binary mode (`"wb"`).
   - Suitable only for small files.
2. **Streaming download**:
   - Add `stream=True` to the request.
   - Use `response.iter_content(chunk_size=8192)` to read in chunks.
   - Write each chunk to disk immediately — memory usage stays constant.
3. **Progress tracking**:
   - Read `Content-Length` header from response for total size.
   - Calculate percentage downloaded.
   - Print progress every 10% or every 50KB if size is unknown.
4. **Main**: Call functions to download test files from httpbin.org/bytes.

---

### 6. Timeout and Retry — `http_timeout_retry.py`

**Goal**: Build robust HTTP clients that handle slow servers and transient failures.

**Implementation Steps**:

1. **Timeout handling**:
   - Pass `timeout=(connect_timeout, read_timeout)` to `requests.get()`.
   - Connect timeout: max time to establish connection.
   - Read timeout: max time to wait for data.
   - Catch timeout exceptions and handle gracefully.
2. **Manual retry loop**:
   - Use a `while` loop with a retry counter.
   - On failure, `time.sleep(delay)` before next attempt.
   - Return on success, continue on failure.
3. **Exponential backoff**:
   - Start with a small delay (e.g., 1 second).
   - After each failure, multiply delay by 2 (1s, 2s, 4s, 8s...).
   - This avoids hammering a struggling server.
4. **Main**: Test with httpbin.org/delay (to trigger timeout) and /status/503 (to trigger retries).

---

## 🏃 How to Run Each Script

1. Navigate to the project directory.
2. Run any of the scripts individually:
   ```bash
   python http_get_json_api.py
   python http_post_json.py
   python http_session.py
   python http_auth_headers.py
   python http_download_streaming.py
   python http_timeout_retry.py
   ```

---

## 📚 Key Concepts Demonstrated

- **REST APIs**: Understanding URLs, endpoints, methods (GET, POST, PUT), and status codes.
- **JSON Processing**: Parsing JSON responses and handling nested data.
- **Connection Reuse**: Using Sessions to improve performance.
- **Security**: Implementing Bearer, API Key, and Basic auth.
- **Memory Efficiency**: Streaming large file downloads.
- **Resilience**: Timeouts and retry strategies for production-grade code.
- **Testing APIs**: Using httpbin.org and JSONPlaceholder for safe, free testing.

---

## ⚠️ Important Notes

- **Testing Services**: This project uses free public testing services (httpbin.org, jsonplaceholder.typicode.com). Do not use real credentials with these — they are for testing only.
- **Environment Variables**: In production code, never hardcode API keys or tokens. Use `os.environ.get("API_KEY")` instead.
- **Error Handling**: Always wrap network calls in try/except blocks to handle timeouts, connection errors, and invalid responses gracefully.
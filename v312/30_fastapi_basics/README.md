# Project 30: FastAPI Basics

A foundational microservice web framework example demonstrating how to build high-performance, asynchronous REST APIs using FastAPI and Pydantic. This implementation covers type validation schemas, path/query parameter handling, status codes, and exception management.

## Architectural Goal
The application shifts from traditional synchronous paradigms (like standard Flask routing) into a modern ASGI-driven architecture. By leveraging `async/await` non-blocking operations alongside Pydantic data modeling layers, it ensures that runtime traffic payloads are validated instantly before reaching core application domains.

## Project Structure
```text
30_fastapi_basics/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Setup & Dependencies
Unlike previous standard library examples, FastAPI requires an external routing framework engine and an ASGI web server runner (uvicorn). Pip install them directly into your virtual environment:

```bash
pip install fastapi uvicorn pydantic

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Set up an isolated directory for this project inside your repository workspace:

```bash
mkdir 30_fastapi_basics
cd 30_fastapi_basics

### Step 2: Formulate the Web Service
Create a file named main.py. Build your API structure step-by-step:

Instantiate the Core Application Instance: Import FastAPI and create an instance variable (e.g., app = FastAPI()). You can optionally pass metadata like title, description, and version to customize the automated openAPI documentation context.

Design Data Validation Schemas: Define your input constraints by inheriting from Pydantic's BaseModel. Use field attributes (Field(...)) to mandate basic requirements, string length boundaries, or positive math validations (e.g., enforcing that price values stay strictly greater than zero via gt=0.0).

Draft Non-Blocking Asynchronous Routes: Implement standard REST verb decorators over asynchronous target routines (async def).

Use plain routing paths for broad actions (e.g., @app.get("/items")).

Use bracket formatting tokens for explicit inline routing parameters (e.g., @app.get("/items/{item_id}")), capturing variables natively as strongly typed function inputs.

Map parameter variables directly inside function declarations (e.g., limit: int = 10) to handle query parameters and pagination effortlessly.

Enforce Error Boundaries: Guard edge cases by raising instances of HTTPException alongside valid status components imported directly from fastapi.status.

### Step 3: Run and Verify
Add a driver block to launch your application using uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True). Run the server script from your terminal:

```bash
python main.py

Open your browser and navigate to the following interactive endpoints:

API Status Check: http://127.0.0.1:8000/

Interactive Swagger Documentation: http://127.0.0.1:8000/docs

Alternative ReDoc UI: http://127.0.0.1:8000/redoc




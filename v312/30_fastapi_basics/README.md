# Project 30: FastAPI Basics

A small REST API built with FastAPI. It keeps an inventory of items in a Python dictionary (in memory) and shows the core FastAPI features on four endpoints:

| Endpoint | What it shows |
|----------|---------------|
| `GET /` | A simple status message |
| `GET /items?limit=10&skip=0` | Query parameters with default values (pagination) |
| `GET /items/{item_id}` | A typed path parameter and a `404` error with `HTTPException` |
| `POST /items` | Request body validation with a Pydantic model, `201` and `400` status codes |

## How It Works
- `ItemSchema` is a Pydantic model. `sku` must be at least 3 characters, `name` at least 1 character and `price` greater than 0. FastAPI checks the request body against it before the function runs and answers invalid requests with `422` automatically.
- `item_id: int` in the path is converted to an integer. A value like `abc` is rejected with `422`.
- `POST /items` rejects a duplicate `sku` with `400`. New items get the next integer ID (`max + 1`).
- The data lives in the `INVENTORY_DB` dictionary, so everything you add is lost when the server restarts.
- `limit` and `skip` are not validated. Negative values fall through to Python list slicing: `/items?limit=-1` returns every item except the last one.
- FastAPI generates interactive documentation at `/docs` (Swagger UI) and `/redoc`.

## Project Structure
```text
30_fastapi_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (current FastAPI, Pydantic and Uvicorn releases require 3.10+; the code itself uses no newer syntax). Tested on 3.12.3.
- Third-party packages: `fastapi` and `uvicorn` (`pydantic` is installed together with FastAPI). Tested with fastapi 0.143.0, pydantic 2.14.1, uvicorn 0.54.0.

## Running
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python3 main.py
```
The server starts on `http://127.0.0.1:8000` with auto-reload enabled. Stop it with `Ctrl+C`.

In a second terminal you can call the endpoints with `curl`, or open `http://127.0.0.1:8000/docs` in your browser.

## Sample Output (Python 3.12.3)
Server terminal:
```text
INFO:     Will watch for changes in these directories: ['/path/to/30_fastapi_basics']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [435840] using StatReload
Launching API Web Server locally...
INFO:     Started server process [435849]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Requests and their responses (the HTTP status code is added in parentheses where it is not `200`):
```bash
curl http://127.0.0.1:8000/
curl "http://127.0.0.1:8000/items?limit=1&skip=1"
curl http://127.0.0.1:8000/items/99
curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" \
     -d '{"sku":"SKU-MON-03","name":"27-inch Monitor","price":199.9}'
curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" \
     -d '{"sku":"AB","name":"","price":0}'
```
```text
{"status":"online","message":"Welcome to the FastAPI Inventory System"}
[{"id":2,"sku":"SKU-MOUS-02","name":"Ergonomic Wireless Mouse","price":49.5}]
{"detail":"Item with ID 99 does not exist."}                                   (HTTP 404)
{"id":3,"sku":"SKU-MON-03","name":"27-inch Monitor","price":199.9}             (HTTP 201)
{"detail":[{"type":"string_too_short","loc":["body","sku"],"msg":"String should have at least 3 characters","input":"AB","ctx":{"min_length":3}},{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1}},{"type":"greater_than","loc":["body","price"],"msg":"Input should be greater than 0","input":0,"ctx":{"gt":0.0}}]}   (HTTP 422)
```
Sending the same `SKU-MON-03` item again returns `{"detail":"An item with SKU 'SKU-MON-03' already exists."}` with status `400`. Process IDs and paths differ on your machine.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/26/fastapi-ile-tanisin-modern-hizli-ve-tip-guvenli-apiler-gelistirmek/
- FastAPI documentation: https://fastapi.tiangolo.com/

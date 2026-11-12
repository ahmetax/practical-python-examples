# Project 53: The Lenient API — limit=-1, a "12.5" Price and an "inf" That Locks the List

Project 30 (FastAPI basics) was written by an AI assistant. Every documented request works, and Pydantic rejects the invalid bodies the README shows. This script sends the requests nobody documents, first to the original app and then to a corrected one.

| Request | Original ("says") | Corrected ("checks") |
|---|---|---|
| `GET /items?limit=-1` / `skip=-1` | 200, wrong records (list slicing) | 422 (`Query(ge=...)`) |
| `GET /items?limit=1000000000` | 200, no upper bound | 422 (`le=100`) |
| `"price": "12.5"` or `true` | 201, stored as 12.5 / 1.0 | 422 (`strict=True`) |
| `"name": "   "`, extra `"discount"` field | 201, blank name / field dropped | 422 (`str_strip_whitespace`, `extra="forbid"`) |
| `"price": "inf"` | 500, **record saved**, `GET /items` returns 500 afterwards | 422 |
| bare `NaN`, `Infinity`, `1e999` | 500 | 422 only with a custom validation error handler |

## How It Works
- `build_says()` contains the model and the two endpoints from project 30, unchanged. `build_checks()` is the corrected version. Every request runs against a fresh app, except in section 3, which shows what happens to the same app after the bad request.
- Requests go through FastAPI's `TestClient` with `raise_server_exceptions=False`, so a server error shows up as a 500 response, the way a real client sees it.
- Section 3: lax Pydantic turns the string `"inf"` into `float("inf")`, which passes `gt=0`. The record is stored, then Starlette fails to write the response (`ValueError: Out of range float values are not JSON compliant: inf`). Every later listing that reaches that record fails too.
- Section 4: Python's `json` module accepts bare `NaN`, `Infinity` and `1e999`. The corrected model rejects them and nothing is stored, but FastAPI's default 422 response echoes the rejected input, cannot be written as JSON, and the client still gets 500. `build_checks()` installs a `RequestValidationError` handler that leaves `input` and `ctx` out of the error list.
- Section 5: `Query(strict=True)` rejects every value, because query strings are always strings. Use `ge`/`le` on query parameters instead.

## Project Structure
```text
53_lenient_api/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer. Tested on 3.12.3 and in Docker on 3.9, 3.10 and 3.14 (3.9 installs fastapi 0.128.8 / pydantic 2.13.5); the output was identical.
- Third-party packages: `fastapi` and `httpx` (for `TestClient`). Tested with fastapi 0.162.5 and pydantic 2.14.3; sections 3 and 4 behave the same with fastapi 0.143.0 / pydantic 2.14.1.

## Running
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi httpx
python3 main.py
```
No server is started.

## Sample Output (Python 3.12.3)
```text
Python 3.12.3, fastapi 0.162.5, pydantic 2.14.3

== 1. Pagination ==
  GET /items?limit=-1
  says      200  ids [1]
  checks    422  greater_than_equal at query.limit
  GET /items?skip=-1
  says      200  ids [2]
  checks    422  greater_than_equal at query.skip
  GET /items?limit=1000000000
  says      200  ids [1, 2]
  checks    422  less_than_equal at query.limit

== 2. Lax types ==
  POST {"sku":"SKU-A1","name":"Cable","price":"12.5"}
  says      201  {"id":3,"sku":"SKU-A1","name":"Cable","price":12.5}
  checks    422  float_type at body.price
  POST {"sku":"SKU-A2","name":"Cable","price":true}
  says      201  {"id":3,"sku":"SKU-A2","name":"Cable","price":1.0}
  checks    422  float_type at body.price
  POST {"sku":"SKU-A3","name":"Cable","price":12}
  says      201  {"id":3,"sku":"SKU-A3","name":"Cable","price":12.0}
  checks    201  {"id":3,"sku":"SKU-A3","name":"Cable","price":12.0}
  POST {"sku":"SKU-A4","name":"   ","price":5}
  says      201  {"id":3,"sku":"SKU-A4","name":"   ","price":5.0}
  checks    422  string_too_short at body.name
  POST {"sku":"SKU-A5","name":"Cable","price":5,"discount":90}
  says      201  {"id":3,"sku":"SKU-A5","name":"Cable","price":5.0}
  checks    422  extra_forbidden at body.discount
  POST {"sku":" SKU-MECH-01","name":"Cable","price":5}
  says      201  {"id":3,"sku":" SKU-MECH-01","name":"Cable","price":5.0}
  checks    400  {"detail":"An item with SKU 'SKU-MECH-01' already exist...

== 3. "inf" passes gt=0 ==
  says      500  Internal Server Error
            records now: 3
  GET       500  Internal Server Error
  GET       200  ids [1, 2]
  checks    422  float_type at body.price
            records now: 2
  GET       200  ids [1, 2]
  GET       200  ids [1, 2]

== 4. Bare NaN / Infinity in the body ==
  POST {"sku":"SKU-N1","name":"Cable","price":NaN}
  says      500  Internal Server Error                    records: 2
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  POST {"sku":"SKU-N2","name":"Cable","price":Infinity}
  says      500  Internal Server Error                    records: 3
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  POST {"sku":"SKU-N3","name":"Cable","price":1e999}
  says      500  Internal Server Error                    records: 3
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  (model = corrected model without the error handler)

== 5. Query(strict=True) ==
  strict    422  int_type at query.limit
  checks    200  ids [1, 2]
```

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/26/sessizce-kabul-eden-api-fastapi-limit-fiyat-inf/
- Original project: `v312/30_fastapi_basics`
- FastAPI numeric validations: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
- FastAPI, override request validation exceptions: https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
- Pydantic strict mode: https://docs.pydantic.dev/latest/concepts/strict_mode/
- Python json, infinite and NaN values: https://docs.python.org/3/library/json.html#infinite-and-nan-number-values

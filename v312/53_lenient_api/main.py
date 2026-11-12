# Author: Ahmet Aksoy & Claude
# Date: 12.11.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - fastapi 0.162.5, pydantic 2.14.3 (same results with fastapi 0.143.0)

"""
An API that silently accepts bad input.

Project 30 (FastAPI basics) was written by an AI assistant. Every documented
request works. This script sends it the requests nobody documents and runs
the same requests against a corrected version.

  says   = the original app from project 30 (endpoints copied unchanged)
  checks = the corrected app

Sections:
  1. Pagination: negative limit/skip go straight into list slicing
  2. Lax types: "12.5", true, extra fields and blank names are accepted
  3. "inf" passes gt=0: the client gets 500, the record is saved anyway,
     and GET /items fails until the server restarts
  4. Bare NaN / Infinity in the JSON body: still 500 after the model fix,
     because FastAPI cannot write the 422 error that contains the input
  5. A trap: Query(strict=True) rejects every query parameter

Run:  pip install fastapi httpx  &&  python3 main.py
"""

import warnings
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

warnings.simplefilter("ignore")  # starlette's TestClient deprecation notice
from fastapi.testclient import TestClient  # noqa: E402


def seed():
    return {
        1: {"id": 1, "sku": "SKU-MECH-01", "name": "Mechanical Keyboard", "price": 89.99},
        2: {"id": 2, "sku": "SKU-MOUS-02", "name": "Ergonomic Wireless Mouse", "price": 49.50},
    }


# --- says: project 30, unchanged ---------------------------------------------
def build_says():
    app = FastAPI()
    INVENTORY_DB = seed()
    app.state.db = INVENTORY_DB

    class ItemSchema(BaseModel):
        sku: str = Field(..., min_length=3)
        name: str = Field(..., min_length=1)
        price: float = Field(..., gt=0.0)

    @app.get("/items")
    async def get_all_items(limit: int = 10, skip: int = 0):
        items_list = list(INVENTORY_DB.values())
        return items_list[skip: skip + limit]

    @app.post("/items", status_code=status.HTTP_201_CREATED)
    async def create_item(payload: ItemSchema):
        for item in INVENTORY_DB.values():
            if item["sku"] == payload.sku:
                raise HTTPException(status_code=400, detail=f"An item with SKU '{payload.sku}' already exists.")
        new_id = max(INVENTORY_DB.keys()) + 1 if INVENTORY_DB else 1
        new_item = {"id": new_id, "sku": payload.sku, "name": payload.name, "price": payload.price}
        INVENTORY_DB[new_id] = new_item
        return new_item

    return app


# --- checks: the corrected version ------------------------------------------
def build_checks(error_handler=True):
    app = FastAPI()
    INVENTORY_DB = seed()
    app.state.db = INVENTORY_DB

    class ItemSchema(BaseModel):
        # strict: no "12.5" -> 12.5, no true -> 1.0 (a JSON integer is still a valid float)
        # extra="forbid": unknown fields are an error, not silently dropped
        # str_strip_whitespace: "   " becomes "" and fails min_length
        model_config = ConfigDict(strict=True, extra="forbid", str_strip_whitespace=True)

        sku: str = Field(..., min_length=3, max_length=32, pattern=r"^[A-Z0-9-]+$")
        name: str = Field(..., min_length=1, max_length=200)
        price: float = Field(..., gt=0, le=1_000_000, allow_inf_nan=False)

    @app.get("/items")
    async def get_all_items(
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
        skip: Annotated[int, Query(ge=0)] = 0,
    ):
        items_list = list(INVENTORY_DB.values())
        return items_list[skip: skip + limit]

    @app.post("/items", status_code=status.HTTP_201_CREATED)
    async def create_item(payload: ItemSchema):
        for item in INVENTORY_DB.values():
            if item["sku"] == payload.sku:
                raise HTTPException(status_code=400, detail=f"An item with SKU '{payload.sku}' already exists.")
        new_id = max(INVENTORY_DB.keys()) + 1 if INVENTORY_DB else 1
        new_item = {"id": new_id, "sku": payload.sku, "name": payload.name, "price": payload.price}
        INVENTORY_DB[new_id] = new_item
        return new_item

    if error_handler:
        # The default 422 response echoes the rejected input. A bare NaN or
        # Infinity in the body cannot be written back as JSON, so the error
        # response itself crashes with 500. Leave the input out.
        @app.exception_handler(RequestValidationError)
        async def validation_error(request: Request, exc: RequestValidationError):
            errors = [{k: v for k, v in e.items() if k not in ("input", "ctx")} for e in exc.errors()]
            return JSONResponse(status_code=422, content={"detail": jsonable_encoder(errors)})

    return app


# --- helpers ---------------------------------------------------------------
def client(app):
    return TestClient(app, raise_server_exceptions=False)


def short(response, width=58):
    text = response.text
    if response.status_code == 422:
        err = response.json()["detail"][0]
        text = f'{err["type"]} at {".".join(str(p) for p in err["loc"])}'
    elif response.headers.get("content-type", "").startswith("application/json"):
        data = response.json()
        if isinstance(data, list):
            text = "ids " + str([row["id"] for row in data])
    return (text[: width - 3] + "...") if len(text) > width else text


def post(c, raw):
    return c.post("/items", content=raw, headers={"content-type": "application/json"})


def row(label, response):
    print(f"  {label:9} {response.status_code}  {short(response)}")


def main():
    import fastapi
    import pydantic
    import sys

    print(f"Python {sys.version.split()[0]}, fastapi {fastapi.__version__}, pydantic {pydantic.VERSION}")

    print("\n== 1. Pagination ==")
    for url in ["/items?limit=-1", "/items?skip=-1", "/items?limit=1000000000"]:
        print(f"  GET {url}")
        row("says", client(build_says()).get(url))
        row("checks", client(build_checks()).get(url))

    print("\n== 2. Lax types ==")
    bodies = [
        '{"sku":"SKU-A1","name":"Cable","price":"12.5"}',
        '{"sku":"SKU-A2","name":"Cable","price":true}',
        '{"sku":"SKU-A3","name":"Cable","price":12}',
        '{"sku":"SKU-A4","name":"   ","price":5}',
        '{"sku":"SKU-A5","name":"Cable","price":5,"discount":90}',
        '{"sku":" SKU-MECH-01","name":"Cable","price":5}',
    ]
    for raw in bodies:
        print(f"  POST {raw}")
        row("says", post(client(build_says()), raw))
        row("checks", post(client(build_checks()), raw))

    print('\n== 3. "inf" passes gt=0 ==')
    for name, app in [("says", build_says()), ("checks", build_checks())]:
        c = client(app)
        row(name, post(c, '{"sku":"SKU-INF","name":"Cable","price":"inf"}'))
        print(f"  {'':9} records now: {len(app.state.db)}")
        row("GET", c.get("/items"))
        row("GET", c.get("/items?limit=2"))

    print("\n== 4. Bare NaN / Infinity in the body ==")
    variants = [
        ("says", build_says),
        ("model", lambda: build_checks(error_handler=False)),
        ("checks", build_checks),
    ]
    for raw in ['{"sku":"SKU-N1","name":"Cable","price":NaN}',
                '{"sku":"SKU-N2","name":"Cable","price":Infinity}',
                '{"sku":"SKU-N3","name":"Cable","price":1e999}']:
        print(f"  POST {raw}")
        for name, build in variants:
            app = build()
            c = client(app)
            r = post(c, raw)
            print(f"  {name:9} {r.status_code}  {short(r, 40):40} records: {len(app.state.db)}")
    print("  (model = corrected model without the error handler)")

    print("\n== 5. Query(strict=True) ==")
    trap = FastAPI()

    @trap.get("/items")
    async def strict_limit(limit: Annotated[int, Query(strict=True, ge=1)] = 10):
        return {"limit": limit}

    row("strict", client(trap).get("/items?limit=5"))
    row("checks", client(build_checks()).get("/items?limit=5"))


if __name__ == "__main__":
    main()

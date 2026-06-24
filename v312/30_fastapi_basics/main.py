# Author: Ahmet Aksoy
# Date: 22.05.2026
# Python3.12 Ubuntu 24.04

"""
FastAPI Basics Example
Demonstrates how to construct an asynchronous REST API utilizing Pydantic 
data schemas, automatic validation, and native path/query parameter handling.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Inventory Management API",
    description="A foundational async REST API demonstrating FastAPI features",
    version="1.0.0"
)

# --- In-Memory Mock Database ---
# Using a dictionary to simulate data persistence for our endpoints
INVENTORY_DB = {
    1: {"id": 1, "sku": "SKU-MECH-01", "name": "Mechanical Keyboard", "price": 89.99},
    2: {"id": 2, "sku": "SKU-MOUS-02", "name": "Ergonomic Wireless Mouse", "price": 49.50},
}


# --- Pydantic Data Models (Request Validation Schemas) ---
class ItemSchema(BaseModel):
    sku: str = Field(..., min_length=3, description="The unique stock keeping unit string identifier")
    name: str = Field(..., min_length=1, description="The commercial name of the item")
    price: float = Field(..., gt=0.0, description="The unit price must be greater than zero")


# --- API Routes / Endpoints ---

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Simple root health-check endpoint."""
    return {"status": "online", "message": "Welcome to the FastAPI Inventory System"}


@app.get("/items", status_code=status.HTTP_200_OK)
async def get_all_items(limit: int = 10, skip: int = 0):
    """
    Retrieves all records with built-in query parameter pagination.
    Example: /items?limit=5&skip=0
    """
    items_list = list(INVENTORY_DB.values())
    return items_list[skip : skip + limit]


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item_by_id(item_id: int):
    """Retrieves a single item using an explicit path parameter."""
    if item_id not in INVENTORY_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} does not exist."
        )
    return INVENTORY_DB[item_id]


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemSchema):
    """
    Creates a new item record. The payload body is automatically validated
    against ItemSchema definitions before this routine executes.
    """
    # Simple conflict verification check
    for item in INVENTORY_DB.values():
        if item["sku"] == payload.sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An item with SKU '{payload.sku}' already exists."
            )
            
    # Auto-generate incremental integer primary key
    new_id = max(INVENTORY_DB.keys()) + 1 if INVENTORY_DB else 1
    
    new_item = {
        "id": new_id,
        "sku": payload.sku,
        "name": payload.name,
        "price": payload.price
    }
    
    INVENTORY_DB[new_id] = new_item
    return new_item


# --- Driver Configuration ---
if __name__ == "__main__":
    import uvicorn
    print("Launching API Web Server locally...")
    # Run the server programmatically on localhost:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

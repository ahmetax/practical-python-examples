# Author: Ahmet Aksoy
# Date: 21.05.2026
# Python3.12 Ubuntu 24.04

"""
Asyncio Basics Example
Demonstrates asynchronous programming in Python using async/await syntax
and the modern asyncio.TaskGroup (introduced in Python 3.11) for concurrency.
"""

import asyncio
import time


async def fetch_product_details(product_id: int) -> dict:
    """Simulates fetching basic product info from a database/API."""
    print(f"[Product] Fetching details for ID {product_id}...")
    # Simulate network latency (I/O bound delay) without blocking the thread
    await asyncio.sleep(1.5)
    print(f"[Product] Done fetching details for ID {product_id}.")
    return {"id": product_id, "name": "Premium Wireless Mouse", "price": 49.99}


async def fetch_stock_status(product_id: int) -> dict:
    """Simulates checking real-time warehouse inventory."""
    print(f"[Stock] Checking inventory for ID {product_id}...")
    await asyncio.sleep(1.0)
    print(f"[Stock] Done checking inventory for ID {product_id}.")
    return {"id": product_id, "in_stock": True, "quantity": 142}


async def fetch_user_reviews(product_id: int) -> list:
    """Simulates retrieving customer ratings and text reviews."""
    print(f"[Reviews] Gathering customer reviews for ID {product_id}...")
    await asyncio.sleep(2.0)
    print(f"[Reviews] Done gathering reviews for ID {product_id}.")
    return [{"user": "Alice", "rating": 5}, {"user": "Bob", "rating": 4}]


async def main():
    product_id = 99
    start_time = time.perf_counter()
    
    print(f"--- Starting Concurrent Tasks for Product ID {product_id} ---")

    # Python 3.11+ TaskGroup manages multiple concurrent tasks safely.
    # If one task fails, it automatically cancels the others.
    async with asyncio.TaskGroup() as tg:
        # tg.create_task schedules the coroutine to run concurrently
        task_details = tg.create_task(fetch_product_details(product_id))
        task_stock = tg.create_task(fetch_stock_status(product_id))
        task_reviews = tg.create_task(fetch_user_reviews(product_id))

    # Once the context manager blocks ends, all tasks are guaranteed to be finished.
    product_info = task_details.result()
    stock_info = task_stock.result()
    reviews_info = task_reviews.result()

    # Consolidate the aggregated results
    aggregated_data = {
        **product_info,
        **stock_info,
        "reviews": reviews_info
    }

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("\n--- Aggregated Result ---")
    print(aggregated_data)
    # The total elapsed time will be roughly equal to the SLOWEST task (2.0s),
    # instead of the sum of all tasks (1.5 + 1.0 + 2.0 = 4.5s).
    print(f"\nSuccessfully fetched all data in: {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    print("--- Asyncio Testing Started ---\n")
    # Run the main async entry point
    asyncio.run(main())

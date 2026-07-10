# Author: Ahmet Aksoy
# Date: 26.05.2026
# Python3.12 Ubuntu 24.04

"""
Asyncio Basics Example
Demonstrates single-threaded, non-blocking concurrent I/O processing
using the modern async/await event loop pattern in Python.
"""

import asyncio
import time


async def simulate_network_fetch(server_name: str, delay_seconds: int) -> dict:
    """
    An asynchronous coroutine that simulates fetching data from a remote API.
    Utilizes 'await asyncio.sleep' to release control back to the event loop,
    allowing other tasks to execute while waiting.
    """
    print(f"[Fetch {server_name}] Initiating connection... (Will take {delay_seconds}s)")
    
    # Non-blocking pause: The event loop shifts to other tasks during this window
    await asyncio.sleep(delay_seconds)
    
    print(f"[Fetch {server_name}] Data packet downloaded successfully.")
    return {"server": server_name, "status": 200, "payload": "Success Data"}


async def main() -> None:
    """Master coroutine coordinating concurrent task execution streams."""
    print("--- Asyncio Non-Blocking Event Loop Active ---\n")
    
    start_time = time.time()

    # 1. Schedule multiple asynchronous coroutine tasks to run concurrently
    task1 = asyncio.create_task(simulate_network_fetch("API-Gateway-Europe", 3))
    task2 = asyncio.create_task(simulate_network_fetch("Database-Cluster-US", 2))
    task3 = asyncio.create_task(simulate_network_fetch("Cache-Node-Asia", 1))

    print("--> All network tasks scheduled onto the event loop thread. <--\n")

    # 2. Gather task promises and await their joint resolution
    # asyncio.gather fires them off concurrently and aggregates responses
    results = await asyncio.gather(task1, task2, task3)
    
    print(f"\nAll resolved packet responses: {results}")
    
    duration = time.time() - start_time
    print(f"\nTotal elapsed non-blocking pipeline duration: {duration:.4f} seconds.")


if __name__ == "__main__":
    # Initialize and execute the asynchronous master event loop
    asyncio.run(main())
# Project 25: Asyncio Basics & Structured Concurrency

A foundational implementation of non-blocking I/O routines using Python's standard `asyncio` ecosystem. This example demonstrates modern asynchronous design patterns using `async/await` and safe context pooling via structured task orchestration.

## Architectural Goal
The application simulates an aggregation router for an e-commerce platform. It needs to query multiple disparate upstream microservices concurrently—fetching individual Core Product Details, checking Real-time Inventory Stocks, and grabbing Public Customer Reviews—minimizing final transaction latencies by executing non-dependent bottlenecks simultaneously.

## Project Structure
```text
25_asyncio_basics/
└── main.py
System Requirements
OS: Ubuntu 24.04

Runtime: Python 3.11+ (Required for asyncio.TaskGroup context syntax)

Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Establish the project directory:

```bash
mkdir 25_asyncio_basics
cd 25_asyncio_basics

### Step 2: Implement the Non-Blocking Pipeline
Create main.py and manage task executions through these systematic layers:

Simulate Async I/O Invocations: Write independent coroutines using the async def descriptor for each microservice boundary. Use await asyncio.sleep() to introduce varying artificial execution latency gaps (e.g., 1.0s, 1.5s, 2.0s) mimicking database or web service calls without freezing the main execution thread.

Utilize Task Pools: In your primary async orchestrator function (async def main()), instantiate an isolated execution scope using Python 3.11+'s advanced context manager: async with asyncio.TaskGroup() as tg:.

Schedule Concurrency: Register individual queries into the group manager via tg.create_task(). This prompts the internal event loop to schedule all operations to fire down parallel tracks concurrently.

Consume Aggregations: Once execution exits the TaskGroup context block, all registered tasks are structurally guaranteed to have finalized safely. Extract their computed dataset payloads using .result() and merge them into a single comprehensive dictionary payload.

### Step 3: Performance Verification
Wrap the runtime inside a benchmarking clock tracking differences via time.perf_counter(). Notice how the absolute final processing time matches the speed of your single slowest task (~2.0 seconds) rather than compounding sequentially (1.5 + 1.0 + 2.0 = 4.5 seconds).

```bash
python main.py



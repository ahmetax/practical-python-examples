# Project 26: Benchmarking Multiprocessing vs Threading

A practical optimization benchmark analyzing the clear computational boundaries between Python's high-level execution models: Multi-Threading (I/O-Bound focus) and Multi-Processing (CPU-Bound focus).

## Architectural Goal
The program exposes how Python's Global Interpreter Lock (GIL) impacts runtime. By running a high-load, math-heavy loop (CPU-bound) alongside a parallel web-network connection sequence (I/O-bound) across both resource allocation systems, it establishes concrete reference points on when to select the appropriate scaling model.

## Project Structure
```text
26_multiprocessing_vs_threading/
└── main.py
System Requirements
OS: Ubuntu 24.04 (Multi-core environment recommended)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a fresh project subdirectory:

```bash
mkdir 26_multiprocessing_vs_threading
cd 26_multiprocessing_vs_threading

### Step 2: Build the Benchmarking Core
Create main.py and implement the computational experiments:

Design the Computational Bottleneck: Define a heavy CPU-bound function that performs heavy iteration (e.g., counting upwards to 50,000,000 using standard loops) to consume raw processor processing cycles.

Design the I/O Bottleneck: Define an I/O-bound function that performs lightweight external interactions, such as fetching real-time website headers using Python's native urllib.request.urlopen module.

Utilize High-Level Executors: Instead of manual resource instantiation, import concurrent.futures. This abstract pool manager streamlines multi-threaded workers (ThreadPoolExecutor) and isolated sub-processes (ProcessPoolExecutor) identically.

Coordinate Execution Cross-Exams: Set up a benchmarking framework that runs your tasks across four unique scenarios:

CPU Tasks via Threads: Notice performance throttling as the GIL forces cores to compete sequentially.

CPU Tasks via Processes: Notice performance gains as separate system processes run concurrently across distinct physical CPU cores.

I/O Tasks via Threads: Watch how threads yield execution efficiently during idle network wait times with minimal system overhead.

I/O Tasks via Processes: Observe the operational resource overhead that comes with spinning up separate processes for simple wait states.

### Step 3: Run the Benchmarks
Run the profiling script. The console output yields precise execution durations showcasing which strategy fits each type of processing bottleneck.

```bash
python main.py



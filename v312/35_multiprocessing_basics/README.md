# Project 35: Multiprocessing Foundations

A computational benchmark project demonstrating how to execute parallel, CPU-bound workloads from scratch using Python's standard `multiprocessing` module. This architecture showcases how to spin up independent operating system processes to completely bypass the limitations of Python's Global Interpreter Lock (GIL).

## Architectural Goal
The application shifts away from synchronous execution loops or thread-sharing pools. When handling heavy computational operations (such as mathematical factorials, image rendering, or dataset transformations), standard threads compete for the same execution core due to the GIL. This module maps distinct workloads directly onto isolated operating system processes, forcing true parallel resource usage across all available CPU cores.

## Project Structure
```text
35_multiprocessing_basics/
└── main.py
```
**System Requirements**
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible multi-core environment)
- Runtime: Python 3.12+
- Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated folder for this project inside your repository workspace:

```bash
mkdir 35_multiprocessing_basics
cd 35_multiprocessing_basics
```
### Step 2: Implement the Parallel Computing Engine
Create a file named main.py. Build your concurrent execution layer step-by-step:

Protect the Entrypoint Execution: Always safeguard your execution block with if __name__ == "__main__":. This is mandatory in multiprocessing; when a new process is spawned, it re-imports the main file, and without this guard, the child process would trigger an infinite, recursive loop of spawning more processes.

Draft the Computational Task: Design a CPU-bound mathematical function (e.g., compute_heavy_factorial) that handles dense loops to keep individual processes engaged.

Instantiate and Launch Processes: Loop through your dataset arrays. For each target workload, construct a separate execution tracking worker instance using multiprocessing.Process(target=..., args=...). Invoke .start() on each instance to command the Ubuntu kernel to map out fresh independent execution memory addresses.

Synchronize Main Loop Lifecycles: Iterate through your array of active process objects and call .join() on each worker. This forces the main master daemon process to pause and wait for all concurrent child processes to finish their calculations before finalizing metrics and exiting cleanly.

### Step 3: Run and Verify
Execute the parallel script natively from your terminal interface:

```bash
python3 main.py
```
Watch the terminal outputs carefully. You will see all workers start almost simultaneously, calculating independent numbers concurrently rather than processing them one after another in a linear line.


---

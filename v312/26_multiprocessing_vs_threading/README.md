# Project 26: Multiprocessing vs Threading Benchmark

The script runs the same work with `ThreadPoolExecutor` and with `ProcessPoolExecutor` from `concurrent.futures` and prints how long each took.

| Stage | Work | What to look for |
|-------|------|------------------|
| 1. CPU-bound | Count to 50,000,000 in a Python loop, 4 times | Threads cannot run Python code in parallel because of the GIL; processes can |
| 2. I/O-bound | Open `https://www.example.com` 4 times with `urllib.request` | Most of the time is spent waiting for the network |

## Project Structure
```text
26_multiprocessing_vs_threading/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3 (no version-specific features are used). Tested on 3.12.3.
- No third-party packages.
- Internet access for stage 2.
- A machine with at least 4 CPU cores to see the full effect in stage 1.

## Running
```bash
python3 main.py
```
Stage 1 is slow on purpose: the threaded run takes about as long as four sequential runs. Expect the whole script to take tens of seconds.

## Sample Output (Python 3.12.3, 8 cores)
```text
--- Threading vs Multiprocessing Benchmark Started ---

==================================================
STAGE 1: CPU-Bound Task (Heavy Calculation)
==================================================
Threading (CPU-Bound) Duration       : 31.6311 seconds
Multiprocessing (CPU-Bound) Duration : 7.8416 seconds

==================================================
STAGE 2: I/O-Bound Task (Network Requests)
==================================================
Threading (I/O-Bound) Duration       : 0.2549 seconds
Multiprocessing (I/O-Bound) Duration : 0.1605 seconds
```
Durations depend on the CPU, the system load and the network; the numbers above were measured while the machine was busy with other work, so an idle machine will show lower values. In three runs the CPU-bound stage was consistently about 4 times faster with processes (31.3 s vs 8.5 s, 31.9 s vs 7.9 s, 31.6 s vs 7.8 s). One `cpu_bound_task(50_000_000)` call alone took 8.6 s on the same machine, so the threaded version is no faster than running the four calls one after another.

## How It Works
- **CPU-bound, threads:** The GIL lets only one thread execute Python bytecode at a time, so four threads take roughly four times as long as one task.
- **CPU-bound, processes:** Each worker is a separate process with its own interpreter and its own GIL, so the four tasks run on four cores at once.
- **I/O-bound:** While a thread waits for the network, it releases the GIL, so threads are well suited to this kind of work. In this script, however, the requests to `example.com` are so short (well under a second in total) that both versions finish in a fraction of a second. In the runs above the process version was even slightly faster. The difference is mostly noise and warm-up (the first request pays for DNS lookup and TLS setup); running the four requests sequentially took about the same time (0.24 s). Stage 2 therefore does not show a clear winner.
- `io_bound_task()` returns `404` for any exception (timeout, DNS failure, no internet), and the return values are not printed. Without a network connection the script still prints durations for stage 2, without any warning.
- With no `max_workers` argument, `ThreadPoolExecutor` uses `min(32, CPU count + 4)` threads and `ProcessPoolExecutor` uses one process per CPU. Only 4 of them get work here.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/15/pythonda-hiz-yarisi-multiprocessing-mi-threading-mi/
- `concurrent.futures` documentation: https://docs.python.org/3/library/concurrent.futures.html
- Global Interpreter Lock (glossary): https://docs.python.org/3/glossary.html#term-global-interpreter-lock

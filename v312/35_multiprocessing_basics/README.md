# Project 35: Multiprocessing Basics

A short example of running CPU-bound work in parallel with the standard `multiprocessing` module. Because of the Global Interpreter Lock (GIL), only one thread at a time can run Python code inside a single interpreter. Separate processes each have their own interpreter and their own GIL, so they can use several CPU cores at the same time.

## How It Works
- `compute_heavy_factorial(name, number)` computes `number!` with a plain loop and prints how long it took. Multiplying ever-larger integers keeps one CPU core busy.
- The main block starts four `multiprocessing.Process` objects for 50000!, 55000!, 60000! and 65000!, then waits for all of them with `join()`.
- The total time is printed at the end. The factorial results are thrown away: a `Process` does not pass its function's return value back to the parent (that needs a `Pool` or a `Queue`).
- The `if __name__ == "__main__":` guard is required. With the `spawn` start method (the default on Windows and macOS) and `forkserver` (the default on Linux from Python 3.14), child processes re-import `main.py`; without the guard they would try to start new processes themselves.
- The names `Worker-Core-1` … `Worker-Core-4` are only labels. The code does not pin processes to cores; the operating system decides where each process runs.

## Project Structure
```text
35_multiprocessing_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.6 or newer (f-strings). Tested on 3.12.3, also runs on 3.15.0rc2.
- No third-party packages.
- A machine with at least four CPU cores shows the full effect.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3, 8 logical CPUs)
```text
--- Multiprocessing Computational Engine Initialized ---

[Process Worker-Core-1] Started heavy computation for number: 50000...
[Process Worker-Core-2] Started heavy computation for number: 55000...
--> Successfully launched 4 parallel worker processes. <--

[Process Worker-Core-3] Started heavy computation for number: 60000...
[Process Worker-Core-4] Started heavy computation for number: 65000...
[Process Worker-Core-1] Finished in 1.2742 seconds.
[Process Worker-Core-2] Finished in 1.5521 seconds.
[Process Worker-Core-3] Finished in 1.9207 seconds.
[Process Worker-Core-4] Finished in 2.3087 seconds.

--- Parallel Computational Lifecycle Concluded ---
Total processing block completion time: 2.3172 seconds.
```
Times depend on the machine and its load, and the order of the lines may change between runs. If you redirect the output to a file or a pipe (`python3 main.py | cat`), each child prints its "Started" and "Finished" lines together when it exits, because output is buffered when it is not going to a terminal.

How much faster is it? Measured on an Intel i7-7700HQ (4 cores, 8 threads, `nproc` = 8) while other programs were also running:

| Method | Total time |
|--------|-----------|
| Four calls one after another | 5.9–6.3 s |
| Four threads (`threading.Thread`) | 6.7–7.0 s |
| Four processes (this project) | 2.3–2.8 s |

Processes are about 2.2–2.7 times faster here, not 4 times. Each process does a different amount of work, so the total time is set by the largest job (65000!), and starting processes has a small cost. Threads are no faster than the plain loop, which shows the effect of the GIL.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/09/10/pythonda-gil-duvarini-yikmak-multiprocessing-ile-gercek-paralellik/
- `multiprocessing` documentation: https://docs.python.org/3/library/multiprocessing.html

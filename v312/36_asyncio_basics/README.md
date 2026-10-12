# Project 36: Asyncio Basics

A short example of running I/O-bound work concurrently with the standard `asyncio` module. Three simulated network requests that take 3, 2 and 1 seconds finish in about 3 seconds in total instead of 6, all in a single thread. No real network access takes place; `asyncio.sleep()` stands in for the waiting time.

## How It Works
- `simulate_network_fetch(server_name, delay_seconds)` is a coroutine (`async def`). It prints a message, waits with `await asyncio.sleep(delay_seconds)`, then returns a dictionary.
- While a coroutine is waiting at `await`, the event loop runs the other tasks. A blocking `time.sleep()` would stop the whole program instead.
- `main()` wraps three coroutines in `asyncio.create_task()`. The tasks are only scheduled at this point; they start running when `main()` reaches its first `await`. That is why the "All network tasks scheduled" line is printed before any "Initiating connection" line.
- `await asyncio.gather(task1, task2, task3)` waits for all three tasks. The shortest task (1 s) finishes first, but `gather` returns the results in the order the tasks were passed in, not in the order they finished.
- `asyncio.run(main())` creates the event loop, runs `main()` and closes the loop.

## Project Structure
```text
36_asyncio_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.7 or newer (`asyncio.run()` and `asyncio.create_task()` were added in 3.7). Tested on 3.12.3.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Asyncio Non-Blocking Event Loop Active ---

--> All network tasks scheduled onto the event loop thread. <--

[Fetch API-Gateway-Europe] Initiating connection... (Will take 3s)
[Fetch Database-Cluster-US] Initiating connection... (Will take 2s)
[Fetch Cache-Node-Asia] Initiating connection... (Will take 1s)
[Fetch Cache-Node-Asia] Data packet downloaded successfully.
[Fetch Database-Cluster-US] Data packet downloaded successfully.
[Fetch API-Gateway-Europe] Data packet downloaded successfully.

All resolved packet responses: [{'server': 'API-Gateway-Europe', 'status': 200, 'payload': 'Success Data'}, {'server': 'Database-Cluster-US', 'status': 200, 'payload': 'Success Data'}, {'server': 'Cache-Node-Asia', 'status': 200, 'payload': 'Success Data'}]

Total elapsed non-blocking pipeline duration: 3.0018 seconds.
```
The total time was between 3.0007 and 3.0020 seconds in five runs. Run one after another, the same three waits would take 6 seconds.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/09/14/pythonda-asyncio-beklerken-diger-isleri-yapan-kod-nasil-yazilir/
- `asyncio` documentation: https://docs.python.org/3/library/asyncio.html

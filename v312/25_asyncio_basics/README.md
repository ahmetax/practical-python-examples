# Project 25: Asyncio Basics with TaskGroup

Three coroutines simulate slow calls for one product: product details (1.5 s), stock status (1.0 s) and user reviews (2.0 s). The delays are produced with `asyncio.sleep()`; there is no real network or database access. The coroutines are started together inside an `asyncio.TaskGroup`, so the whole run takes about as long as the slowest one (2.0 s) instead of the sum (4.5 s). The results are then merged into one dictionary.

## Project Structure
```text
25_asyncio_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.11 or newer (`asyncio.TaskGroup` was added in 3.11). On 3.10 the script fails with `AttributeError: module 'asyncio' has no attribute 'TaskGroup'`. Tested on 3.12.3; also runs on 3.11.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Asyncio Testing Started ---

--- Starting Concurrent Tasks for Product ID 99 ---
[Product] Fetching details for ID 99...
[Stock] Checking inventory for ID 99...
[Reviews] Gathering customer reviews for ID 99...
[Stock] Done checking inventory for ID 99.
[Product] Done fetching details for ID 99.
[Reviews] Done gathering reviews for ID 99.

--- Aggregated Result ---
{'id': 99, 'name': 'Premium Wireless Mouse', 'price': 49.99, 'in_stock': True, 'quantity': 142, 'reviews': [{'user': 'Alice', 'rating': 5}, {'user': 'Bob', 'rating': 4}]}

Successfully fetched all data in: 2.00 seconds.
```
The measured time was 2.00 seconds on both Python 3.12.3 and 3.11. Since the work is only `asyncio.sleep()`, the result stays very close to 2.0 seconds on any machine.

## How It Works
- `async with asyncio.TaskGroup() as tg:` opens a group; each `tg.create_task(...)` schedules a coroutine immediately. All three "Fetching/Checking/Gathering" lines are printed before any of them finishes.
- While one coroutine waits in `await asyncio.sleep(...)`, the event loop runs the others. Everything runs in a single thread; this is concurrency, not parallelism.
- The `Done` lines appear in order of delay: stock (1.0 s), product (1.5 s), reviews (2.0 s).
- The `async with` block does not exit until every task has finished, so `.result()` can be called safely afterwards. If one task raises an exception, the group cancels the remaining tasks and raises the error as an `ExceptionGroup`.
- `{**product_info, **stock_info, "reviews": ...}` merges the dictionaries. Both contain the key `id`, so the later value wins (both are 99 here).

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/10/python-asyncio-ile-hizlanin-modern-eszamanlilik-ve-taskgroup/
- `asyncio` task groups: https://docs.python.org/3/library/asyncio-task.html#task-groups

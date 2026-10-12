# Project 43: Python Decorators Tour

A runnable walkthrough of decorators: what the `@` syntax really does and how to write your own. `@timer` above a function is shorthand for `slow_sum = timer(slow_sum)`.

| # | Topic | Key idea |
|---|-------|----------|
| 1 | Functions as objects and closures | `make_multiplier(2)` remembers `factor` |
| 2 | A first decorator that measures runtime | `@timer` with `*args, **kwargs` |
| 3 | Keeping the original name and docstring | `functools.wraps` |
| 4 | Decorators with arguments | `@retry(times=3, exceptions=(ConnectionError,))` |
| 5 | Built-in memoization (with call counts and timings) | `@functools.cache` on Fibonacci |
| 6 | Registering functions without wrapping them | `@command("name")` registry |
| 7 | Stacking decorators | the decorator closest to the function is applied first |

## Project Structure
```text
43_decorators/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (`functools.cache` was added in 3.9). Tested on 3.12.3.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
== 4. @retry(times=3) ==
[retry] fetch_rates deneme 1/3 başarısız: sunucu yanıt vermedi
[retry] fetch_rates deneme 2/3 başarısız: sunucu yanıt vermedi
sonuç        : {'USD': 41.6, 'EUR': 48.4}
ValueError yeniden denenmedi: could not convert string to float: 'kırk iki'

== 5. @functools.cache ==
fib(30) önbelleksiz: 832040, 2,692,537 çağrı,    776.3 ms
fib(30) önbellekli : 832040,        31 çağrı,    0.029 ms
cache_info   : CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```
Output labels are in Turkish to match the accompanying blog post. The exchange rates come from a simulated server that fails twice before answering. Timings depend on the machine; call counts are the same everywhere.

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/10/15/pythonda-dekoratorler-isaretinin-arkasinda-ne-var/
- `functools` documentation: https://docs.python.org/3/library/functools.html
- PEP 318: Decorators for Functions and Methods

# Project 44: Python Context Managers Tour

A runnable walkthrough of the `with` statement: how context managers guarantee that files, connections and other resources are released even when an error occurs, and how to write your own.

| # | Topic | Key API |
|---|-------|---------|
| 1 | A file left open after an error (the problem) | `try/except` without `finally` |
| 2 | Files closing themselves even on errors | `with open(...)` |
| 3 | A class-based timer | `__enter__`, `__exit__` |
| 4 | Ignoring one specific error on purpose | `contextlib.suppress` |
| 5 | Generator-based context managers | `@contextlib.contextmanager`, `contextlib.chdir` |
| 6 | Transactions: `with conn` commits or rolls back but does not close | `sqlite3.connect(..., autocommit=False)`, `contextlib.closing` |
| 7 | A variable number of resources in one block | `contextlib.ExitStack` |

## Project Structure
```text
44_context_managers/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.12 or newer (the `autocommit` parameter of `sqlite3.connect` was added in 3.12). Tested on 3.12.3 (Ubuntu 24.04) and 3.12.15 (Docker `python:3.12-slim`).
- No third-party packages. All files are created in a temporary directory.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
== 6. sqlite3 ve with ==
hata         : CHECK constraint failed: sayfa > 0
kayıtlar     : ['Kuyucaklı Yusuf']
with sonrası bağlantı hâlâ açık: sorgu çalıştı
closing ile  : Cannot operate on a closed database.
son durum    : ['Kuyucaklı Yusuf', 'Çalıkuşu']
```
Output labels are in Turkish to match the accompanying blog post. Timings depend on the machine; all other output is the same everywhere.

## Note on sqlite3 Transactions
Without `autocommit=False`, sqlite3 uses its legacy transaction mode and decides from the first word of the statement whether to open a transaction implicitly. In Python 3.11 and 3.12 that check uses the locale-dependent C `tolower()`. Under a Turkish locale (`tr_TR.UTF-8`) `tolower('I')` is not `'i'`, so `INSERT` is not recognised, no `BEGIN` is sent and the failed `with conn:` block in section 6 does **not** roll back. Lower-case `insert`, `UPDATE`, `DELETE` and `REPLACE` are unaffected. Tested on the same machine with `LC_ALL=tr_TR.UTF-8` (fails) and `LC_ALL=C.UTF-8` (works), and in Docker: 3.11.17 and 3.12.15 fail under `tr_TR.UTF-8`, 3.13.16 and 3.14.8 work (fixed by [gh-108767](https://github.com/python/cpython/issues/108767)). With `autocommit=False` every locale behaves the same, which is why the example uses it.

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/10/19/dogru-gorunen-kod-yanlis-sonuc-pythonda-with-ve-sqlite3-tuzagi/
- `contextlib` documentation: https://docs.python.org/3/library/contextlib.html
- sqlite3 transaction control: https://docs.python.org/3/library/sqlite3.html#sqlite3-transaction-control
- PEP 343: The "with" Statement

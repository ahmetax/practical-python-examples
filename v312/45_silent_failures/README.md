# Project 45: Silent Failures — Code That Says "Success" Without Checking

While rewriting the READMEs of projects 23–41 we ran every script and found five places where the code reports success (or a plausible status) without checking it. This project reproduces each pattern twice: the version that only **says** it worked and the version that **checks**.

| # | Pattern | Found in | The check |
|---|---------|----------|-----------|
| 1 | Prints an error, exits with code 0 | 37, 39 | `sys.exit(message)` → exit code 1 |
| 2 | Overwrites an existing file without warning | 37 | refuse if destination exists |
| 3 | Turns every exception into "404" | 26 | separate `HTTPError` (server answered) from `URLError` (no answer) |
| 4 | Status text hard-coded in the source | 34 | read it: `importlib.metadata.version`, `sys.prefix` |
| 5 | Prints "rolled back" without looking | 29 | count the rows after the failure; `autocommit=False` |

## Project Structure
```text
45_silent_failures/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.12 or newer (`sqlite3.connect(..., autocommit=False)`). Tested with Python 3.12.3 (Ubuntu 24.04) and 3.12.15 (Docker `python:3.12-slim`, `--network none`).
- No third-party packages, no network access needed. Files are created in a temporary folder and removed at the end.

## Run
```bash
python3 main.py
```

## Sample Output (Python 3.12.3, Ubuntu 24.04, LC_CTYPE=tr_TR.UTF-8)
```text
--- Silent Failures Demo ---

== 1. Exit code ==
  says  : exit code 0 -> 'cmd && next' continues
  checks: exit code 1 -> 'cmd && next' stops

== 2. Overwrite ==
  says  : moved                      report.txt now: 'new report'
  checks: refused (FileExistsError)  report.txt now: 'OLD report, only copy'

== 3. Error -> 404 ==
  says  : 404
  checks: no response: [Errno -2] Name or service not known

== 4. Hard-coded status ==
  says  : Rich Library Status -> Successfully Resolved via Poetry
  checks: rich 13.7.1, virtualenv: False, POETRY_ACTIVE=-

== 5. 'rolled back' ==
  Python 3.12.3, LC_CTYPE=tr_TR.UTF-8
  says          : rolled back
  checks        : NOT rolled back, 1 row(s) left
  checks + fixed: rolled back
```
- Section 3's error text depends on the resolver (`[Errno -3] Temporary failure in name resolution` in Docker without network).
- Section 4 shows whatever is really installed (`rich NOT INSTALLED` in a clean container).
- Section 5 only shows the failure where the `tr_TR.UTF-8` locale exists and Python is 3.11/3.12 (see project 44, [gh-108767](https://github.com/python/cpython/issues/108767)). Elsewhere all three lines say `rolled back`, and the script prints a note.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/10/26/tamamlandi-diyen-kod-kontrol-etmeden-basari-bildiren-bes-ornek/
- Projects with the original code: 26, 29, 34, 37, 39 in this repository
- `sys.exit`: https://docs.python.org/3/library/sys.html#sys.exit
- `urllib.error`: https://docs.python.org/3/library/urllib.error.html

# Project 41: Python 3.15 Feature Tour

A runnable walkthrough of the headline features in Python 3.15 (final release scheduled for 9 October 2026).

| # | Feature | PEP |
|---|---------|-----|
| 1 | `frozendict`: immutable, hashable dictionary builtin | PEP 814 |
| 2 | `*` / `**` unpacking inside comprehensions | PEP 798 |
| 3 | `sentinel()` builtin for unique marker values | PEP 661 |
| 4 | UTF-8 as the default text encoding | PEP 686 |
| 5 | `lazy import` / `lazy from ... import` (with a startup benchmark) | PEP 810 |

## Project Structure
```text
41_python315_features/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.15 (3.15.0rc2 or newer). No third-party packages.
- The script exits with a message on older interpreters.

## Running

**With Docker (no local install needed):**
```bash
docker run --rm -v "$PWD":/app -w /app python:3.15-rc-slim python main.py
```

**With uv** (update uv first with `uv self update`; older uv versions only offer 3.15 betas):
```bash
uv python install 3.15
uv run --python 3.15 main.py
```

## Sample Output (3.15.0rc2, Docker)
```text
=== 5. Lazy imports ===
eager imports :  164.2 ms
lazy imports  :   20.7 ms  (7.9x faster startup)
```
Timings depend on the machine; the ratio is what matters.

## Further Reading
- What's New in Python 3.15: https://docs.python.org/3.15/whatsnew/3.15.html

# Project 28: Parsing Log Lines with Regular Expressions

Turns a block of plain-text log lines into Python dictionaries with a single regular expression, using only the standard `re` and `json` modules.

| Technique | Where it is used |
|-----------|------------------|
| Named groups `(?P<name>...)` and `match.groupdict()` | `parse_system_logs()` |
| `re.MULTILINE`, so `^` and `$` match at every line | both functions |
| Optional group `(?:...)?` for the `[code:NNN]` suffix | `parse_system_logs()` |
| Lazy quantifier `.+?` so the message does not swallow the code | `parse_system_logs()` |
| Positive lookahead `(?=...)` plus `re.IGNORECASE` | `extract_critical_failures_with_lookahead()` |

## How It Works
Each log line has the form:
```text
[2026-05-22 08:30:15,123] [ERROR] [auth.service] (192.168.1.50) - Invalid credentials provided [code:401]
```
- `parse_system_logs()` walks the text with `finditer()` and turns each match into a dictionary with the keys `timestamp`, `level`, `component`, `ip_address`, `message` and `status_code`. `status_code` is converted to `int`, or set to `None` when the line has no `[code:...]` part.
- `extract_critical_failures_with_lookahead()` returns whole lines that contain `[database]` anywhere and also contain `denied` or `failed` (case-insensitive). In the sample data only one line meets both conditions; the `payment.gateway` line contains `failed` but is not a database line.

Limits worth knowing (checked by running the functions with extra inputs):
- Lines that do not match are skipped silently. A `[DEBUG]` line, for example, is not in the allowed levels (`INFO|WARNING|ERROR|CRITICAL`) and simply does not appear in the result.
- The IP pattern `\d{1,3}(?:\.\d{1,3}){3}` checks the shape only; `999.300.1.1` is accepted.
- With Windows line endings (`\r\n`), `$` matches after the `\r`, so the code group no longer fits: the message becomes `'Invalid credentials provided [code:401]\r'` and `status_code` is `None`. Use `splitlines()` or strip `\r` before parsing such files.
- The lookahead checks for `[database]` anywhere in the line, so a line whose message mentions `[database]` also matches.

## Project Structure
```text
28_regex_mastery/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (the `list[dict]` type hints need 3.9). Tested on Python 3.12.3 (Ubuntu 24.04).
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Advanced Regex Analytical Engine Started ---

=== 1. Parsing Full Log Stack via Named Capture Groups ===
[
  {
    "timestamp": "2026-05-22 08:30:12,001",
    "level": "INFO",
    "component": "web.server",
    "ip_address": "192.168.1.10",
    "message": "Connection established successfully",
    "status_code": null
  },
  {
    "timestamp": "2026-05-22 08:30:15,123",
    "level": "ERROR",
    "component": "auth.service",
    "ip_address": "192.168.1.50",
    "message": "Invalid credentials provided",
    "status_code": 401
  }
]
Total structured log profiles extracted: 6
-----------------------------------------------------------------

=== 2. Filtering Specific Contexts using Lookaheads ===
Targeting lines matching 'database' containing failures ('denied' / 'failed'):
  Match #1: [2026-05-22 08:31:05,890] [CRITICAL] [database] (10.0.0.5) - Access denied for user 'admin_app' [code:1045]
-----------------------------------------------------------------
```
Only the first two of the six parsed records are printed.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/22/pythonda-regex-ustalik-sinifi-karmasik-log-dosyalarini-duzenli-veriye-donusturmek/
- `re` documentation: https://docs.python.org/3/library/re.html
- Regular Expression HOWTO: https://docs.python.org/3/howto/regex.html

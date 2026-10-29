# Project 50: Version Matrix — Does "Requires Python 3.12+" Hold?

A small tool that runs a project folder under the official `python:X-slim` Docker images (3.8 to 3.15 by default) and reports, for every version, whether the code **compiles** and whether `main.py` **runs**. The lowest version that runs is the project's real minimum; compare it with the version line in the README.

We used it on projects 23–32, 35–38 and 41 of this repository. The three claims that named a reason ("3.10+ for `match`", "3.11+ for `asyncio.TaskGroup`", "3.12+ for PEP 695") were right. None of the ten claims that only said "Runtime: Python 3.12+" were: six of those projects run on 3.8, four on 3.9.

## How It Works
For each version the tool starts a container with networking disabled, mounts the project read-only at `/src`, copies it to `/tmp/app` (so scripts that write files still work) and then:

1. passes every `.py` file to `compile()` — a `SyntaxError` here means the syntax does not exist in that version;
2. runs `main.py` (stdin closed, optional arguments) and records the exit code and the last line of stderr.

| Result | Meaning |
|--------|---------|
| `ok` | exit code 0 |
| `SyntaxError` | a file does not compile in that version |
| `ImportError`, `TypeError`, … | compiles, but stops at run time (e.g. `list[str]` on 3.8) |
| `timeout (no answer)` | no result within `--timeout`; **not** proof of incompatibility |

## Project Structure
```text
50_version_matrix/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.8 or newer (the tool checked itself with `--args=--help` on 3.8, 3.9 and 3.15; vermin reports 3.7). Standard library only.
- Docker. Images are pulled on first use (about 120 MB each on disk).

## Usage
```bash
python3 main.py ../38_regex_validation
python3 main.py ../37_argparse_cli --args=--help
python3 main.py ../26_multiprocessing_vs_threading --versions 3.9,3.10 --timeout 600 -v
```

- `--versions` comma-separated image tags (default `3.8,…,3.15`; `3.15-rc` also works)
- `--timeout` seconds per run (default 300)
- `--args` arguments passed to every `main.py`
- `-v` also prints the raw error line

## Sample Output (Python 3.12.3 host, Docker images 3.8–3.15.2)
```text
== 32_data_structures_bin_tree ==
  3.8    ImportError
  3.9    ImportError
  3.10   ImportError
  3.11   ok
  3.12   ok
  3.13   ok
  3.14   ok
  3.15   ok
  lowest version that runs: 3.11

== 24_advanced_type_hinting ==
  3.8    SyntaxError
  3.9    SyntaxError
  3.10   SyntaxError
  3.11   SyntaxError
  3.12   ok
  3.13   ok
  3.14   ok
  3.15   ok
  lowest version that runs: 3.12
```

## Limitations
- **"ok" is not "correct".** The tool only looks at the exit code. Project 29 exits with 0 everywhere, yet on a Turkish-locale machine Python 3.11 and 3.12 leave wrong data behind (the images use `C.UTF-8`). Project 26 exits with 0 without a network because it turns every error into "404". Run the project's own tests per version if you need correctness.
- **Third-party packages are not installed.** For such projects install inside the container yourself; note that pip quietly picks older package releases on older Pythons (project 30 ran on 3.8 with fastapi 0.124.4).
- Interactive scripts get a closed stdin; GUI programs and servers need their own setup.
- The first version of this tool mounted the folder read-only without copying it (project 29 failed with "unable to open database file") and used a 60-second limit (project 26 timed out on 3.8 and 3.9, where it simply runs slower: 79 s on 3.9). Both are fixed; they are why the copy step and the "no answer" wording exist.

## Static Check
[vermin](https://github.com/netromdk/vermin) estimates the minimum version without running the code and agreed with the matrix on every project here, except project 41: run on Python 3.12, it cannot parse 3.15 syntax and answers "~2, ~3".
```bash
pip install vermin
vermin --no-tips --eval-annotations main.py
```

## Links
- Blog post (Turkish): https://gurmezin.com/2026/11/12/python-3-12-gerekir-dogru-mu-surum-iddialarini-dockerda-sinadik/
- Status of Python versions: https://devguide.python.org/versions/

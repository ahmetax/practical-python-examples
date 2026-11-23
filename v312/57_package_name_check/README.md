# Project 57: Does Claude Suggest Packages That Don't Exist? A PyPI Name Checker

Claude (Claude Code 2.1.330, `claude-opus-5-5`, tools off) was asked three times each for 32 Python tasks that need third-party packages or Turkey-specific services (PDF tables, HEIC, OCR, Turkish stemming, IBAN, courier tracking, MERNİS, central bank rates...). The 96 answers contained 134 `pip install` names (33 distinct packages); all 134 exist on PyPI. Imports, `from X import Y` names (heavy packages aside) and three Hugging Face model ids were real too. Existence is a weak guarantee, though: while parsing, our own script briefly treated `python_version` as a package name, and PyPI has a real package called that.

This script is the checker. Given an answer text (a `python` block and a `bash` block with `pip install` lines) it extracts the `pip` names, asks the PyPI JSON API about each one, and warns when a third-party `import` has no matching `pip` name. Without arguments it checks two embedded examples: real packages and one made-up name.

| Check | Scope | Result |
|---|---|---|
| `pip install` names | 134 occurrences, 33 distinct packages | 134/134 exist |
| `import` vs `pip` names | 96 answers | 0 mismatches |
| `from X import Y`, `X.a.b` chains | 96 answers, 4 heavy packages skipped | 0 missing names |
| Hugging Face model ids | 3 distinct ids | 3/3 exist |

## How It Works
- `pip_adlari` reads `pip install` lines from `bash` blocks with `shlex.split` and drops version specifiers and environment markers (`;`).
- `import_adlari` parses the `python` block with `ast` and keeps top-level third-party modules (`sys.stdlib_module_names` filtered out).
- `pypi_var_mi` GETs `https://pypi.org/pypi/<name>/json`: 200 = exists, 404 = does not, anything else or a network error = unknown.
- Import names that differ from pip names (`PIL`, `cv2`, `bs4`, `yaml`, ...) are mapped by a small table.

## Limits
- "Exists on PyPI" does not mean "the right package" or "a safe package": a squatted name passes this check.
- One model, one version, three tries per task, tools off (an agent that runs `pip` itself is a different scenario).
- The script checks names, not release age, download counts or maintainers.

## Project Structure
```text
57_package_name_check/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (`sys.stdlib_module_names`). Tested with Python 3.12.3.
- No third-party packages. Needs network access to pypi.org (read-only GET requests).

## Usage
```bash
python3 main.py                # two embedded examples
python3 main.py answer.md ...  # your own answer files
```

## Example Output (Python 3.12.3)
```text
== örnek: gerçek paketler
  pip hijridate                      var    2.6.0, 5 sürüm
  pip schwifty                       var    2026.11.3, 97 sürüm
  pip requests                       var    2.34.2, 163 sürüm
== örnek: uydurma paket
  pip turkce-kimlik-dogrula-pro      YOK    404
```
Version numbers show whatever PyPI has on the day you run it.

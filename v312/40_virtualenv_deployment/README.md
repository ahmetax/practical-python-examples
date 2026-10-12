# Project 40: Virtual Environment Check Before Deployment

A small pre-deployment health check. `main.py` refuses to run unless it is inside a virtual environment (`venv`) and its third-party dependency (`requests`) is installed. This is the kind of guard you would put at the start of a deployment pipeline so that a service never runs against the global system Python by accident.

## How It Works
- **Isolation check:** Inside a virtual environment, `sys.prefix` points to the environment while `sys.base_prefix` still points to the base Python installation. If the two are equal, the script is running globally and exits with code `1`.
- **Dependency check:** The script tries to `import requests`. If the import fails, it exits with code `1` and asks you to install the requirements.
- If both checks pass, it prints a success message and exits with code `0`, so a CI/CD step can rely on the exit code.

## Project Structure
```text
40_virtualenv_deployment/
├── main.py
├── README.md
└── README_TR.md
```
`requirements.txt` is not included; you create it in step 2 below.

## Requirements
- Python 3.12+ (any Python 3 with the built-in `venv` module works)
- Ubuntu 24.04 or any Linux/macOS system. On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.
- On Ubuntu, `venv` may need the system package: `sudo apt install python3-venv`

## Running

**1. Run it globally (expected to fail):**
```bash
python3 main.py
```
```text
--- Running Production Deployment Sanity Monitor ---
 -> Isolation Layer Status   : INACTIVE (GLOBAL)
 -> Python Interpreter Path   : /usr/bin/python3
 -> Python Core Version       : 3.12.3
 -> Third-Party Requirements : RESOLVED
-------------------------------------------------------
[Critical Danger] Application is running globally! Aborting pipeline to prevent host pollution.
```

**2. Create the virtual environment and the requirements file:**
```bash
python3 -m venv .venv
source .venv/bin/activate
echo "requests==2.32.3" > requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
```
Your prompt now starts with `(.venv)`. Pinning an exact version (`==`) makes every deployment install the same package.

**3. Run it inside the virtual environment (expected to pass):**
```bash
python3 main.py
```
```text
--- Running Production Deployment Sanity Monitor ---
 -> Isolation Layer Status   : ACTIVE (.venv)
 -> Python Interpreter Path   : /path/to/40_virtualenv_deployment/.venv/bin/python3
 -> Python Core Version       : 3.12.3
 -> Third-Party Requirements : RESOLVED
-------------------------------------------------------
[SUCCESS] Environment sanity check passed. The container/host is safe for heavy web routing operations.
```

If you skip `pip install -r requirements.txt`, the script detects the active environment but reports `UNRESOLVED (CRITICAL)` for the requirements and exits with code `1`.

When you are done, leave the environment with `deactivate`.

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/09/28/pythonda-sanal-ortam-kontrolu-uretime-cikmadan-once-son-guvenlik-adimi/
- `venv` documentation: https://docs.python.org/3/library/venv.html

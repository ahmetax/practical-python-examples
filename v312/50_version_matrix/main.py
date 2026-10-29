# Author: Ahmet Aksoy & Claude
# Date: 29.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - runs on Python 3.8+ (checked with itself and vermin), needs Docker

"""
Version Matrix: Does "Requires Python 3.12+" Hold?
Runs each project folder under the official python:X-slim Docker images and
reports, per version, whether the code compiles and whether main.py runs.
The lowest version that runs is the real minimum; compare it with the claim.

Usage: python3 main.py PROJECT_DIR [PROJECT_DIR ...] [--versions 3.8,3.9,...]
       [--timeout SECONDS] [--args "ARGS FOR main.py"]
Standard library only. The project folder is mounted read-only and copied
to /tmp inside the container, so a script that writes files still runs.
A timeout means "no answer", not "incompatible": raise --timeout and retry.
"""
import argparse
import subprocess
import sys
from pathlib import Path

VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14", "3.15"]
TIMEOUT = 300

# Runs inside the container: copy the project, compile every .py file, then
# run main.py with the given arguments.
PROBE = r"""
import os, pathlib, shutil, subprocess, sys
shutil.copytree('/src', '/tmp/app')
os.chdir('/tmp/app')
for f in sorted(pathlib.Path('.').rglob('*.py')):
    try:
        compile(f.read_text(encoding='utf-8'), str(f), 'exec')
    except SyntaxError as e:
        print(f'COMPILE SyntaxError {f}:{e.lineno} {e.msg}')
        sys.exit(0)
try:
    r = subprocess.run([sys.executable, 'main.py', *sys.argv[1:]], stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, timeout=%d)
except subprocess.TimeoutExpired:
    print('RUN timeout')
    sys.exit(0)
last = (r.stderr.strip().splitlines() or [''])[-1]
print(f'RUN exit={r.returncode} {last}')
"""


def probe(project: Path, version: str, timeout: int, extra: list) -> str:
    cmd = ["docker", "run", "--rm", "--network", "none",
           "-e", "PYTHONDONTWRITEBYTECODE=1",
           "-v", f"{project.resolve()}:/src:ro",
           f"python:{version}-slim", "python", "-c", PROBE % timeout, *extra]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        return "docker timeout"
    return (out.stdout.strip() or out.stderr.strip().splitlines()[-1]).strip()


def verdict(line: str) -> str:
    if line.startswith("COMPILE"):
        return "SyntaxError"
    if line.startswith("RUN exit=0"):
        return "ok"
    if line == "RUN timeout":
        return "timeout (no answer)"
    if line.startswith("RUN exit="):
        error = line.split(" ", 2)[2] if line.count(" ") >= 2 else ""
        return error.split(":")[0] or f"exit {line[9:].split()[0]}"
    return line


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("projects", nargs="+", type=Path)
    parser.add_argument("--versions", default=",".join(VERSIONS))
    parser.add_argument("--timeout", type=int, default=TIMEOUT)
    parser.add_argument("--args", default="", help="arguments passed to every main.py")
    parser.add_argument("-v", "--verbose", action="store_true", help="show the raw error line")
    args = parser.parse_args()
    versions = args.versions.split(",")

    for project in args.projects:
        if not (project / "main.py").is_file():
            print(f"{project}: no main.py, skipped")
            continue
        print(f"== {project.name} ==")
        lowest = None
        for version in versions:
            line = probe(project, version, args.timeout, args.args.split())
            result = verdict(line)
            if result == "ok" and lowest is None:
                lowest = version
            extra = f"  | {line}" if args.verbose and result != "ok" else ""
            print(f"  {version:<6} {result}{extra}")
        print(f"  lowest version that runs: {lowest or 'none'}\n")


if __name__ == "__main__":
    main()

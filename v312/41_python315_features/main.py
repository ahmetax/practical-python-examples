# Author: Ahmet Aksoy
# Date: 03.10.2026
# Python 3.15 (3.15.0rc2) - Docker python:3.15-rc-slim / Ubuntu 24.04

"""
Python 3.15 Feature Tour
A hands-on walkthrough of the headline features arriving with Python 3.15:
frozendict (PEP 814), unpacking in comprehensions (PEP 798), the sentinel
builtin (PEP 661), UTF-8 as the default encoding (PEP 686) and lazy imports
(PEP 810), including a small startup-time benchmark.
"""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

if sys.version_info < (3, 15):
    sys.exit("This tour needs Python 3.15 or newer.")


def demo_frozendict() -> None:
    """PEP 814: an immutable, hashable dictionary as a builtin type."""
    print("\n=== 1. frozendict ===")
    config = frozendict(host="localhost", port=8080)
    print(f"config            : {config}")

    try:
        config["port"] = 9090
    except TypeError as exc:
        print(f"assignment blocked: {exc}")

    # The | operator returns a NEW frozendict; the original stays untouched
    prod = config | {"host": "gurmezin.com"}
    print(f"derived config    : {prod}")

    # Hashable -> usable as a dict key or a set member (cache keys!)
    cache = {config: "dev server", prod: "prod server"}
    print(f"lookup by value   : {cache[frozendict(port=8080, host='localhost')]}")


def demo_comprehension_unpacking() -> None:
    """PEP 798: * and ** unpacking directly inside comprehensions."""
    print("\n=== 2. Unpacking in comprehensions ===")
    weekly_tags = [["python", "asyncio"], ["regex"], ["python", "pytest"]]
    defaults = [{"lang": "tr", "theme": "light"}, {"theme": "dark"}]

    print(f"flattened list : {[*tags for tags in weekly_tags]}")
    print(f"unique set     : {sorted({*tags for tags in weekly_tags})}")
    merged = {**d for d in defaults}
    print(f"merged dict    : {merged}")


# PEP 661: a unique, readable "no value given" marker
MISSING = sentinel("MISSING")


def get_setting(settings: dict, key: str, default=MISSING):
    """Distinguishes 'no default given' from an explicit default of None."""
    if key in settings:
        return settings[key]
    if default is MISSING:
        raise KeyError(f"{key!r} not found and no default given")
    return default


def demo_sentinel() -> None:
    print("\n=== 3. sentinel ===")
    settings = {"debug": False}
    print(f"repr                : {MISSING!r}")
    print(f"explicit None       : {get_setting(settings, 'timeout', None)}")
    try:
        get_setting(settings, "timeout")
    except KeyError as exc:
        print(f"no default -> error : {exc}")


def demo_utf8_default() -> None:
    """PEP 686: open() without encoding= now means UTF-8 everywhere."""
    print("\n=== 4. UTF-8 by default ===")
    print(f"sys.flags.utf8_mode : {sys.flags.utf8_mode}")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "notlar.txt"
        path.write_text("Işık, ğüşiöç — İstanbul")  # no encoding argument
        raw = path.read_bytes()
        print(f"bytes on disk       : {len(raw)} (UTF-8: {raw.decode('utf-8')})")


EAGER_SCRIPT = "import asyncio, decimal, email.mime.multipart, http.client, json"
LAZY_SCRIPT = (
    "lazy import asyncio\nlazy import decimal\nlazy import email.mime.multipart\n"
    "lazy import http.client\nlazy import json"
)


def startup_ms(code: str, runs: int = 7) -> float:
    """Median wall-clock time of starting a fresh interpreter that runs `code`."""
    timings = []
    for _ in range(runs):
        start = time.perf_counter()
        subprocess.run([sys.executable, "-c", code], check=True)
        timings.append((time.perf_counter() - start) * 1000)
    return sorted(timings)[runs // 2]


def demo_lazy_imports() -> None:
    """PEP 810: `lazy import` defers loading until the name is first used."""
    print("\n=== 5. Lazy imports ===")
    startup_ms(EAGER_SCRIPT, runs=1)  # warm-up: build .pyc caches first
    eager = startup_ms(EAGER_SCRIPT)
    lazy = startup_ms(LAZY_SCRIPT)
    print(f"eager imports : {eager:6.1f} ms")
    print(f"lazy imports  : {lazy:6.1f} ms  ({eager / lazy:.1f}x faster startup)")


def main() -> None:
    print(f"Python {sys.version.split()[0]}")
    demo_frozendict()
    demo_comprehension_unpacking()
    demo_sentinel()
    demo_utf8_default()
    demo_lazy_imports()


if __name__ == "__main__":
    main()

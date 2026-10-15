# Author: Ahmet Aksoy & Claude
# Date: 15.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.12+ (sqlite3 autocommit)

"""
Silent Failures: Code That Says "Success" Without Checking
Five patterns found in this repository (projects 26, 29, 34, 37, 39), each
shown twice: the version that only *says* it worked and the version that
*checks*. Runs offline, standard library only.
"""
import importlib.metadata
import locale
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

WORKDIR = Path(tempfile.mkdtemp(prefix="silent_demo_"))


# --- 1. Hata mesajı basıp 0 ile çıkmak (proje 37, 39) ------------------------------
SAYS = """
import sys
from pathlib import Path
if not Path(sys.argv[1]).is_dir():
    print("[Error] source directory does not exist")
"""

CHECKS = """
import sys
from pathlib import Path
if not Path(sys.argv[1]).is_dir():
    sys.exit(f"[Error] source directory does not exist: {sys.argv[1]}")
"""


def demo_exit_code():
    print("== 1. Exit code ==")
    for name, code in (("says  ", SAYS), ("checks", CHECKS)):
        r = subprocess.run([sys.executable, "-c", code, "/no/such/dir"],
                           capture_output=True, text=True)
        chain = "continues" if r.returncode == 0 else "stops"
        print(f"  {name}: exit code {r.returncode} -> 'cmd && next' {chain}")


# --- 2. Uyarısız üzerine yazmak (proje 37) ------------------------------------------
def move_says(src: Path, dst: Path) -> None:
    shutil.move(src, dst)  # Linux'ta var olan dst sessizce ezilir


def move_checks(src: Path, dst: Path) -> None:
    if dst.exists():
        raise FileExistsError(f"refusing to overwrite {dst}")
    shutil.move(src, dst)


def demo_overwrite():
    print("\n== 2. Overwrite ==")
    for name, mover in (("says  ", move_says), ("checks", move_checks)):
        target = WORKDIR / name.strip() / "Documents"
        target.mkdir(parents=True)
        (target / "report.txt").write_text("OLD report, only copy\n")
        new = WORKDIR / f"{name.strip()}_new.txt"
        new.write_text("new report\n")
        try:
            mover(new, target / "report.txt")
            result = "moved"
        except FileExistsError as exc:
            result = f"refused ({exc.__class__.__name__})"
        kept = (target / "report.txt").read_text().strip()
        print(f"  {name}: {result:<26} report.txt now: {kept!r}")


# --- 3. Her hatayı 404'e çevirmek (proje 26) ----------------------------------------
def status_says(url: str) -> int:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status
    except Exception:
        return 404


def status_checks(url: str) -> int | str:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:  # sunucu yanıt verdi
        return exc.code
    except (urllib.error.URLError, TimeoutError) as exc:  # yanıt hiç gelmedi
        return f"no response: {getattr(exc, 'reason', exc)}"


def demo_status():
    print("\n== 3. Error -> 404 ==")
    url = "https://nonexistent.invalid"
    print(f"  says  : {status_says(url)}")
    print(f"  checks: {status_checks(url)}")


# --- 4. Koda gömülü durum metni (proje 34) ------------------------------------------
def demo_hardcoded():
    print("\n== 4. Hard-coded status ==")
    print("  says  : Rich Library Status -> Successfully Resolved via Poetry")
    try:
        version = importlib.metadata.version("rich")
    except importlib.metadata.PackageNotFoundError:
        version = "NOT INSTALLED"
    in_venv = sys.prefix != sys.base_prefix
    print(f"  checks: rich {version}, virtualenv: {in_venv}, "
          f"POETRY_ACTIVE={os.environ.get('POETRY_ACTIVE', '-')}")


# --- 5. "rolled back" yazıp geri almamak (proje 29) ---------------------------------
ROWS = [("A-1", "first"), ("A-1", "duplicate")]  # ikinci satır UNIQUE'i bozar


def insert_rows(conn: sqlite3.Connection, verify: bool) -> str:
    try:
        with conn:
            for row in ROWS:
                conn.execute("INSERT INTO items VALUES (?, ?)", row)
        return "committed"
    except sqlite3.IntegrityError:
        if not verify:
            return "rolled back"
        left = conn.execute("SELECT count(*) FROM items").fetchone()[0]
        return "rolled back" if left == 0 else f"NOT rolled back, {left} row(s) left"


def demo_rollback():
    print("\n== 5. 'rolled back' ==")
    # Python 3.11/3.12 legacy modda INSERT'i yerel ayara bağlı tolower() ile
    # tanır; tr_TR'de 'I' küçülmez, BEGIN açılmaz. Bkz. gh-108767 (3.13'te düzeldi).
    try:
        locale.setlocale(locale.LC_CTYPE, "tr_TR.UTF-8")
    except locale.Error:
        print("  (tr_TR.UTF-8 locale not available; 'says' may look correct here)")
    print(f"  Python {sys.version.split()[0]}, LC_CTYPE={locale.setlocale(locale.LC_CTYPE)}")
    cases = (("says          ", {}, False),
             ("checks        ", {}, True),
             ("checks + fixed", {"autocommit": False}, True))
    for name, kwargs, verify in cases:
        conn = sqlite3.connect(":memory:", **kwargs)
        conn.execute("CREATE TABLE items (sku TEXT UNIQUE, name TEXT)")
        conn.commit()
        print(f"  {name}: {insert_rows(conn, verify)}")
        conn.close()


if __name__ == "__main__":
    print("--- Silent Failures Demo ---\n")
    try:
        demo_exit_code()
        demo_overwrite()
        demo_status()
        demo_hardcoded()
        demo_rollback()
    finally:
        shutil.rmtree(WORKDIR)

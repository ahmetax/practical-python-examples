# Author: Ahmet Aksoy
# Date: 08.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.12+

"""
Python Context Managers Tour
A hands-on walkthrough of the with statement: why try/finally is needed,
files closing themselves even on errors, a class-based timer with
__enter__/__exit__, suppressing exceptions, generator-based managers with
@contextmanager, sqlite3 transactions with autocommit=False and ExitStack.
"""
import contextlib
import os
import sqlite3
import tempfile
import time
from pathlib import Path

WORKDIR = Path(tempfile.mkdtemp(prefix="ctx_demo_"))


# --- 1. Sorun: kaynağı kapatmayı unutmak ------------------------------------------
def demo_problem():
    print("== 1. with olmadan ==")
    path = WORKDIR / "notlar.txt"
    f = open(path, "w", encoding="utf-8")
    try:
        f.write("ilk satır\n")
        raise ValueError("yazarken bir şey ters gitti")
    except ValueError as exc:
        print("hata         :", exc)
    print("dosya kapalı mı?", f.closed)   # hata yüzünden close() hiç çalışmadı
    f.close()


# --- 2. with: hata olsa bile kapanır ---------------------------------------------
def demo_with_file():
    print("\n== 2. with open ==")
    path = WORKDIR / "notlar.txt"
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("ilk satır\n")
            raise ValueError("yazarken bir şey ters gitti")
    except ValueError as exc:
        print("hata         :", exc)
    print("dosya kapalı mı?", f.closed)
    print("dosyada      :", path.read_text(encoding="utf-8").strip())


# --- 3. Kendi context manager'ımız: sınıf ile ---------------------------------
class Timer:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        return self                     # "as" ile alınan değer

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = (time.perf_counter() - self.start) * 1000
        status = "hata ile" if exc_type else "sorunsuz"
        print(f"[{self.label}] {self.elapsed:.1f} ms, {status} bitti")
        return False                    # hatayı yutma, yukarı ilet


def demo_class_based():
    print("\n== 3. __enter__ / __exit__ ==")
    with Timer("kareler") as t:
        total = sum(i * i for i in range(500_000))
    print("toplam       :", total, "| ölçülen:", round(t.elapsed) > 0)
    try:
        with Timer("bölme"):
            1 / 0
    except ZeroDivisionError as exc:
        print("hata yukarı iletildi:", exc)


# --- 4. Hatayı bilerek yutmak: contextlib.suppress ----------------------------
def demo_suppress():
    print("\n== 4. contextlib.suppress ==")
    missing = WORKDIR / "olmayan.tmp"
    with contextlib.suppress(FileNotFoundError):
        missing.unlink()
    print("silinecek dosya yoktu, program devam ediyor")


# --- 5. @contextmanager: üreteç ile context manager ---------------------------
@contextlib.contextmanager
def working_dir(path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield Path.cwd()                # with bloğu burada çalışır
    finally:
        os.chdir(old)                   # hata olsa bile geri dön


def demo_contextmanager():
    print("\n== 5. @contextmanager ==")
    before = Path.cwd()
    with working_dir(WORKDIR) as here:
        Path("rapor.txt").write_text("göreli yol ile yazıldı", encoding="utf-8")
        print("blok içinde  :", here.name.startswith("ctx_demo_"))
    print("geri döndü mü?", Path.cwd() == before)
    print("dosya nerede :", (WORKDIR / "rapor.txt").exists())
    with contextlib.chdir(WORKDIR):     # Python 3.11+ hazır sürümü
        print("contextlib.chdir:", Path("rapor.txt").exists())


# --- 6. sqlite3: with işlemi yönetir ama bağlantıyı kapatmaz ----------------
def demo_sqlite():
    print("\n== 6. sqlite3 ve with ==")
    db = WORKDIR / "kutuphane.db"
    # autocommit=False (3.12+): işlemi Python her zaman kendisi açar
    conn = sqlite3.connect(db, autocommit=False)
    conn.execute("CREATE TABLE kitap (ad TEXT NOT NULL, sayfa INTEGER CHECK (sayfa > 0))")
    with conn:                                          # başarılıysa commit
        conn.execute("INSERT INTO kitap VALUES (?, ?)", ("Kuyucaklı Yusuf", 230))
    try:
        with conn:                                      # hata olursa rollback
            conn.execute("INSERT INTO kitap VALUES (?, ?)", ("Sinekli Bakkal", 348))
            conn.execute("INSERT INTO kitap VALUES (?, ?)", ("Hatalı Kayıt", -5))
    except sqlite3.IntegrityError as exc:
        print("hata         :", exc)
    print("kayıtlar     :", [r[0] for r in conn.execute("SELECT ad FROM kitap")])
    conn.execute("SELECT 1")
    print("with sonrası bağlantı hâlâ açık: sorgu çalıştı")
    conn.close()

    with contextlib.closing(sqlite3.connect(db, autocommit=False)) as conn2, conn2:
        conn2.execute("INSERT INTO kitap VALUES (?, ?)", ("Çalıkuşu", 420))
    try:
        conn2.execute("SELECT 1")
    except sqlite3.ProgrammingError as exc:
        print("closing ile  :", exc)
    with contextlib.closing(sqlite3.connect(db)) as check:
        print("son durum    :", [r[0] for r in check.execute("SELECT ad FROM kitap")])


# --- 7. ExitStack: sayısı önceden bilinmeyen kaynaklar ----------------------
def demo_exitstack():
    print("\n== 7. ExitStack ==")
    names = ["ocak.csv", "subat.csv", "mart.csv"]
    for i, name in enumerate(names, 1):
        (WORKDIR / name).write_text(f"ay,satis\n{name[:-4]},{i * 100}\n", encoding="utf-8")
    with contextlib.ExitStack() as stack:
        files = [stack.enter_context(open(WORKDIR / n, encoding="utf-8")) for n in names]
        rows = [f.read().splitlines()[1] for f in files]
        print("açık dosya   :", sum(not f.closed for f in files))
    print("satırlar     :", rows)
    print("blok sonrası açık dosya:", sum(not f.closed for f in files))


if __name__ == "__main__":
    demo_problem()
    demo_with_file()
    demo_class_based()
    demo_suppress()
    demo_contextmanager()
    demo_sqlite()
    demo_exitstack()

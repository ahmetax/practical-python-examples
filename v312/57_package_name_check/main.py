"""Yapay zekânın yazdığı koddaki paket adlarını PyPI'da denetler.

Bir yanıt metninden (kod bloğu + pip install satırları):
  1. pip install ile kurulması istenen adları çıkarır,
  2. kodda import edilen üçüncü taraf modülleri çıkarır,
  3. her pip adını PyPI JSON API'siyle sorar (404 = böyle bir paket yok),
  4. import edilen modüle karşılık gelen bir pip adı yazılmış mı bakar.

Kullanım:
  python3 main.py              # gömülü örnekleri çalıştırır
  python3 main.py yanit.md ... # kendi yanıt dosyalarınızı denetler

Yalnızca standart kütüphane kullanır; PyPI'ya salt okunur GET gönderir.
"""
import ast
import json
import re
import shlex
import sys
import urllib.error
import urllib.request

# import adı ile pip adı farklı olan sık durumlar
IMPORT_PIP = {
    "PIL": "pillow", "cv2": "opencv-python", "bs4": "beautifulsoup4",
    "yaml": "pyyaml", "sklearn": "scikit-learn", "stdnum": "python-stdnum",
    "pillow_heif": "pillow-heif", "sentence_transformers": "sentence-transformers",
}

ORNEK_GERCEK = '''```python
import hijridate
from schwifty import IBAN
import requests
print(hijridate.Gregorian(2026, 12, 10).to_hijri())
```
```bash
pip install hijridate schwifty requests
```'''

# Kasıtlı olarak uydurulmuş bir ad: bu paketin PyPI'da bulunmaması beklenir
ORNEK_UYDURMA = '''```python
import turkce_kimlik_dogrula_pro
print(turkce_kimlik_dogrula_pro.dogrula("10000000146"))
```
```bash
pip install turkce-kimlik-dogrula-pro
```'''


def pip_adlari(metin):
    adlar = []
    for blok in re.findall(r"```(?:bash|sh|shell)\n(.*?)```", metin, re.S):
        for satir in blok.splitlines():
            m = re.match(r"\s*(?:python3? -m )?pip3? install\s+(.*)", satir)
            if not m:
                continue
            for parca in shlex.split(m.group(1)):
                if parca.startswith("-"):
                    continue
                ad = re.split(r"[<>=!~\[;\s]", parca)[0]
                if ad:
                    adlar.append(ad)
    return adlar


def import_adlari(metin):
    m = re.search(r"```python\n(.*?)```", metin, re.S)
    if not m:
        return set()
    bulunan = set()
    for n in ast.walk(ast.parse(m.group(1))):
        if isinstance(n, ast.Import):
            bulunan |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            bulunan.add(n.module.split(".")[0])
    return {b for b in bulunan if b not in sys.stdlib_module_names}


def pypi_var_mi(ad):
    """True/False; ağ hatasında None (belirsiz)."""
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{ad}/json", timeout=20) as r:
            d = json.load(r)
            return True, f"{d['info']['version']}, {len(d['releases'])} sürüm"
    except urllib.error.HTTPError as e:
        return (False, "404") if e.code == 404 else (None, f"HTTP {e.code}")
    except OSError as e:
        return None, str(e)


def norm(ad):
    return ad.lower().replace("_", "-")


def denetle(etiket, metin):
    print(f"== {etiket}")
    pipler = pip_adlari(metin)
    for ad in dict.fromkeys(pipler):
        var, ayrinti = pypi_var_mi(ad)
        isaret = {True: "var   ", False: "YOK   ", None: "BELİRSİZ"}[var]
        print(f"  pip {ad:30} {isaret} {ayrinti}")
    yazilanlar = {norm(p) for p in pipler}
    for mod in sorted(import_adlari(metin)):
        beklenen = norm(IMPORT_PIP.get(mod, mod))
        if not any(beklenen in p or p in beklenen for p in yazilanlar):
            print(f"  import {mod}: pip satırında karşılığı yok (beklenen: {beklenen})")


def main():
    if len(sys.argv) > 1:
        for yol in sys.argv[1:]:
            with open(yol, encoding="utf-8") as f:
                denetle(yol, f.read())
    else:
        denetle("örnek: gerçek paketler", ORNEK_GERCEK)
        denetle("örnek: uydurma paket", ORNEK_UYDURMA)


if __name__ == "__main__":
    main()

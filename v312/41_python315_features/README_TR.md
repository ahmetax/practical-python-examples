# Proje 41: Python 3.15 Yenilikler Turu

Python 3.15'in (kararlı sürüm 9 Ekim 2026'da bekleniyor) öne çıkan yeniliklerini çalıştırılabilir örneklerle gösteren proje.

| # | Yenilik | PEP |
|---|---------|-----|
| 1 | `frozendict`: değiştirilemeyen, hash'lenebilen yerleşik sözlük | PEP 814 |
| 2 | Kavrayışlar (comprehension) içinde `*` / `**` ile açma | PEP 798 |
| 3 | Benzersiz işaret değerleri için yerleşik `sentinel()` | PEP 661 |
| 4 | Varsayılan metin kodlamasının UTF-8 olması | PEP 686 |
| 5 | `lazy import` / `lazy from ... import` (açılış süresi ölçümüyle) | PEP 810 |

## Proje Yapısı
```text
41_python315_features/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.15 (3.15.0rc2 veya üstü). Üçüncü taraf paket gerekmez.
- Daha eski sürümlerde betik bir mesajla sonlanır.

## Çalıştırma

**Docker ile (yerel kurulum gerekmez):**
```bash
docker run --rm -v "$PWD":/app -w /app python:3.15-rc-slim python main.py
```

**uv ile** (önce `uv self update` ile uv'yi güncelleyin; eski uv sürümleri yalnızca 3.15 beta sürümlerini sunar):
```bash
uv python install 3.15
uv run --python 3.15 main.py
```

## Örnek Çıktı (3.15.0rc2, Docker)
```text
=== 5. Lazy imports ===
eager imports :  164.2 ms
lazy imports  :   20.7 ms  (7.9x faster startup)
```
Süreler makineye göre değişir; asıl önemli olan oran.

## Ek Okuma
- What's New in Python 3.15: https://docs.python.org/3.15/whatsnew/3.15.html

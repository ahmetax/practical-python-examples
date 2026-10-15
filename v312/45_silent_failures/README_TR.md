# Proje 45: Sessiz Hatalar — Kontrol Etmeden "Başarılı" Diyen Kod

23–41 numaralı projelerin README dosyalarını yeniden yazarken her betiği gerçekten çalıştırdık. Beş yerde kodun bir şeyi kontrol etmeden başarı (ya da makul görünen bir durum) bildirdiğini gördük. Bu proje her örüntüyü iki kez gösteriyor: yalnızca **söyleyen** sürüm ve **kontrol eden** sürüm.

| # | Örüntü | Bulunduğu proje | Kontrol |
|---|--------|-----------------|---------|
| 1 | Hata mesajı basıp 0 koduyla çıkmak | 37, 39 | `sys.exit(mesaj)` → çıkış kodu 1 |
| 2 | Var olan dosyanın üzerine uyarısız yazmak | 37 | hedef varsa reddetmek |
| 3 | Her hatayı "404" yapmak | 26 | `HTTPError` (sunucu yanıt verdi) ile `URLError`'ı (yanıt yok) ayırmak |
| 4 | Koda gömülü durum metni | 34 | durumu okumak: `importlib.metadata.version`, `sys.prefix` |
| 5 | Bakmadan "rolled back" yazmak | 29 | hatadan sonra satırları saymak; `autocommit=False` |

## Proje Yapısı
```text
45_silent_failures/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.12 veya üstü (`sqlite3.connect(..., autocommit=False)`). Python 3.12.3 (Ubuntu 24.04) ve 3.12.15 (Docker `python:3.12-slim`, `--network none`) ile test edildi.
- Üçüncü taraf paket ve internet bağlantısı gerekmez. Dosyalar geçici bir klasörde oluşturulur ve sonunda silinir.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3, Ubuntu 24.04, LC_CTYPE=tr_TR.UTF-8)
```text
--- Silent Failures Demo ---

== 1. Exit code ==
  says  : exit code 0 -> 'cmd && next' continues
  checks: exit code 1 -> 'cmd && next' stops

== 2. Overwrite ==
  says  : moved                      report.txt now: 'new report'
  checks: refused (FileExistsError)  report.txt now: 'OLD report, only copy'

== 3. Error -> 404 ==
  says  : 404
  checks: no response: [Errno -2] Name or service not known

== 4. Hard-coded status ==
  says  : Rich Library Status -> Successfully Resolved via Poetry
  checks: rich 13.7.1, virtualenv: False, POETRY_ACTIVE=-

== 5. 'rolled back' ==
  Python 3.12.3, LC_CTYPE=tr_TR.UTF-8
  says          : rolled back
  checks        : NOT rolled back, 1 row(s) left
  checks + fixed: rolled back
```
- 3. bölümdeki hata metni ad çözümleyicisine göre değişir (ağsız Docker'da `[Errno -3] Temporary failure in name resolution`).
- 4. bölüm gerçekte ne kuruluysa onu gösterir (temiz konteynerde `rich NOT INSTALLED`).
- 5. bölümdeki hata yalnızca `tr_TR.UTF-8` yerel ayarı kurulu ve Python 3.11/3.12 olan makinelerde görülür (bkz. proje 44, [gh-108767](https://github.com/python/cpython/issues/108767)). Başka ortamlarda üç satır da `rolled back` der ve betik bir not yazar.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/10/26/tamamlandi-diyen-kod-kontrol-etmeden-basari-bildiren-bes-ornek/
- Özgün kodun bulunduğu projeler: bu depodaki 26, 29, 34, 37, 39
- `sys.exit`: https://docs.python.org/3/library/sys.html#sys.exit
- `urllib.error`: https://docs.python.org/3/library/urllib.error.html

# Proje 44: Python Context Manager Turu

`with` deyimini çalıştırılabilir örneklerle anlatan proje. Context manager'ların dosyaları, bağlantıları ve diğer kaynakları hata olsa bile nasıl serbest bıraktığını ve kendi context manager'larınızı nasıl yazacağınızı gösteriyor.

| # | Konu | Temel API |
|---|------|-----------|
| 1 | Hata yüzünden açık kalan dosya (sorun) | `finally` olmadan `try/except` |
| 2 | Hata olsa bile kendiliğinden kapanan dosyalar | `with open(...)` |
| 3 | Sınıf tabanlı zamanlayıcı | `__enter__`, `__exit__` |
| 4 | Belirli bir hatayı bilerek yutmak | `contextlib.suppress` |
| 5 | Üreteç tabanlı context manager | `@contextlib.contextmanager`, `contextlib.chdir` |
| 6 | İşlemler: `with conn` commit ya da rollback yapar ama kapatmaz | `sqlite3.connect(..., autocommit=False)`, `contextlib.closing` |
| 7 | Sayısı önceden bilinmeyen kaynakları tek blokta yönetmek | `contextlib.ExitStack` |

## Proje Yapısı
```text
44_context_managers/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.12 veya üstü (`sqlite3.connect` fonksiyonunun `autocommit` parametresi 3.12'de geldi). Python 3.12.3 (Ubuntu 24.04) ve 3.12.15 (Docker `python:3.12-slim`) ile test edildi.
- Üçüncü taraf paket gerekmez. Bütün dosyalar geçici bir klasörde oluşturulur.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
== 6. sqlite3 ve with ==
hata         : CHECK constraint failed: sayfa > 0
kayıtlar     : ['Kuyucaklı Yusuf']
with sonrası bağlantı hâlâ açık: sorgu çalıştı
closing ile  : Cannot operate on a closed database.
son durum    : ['Kuyucaklı Yusuf', 'Çalıkuşu']
```
Süreler makineye göre değişir, diğer çıktılar her makinede aynıdır.

## sqlite3 İşlemleri Hakkında Not
`autocommit=False` verilmezse sqlite3 eski (legacy) işlem modunu kullanır ve işlemi örtük olarak açıp açmayacağına komutun ilk kelimesine bakarak karar verir. Python 3.11 ve 3.12 bu kontrolde yerel ayara bağlı C `tolower()` fonksiyonunu kullanır. Türkçe yerel ayarda (`tr_TR.UTF-8`) `tolower('I')` sonucu `'i'` olmadığı için `INSERT` tanınmaz, `BEGIN` gönderilmez ve 6. bölümdeki başarısız `with conn:` bloğu geri **alınmaz**. Küçük harfle yazılmış `insert` ile `UPDATE`, `DELETE` ve `REPLACE` etkilenmez. Aynı makinede `LC_ALL=tr_TR.UTF-8` (hatalı) ve `LC_ALL=C.UTF-8` (doğru) ile, Docker'da ise 3.11.17 ve 3.12.15 (Türkçe yerel ayarda hatalı), 3.13.16 ve 3.14.8 (doğru) ile denendi. Sorun [gh-108767](https://github.com/python/cpython/issues/108767) ile Python 3.13'te giderildi. `autocommit=False` ile her yerel ayar aynı davrandığı için örnek bu parametreyi kullanıyor.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/10/19/dogru-gorunen-kod-yanlis-sonuc-pythonda-with-ve-sqlite3-tuzagi/
- `contextlib` belgeleri: https://docs.python.org/3/library/contextlib.html
- sqlite3 işlem kontrolü: https://docs.python.org/3/library/sqlite3.html#sqlite3-transaction-control
- PEP 343: The "with" Statement

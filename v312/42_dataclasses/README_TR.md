# Proje 42: Python dataclasses Turu

`dataclasses` modülünü çalıştırılabilir örneklerle anlatan proje. `@dataclass` dekoratörünün elle yazılan tekrar kodunun yerini nasıl aldığını ve bilinmesi gereken seçenekleri gösteriyor. Elle yazıldığında 13 satır tutan üç alanlı bir sınıf, dataclass ile 5 satıra iniyor.

| # | Konu | Temel API |
|---|------|-----------|
| 1 | Otomatik üretilen `__init__`, `__repr__`, `__eq__` | `@dataclass` |
| 2 | Varsayılan değerler ve değiştirilebilir varsayılan tuzağı | `field(default_factory=list)` |
| 3 | Doğrulama ve hesaplanan alanlar | `__post_init__`, `field(init=False)` |
| 4 | Değiştirilemeyen, hash'lenebilen değer nesneleri | `frozen=True`, `replace()` |
| 5 | Nesneleri alan sırasına göre sıralama | `order=True`, `field(compare=False)` |
| 6 | Yalnızca isimle verilen parametreler ve daha hafif nesneler (bellek ölçümüyle) | `kw_only=True`, `slots=True` |
| 7 | İç içe dataclass'ları JSON'a dönüştürme | `asdict()` |

## Proje Yapısı
```text
42_dataclasses/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü (`slots` ve `kw_only` 3.10'da geldi). Python 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
== 5. order=True ==
['3.9.0', '3.10.14', '3.12.3', '3.15.0']
max          : Version(major=3, minor=15, patch=0, label='rc')

== 6. kw_only ve slots ==
hata         : UserSlots.__init__() takes 1 positional argument but 4 were given
hata         : 'UserSlots' object has no attribute 'nickname'
100.000 nesne (normal):   19,806 KB
100.000 nesne (slots) :   16,678 KB  (%16 daha az)
```
Bellek değerleri makineye ve Python sürümüne göre değişir. Ölçüme isim ve e-posta metinleri de dahil olduğundan nesne başına kazanç yaklaşık 32 bayttır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/10/08/pythonda-dataclasses-sinif-yazmanin-kisa-yolu/
- `dataclasses` belgeleri: https://docs.python.org/3/library/dataclasses.html
- PEP 557: Data Classes

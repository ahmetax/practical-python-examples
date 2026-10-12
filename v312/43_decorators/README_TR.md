# Proje 43: Python Dekoratörler Turu

Dekoratörleri çalıştırılabilir örneklerle anlatan proje. `@` sözdiziminin gerçekte ne yaptığını ve kendi dekoratörlerinizi nasıl yazacağınızı gösteriyor. Bir fonksiyonun üstündeki `@timer` satırı, `slow_sum = timer(slow_sum)` yazmanın kısaltmasıdır.

| # | Konu | Temel fikir |
|---|------|-------------|
| 1 | Nesne olarak fonksiyonlar ve closure | `make_multiplier(2)`, `factor` değerini hatırlar |
| 2 | Çalışma süresini ölçen ilk dekoratör | `*args, **kwargs` ile `@timer` |
| 3 | Fonksiyonun adını ve açıklamasını korumak | `functools.wraps` |
| 4 | Parametre alan dekoratörler | `@retry(times=3, exceptions=(ConnectionError,))` |
| 5 | Hazır önbellek dekoratörü (çağrı sayısı ve süre ölçümüyle) | Fibonacci üzerinde `@functools.cache` |
| 6 | Fonksiyonu sarmadan kaydetmek | `@command("ad")` komut tablosu |
| 7 | Üst üste dekoratörler | Fonksiyona en yakın dekoratör önce uygulanır |

## Proje Yapısı
```text
43_decorators/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`functools.cache` 3.9'da geldi). Python 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
== 4. @retry(times=3) ==
[retry] fetch_rates deneme 1/3 başarısız: sunucu yanıt vermedi
[retry] fetch_rates deneme 2/3 başarısız: sunucu yanıt vermedi
sonuç        : {'USD': 41.6, 'EUR': 48.4}
ValueError yeniden denenmedi: could not convert string to float: 'kırk iki'

== 5. @functools.cache ==
fib(30) önbelleksiz: 832040, 2,692,537 çağrı,    776.3 ms
fib(30) önbellekli : 832040,        31 çağrı,    0.029 ms
cache_info   : CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```
Kur değerleri, iki kez hata verdikten sonra yanıt veren sahte bir sunucudan gelir. Süreler makineye göre değişir, çağrı sayıları her makinede aynıdır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/10/15/pythonda-dekoratorler-isaretinin-arkasinda-ne-var/
- `functools` belgeleri: https://docs.python.org/3/library/functools.html
- PEP 318: Decorators for Functions and Methods

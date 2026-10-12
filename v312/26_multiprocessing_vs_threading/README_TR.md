# Proje 26: Multiprocessing ve Threading Karşılaştırması

Betik aynı işi `concurrent.futures` modülündeki `ThreadPoolExecutor` (iş parçacıkları) ve `ProcessPoolExecutor` (süreçler) ile çalıştırır ve her birinin ne kadar sürdüğünü yazdırır.

| Aşama | İş | Neye bakmalı? |
|-------|----|---------------|
| 1. CPU yoğun | Python döngüsüyle 50.000.000'a kadar saymak, 4 kez | GIL yüzünden iş parçacıkları Python kodunu paralel çalıştıramaz; süreçler çalıştırabilir |
| 2. G/Ç yoğun | `urllib.request` ile `https://www.example.com` adresini 4 kez açmak | Sürenin çoğu ağı beklemekle geçer |

## Proje Yapısı
```text
26_multiprocessing_vs_threading/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3 (sürüme özgü bir özellik kullanılmaz). 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez.
- 2. aşama için internet bağlantısı.
- 1. aşamadaki etkiyi tam görmek için en az 4 çekirdekli bir işlemci.

## Çalıştırma
```bash
python3 main.py
```
1. aşama bilerek yavaştır: iş parçacıklı çalıştırma, dört görevi art arda çalıştırmak kadar sürer. Betiğin tamamı onlarca saniye sürebilir.

## Örnek Çıktı (Python 3.12.3, 8 çekirdek)
```text
--- Threading vs Multiprocessing Benchmark Started ---

==================================================
STAGE 1: CPU-Bound Task (Heavy Calculation)
==================================================
Threading (CPU-Bound) Duration       : 31.6311 seconds
Multiprocessing (CPU-Bound) Duration : 7.8416 seconds

==================================================
STAGE 2: I/O-Bound Task (Network Requests)
==================================================
Threading (I/O-Bound) Duration       : 0.2549 seconds
Multiprocessing (I/O-Bound) Duration : 0.1605 seconds
```
Süreler işlemciye, sistem yüküne ve ağa bağlıdır. Yukarıdaki değerler makine başka işlerle meşgulken ölçüldü; boş bir makinede daha düşük değerler görürsünüz. Üç çalıştırmada CPU yoğun aşama süreçlerle her seferinde yaklaşık 4 kat hızlıydı (31,3 sn / 8,5 sn, 31,9 sn / 7,9 sn, 31,6 sn / 7,8 sn). Aynı makinede tek bir `cpu_bound_task(50_000_000)` çağrısı tek başına 8,6 sn sürdü; yani iş parçacıklı sürüm, dört çağrıyı sırayla çalıştırmaktan daha hızlı değildir.

## Nasıl Çalışır?
- **CPU yoğun, iş parçacıkları:** GIL, aynı anda yalnızca bir iş parçacığının Python bayt kodu çalıştırmasına izin verir; dört iş parçacığı, tek görevin yaklaşık dört katı kadar sürer.
- **CPU yoğun, süreçler:** Her işçi kendi yorumlayıcısı ve kendi GIL'i olan ayrı bir süreçtir; dört görev aynı anda dört çekirdekte çalışır.
- **G/Ç yoğun:** Ağı bekleyen iş parçacığı GIL'i bırakır; bu yüzden iş parçacıkları bu tür işlere uygundur. Ancak bu betikte `example.com` istekleri o kadar kısadır ki (toplamı bir saniyenin çok altında) iki sürüm de saniyenin küçük bir kesrinde biter. Yukarıdaki çalıştırmalarda süreç sürümü biraz daha hızlı bile çıktı. Fark büyük ölçüde ölçüm gürültüsü ve ısınma etkisidir (ilk istek DNS çözümleme ve TLS kurulumu maliyetini öder); dört isteği sırayla göndermek de yaklaşık aynı sürdü (0,24 sn). Yani 2. aşama net bir kazanan göstermez.
- `io_bound_task()` her türlü hatada (zaman aşımı, DNS hatası, internet yokluğu) `404` döndürür ve dönüş değerleri yazdırılmaz. İnternet bağlantısı olmasa bile betik 2. aşamanın sürelerini hiçbir uyarı vermeden yazar.
- `max_workers` verilmediğinde `ThreadPoolExecutor` `min(32, CPU sayısı + 4)` iş parçacığı, `ProcessPoolExecutor` ise CPU başına bir süreç kullanır. Burada bunlardan yalnızca 4'üne iş düşer.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/15/pythonda-hiz-yarisi-multiprocessing-mi-threading-mi/
- `concurrent.futures` belgeleri: https://docs.python.org/3/library/concurrent.futures.html
- Global Interpreter Lock (sözlük): https://docs.python.org/3/glossary.html#term-global-interpreter-lock

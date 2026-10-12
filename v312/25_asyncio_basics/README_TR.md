# Proje 25: TaskGroup ile Asyncio Temelleri

Üç eşyordam (coroutine), bir ürün için yavaş çağrıları taklit eder: ürün ayrıntıları (1,5 sn), stok durumu (1,0 sn) ve kullanıcı yorumları (2,0 sn). Gecikmeler `asyncio.sleep()` ile üretilir; gerçek bir ağ ya da veritabanı erişimi yoktur. Eşyordamlar bir `asyncio.TaskGroup` içinde birlikte başlatılır; bu yüzden toplam süre, sürelerin toplamı (4,5 sn) yerine en yavaş olanın süresi (2,0 sn) kadardır. Sonuçlar ardından tek bir sözlükte birleştirilir.

## Proje Yapısı
```text
25_asyncio_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.11 veya üstü (`asyncio.TaskGroup` 3.11'de eklendi). 3.10'da betik `AttributeError: module 'asyncio' has no attribute 'TaskGroup'` hatası verir. 3.12.3 ile test edildi; 3.11'de de çalışır.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Asyncio Testing Started ---

--- Starting Concurrent Tasks for Product ID 99 ---
[Product] Fetching details for ID 99...
[Stock] Checking inventory for ID 99...
[Reviews] Gathering customer reviews for ID 99...
[Stock] Done checking inventory for ID 99.
[Product] Done fetching details for ID 99.
[Reviews] Done gathering reviews for ID 99.

--- Aggregated Result ---
{'id': 99, 'name': 'Premium Wireless Mouse', 'price': 49.99, 'in_stock': True, 'quantity': 142, 'reviews': [{'user': 'Alice', 'rating': 5}, {'user': 'Bob', 'rating': 4}]}

Successfully fetched all data in: 2.00 seconds.
```
Ölçülen süre hem Python 3.12.3'te hem 3.11'de 2.00 saniyeydi. Yapılan iş yalnızca `asyncio.sleep()` olduğu için sonuç her makinede 2,0 saniyeye çok yakın çıkar.

## Nasıl Çalışır?
- `async with asyncio.TaskGroup() as tg:` bir grup açar; her `tg.create_task(...)` çağrısı bir eşyordamı hemen sıraya koyar. Üç "Fetching/Checking/Gathering" satırının hepsi, hiçbiri bitmeden yazdırılır.
- Bir eşyordam `await asyncio.sleep(...)` ile beklerken olay döngüsü (event loop) diğerlerini çalıştırır. Her şey tek bir iş parçacığında çalışır; bu paralellik değil, eşzamanlılıktır.
- `Done` satırları gecikme sırasıyla gelir: stok (1,0 sn), ürün (1,5 sn), yorumlar (2,0 sn).
- `async with` bloğu, tüm görevler bitmeden sona ermez; bu yüzden ardından `.result()` güvenle çağrılabilir. Görevlerden biri hata fırlatırsa grup kalan görevleri iptal eder ve hatayı bir `ExceptionGroup` içinde yükseltir.
- `{**product_info, **stock_info, "reviews": ...}` sözlükleri birleştirir. İkisinde de `id` anahtarı olduğundan sonraki değer geçerli olur (burada ikisi de 99).

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/10/python-asyncio-ile-hizlanin-modern-eszamanlilik-ve-taskgroup/
- `asyncio` görev grupları: https://docs.python.org/3/library/asyncio-task.html#task-groups

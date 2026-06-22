# Proje 25: Asyncio Temelleri ve Yapılandırılmış Eşzamanlılık

Python'ın standart `asyncio` ekosistemini kullanarak bloklamayan I/O rutinlerinin temel bir uygulaması. Bu örnek, `async/await` ve yapılandırılmış görev orkestrasyonu yoluyla güvenli bağlam havuzlama kullanarak modern asenkron tasarım desenlerini gösterir.

## Mimari Hedef
Uygulama, bir e-ticaret platformu için bir toplama yönlendiricisini simüle eder. Bireysel Core Product Details'ı almak, Real-time Inventory Stocks'u kontrol etmek ve Public Customer Reviews'ı almak gibi birden fazla farklı yukarı akış mikroservisini eşzamanlı olarak sorgulaması gerekir; bu, bağımlı olmayan darboğazları aynı anda çalıştırarak nihai işlem gecikmelerini (latencies) en aza indirir.

## Proje Yapısı
```text
25_asyncio_basics/
└── main.py
System Requirements
OS: Ubuntu 24.04

Runtime: Python 3.11+ (Required for asyncio.TaskGroup context syntax)

Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Establish the project directory:

```bash
mkdir 25_asyncio_basics
cd 25_asyncio_basics

### Adım 2: Bloklamayan Pipeline'ı Uygulama
main.py dosyasını oluşturun ve görev yürütmelerini bu sistematik katmanlar aracılığıyla yönetin:

Async I/O Çağrılarını Simüle Etme: Her mikroservis sınırı için `async def` descriptor'ını kullanarak bağımsız coroutine'ler yazın. Ana yürütme iş parçacığını dondurmadan veritabanı veya web hizmeti çağrılarını taklit etmek için değişken yapay yürütme gecikme boşlukları (örneğin, 1.0s, 1.5s, 2.0s) eklemek için `await asyncio.sleep()` kullanın.

Task Havuzlarını Kullanma: Birincil async orchestrator fonksiyonunuzda (`async def main()`), Python 3.11+'ın gelişmiş context manager'ını kullanarak izole bir yürütme kapsamı oluşturun: async with asyncio.TaskGroup() as tg:

Eşzamanlılığı Planlama: Bireysel sorguları `tg.create_task()` aracılığıyla grup yöneticisine kaydedin. Bu, dahili event loop'u tüm işlemlerin paralel izler üzerinde eş zamanlı olarak ateşlenmesi için planlamaya yönlendirir.

Toplamları Tüketme: Yürütme TaskGroup context bloğundan çıktıktan sonra, kaydedilen tüm görevlerin yapısal olarak güvenli bir şekilde tamamlandığı garanti edilir. Hesaplanan dataset payload'larını `.result()` kullanarak çıkarın ve bunları tek bir kapsamlı dictionary payload'unda birleştirin.

### Adım 3: Performans Doğrulaması
Runtime'ı, `time.perf_counter()` aracılığıyla farkları izleyen bir benchmark saati içine sarın. Mutlak son işlem süresinin, ardışık olarak birikmek yerine (1.5 + 1.0 + 2.0 = 4.5 saniye) tek en yavaş görevin hızına (~2.0 saniye) eşleştiğini fark edin.
```bash
python main.py



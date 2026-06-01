# Proje 26: Multiprocessing ve Threading Karşılaştırmalı Testi

Python'ın yüksek seviyeli yürütme modelleri arasındaki net hesaplama sınırlarını analiz eden pratik bir optimizasyon kıyaslaması: Multi-Threading (I/O-Bound odak) ve Multi-Processing (CPU-Bound odak).

## Mimari Amaç
Program, Python'ın Global Interpreter Lock (GIL)'ün `runtime` üzerindeki etkisini ortaya koyar. Hem kaynak tahsisi sistemlerinde yüksek yük, matematik ağırlıklı bir döngüyü (CPU-bound) paralel bir web-ağ bağlantı dizisiyle (I/O-bound) çalıştırarak, uygun ölçeklendirme modelini ne zaman seçeceğine dair somut referans noktaları belirler.

## Proje Yapısı
```text
26_multiprocessing_vs_threading/
└── main.py
System Requirements
OS: Ubuntu 24.04 (Multi-core environment recommended)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a fresh project subdirectory:

```bash
mkdir 26_multiprocessing_vs_threading
cd 26_multiprocessing_vs_threading

### Adım 2: Benchmark Çekirdeğini Oluşturma
`main.py` dosyasını oluşturun ve hesaplamalı deneyleri uygulayın:

Hesaplama Darboğazını Tasarlama: Ham işlemci işleme döngülerini tüketmek için ağır yineleme yapan (örneğin, standart döngüler kullanarak 50.000.000'a kadar saymak) CPU-bound bir fonksiyon tanımlayın.

G/Ç Darboğazını Tasarlama: Python'ın yerel `urllib.request.urlopen` modülünü kullanarak gerçek zamanlı web sitesi başlıkları çekmek gibi hafif harici etkileşimler gerçekleştiren bir I/O-bound fonksiyon tanımlayın.

Yüksek Seviyeli Executor'ları Kullanma: Manuel kaynak örneklendirme yerine, `concurrent.futures` içeri aktarın. Bu soyut havuz yöneticisi, çok iş parçacıklı işçileri (`ThreadPoolExecutor`) ve izole alt süreçleri (`ProcessPoolExecutor`) aynı şekilde basitleştirir.

Çapraz Sınavlarda Yürütmeyi Koordinasyon: Dört benzersiz senaryo boyunca görevlerinizi çalıştıran bir benchmark çerçevesi kurun:

İş Parçacığı Yoluyla CPU Görevleri: GIL'in çekirdekleri sırayla rekabet etmeye zorlaması nedeniyle performans kısıtlamasına dikkat edin.

Süreç Yoluyla CPU Görevleri: Ayrı sistem süreçlerinin farklı fiziksel CPU çekirdekleri üzerinde eş zamanlı çalıştığı için performans artışına dikkat edin.

İş Parçacığı Yoluyla I/O Görevleri: İş parçacıklarının, minimum sistem yüküyle boş ağ bekleme süreleri sırasında yürütmeyi nasıl verimli bir şekilde bıraktığını izleyin.

Süreç Yoluyla I/O Görevleri: Basit bekleme durumları için ayrı süreçler başlatmanın getirdiği operasyonel kaynak yüküne dikkat edin.

### Adım 3: Benchmark'ları Çalıştırma
Profilleme betiğini çalıştırın. Konsol çıktısı, hangi stratejinin her tür işlem darboğazına uyduğunu gösteren hassas yürütme süreleri sunar.
```bash
python main.py



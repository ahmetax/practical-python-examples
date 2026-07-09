# Proje 35: Multiprocessing Temelleri

Python'ın standart `multiprocessing` modülünü kullanarak paralel, CPU-bound iş yüklerinin sıfırdan nasıl yürütüleceğini gösteren bir hesaplama benchmark projesi. Bu mimari, Python'ın Global Interpreter Lock (GIL) kısıtlamalarını tamamen atlatmak için bağımsız işletim sistemi süreçleri (process) nasıl başlatılacağını gösteriyor.

## Mimari Hedef
Uygulama, senkron (synchronous) yürütme döngülerinden veya thread paylaşım havuzlarından uzaklaşır. Ağır hesaplama işlemleri (matematiksel faktöriyeller, görüntü işleme veya veri kümesi dönüşümleri gibi) ele alınırken, standart thread'ler GIL nedeniyle aynı yürütme çekirdeği için rekabet eder. Bu modül, farklı iş yüklerini doğrudan izole işletim sistemi süreçlerine eşleyerek, mevcut tüm CPU çekirdekleri üzerinde gerçek paralel kaynak kullanımını zorlar.

## Proje Yapısı
```text
35_multiprocessing_basics/
└── main.py
```

**System Requirements**
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible multi-core environment)
- Runtime: Python 3.12+
- Dependencies: None (Uses standard library built-ins)

## How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated folder for this project inside your repository workspace:

```bash
mkdir 35_multiprocessing_basics
cd 35_multiprocessing_basics
```

### Adım 2: Paralel Hesaplama Motorunu Uygulama
`main.py` adında bir dosya oluşturun. Eş zamanlı yürütme katmanınızı adım adım oluşturun:

Giriş Noktası Yürütmesini Korumak: Yürütme bloğunuzu her zaman `if __name__ == "__main__":` ile güvence altına alın. Bu, multiprocessing'te zorunludur; yeni bir süreç oluşturulduğunda, ana dosya yeniden içe aktarılır ve bu koruma olmadan, alt süreç daha fazla süreç oluşturmanın sonsuz, özyinelemeli bir döngüsünü tetikler.

Hesaplama Görevini Taslağını Çıkarmak: Bireysel süreçleri meşgul tutmak için yoğun döngülerle ilgilenen bir CPU-bound matematiksel fonksiyon (örneğin, `compute_heavy_factorial`) tasarlayın.

Süreçleri Örneklemek ve Başlatmak: Veri kümesi dizileriniz üzerinde döngü yapın. Her hedef iş yükü için, `multiprocessing.Process(target=..., args=...)` kullanarak ayrı bir yürütme izleme işçi örneği oluşturun. Her örneğe `.start()` çağrısı yaparak Ubuntu çekirdeğine taze bağımsız yürütme bellek adresleri haritalamasını emredin.

Ana Döngü Yaşam Döngülerini Senkronize Etmek: Aktif süreç nesnelerinizin dizisi üzerinde döngü yapın ve her işçiye `.join()` çağrısı yapın. Bu, ana master daemon sürecini duraklatmaya ve tüm eş zamanlı alt süreçlerin hesaplamalarını bitirmesini beklemeye zorlar, böylece metrikleri sonlandırıp temiz bir şekilde çıkış yapabilir.

### Adım 3: Çalıştırma ve Doğrulama
Paralel betiği yerel terminal arayüzünüzden çalıştırın:

```bash
python3 main.py
```

Watch the terminal outputs carefully. You will see all workers start almost simultaneously, calculating independent numbers concurrently rather than processing them one after another in a linear line.


---

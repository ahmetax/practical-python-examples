# Proje 36: Asyncio Temelleri

Python'ın standart `asyncio` çatısını kullanarak tek iş parçacıklı, engellemeyen (non-blocking) eşzamanlılığı gösteren bir ağ simülasyon projesi. Bu mimari, modern `async/await` paradigmasının yüksek performanslı I/O-bound iş akışlarını nasıl yapılandırdığını sergiliyor.

## Mimari Hedef
Uygulama, senkron sistemlerde tipik olan boş iş parçacığı bekleme sürelerini ortadan kaldırır. Uzak API'ler çekilirken, yavaş kalıcılık (persistence) veritabanlarına erişilirken veya devasa disk segmentleri okunurken, geleneksel betikler işlem hatlarını kilitler. Bu servis, bekleme aralıkları sırasında kontrolü merkezi bir koordinasyonlu Event Loop'a geri bırakarak, tek bir işlemci çekirdeğinin binlerce açık soketi aynı anda işlemesine olanak tanır.

## Proje Yapısı
```text
36_asyncio_basics/
└── main.py
```
## Sistem Gereksinimleri
- **OS**: Ubuntu 24.04 (veya herhangi bir Linux/UNIX uyumlu sistem)
- **Runtime**: Python 3.12+
- **Dependencies**: Yok (Standart kütüphane yerleşik özelliklerini kullanır)

## Bu Projeyi Sıfırdan Nasıl Oluşturursunuz

### Adım 1: Dizin Kurulumu
Çalışma alanı deponuz içinde özel bir proje dizin yapısı oluşturun:
```bash
mkdir 36_asyncio_basics
cd 36_asyncio_basics
```
### Adım 2: Asenkron Döngü Mantığını Uygulama
`main.py` adında bir dosya oluşturun. Non-blocking concurrency bileşenlerinizi adım adım oluşturun:

1. **Async Sözdizimi ile Coroutine Tanımlama**: Takip fonksiyonlarınızı açık `async def` sözdizimi kullanılarak bildirin. Bu, fonksiyonu düz bir primitive değer yerine awaitable bir nesne döndüren bir coroutine olarak işaretler.
2. **Non-Blocking Duraklamaları Kullanma**: Coroutine içinde, standart blocking hook'lar olan `time.sleep()` yerine `await asyncio.sleep()` kullanın. `await` anahtar kelimesi, ağ yanıtları veya zaman aşımları beklenirken yürütmeyi paylaşılan event loop örneğine geri vermesini açıkça komuta eder.
3. **Concurrency İçin Görevleri Sarmalama**: Ana koordinatör rutini içinde, coroutine çağrılarını `asyncio.create_task()` içine sarın. Bu, yürütmeyi hemen alttaki event loop kuyruğuna kaydeder ve anında arka plan işleme zamanlar.
4. **Gather ile Sonuçları Toplama**: Tüm kayıtlı görevler nihai çözüm durumlarına ulaşana kadar süpervizör bloğunu duraklatmak için `await asyncio.gather(task1, task2, ...)` kullanın ve tüm dönüş değerlerini yapılandırılmış bir sonuç listesine toplayın.

### Adım 3: Çalıştırma ve Doğrulama
Asenkron motoru doğrudan konsolunuzdan çalıştırın:
```bash
python3 main.py
```
Terminal çıktı dizisine dikkat edin. En kısa görev olan ("Cache-Node-Asia", 1s)'ın, en son planlanmasına rağmen, önce tamamladığını ve başarı mesajını yazdırdığını fark edin! Tüm betik, yaklaşık 3 saniyede (en uzun tek görevin süresi) bitiyor, bu da işlemlerin sırayla değil, eş zamanlı olarak yürütüldüğünü kanıtlıyor.
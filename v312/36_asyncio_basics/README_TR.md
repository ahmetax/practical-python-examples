# Proje 36: Asyncio Temelleri

Girdi/çıktı (I/O) beklemesi içeren işleri standart `asyncio` modülüyle eşzamanlı çalıştırmayı gösteren kısa bir örnek. 3, 2 ve 1 saniye süren üç sahte ağ isteği, tek bir iş parçacığında, toplam 6 saniye yerine yaklaşık 3 saniyede biter. Gerçek bir ağ bağlantısı kurulmaz; bekleme süresini `asyncio.sleep()` taklit eder.

## Nasıl Çalışır?
- `simulate_network_fetch(server_name, delay_seconds)` bir eşyordamdır (coroutine, `async def`). Bir mesaj yazdırır, `await asyncio.sleep(delay_seconds)` ile bekler, sonra bir sözlük döndürür.
- Bir eşyordam `await` noktasında beklerken olay döngüsü (event loop) diğer görevleri çalıştırır. Engelleyen `time.sleep()` ise bütün programı durdururdu.
- `main()`, üç eşyordamı `asyncio.create_task()` ile göreve dönüştürür. Görevler bu noktada yalnızca zamanlanır; `main()` ilk `await` satırına geldiğinde çalışmaya başlarlar. Bu yüzden "All network tasks scheduled" satırı, "Initiating connection" satırlarından önce yazdırılır.
- `await asyncio.gather(task1, task2, task3)` üç görevin de bitmesini bekler. En kısa görev (1 sn) önce biter, ama `gather` sonuçları bitiş sırasına göre değil, görevlerin verildiği sıraya göre döndürür.
- `asyncio.run(main())` olay döngüsünü oluşturur, `main()`i çalıştırır ve döngüyü kapatır.

## Proje Yapısı
```text
36_asyncio_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.7 veya üstü (`asyncio.run()` ve `asyncio.create_task()` 3.7'de eklendi). Python 3.12.3 ile test edilmiştir.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Asyncio Non-Blocking Event Loop Active ---

--> All network tasks scheduled onto the event loop thread. <--

[Fetch API-Gateway-Europe] Initiating connection... (Will take 3s)
[Fetch Database-Cluster-US] Initiating connection... (Will take 2s)
[Fetch Cache-Node-Asia] Initiating connection... (Will take 1s)
[Fetch Cache-Node-Asia] Data packet downloaded successfully.
[Fetch Database-Cluster-US] Data packet downloaded successfully.
[Fetch API-Gateway-Europe] Data packet downloaded successfully.

All resolved packet responses: [{'server': 'API-Gateway-Europe', 'status': 200, 'payload': 'Success Data'}, {'server': 'Database-Cluster-US', 'status': 200, 'payload': 'Success Data'}, {'server': 'Cache-Node-Asia', 'status': 200, 'payload': 'Success Data'}]

Total elapsed non-blocking pipeline duration: 3.0018 seconds.
```
Beş çalıştırmada toplam süre 3,0007 ile 3,0020 saniye arasında çıktı. Aynı üç bekleme art arda yapılsaydı 6 saniye sürerdi.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/14/pythonda-asyncio-beklerken-diger-isleri-yapan-kod-nasil-yazilir/
- `asyncio` belgeleri: https://docs.python.org/3/library/asyncio.html

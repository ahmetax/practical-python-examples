# Proje 35: Multiprocessing Temelleri

CPU'yu yoğun kullanan işleri standart `multiprocessing` modülüyle paralel çalıştırmayı gösteren kısa bir örnek. Global Interpreter Lock (GIL) nedeniyle tek bir yorumlayıcının içinde aynı anda yalnızca bir iş parçacığı (thread) Python kodu çalıştırabilir. Ayrı süreçlerin (process) ise her birinin kendi yorumlayıcısı ve kendi GIL'i vardır. Bu yüzden birden çok CPU çekirdeğini aynı anda kullanabilirler.

## Nasıl Çalışır?
- `compute_heavy_factorial(name, number)`, `number!` değerini düz bir döngüyle hesaplar ve ne kadar sürdüğünü yazdırır. Giderek büyüyen tamsayıların çarpılması bir CPU çekirdeğini meşgul eder.
- Ana blok 50000!, 55000!, 60000! ve 65000! için dört `multiprocessing.Process` nesnesi başlatır, sonra `join()` ile hepsinin bitmesini bekler.
- Sonunda toplam süre yazdırılır. Faktöriyel sonuçları kullanılmaz: `Process`, çalıştırdığı fonksiyonun dönüş değerini ana sürece geri iletmez (bunun için `Pool` ya da `Queue` gerekir).
- `if __name__ == "__main__":` koruması zorunludur. `spawn` başlatma yönteminde (Windows ve macOS'ta varsayılan) ve `forkserver` yönteminde (Python 3.14'ten itibaren Linux'ta varsayılan) alt süreçler `main.py` dosyasını yeniden içe aktarır. Koruma olmasaydı alt süreçler de yeni süreçler başlatmaya çalışırdı.
- `Worker-Core-1` … `Worker-Core-4` adları yalnızca etikettir. Kod süreçleri belirli çekirdeklere bağlamaz; hangi sürecin nerede çalışacağına işletim sistemi karar verir.

## Proje Yapısı
```text
35_multiprocessing_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.6 veya üstü (f-string). Python 3.12.3 ile test edilmiştir, 3.15.0rc2'de de çalışır.
- Üçüncü taraf paket gerekmez.
- Etkiyi tam görmek için en az dört CPU çekirdeği olan bir makine gerekir.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3, 8 mantıksal CPU)
```text
--- Multiprocessing Computational Engine Initialized ---

[Process Worker-Core-1] Started heavy computation for number: 50000...
[Process Worker-Core-2] Started heavy computation for number: 55000...
--> Successfully launched 4 parallel worker processes. <--

[Process Worker-Core-3] Started heavy computation for number: 60000...
[Process Worker-Core-4] Started heavy computation for number: 65000...
[Process Worker-Core-1] Finished in 1.2742 seconds.
[Process Worker-Core-2] Finished in 1.5521 seconds.
[Process Worker-Core-3] Finished in 1.9207 seconds.
[Process Worker-Core-4] Finished in 2.3087 seconds.

--- Parallel Computational Lifecycle Concluded ---
Total processing block completion time: 2.3172 seconds.
```
Süreler makineye ve o anki yüke göre değişir; satırların sırası da çalıştırmadan çalıştırmaya farklı olabilir. Çıktıyı bir dosyaya ya da boruya (`python3 main.py | cat`) yönlendirirseniz her alt süreç "Started" ve "Finished" satırlarını bitişte birlikte yazar. Bunun nedeni, çıktı terminale gitmediğinde arabelleğe alınmasıdır.

Ne kadar hızlanıyor? Intel i7-7700HQ (4 çekirdek, 8 iş parçacığı, `nproc` = 8) üzerinde, arka planda başka programlar da çalışırken ölçülen değerler:

| Yöntem | Toplam süre |
|--------|-------------|
| Dört çağrı art arda | 5,9–6,3 sn |
| Dört thread (`threading.Thread`) | 6,7–7,0 sn |
| Dört süreç (bu proje) | 2,3–2,8 sn |

Süreçler burada 4 kat değil, yaklaşık 2,2–2,7 kat daha hızlıdır. Her süreç farklı miktarda iş yapar; toplam süreyi en büyük iş (65000!) belirler. Süreç başlatmanın da küçük bir maliyeti vardır. Thread'ler düz döngüden hızlı değildir; bu da GIL'in etkisini gösterir.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/10/pythonda-gil-duvarini-yikmak-multiprocessing-ile-gercek-paralellik/
- `multiprocessing` belgeleri: https://docs.python.org/3/library/multiprocessing.html

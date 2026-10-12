# Proje 31: Kendi Sıralama Algoritmalarımız

`sorted()` ya da `list.sort()` kullanmadan, sıfırdan yazılmış iki klasik sıralama algoritması:

| Fonksiyon | Algoritma | Zaman karmaşıklığı |
|-----------|-----------|--------------------|
| `bubble_sort()` | Sırası bozuk komşu elemanların yerini tekrar tekrar değiştirir | O(n²), zaten sıralı listede O(n) |
| `merge_sort()` | Listeyi özyinelemeli olarak ikiye böler, sıralı yarıları birleştirir | O(n log n) |

İki fonksiyon da yeni bir liste döndürür ve girdi listesini değiştirmez.

## Nasıl Çalışır?
- **Bubble sort:** Bir kopya (`list(arr)`) üzerinde çalışır. Her geçişten sonra kalan en büyük eleman sona taşınmış olur, bu yüzden iç döngü her seferinde bir adım kısalır. Bir geçişte hiç yer değiştirme olmazsa liste zaten sıralıdır ve döngü erken biter.
- **Merge sort:** 0 ya da 1 elemanlı liste olduğu gibi döndürülür. Daha uzun listeler `len(arr) // 2` noktasından bölünür, iki yarı özyinelemeli olarak sıralanır ve `_merge()` iki indeksi (`i` ve `j`) yarılar üzerinde ilerleterek her adımda küçük olan elemanı alır.
- Örnek kod, aynı listeyi (bir negatif sayı, bir sıfır ve iki kez geçen `22` ile) iki fonksiyonla sıralar ve sonda orijinal listeyi yazdırarak değişmediğini gösterir.
- Bu `merge_sort()` **kararlı (stable) değildir**: `_merge()` içinde `left[i] < right[j]` karşılaştırması kullanıldığı için iki eleman eşit olduğunda önce sağ yarıdaki alınır. Düz tamsayılarda bunun bir etkisi yoktur, ancak anahtarı eşit olan kayıtların sırası değişebilir. `left[i] <= right[j]` yazılsaydı orijinal sıra korunurdu.

## Proje Yapısı
```text
31_custom_sorting_algorithms/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`list[int]` tip ipuçları 3.9 gerektirir). Python 3.12.3 ve 3.10 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Custom Sorting Engine Initialized ---

Original Unsorted Array : [64, 34, 25, 12, 22, 11, 90, -5, 0, 22]
------------------------------------------------------------
=== 1. Executing Bubble Sort O(n^2) ===
Bubble Sorted Result    : [-5, 0, 11, 12, 22, 22, 25, 34, 64, 90]
------------------------------------------------------------

=== 2. Executing Merge Sort O(n log n) ===
Merge Sorted Result     : [-5, 0, 11, 12, 22, 22, 25, 34, 64, 90]
------------------------------------------------------------

Verification (Original remains safe): [64, 34, 25, 12, 22, 11, 90, -5, 0, 22]
```
Betik süre ölçmez. Bir test makinesinde 3.000 rastgele tamsayıyı sıralamak `bubble_sort()` ile yaklaşık 1,5 saniye, `merge_sort()` ile yaklaşık 0,02 saniye sürdü; sizin sonuçlarınız farklı olacaktır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/28/python-ile-siralama-algoritmalari-bubble-sort-ve-merge-sort-karsilastirmasi/
- Python sıralama rehberi: https://docs.python.org/3/howto/sorting.html

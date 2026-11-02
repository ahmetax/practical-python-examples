# Proje 51: Testten Geçen Ama Yanlış — Kararsız Merge Sort ve 997. Elemanda Çöken Ağaç

31 (merge sort) ve 32 (ikili arama ağacı) numaralı projeleri bir yapay zekâ yazdı. Örnek çıktıları doğru. Bir yapay zekânın bu kodlar için tipik olarak yazacağı testler de geçiyor: "1.000 rastgele tamsayı listesinde sonuç `sorted(data)` ile aynı", "karıştırılmış 1.000 değerin hepsi bulunuyor". Bu betik, bu testlerin göremediği dört sorunu gösteriyor ve aynı testleri düzeltilmiş sürümlerde çalıştırıyor.

| | Özgün ("says") | Düzeltilmiş ("checks") |
|---|---|---|
| `merge_sort`'ta eşit anahtarlar | ters dönüyor (birleştirmede `<`) | özgün sıra korunuyor (`<=`) |
| `merge_sort`, 0 ya da 1 eleman | çağıranın kendi listesini döndürüyor | yeni liste döndürüyor |
| Sıralı girdiyle ağaç | ~997 eklemeden sonra `RecursionError` | çökmüyor (özyineleme yerine döngü) |
| Sıralı girdide arama maliyeti | O(n) | yine O(n): "O(log n)" dengeli ağaç ister |

## Nasıl Çalışır?
- 31 ve 32'deki özgün fonksiyon ve sınıflar `says_merge_sort` ve `SaysTree` adıyla değiştirilmeden (yalnızca tip ipuçları çıkarılarak) kopyalandı.
- 1. bölüm tipik testleri iki sürümde de çalıştırır. Hepsi geçer.
- 2. bölüm yalnızca puana göre karşılaştırılan kayıtları (`@dataclass(order=True)`, ad için `field(compare=False)`) bir kez doğrudan, bir kez de iki aşamalı olarak (önce ada, sonra puana göre) sıralar.
- 3. bölüm tek elemanlı bir listeyi sıralar ve sonuca eleman ekler.
- 4. bölüm 900 ve 1.000 sıralı tamsayı ekler. Varsayılan özyineleme sınırı 1.000. Çöküş noktası Python 3.11–3.15'te, işleme ve çağrı yığınının o anki derinliğine göre 996–999 eleman arasında çıktı.
- 5. bölüm döngüyle yazılmış ağacı 10.000 karışık ve 10.000 sıralı tamsayıyla kurar ve `bisect.insort` ile sıralı tutulan sıradan bir listeyle karşılaştırır.

## Proje Yapısı
```text
51_tested_but_wrong/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü. 3.12.3'te ve Docker'da 3.9, 3.13, 3.15'te denendi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```
5. bölüm birkaç saniye sürer (zincire dönmüş ağacı kurmak O(n²)).

## Örnek Çıktı (Python 3.12.3)
```text
Python 3.12.3

== 1. The typical tests ==
  says merge_sort        1000 random int lists == sorted(): True
  checks merge_sort      1000 random int lists == sorted(): True
  says tree              1000 shuffled inserts, search + in-order: True
  checks tree            1000 shuffled inserts, search + in-order: True

== 2. merge sort and equal keys ==
  input                  Ayse Can Berk Deniz   (Ayse, Berk, Deniz share score 1)
  sorted()               Can Ayse Berk Deniz
  says                   Can Deniz Berk Ayse
  checks                 Can Ayse Berk Deniz
  score, then name       expected Ali Bora Cem Dila Eda
  says (two passes)      Bora Ali Eda Dila Cem
  checks (two passes)    Ali Bora Cem Dila Eda

== 3. merge sort and short lists ==
  says                   same object: True   original after append: [42, -1]
  checks                 same object: False  original after append: [42]

== 4. sorted input and the recursive tree ==
  says, 900 sorted       ok, height 900
  says, 1000 sorted      RecursionError after 997 inserts
  checks, 1000 sorted    ok, height 1000

== 5. 'O(log n)' needs a balanced tree ==
  checks, 10000 shuffled height    34  build   0.03 s  2000 lookups  0.006 s
  checks, 10000 sorted   height 10000  build   5.77 s  2000 lookups  1.541 s
  bisect list, 10000 sorted               build   0.01 s  2000 lookups  0.002 s
```
Süreler makineye bağlıdır. 3.9 ve 3.13'te 4. bölümdeki çöküş 997 yerine 996. eklemeden sonra gelir; geri kalan her şey aynıdır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/16/testten-gecen-ama-yanlis-kararsiz-merge-sort-ikili-arama-agaci/
- Sıralama kararlılığı: https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts
- sys.setrecursionlimit: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
- bisect: https://docs.python.org/3/library/bisect.html

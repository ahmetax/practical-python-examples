# Proje 32: İkili Arama Ağacı

`Node` ve `BinarySearchTree` adlı iki sınıfla sıfırdan yazılmış bir ikili arama ağacı (BST). Bir düğümden küçük değerler soluna, büyük ya da eşit değerler sağına yerleşir. Ağaç üç işlemi destekler:

| Metot | Ne yapar? |
|-------|-----------|
| `insert(value)` | Kökten aşağı inerek değeri yeni bir yaprak olarak ekler |
| `search(target)` | `True` ya da `False` döndürür; her düğümde yalnızca sol ya da sağ alt ağaçla devam eder |
| `get_inorder_list()` | Sıralı dolaşım (sol, düğüm, sağ); değerleri sıralı olarak döndürür |

Silme ya da güncelleme işlemi yoktur.

## Nasıl Çalışır?
- `Node` bir `value` ile başlangıçta `None` olan iki referans (`left` ve `right`) tutar.
- `insert()`, `search()` ve dolaşım işi özyinelemeli yardımcı metotlarla yapılır (`_insert_recursive`, `_search_recursive`, `_inorder_recursive`).
- Tekrarlanan değerlere izin verilir: eşit değer sağ alt ağaca gider, bu yüzden `5` değerini üç kez eklerseniz dolaşım `[5, 5, 5]` verir.
- Arama ve ekleme ortalamada O(log n) adım sürer, ama yalnızca ağaç dengeli kaldığı sürece. Ağaç kendini dengelemez: zaten sıralı değerler eklerseniz her düğüm sağa gider, ağaç bağlı listeye dönüşür ve iki işlem de O(n) adım sürer. Metotlar özyinelemeli olduğu için 1.000 sıralı değer eklemek (`for i in range(1000): bst.insert(i)`) varsayılan özyineleme sınırında `RecursionError: maximum recursion depth exceeded` hatasıyla durur.

## Proje Yapısı
```text
32_data_structures_bin_tree/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.11 veya üstü. `Node | None` tip ipuçları 3.10 ister, ancak `main.py` ayrıca `from typing import Self` satırını içerir (3.11'de eklendi, kodda kullanılmıyor). Bu yüzden Python 3.10'da betik `ImportError: cannot import name 'Self' from 'typing'` hatasıyla durur. Python 3.12.3 ve 3.11 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Custom Binary Search Tree Engine Started ---

Inserting data sequentially: [50, 30, 70, 20, 40, 60, 80]
Tree populated successfully.
-------------------------------------------------------
=== 1. Tree Traversal Assessment ===
In-Order Traversal Output (Sorted): [20, 30, 40, 50, 60, 70, 80]
-------------------------------------------------------

=== 2. Targeted Binary Lookup Testing ===
Searching for target element [40]: FOUND
Searching for target element [99]: NOT FOUND
Searching for target element [20]: FOUND
-------------------------------------------------------
```
`[50, 30, 70, 20, 40, 60, 80]` ekleme sırası, derinliği 3 olan tam dengeli bir ağaç oluşturur.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/01/python-ile-ikili-arama-agaci-verileri-kendi-kendine-siralayan-bir-yapi-kurmak/
- Python eğitimi, Sınıflar: https://docs.python.org/3/tutorial/classes.html

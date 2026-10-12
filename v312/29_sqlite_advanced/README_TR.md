# Proje 29: İşlem Bağlam Yöneticisiyle SQLite CRUD

Standart `sqlite3` modülüyle yazılmış küçük bir stok örneği. Şunları gösterir:
- bağlantıyı açan, başarılı olursa commit eden, hata çıkarsa rollback yapan ve bağlantıyı her durumda kapatan bir `@contextmanager`,
- sütunlara isimle erişebilmeniz için (`row['sku']`) `row_factory` olarak `sqlite3.Row`,
- her değer için parametreli sorgular (`?` yer tutucuları); böylece kullanıcı girdisi SQL metnine karışmaz ve SQL enjeksiyonu önlenir,
- `sku` sütununda yinelenen bir kaydı `sqlite3.IntegrityError` hatasına dönüştüren `UNIQUE` kısıtı.

## Nasıl Çalışır?
- `DatabaseManager.connection()` her `with` bloğu için **yeni** bir bağlantı açar. Demonun bir dosya (`inventory.db`) kullanmasının nedeni budur: `":memory:"` verilirse her blok kendi boş veritabanını alır ve ikinci blok `no such table: inventory_items` hatasıyla durur.
- `initialize_database()`, `inventory_items` tablosunu (`id`, `sku`, `name`, `quantity`, `price`) oluşturur.
- `create_item()`, `read_all_items()`, `update_item_stock()` ve `delete_item()` her biri kendi `with db.connection()` bloğunda tek bir komut çalıştırır. `create_item()`, `IntegrityError` hatasını yakalar ve `False` döndürür.
- Betik `inventory.db` dosyasını başta ve sonda siler; normal bir çalıştırmadan sonra geride dosya kalmaz. Hatayla durursa `inventory.db` geçerli klasörde kalır.

Yöneticinin iş parçacığı (thread) güvenliği için özel bir önlemi yoktur; yalnızca her blok için ayrı bir bağlantı açar.

## Proje Yapısı
```text
29_sqlite_advanced/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`list[sqlite3.Row]` tip ipucu 3.9 gerektirir). Python 3.12.3 ve SQLite 3.45.1 (Ubuntu 24.04) ile, ayrıca `python:3.12-slim` Docker imajında (Python 3.12.15, SQLite 3.46.1) test edildi; çıktı aynıydı.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```
Betik geçerli klasörde `inventory.db` dosyasını oluşturur ve sonra siler.

## Örnek Çıktı (Python 3.12.3)
```text
--- Advanced SQLite Transaction Engine Started ---

Database schema tables initialized successfully.
-------------------------------------------------------
=== 1. Populating Data (Create) ===
[Database Error] Transaction aborted & rolled back: UNIQUE constraint failed: inventory_items.sku
[Warning] Failed to insert: SKU 'SKU-MECH-01' already exists.
-------------------------------------------------------

=== 2. Fetching Catalog Inventory (Read) ===
Item #1 | SKU: SKU-MECH-01 | Mechanical Keyboard | Stock: 45 | Price: $89.99
Item #2 | SKU: SKU-MOUS-02 | Ergonomic Wireless Mouse | Stock: 120 | Price: $49.50
-------------------------------------------------------

=== 3. Adjusting Asset Configurations (Update) ===
Stock updated successfully for item 'SKU-MECH-01'.
-------------------------------------------------------

=== 4. Deleting Records (Delete) ===
Item 'SKU-MOUS-02' removed from the active database system.
-------------------------------------------------------

=== Final Active Database State ===
Remaining -> Mechanical Keyboard | Current Stock: 50
```

## Not: Rollback ve Türkçe Yerel Ayar
Python'un `sqlite3` modülü varsayılan (eski, "legacy") işlem modunda `INSERT`, `UPDATE`, `DELETE` ve `REPLACE` komutlarından önce örtük olarak bir işlem (transaction) başlatır. Python 3.12'ye kadar bu anahtar kelimeleri, yerel ayara bağlı C düzeyinde bir büyük/küçük harf duyarsız karşılaştırmayla tanır. Türkçe yerel ayarda (`LC_CTYPE=tr_TR.UTF-8`) `I` harfi küçültülünce `i` olmaz; bu yüzden `INSERT` diye yazılmış bir komut tanınmaz: işlem açılmaz, satır hemen kalıcı olarak yazılır ve sonraki `rollback()` bunu geri alamaz. Küçük harfle yazılmış `insert`, `UPDATE` ve `DELETE` etkilenmez.

Demo bundan etkilenmez, çünkü her blok tek bir komut çalıştırır. Aynı `with db.connection()` bloğuna iki komut koyduğunuzda fark ortaya çıkar. Aynı blokta önce yeni bir satır, sonra yinelenen bir SKU ekleyen bir test şu sonuçları verdi:

| Ortam | `INSERT` sonrası `in_transaction` | Başarısız bloktan sonra satır sayısı |
|-------|-----------------------------------|--------------------------------------|
| Python 3.12.3, `LC_CTYPE=tr_TR.UTF-8` | `False` | 2 (ekranda `rolled back` yazmasına rağmen ilk kayıt kaldı) |
| Python 3.12.3, `LC_ALL=C.UTF-8` | `True` | 1 (geri alındı) |
| Docker Python 3.12.15, `tr_TR.UTF-8` | `False` | 2 |
| Docker Python 3.13.16, `tr_TR.UTF-8` | `True` | 1 (geri alındı) |

Python 3.12'de çözüm: bağlantıyı `sqlite3.connect(..., autocommit=False)` ile açın (3.12'de geldi; her zaman açık bir işlem vardır ve `commit()`/`rollback()` beklendiği gibi çalışır), işlemi `conn.execute("BEGIN")` ile kendiniz başlatın ya da programı Türkçe olmayan bir `LC_CTYPE` ile çalıştırın. Python 3.13'te bu sorun yoktur.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/25/python-ve-sqlite-guvenli-ve-profesyonel-veritabani-yonetimi/
- `sqlite3` belgeleri: https://docs.python.org/3/library/sqlite3.html
- `sqlite3` ile işlem denetimi: https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions

# Proje 29: Gelişmiş SQLite Veritabanı Yönetimi

Python'ın yerel `sqlite3` sürücüsünü kullanarak sağlam ilişkisel veritabanı etkileşimlerini gösteren, üretim düzeyinde bir örnek projedir. Bu uygulama, özel işlem bağlam yönetimi, açık varlık kısıtlamaları, sözlük benzeri kayıt kod çözme ve parametrelendirme yoluyla katı SQL Injection önlemlerini kapsar.

## Mimari Hedef
Uygulama, yerel dosya depolama veya hızlı bellekteki geçici önbellekler için uyarlanmış, dayanıklı, thread-safe bir kalıcılık yönetimi modülü sağlar. Veritabanı bağlantı iş akışlarını otomatikleştirir; işlemler başarı durumunda otomatik olarak commit edilir ve operasyonel anormallikler veya bütünlük kısıtlaması hataları oluştuğunda temiz bir şekilde rollback yapılır.

## Proje Yapısı
```text
29_sqlite_advanced/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Set up an isolated directory for this specific project inside your repository workspace:

```bash
mkdir 29_sqlite_advanced
cd 29_sqlite_advanced

### Adım 2: Kalıcılık Katmanını Oluşturma
`main.py` adında bir dosya oluşturun. İlişkisel sarmalayıcı sisteminizi adım adım inşa edin:

Bir Bağlantı Context Utility'si Oluşturma: Veritabanı yaşam döngülerini güvenli bir şekilde yönetmek için `contextlib` kütüphanesindeki `@contextmanager` özelliğinden yararlanın. Jeneratör context bloğunuzun içinde, `sqlite3.connect()` kullanarak bağlantılar kurun. Düz indeks demetlerini okunabilir, sözlük benzeri anahtar eşleme örneklerine dönüştürmek için `conn.row_factory = sqlite3.Row` olarak ayarlayın.

İşlemleri ve Hataları Yönetme: Yöneticinin içine açık bir `try/except/finally` dizisi uygulayın. Veritabanı bağlantılarını işlemlerinize iletmek için bir `yield` ifadesi kullanın. İşlemler başarıyla çalışırsa, `conn.commit()` çağırın. Bir istisna oluşursa, onu yakalayın ve veritabanı bütünlüğünü korumak için `finally` bloğunda bağlantıları kapatmadan önce zorla bir `conn.rollback()` yapın.

Temel Veritabanı Şemasını Tasarlama: Otomatik artan birincil anahtarlar, benzersiz SKU etiketleri, stringler, tamsayı sayımları ve hassasiyet float alanları içeren temel bir referans tablo oluşturan bir başlatma fonksiyonu tanımlayın (örneğin, `initialize_database(db)`).

Güvenli Parametreli CRUD Bloklarını Uygulama: Özel veri hattı metotları oluşturun (`create_item`, `read_all_items`, `update_item_stock`, `delete_item`). Ham değişkenleri asla SQL satırlarına string-interpolate etmeyin. Bunun yerine, yer tutucu semboller (?) kullanarak temiz sorgu ifadeleri iletin ve değişkenlerinizi eşleşen argüman demetleri içinde iletin. Bu, veritabanı motorunun girdi verilerini güvenli bir şekilde kaçırmasını (escape) ve kötü amaçlı SQL enjeksiyon dizilerini engellemesini sağlar.

### Adım 3: Çalıştırma ve Doğrulama
Yürütme bloğunuzun içine (if `__name__ == "__main__":`) hızlı bir deneme çalıştırması yapılandırın. Özel dosya adı ":memory:" kullanarak bellekte bir veritabanı başlatın, oluşturma prosedürlerini çağırın, kayıt varyasyonlarını tetikleyin, kısıtlama limitlerini yakalayın ve sonuçları konsola kaydedin. Betiği çalıştırın:
```bash
python main.py



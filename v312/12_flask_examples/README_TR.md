# 🚀 Python ile Flask Örnekleri

Bu proje, farklı karmaşıklık seviyelerinde iki pratik Flask uygulaması içermektedir: minimal bir "Hello World" sunucusu ve SQLite tabanlı, tam fonksiyonel bir REST API. Bu örnekler, Flask temellerini öğrenmek ve veritabanı entegrasyonuna sahip web servisleri oluşturmak için mükemmeldir.

---

## 📁 Proje Yapısı

```text
12_flask_examples/
├── 01_flask_hello.py           # Minimal Flask sunucusu
├── flask_helpers.py           # Minimal uygulama için rotalar
├── 02_flask_sqlite_api.py     # SQLite veritabanlı REST API
├── flask_sqlite_helpers.py    # API rota yöneticileri ve VB mantığı
├── library.db                 # SQLite veritabanı (otomatik oluşturulur)
└── flask_sqlite_api_guide.md  # Ek API dokümantasyonu
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### Gereksinimler
Flask'ı yükleyin:
```bash
pip install flask
```

---

## Bölüm 1: Minimal Flask Sunucusu (`01_flask_hello.py`)

**Hedef**: Metin ve JSON yanıtları veren basit bir Flask web sunucusu oluşturmak.

### Adım 1: Yardımcı Modülü Oluşturun (`flask_helpers.py`)
Bu dosya, ana uygulamayı temiz tutmak için rota tanımlarını içerir.

1. `flask` modülünden `jsonify` fonksiyonunu içe aktarın.
2. Flask uygulamasını parametre olarak alan `setup_routes(app)` fonksiyonunu tanımlayın.
3. **İndeks rotasını tanımlayın**:
   - `@app.route('/')` dekoratörünü kullanın.
   - `'Hello from Python + Flask!'` dizisini döndürün.
4. **Ping rotasını tanımlayın**:
   - `@app.route('/ping')` dekoratörünü kullanın.
   - JSON döndürmek için `jsonify({'status': 'ok', 'message': 'Python + Flask is running!'})` kullanın.
5. Dosyayı kaydedin.

### Adım 2: Ana Uygulamayı Oluşturun (`01_flask_hello.py`)
Bu dosya Flask sunucusunu başlatır ve çalıştırır.

1. `flask` ve `flask_helpers` modüllerini içe aktarın.
2. Bir `main()` fonksiyonu tanımlayın.
3. Bir Flask uygulaması oluşturun: `app = flask.Flask("__main__")`.
4. Rotaları kaydetmek için `flask_helpers.setup_routes(app)` fonksiyonunu çağırın.
5. Başlangıç bilgilerini (URL, port) yazdırın.
6. Uygulamayı çalıştırın: `app.run(host="0.0.0.0", port=8117, debug=False)`.
7. Dosyanın sonunda `main()` fonksiyonunu çağırın.

### Adım 3: Sunucuyu Çalıştırın
```bash
python 01_flask_hello.py
```
- Merhaba mesajını görmek için `http://localhost:8117` adresini ziyaret edin.
- JSON yanıtını görmek için `http://localhost:8117/ping` adresini ziyaret edin.

---

## Bölüm 2: SQLite ile REST API (`02_flask_sqlite_api.py`)

**Hedef**: Kitaplar ve yazarlardan oluşan bir kütüphaneyi yönetmek için, tam CRUD operasyonları ve istatistiklere sahip eksiksiz bir REST API oluşturmak.

### Adım 1: Veritabanı Kurulumu (`02_flask_sqlite_api.py`)
Bu dosya, veritabanının mevcut olduğundan ve örnek verilerle doldurulduğundan emin olur.

1. `flask`, `sqlite3` ve `os` modüllerini içe aktarın. `flask_sqlite_helpers` modülünü ekleyin.
2. `ensure_db()` fonksiyonunu tanımlayın:
   - `db_path` değerini mevcut dizindeki `library.db` olarak belirleyin.
   - SQLite'a bağlanın ve sütun erişimi için `row_factory = sqlite3.Row` ayarını yapın.
   - Daha iyi eşzamanlılık için `PRAGMA journal_mode=WAL` komutunu çalıştırın.
   - **`authors` tablosunu oluşturun**: id (PK), name (TEXT, UNIQUE).
   - **`books` tablosunu oluşturun**: id (PK), title, author_id (FK), year, genre, rating.
   - **Yazarları ekleyin**: `INSERT OR IGNORE` kullanarak "George Orwell", "Frank Herbert", "Isaac Asimov" vb. ekleyin.
   - **Kitapları ekleyin**: Yardımcı bir fonksiyonla yazar ID'lerini alın, ardından "1984", "Dune", "Foundation" gibi kitap kayıtlarını ekleyin.
   - Bağlantıyı onaylayın (commit) ve kapatın.
3. `main()` fonksiyonunu tanımlayın:
   - Veritabanını başlatmak için `ensure_db()` fonksiyonunu çağırın.
   - Flask uygulamasını oluşturun: `app = flask.Flask("__main__")`.
   - API rotalarını kaydetmek için `flask_sqlite_helpers.setup_routes(app)` fonksiyonunu çağırın.
   - API uç nokta bilgilerini yazdırın.
   - Uygulamayı 8117 portunda çalıştırın.

### Adım 2: API Yardımcılarını Oluşturun (`flask_sqlite_helpers.py`)
Bu dosya tüm rota yöneticilerini ve veritabanı mantığını içerir.

1. `sqlite3`, `Flask`, `jsonify` ve `request` modüllerini içe aktarın.
2. `DB_PATH = "library.db"` değerini tanımlayın.
3. **Veritabanı Yardımcı Fonksiyonları**:
   - `get_conn()`: `row_factory = sqlite3.Row` ayarına sahip bir sqlite3 bağlantısı döndürür.
   - `row_to_dict(row)`: Bir sqlite3 satırını (Row) Python sözlüğüne (dictionary) dönüştürür.
4. **`setup_routes(app)` fonksiyonunu tanımlayın** ve aşağıdaki uç noktaları uygulayın:

   #### GET `/api/books`
   - İsteğe bağlı `?genre=Sci-Fi` sorgu parametresini kabul eder.
   - Tür belirtilmişse türe göre filtreler; aksi takdirde tüm kitapları döndürür.
   - Yazar adını almak için `books` ve `authors` tablolarını birleştirir (Join).
   - Kitapların JSON listesini döndürür.

   #### GET `/api/books/<id>`
   - ID'ye göre tek bir kitabı getirir.
   - Bulunamazsa 404 döndürür, aksi takdirde JSON kitap nesnesini döndürür.

   #### GET `/api/authors`
 la
   - Tüm yazarları, kitap sayılarını hesaplayan bir LEFT JOIN ile seçer.
   - Yazarlara göre gruplar ve kitap sayısına göre azalan sırada sıralar.
   - Kitap sayılarıyla birlikte yazarların JSON listesini döndürür.

   #### POST `/api/books`
   - JSON gövdesi bekler: `{"title": "...", "author": "...", "year": 1984, "genre": "...", "rating": 4.5}`.
   - Gerekli alanları doğrular.
   - **Yazar Mantığı**: Yazar var mı kontrol eder; yoksa ekler.
   - Yeni kitabı ekler ve yeni ID ile birlikte 201 Created döndürür.

   #### PUT `/api/books/<id>`
   - Alanların herhangi bir alt kümesini içeren JSON gövdesi bekler: title, year, genre, rating.
   - İzin verilen alanları doğrular.
   - Dinamik SQL oluşturur: `UPDATE books SET field1=?, field2=? WHERE id=?`.
 la
   - Başarı mesajı döndürür veya bulunamazsa 404 döndürür.

   #### DELETE `/api/books/<id>`
   - ID'ye göre kitabı siler.
   - Başarı mesajı döndürür veya bulunamazsa 404 döndürür.

   #### GET `/api/stats`
   - Toplam kitap sayısı ve ortalama puanı hesaplar.
   - Tür başına kitap sayısını almak için türe göre gruplandırır.
   - Özet istatistikleri içeren bir JSON döndürür.
5. Dosyayı kaydedin.

### Adım 3: API Sunucusunu Çalıştırın
```bash
python 02_flask_sqlite_api.py
```

### Adım 4: API'yi Test Edin
`curl` kullanarak test edebilirsiniz:

```bash
# Tüm kitapları getir
curl http://localhost:8117/api/books

# Türe göre filtreleyerek kitapları getir
curl "http://localhost:8117/api/books?genre=Sci-Fi"

# Tek bir kitabı getir
curl http://localhost:8117/api/books/1

# Tüm yazarları getir
curl http://localhost:8117/api/authors

# İstatistikleri getir
curl http://localhost:8117/api/stats

# Yeni bir kitap ekle
curl -X POST http://localhost:8117/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Yeni Kitap", "author": "Yeni Yazar", "year": 2024, "genre": "Kurgu", "rating": 4.0}'

# Bir kitabı güncelle
curl -X PUT http://localhost:8117/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"rating": 4.8}'

# Bir kitabı sil
curl -X DELETE http://localhost:8117/api/books/1
```

---

## 📖 Gösterilen Temel Kavramlar

- **Flask Uygulama Başlatma**: Bir Flask uygulaması oluşturmak ve geliştirme sunucusunu çalıştırmak.
- **Rota Tanımlama**: URL'leri Python fonksiyonlarına eşlemek için dekoratörleri (`@app.route`) kullanmak.
- **JSON Yanıtları**: JSON formatında veri döndürmek için `jsonify` kullanmak.
- **SQLite Entegrasyonu**: Veritabanına bağlanmak, sorgular yürütmek ve satırları işlemek.
- **Veritabanı Besleme (Seeding)**: Başlangıçta otomatik olarak tablolar oluşturmak ve örnek veriler eklemek.
- **REST API Tasarımı**: CRUD operasyonları için REST ilkelerini (GET, POST, PUT, DELETE) takip etmek.
- **Dinamik SQL**: Kısmi güncellemeler (PUT) için dinamik SQL sorguları oluşturmak.
- **Hata Yönetimi**: Uygun HTTP durum kodlarını (404, 400, 201) döndürmek.

---

## 🏃 Her İki Örneği Çalıştırma

1. Proje klasörüne gidin.
2. Minimal Flask sunucusunu çalıştırın:
   ```bash
   python 01_flask_hello.py
   ```
   Ardından tarayıcınızda `http://localhost:8117` adresini açın.

3. Sunucuyu durdurun (Ctrl+C) ve REST API'yi çalıştırın:
   ```bash
   python 02_flask_sqlite_api.py
 la
   ```
   Uç noktaları curl veya Postman gibi bir araçla test edin.

---

## 🔧 Genişletme Fikirleri

- Bearer tokenları kullanarak API'ye **kimlik doğrulama** ekleyin.
- `/api/books` uç noktasına **sayfalama (pagination)** ekleyin.
- Bu API'yi tüketmek için HTML/JS kullanarak bir **ön yüz (frontend)** oluşturun.
- SQL `LIKE` sorguları ile **arama fonksiyonu** ekleyin.

# 💰 Gider Takip Web Uygulaması

Kişisel harcamaları takip etmek için geliştirilmiş, hafif ve kullanıcı dostu bir Flask uygulaması. Kullanıcıların harcamaları kaydetmesine, bir panel üzerinden özet istatistikleri görüntülemesine ve görsel grafiklerle detaylı aylık raporlar oluşturmasına olanak tanır.

## 🚀 Özellikler

- **Harcama Ekleme**: Açıklama, tutar, kategori ve tarih ile işlemleri kaydedin.
- **Panel Özeti**: Toplam harcamaları, aylık harcamaları ve haftalık harcamaları tek bakışta görüntüleyin.
- **Görsel Analiz**: Kategorilere göre harcama dağılımını gösteren bir halka (doughnut) grafik.
- **Harcama Silme**: Tekil kayıtları kolayca kaldırın.
- **Aylık Raporlar**: Aylar arasında geçiş yaparak şunları görüntüleyin:
  - Günlük harcama sütun grafiği (Chart.js kullanılarak)
  - Kategori dağılım tablosu
  - Günlük ortalama harcama
  - En yüksek harcama yapılan kategori

---

## 📁 Proje Yapısı

```text
expense_app/
├── expense_app.py          # Uygulama giriş noktası ve DB başlatma
├── expense_helpers.py      # Flask rotaları, mantık ve DB yardımcıları
├── expense.db              # SQLite veritabanı (otomatik oluşturulur)
└── expense_templates/      # HTML UI şablonları
    ├── base.html           # Ortak düzen (Navbar, CSS, Flash mesajları)
    ├── index.html         # İstatistikler, grafik ve son harcamaların olduğu panel
    ├── add.html           # Yeni harcama ekleme formu
    └── report.html        # Grafiklerle birlikte aylık rapor
```

---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Gereksinimler
Gerekli kütüphaneyi yükleyin:
```bash
pip install flask
```

### 2. Veritabanı Kurulumu
Giriş noktası script'inizde bir `ensure_db()` fonksiyonu oluşturun. Bu fonksiyon şunları yapacaktır:
- `expense.db` adında bir SQLite veritabanı dosyasına bağlanacaktır.
- Eğer mevcut değilse, aşağıdaki şema ile bir `expenses` tablosu oluşturacaktır:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - `description` (TEXT, NOT NULL)
  - `amount` (REAL, NOT NULL)
  - `category` (TEXT, DEFAULT 'Other')
  - `date` (TEXT, NOT NULL)
- Değişiklikleri onaylayacak (commit) ve bağlantıyı kapatacaktır.

### 3. Uygulama Girişi (`expense_app.py`)
- Bir Flask uygulama nesnesi başlatın.
- Oturum yönetimi için bir `secret_key` belirleyin.
- Veritabanı kurulum fonksiyonunu çağırın.
- Yardımcı modülünüzden `setup_routes()` fonksiyonunu içe aktarın ve çağırın.
- Flask uygulamasını `0.0.0.0` hostu ve `8117` portu üzerinde çalıştırın.

### 4. Çekirdek Mantık (`expense_helpers.py`)
Tüm rota mantığını ve veritabanı işlemlerini yönetmek için bir yardımcı modül oluşturun.

#### Veritabanı Yardımcıları
- **`get_conn()`**: Sütunlara isimle erişebilmek için `row_factory = sqlite3.Row` ile bir sqlite3 bağlantısı döndürür.
- **`row_to_dict(row)`**: Bir sqlite3 Row nesnesini standart bir Python sözlüğüne dönüştürür.
- **`get_stats(conn)`**: Şunları hesaplamak için SQL sorguları yürütür:
  - Toplam harcama (tüm harcamaların toplamı).
  - Bu ayın harcamaları (mevcut yıl-ay üzerinde `LIKE` sorgusu kullanarak).
  - Bu haftanın harcamaları (tarih >= haftanın başlangıcı filtresiyle).
  - Toplam harcama sayısı.
- **`get_cat_data(conn, year, month)`**: Harcamaları kategoriye göre gruplandırarak toplamlar ve sayılarla birlikte toplulaştırılmış verileri döndürür.

#### Rota İşleyicileri

1. **`index` (GET `/`)**:
   - Tüm istatistikleri ve son harcamaları çeker (LIMIT 20, tarihe göre DESC sıralı).
   - Kategori dağılım verilerini alır.
   - Halka grafik için etiketleri ve değerleri şablona gönderir.

2. **`add_expense` (GET/POST `/add`)**:
   - **GET**: Bugünün tarihini önceden doldurarak formu oluşturur.
   - **POST**: Açıklama, tutar ve tarihin girildiğini doğrular. Tutarın pozitif bir sayı olduğundan emin olur. Yeni kaydı veritabanına ekler ve bir başarı mesajı gönderir (flash).

3. **`delete_expense` (POST `/delete/<id>`)**:
   - Verilen ID'ye sahip harcamayı siler.
   - Yönlendiren sayfaya (panel veya rapor) geri döner.

4. **`report` (GET `/report`)**:
   - İsteğe bağlı `year` (yıl) ve `month` (ay) sorgu parametrelerini kabul eder (varsayılan olarak mevcut tarih).
   - Gezinme bağlantıları için önceki ve sonraki ayı hesaplar.
   - Seçilen ay için tüm harcamaları çeker.
 la- Verileri günlük bir haritaya (gün -> toplam tutar) toplulaştırır.
   - Chart.js için diziler oluşturur: ayın günleri (etiketler) ve günlük toplamlar (değerler).
   - Aylık toplamı, kayıt sayısını, günlük ortalamayı ve en yüksek harcama kategorisini hesaplar.
   - Tüm bu verileri rapor şablonuna gönderir.

### 5. UI Şablonları (`expense_templates/`)

- **`base.html`**: HTML iskeletini tanımlayın, grafikler için CDN üzerinden Chart.js'i dahil edin ve "Panel" ve "Harcama Ekle" bağlantılarını içeren bir navigasyon çubuğu oluşturun. Flash mesajları için bir bölüm ekleyin.
- **`index.html`**: Dört adet istatistik kartı (Toplam, Bu Ay, Bu Hafta, Toplam Kayıt) görüntüleyin. Halka grafik için bir canvas elementi ekleyin. Alt kısımda, her satır için bir silme butonu içeren bir tabloda son harcamaları listeleyin.
- **`add.html`**: Açıklama (metin), Tutar (sayı), Kategori (Yemek, Ulaşım, Faturalar, Eğlence, Diğer gibi seçenekleri içeren açılır menü) ve Tarih (tarih girişi) alanlarına sahip bir form oluşturun. Göndermek için POST kullanın.
- **`report.html`**: Önceki/sonraki aya gitmek için gezinme okları ekleyin. "Ay Yıl" gösteren bir başlık ekleyin. Günlük harcamalar için bir sütun grafiği (bar chart) canvas'ı ekleyin. Alt kısımda, kategori dağılım tablosunu gösterin. En altta, özet istatistikleri (Aylık Toplam, Günlük Ortalama, En Yüksek Kategori) görüntüleyin.

---

## 🏃 Nasıl Çalıştırılır?

1. Flask'ın yüklü olduğundan emin olun:
   ```bash
   pip install flask
   ```
2. Uygulamayı çalıştırın:
   ```bash
   python expense_app.py
   ```
3. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📖 Gösterilen Temel Kavramlar

- **Flask Web Geliştirme**: Yönlendirme (routing), şablonlar (Jinja2) ve form yönetimi.
- **SQLite Entegrasyonu**: Veritabanı oluşturma, sorgu çalıştırma ve verileri toplulaştırma.
- **Veri Görselleştirme**: Python verilerinden halka ve sütun grafikleri oluşturmak için **Chart.js** entegrasyonu.
- **Tarih Yönetimi**: Aylık görünümleri ve hesaplamaları yönetmek için Python'un `datetime` ve `calendar` modüllerinin kullanımı.
- **Oturum Flash Mesajları**: Eylemler için kullanıcı geri bildirimi (başarı/hata mesajları) sağlama.

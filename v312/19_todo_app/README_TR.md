# ✅ Yapılacaklar Listesi Web Uygulaması

**Python**, **Flask** ve **SQLite** ile oluşturulmuş temiz ve işlevsel bir Yapılacaklar Listesi uygulaması. Bu uygulama, kullanıcılara öncelik seviyeleri, filtreleme ve gerçek zamanlı ilerleme istatistikleri ile günlük görevlerini yönetmelerine yardımcı olur.

## 🚀 Özellikler

- **Görev Yönetimi**: Görevler için tam CRUD (Oluşturma, Okuma, Güncelleme, Silme) yetenekleri.
- **Öncelik Seviyeleri**: Görevleri önem sırasına göre düzenlemek için öncelikler (Yüksek, Orta, Düşük) atama.
- **Hızlı Anahtarlar**: Görevleri tek bir tıklama ile tamamlandı veya bekliyor olarak işaretleme.
- **Akıllı Filtreleme**: Görevleri durumlarına göre görüntüleme:
  - **Tümü**: Her şeyi görüntüle.
  - **Bekleyen**: Yalnızca tamamlanmamış görevleri gösterir (önceliğe göre sıralanmış).
  - **Tamamlandı**: Yalnızca tamamlanmış görevleri görüntüle.
  - **Yüksek Öncelik**: Kritik bekleyen görevlere odaklanma.
- **Canlı İstatistikler**: Toplam görev sayısı, bekleyen görev sayısı, tamamlanmış görev sayısı ve yüksek öncelikli bekleyen görevleri gösteren bir gösterge paneli.
- **Toplu İşlemler**: Tüm tamamlanmış görevleri tek bir tıklamayla temizleme yeteneği.

---

## 📁 Proje Yapısı
```text
19_todo_app/
├── todo_app.py           # Application entry point & DB initialization
├── todo_helpers.py       # Flask routes and DB logic
├── todo.db               # SQLite database (auto-created)
└── todo_templates/       # UI templates
    ├── base.html         # Shared layout and CSS
    ├── index.html        # Main task list and dashboard
    └── edit.html         # Task modification form
```
---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Koşullar
Gerekli kütüphaneyi kurun:
```bash
pip install flask
```
### 2. Veritabanı Kurulumu (`todo_app.py`)
Uygulama başlangıcında çalışacak ve SQLite veritabanını başlatacak bir `ensure_db()` fonksiyonu uygulayın.
- **Veritabanı Dosyası**: `todo.db`.
- **Tablo Şeması**: Aşağıdaki sütunlara sahip bir `tasks` tablosu oluşturun:
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT.
  - `title`: TEXT NOT NULL.
  - `priority`: TEXT (örn: 'high', 'medium', 'low') varsayılan değeri 'medium' olmalıdır.
  - `done`: INTEGER (beklemede için 0, tamamlandı için 1) varsayılan değeri 0 olmalıdır.
  - `created_at`: TEXT (oluşturulma zaman damgası).

### 3. Çekirdek Mantık (`todo_helpers.py`)

Aşağıdaki yardımcı fonksiyonları ve route handler'ları uygulayın:

#### A. Veritabanı Yardımcı Fonksiyonları
- **`get_conn()`**: Sütunlara isimle erişim sağlamak için `row_factory = sqlite3.Row` içeren `todo.db` bağlantısını döndürür.
- **`row_to_dict(row)`**: SQLite satırlarını şablonlarda daha kolay kullanılabilmesi için Python sözlüklerine dönüştüren bir yardımcı fonksiyondur.
- **`get_stats(conn)`**: Toplam, tamamlanan, bekleyen ve yüksek öncelikli görevler için sayım işlemleri gerçekleştirir.

#### B. Route Handler'lar
- **Index (`GET /`)**:
  - `filter` sorgu parametresini okur.
  - Görevleri önceliğe göre (`high` $\rightarrow$ `medium` $\rightarrow$ `low`) sıralamak için SQL'de bir `CASE` ifadesi kullanır.
  - Karşılık gelen görevleri ve mevcut istatistikleri çeker.
  - `index.html` şablonunu render eder.
- **Görev Ekleme (`POST /add`)**:
  - Formdan `title` ve `priority` değerlerini çıkarır.
  - Başlığın boş olmadığından emin olmak için doğrulama yapar.
  - Mevcut zaman damgası ile `tasks` tablosuna yeni bir kayıt ekler.
- **Durum Değiştirme (`POST /toggle/<id>`)**:
  - `done` sütununu değerini ters çevirerek günceller (`done = 1 - done`).
- **Görev Düzenleme (`GET` ve `POST /edit/<id>`)**:
  - **GET**: Belirli görevi ID ile çeker ve düzenleme formunda gösterir.
  - **POST**: Görevin `title` ve `priority` değerlerini günceller.
- **Görev Silme (`POST /delete/<id>`)**:
  - Belirli görevi veritabanından kaldırır.
- **Tamamlananları Temizle (`POST /clear_done`)**:
  - `done = 1` olan kayıtlar için bir `DELETE` sorgusu çalıştırır.

### 4. Uygulama Girişi (`todo_app.py`)
- Flask uygulamasını başlatır.
- Bir `secret_key` ayarlar ( `flash()` mesajları kullanmak için esastır).
- Veritabanını hazırlamak için `ensure_db()` çağrılır.
- Tüm endpoint'leri kaydetmek için `todo_helpers.setup_routes(app)` çağrılır.
- Sunucu 8117 portunda çalıştırılır.

### 5. Frontend Uygulaması (`todo_templates/`)

- **`base.html`**: Temiz bir tipografi ve bir navigasyon barı dahil olmak üzere global stili tanımlar. "Görev eklendi!" veya "Görev silindi!" uyarılarını göstermek için bir flash mesajları bloğu oluşturur.
- **`index.html`**:
  - **İstatistik Çubuğu**: Özet sayımları (Toplam, Bekleyen, Tamamlanan, Yüksek) gösterir.
  - **Filtre Çubuğu**: Tümünü, Bekleyen, Tamamlanan ve Yüksek'e göre filtreleme bağlantıları oluşturur.
  - **Giriş Formu**: Bir görev başlığı girmek ve bir açılır menüden öncelik seçmek için basit bir form.
  - **Görev Listesi**: Görevlerin bir tablosu veya listesi. Her öğe, önceliği (renk kodlaması ile), tamamlanma için bir değiştirme kutusu ve düzenleme ve silme düğmeleri göstermelidir.
- **`edit.html`**: Kullanıcının görevin başlığını ve önceliğini değiştirmesine olanak tanıyan basit bir form.

---

## 🏃 Nasıl Çalıştırılır

1. Sunucuyu çalıştırın:
   ```bash
   python todo_app.py
   ```
2. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **CRUD Uygulaması**: Oluşturma, Okuma, Güncelleme ve Silme işlemlerinin klasik bir uygulamasıdır.
- **SQLite Entegrasyonu**: Basit uygulama verilerinin kalıcı depolanması için ilişkisel bir veritabanı kullanmak.
- **Dinamik Filtreleme**: Sunucu tarafında verileri filtrelemek için SQL sorgu parametreleri kullanmak.
- **Flask Oturumları ve Flashing**: Flash mesajları aracılığıyla anında kullanıcı geri bildirimi sağlamak.
- **Durum Yönetimi**: Bir görevin "Yapıldı/Yapılmadı" durumunu yönetmek.
- **Öncelik Tabanlı Sıralama**: SQL'de özel sıralama düzenleri uygulamak.

---

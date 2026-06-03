# ✍️ Flask Blog Uygulaması (Mini CMS)

**Python**, **Flask** ve **SQLite** ile geliştirilmiş, tamamen işlevsel ve hafif bir İçerik Yönetim Sistemi (CMS). Bu uygulama; kullanıcı kimlik doğrulaması, profil yönetimi ve blog yazıları için tam bir CRUD (Oluşturma, Okuma, Güncelleme, Silme) sistemini içeren eksiksiz bir kullanıcıdan-içeriğe iş akışını uygular.

## 🚀 Özellikler

### 🌍 Genel Erişim
- **Ana Sayfa**: Tüm kullanıcılardan yayınlanmış tüm blog yazılarının, en yeniden eskiye doğru sıralandığı bir akış.
- **Yazı Görünümü**: Belirli bir yazının tüm içeriğini okumak için ayrılmış özel bir sayfa.

### 🔐 Kullanıcı Kimlik Doğrulaması
- **Kayıt**: Kullanıcı adları, e-postalar ve şifre eşleşmeleri için doğrulamalar içeren yeni bir hesap oluşturma.
- **Güvenlik**: Şifreler, `bcrypt` kullanılarak güvenli bir şekilde özetlenir (hash).
- **Oturum Yönetimi**: Flask oturumları kullanılarak güvenli giriş/çıkış işlemleri.
- **Korumalı Rotalar**: Özel bir `login_required` dekoratörü, gizli sayfaların yalnızca kimliği doğrulanmış kullanıcılar tarafından erişilebilir olmasını sağlar.

### 🛠️ Kullanıcı Paneli ve Yönetimi
- **Kişisel Panel**: Kullanıcıların yalnızca kendi yazılarını görebileceği ve yönetebileceği özel bir alan.
- **Yazı Yönetimi**: Tam CRUD yetenekleri (Yeni yazılar oluşturma, mevcut olanları düzenleme, yazıları silme).
- **Profil Ayarları**: Şifre değiştirme (mevcut şifre doğrulaması ile) ve hesabı kalıcı olarak silme seçeneği.

---

## 📁 Proje Yapısı

Bu projeyi oluşturmak için dosyalarınızı şu şekilde organize edin:

```text
blog_app/
├── blog_app.py          # Uygulama giriş noktası ve DB başlatma
├── blog_helpers.py      # Rota işleyicileri, kimlik doğrulama mantığı ve DB yardımcıları
├── blog.db              # SQLite veritabanı dosyası (otomatik oluşturulur)
└── blog_templates/      # UI Klasörü
    ├── base.html        # Ortak düzen (Navbar, Flash mesajları)
    ├── index.html       # Genel akış
    ├── post.html        # Tekil yazı görünümü
    ├── login.html       # Giriş formu
    ├── register.html    # Kayıt formu
    ├── dashboard.html   # Kullanıcının özel yazı listesi
    ├── post_form.html    # Yazı oluşturma/düzenleme formu
    └── profile.html      # Hesap ayarları
```

---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ortam Kurulumu
Gerekli kütüphaneleri yükleyin:
```bash
pip install flask bcrypt
```

### 2. Veritabanı Tasarımı
SQLite veritabanının mevcut olduğundan emin olmak için giriş noktanızda bir yardımcı fonksiyon uygulayın. İki tabloya ihtiyacınız var:
- **`users`**: `id` (PK), `username` (Benzersiz), `email` (Benzersiz), `password` (Hash'lenmiş) ve `created_at` saklar.
- **`posts`**: `id` (PK), `user_id` (users tablosuna FK), `title`, `body`, `created_at` ve `updated_at` saklar.

### 3. Çekirdek Mantık (`blog_helpers.py`)
Ana uygulamayı temiz tutmak için bir yardımcı modül oluşturun. Şunları uygulayın:
- **Veritabanı Bağlantısı**: Sütunlara isimle erişebilmek için `row_factory = sqlite3.Row` ile bir `sqlite3` bağlantısı döndüren bir fonksiyon.
- **Kimlik Doğrulama Yardımcıları**:
    - `hash_password(password)`: `bcrypt.hashpw` kullanır.
    - `check_password(password, hashed)`: `bcrypt.checkpw` kullanır.
    - `login_required(f)`: Oturumda `user_id` olup olmadığını kontrol eden; yoksa giriş sayfasına yönlendiren bir sarmalayıcı (wrapper).
- **Rota İşleyicileri**:
    - **Genel Rotalar**: Yazıları yazarlarıyla ilişkilendirmek için `JOIN` içeren `SELECT` sorguları kullanın.
    - **Kimlik Doğrulama Rotaları**: Kayıt (regex doğrulaması ile) ve giriş için `POST` isteklerini yönetin.
    - **Özel Rotalar**: Kullanıcıların yalnızca `user_id`'si oturumdaki `user_id` ile eşleşen yazıları düzenleyebilmesini veya silebilmesini sağlayacak mantığı kurun.

### 4. Uygulama Girişi (`blog_app.py`)
- Flask uygulamasını başlatın.
- Oturum güvenliği için bir `secret_key` belirleyin.
- Veritabanı başlatma fonksiyonunu çağırın.
- Tüm uç noktaları kaydetmek için yardımcılar modülünüzdeki `setup_routes` fonksiyonunu çağırın.

### 5. UI Şablonları (`blog_templates/`)
Önyüzünüzü **Jinja2** şablonlarını kullanarak oluşturun:
- HTML iskeletini ve kullanıcının giriş yapıp yapmadığına göre değişen bir navigasyon çubuğunu tanımlamak için `base.html` kullanın.
- Başarı/hata uyarılarını göstermek için temel şablonda `flash` mesajlarını kullanın.
- `post_form.html` içerisinde, hem oluşturma hem de düzenleme (post nesnesi geçilerek) için çalışan formlar kullanın.

---

## 🏃 Nasıl Çalıştırılır?

1. Tüm dosyaları yukarıda açıklanan yapıya göre yerleştirin.
2. Uygulamayı çalıştırın:
   ```bash
   python blog_app.py
   ```
3. Web tarayıcınızda `http://localhost:8117` adresine gidin.

## 📈 Karmaşıklık ve Güvenlik Notları
- **Zaman Karmaşıklığı**: Çoğu veritabanı işlemi $O(1)$ veya $N$ yazı sayısı olmak üzere $O(N)$'dir; bu da küçük ve orta ölçekli bloglar için verimlidir.
- **Güvenlik**: Bu uygulama, düz metin sızıntılarını önlemek için şifrelerde **Bcrypt** ve panoya yetkisiz erişimi önlemek için **Sunucu Taraflı Oturumlar (Server-side Sessions)** kullanır.

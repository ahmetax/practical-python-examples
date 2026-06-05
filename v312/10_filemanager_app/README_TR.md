# 📁 Dosya Yöneticisi Web Uygulaması

**Python** ve **Flask** ile geliştirilmiş, tam özellikli, web tabanlı bir dosya yöneticisi. Kullanıcıların doğrudan web tarayıcısı üzerinden dosyaları yüklemesine, görüntülemesine, önizlemesine, indirmesine ve silmesine olanak tanır. Uygulama; tür tespiti, çeşitli dosya formatları için satır içi önizlemeler ve depolama istatistiklerini içeren bir panel sunar.

## 🚀 Özellikler

- **Çoklu Dosya Yükleme**: Bir form veya sürükle-bırak aracılığıyla aynı anda birden fazla dosya yükleyin.
- **Dosya Türü Tespiti**: Görselleri, PDF'leri, metin dosyalarını, arşivleri, videoları, ses dosyalarını, hesap tablolarını ve belgeleri otomatik olarak tanımlar ve bunlara uygun simgeler atar.
- **Satır İçi Önizleme**: 
  - **Görseller**: Doğrudan tarayıcıda görüntülenir.
  - **PDF'ler**: Satır içi olarak görüntülenir.
  - **Metin/Kod**: Hızlı inceleme için içeriğin ilk 20KB'lık kısmı gösterilir.
- **Dosya Bilgileri**: Dosya boyutunu (insan tarafından okunabilir formatta), yükleme/değiştirme tarihini ve MIME türünü görüntüler.
- **İndirme**: Yöneticideki herhangi bir dosyayı indirin.
- **Silme**: Depolama alanındaki dosyaları kaldırın.
- **Filtreleme**: Dosyaları kategoriye göre filtreleyin (Hepsi, Görseller, PDF'ler, Diğer).
- **İstatistikler Paneli**: Toplam dosya sayısını, kullanılan toplam alanı ve kategori başına dosya sayılarını gösterir.
- **Kopya Yönetimi**: Aynı isimle bir dosya mevcutsa, üzerine yazmayı önlemek için dosya adına bir zaman damgası ekler.

---

## 📁 Proje Yapısı

```text
filemanager_app/
├── filemanager_app.py          # Uygulama giriş noktası
├── filemanager_helpers.py      # Flask rotaları ve dosya mantığı
├── uploads/                    # Yüklenen dosyaların saklandığı dizin
└── filemanager_templates/      # HTML UI şablonları
    ├── base.html               # Ortak düzen (Navbar, CSS, Flash mesajları)
    ├── index.html              # Dosya listesi, yükleme formu, istatistikler, filtreler
    └── preview.html            # Dosya önizleme sayfası
```

---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Gereksinimler
Gerekli kütüphaneleri yükleyin:
```bash
pip install flask werkzeug
```

### 2. Uygulama Girişi (`filemanager_app.py`)
- `flask` modülünü içe aktarın.
- Bir `main()` fonksiyonu oluşturun.
- `template_folder="filemanager_templates"` belirterek bir Flask uygulama nesnesi başlatın.
- Oturum yönetimi için bir `secret_key` belirleyin.
- `filemanager_helpers` modülünü içe aktarın ve rotaları kaydetmek için `setup_routes(app)` fonksiyonunu çağırın.
- Flask uygulamasını `0.0.0.0` hostu ve `8117` portu üzerinde çalıştırın.

### 3. Çekirdek Mantık (`filemanager_helpers.py`)

#### Yapılandırma Sabitleri
- `UPLOAD_FOLDER = "uploads"` ve `MAX_MB = 16` olarak tanımlayın.
- Dosyaları kategorize etmek için `IMAGE_EXTS`, `PDF_EXTS`, `TEXT_EXTS` şeklinde uzantı kümeleri oluşturun.

#### Yardımcı Fonksiyonlar

1. **`file_icon(ext)`**:
   - Dosya uzantısına göre bir emoji dizesi döndürür (örneğin; görseller için 🖼, PDF'ler için 📄, metinler için 📝).

2. **`human_size(nbytes)`**:
   - Ham bayt boyutunu insan tarafından okunabilir bir dizeye dönüştürür (B, KB, MB, GB).

3. **`file_info(filename)`**:
 la- Bir dosya adı alır ve şunları içeren bir sözlük döndürür:
     - `filename`, `ext` (küçük harf uzantı), `icon`, `is_image`, `is_pdf`
     - `size` (biçimlendirilmiş), `size_raw` (bayt cinsinden), `date` (biçimlendirilmiş zaman damgası)

4. **`get_all_files(filter_type='all')`**:
   - `UPLOAD_FOLDER` dizinini tarar.
   - Eğer `filter_type` 'image', 'pdf' veya 'other' ise uygun şekilde filtreleme yapar.
 la- En yeniden eskiye doğru sıralanmış dosya bilgisi sözlüklerinin bir listesini döndürür.

5. **`get_stats()`**:
   - `get_all_files()` fonksiyonunu çağırır ve şunları hesaplar:
     - Toplam sayı, toplam boyut, görsel sayısı, PDF sayısı, diğerlerinin sayısı.

#### Rota İşleyicileri

1. **Ana Sayfa (GET `/`)**:
   - `filter` sorgu parametresini alır (varsayılan 'all').
 la- Filtrelenmiş dosya listesini ve istatistikleri getirir.
   - `files`, `stats`, `filter` ve `max_mb` değişkenlerini `index.html` şablonuna gönderir.

2. **Yükleme (POST `/upload`)**:
   - `request.files.getlist('files')` aracılığıyla çoklu dosya yüklemelerini yönetir.
 la- Dosya adlarını sanitize etmek (temizlemek) için Werkzeug'dan `secure_filename()` kullanır.
   - **Kopya Yönetimi**: Hedef dosya mevcutsa, yeni dosyayı bir zaman damgası ekleyerek yeniden adlandırır (örneğin, `dosya_20260516_143022.txt`).
 la- Dosyayı `uploads` dizinine kaydeder.
 la- Başarı veya hata mesajlarını flash ile bildirir.

3. **Önizleme (GET `/preview/<filename>`)**:
 la- Dosya adını güvenli hale getirir ve varlığını kontrol eder. la- Dosya türünü belirler:
     - **Görsel**: `file_type = 'image'` olarak ayarlar.
     - **PDF**: `file_type = 'pdf'` olarak ayarlar.
     - **Metin**: Önizleme için içeriğin ilk 20KB'ını okur.
     - **Diğer**: Yalnızca meta verileri gösterir. la- Dosya detayları ve (varsa) içeriği ile `preview.html` şablonunu oluşturur.

4. **İndirme (GET `/download/<filename>`)**:
 la- Flask'ın `send_from_directory` fonksiyonunu `as_attachment=True` ile kullanır.

5. **Dosya Sunma (GET `/uploads/<filename>`)**:
 la- Dosyaları satır içi olarak sunar (görsellerin/PDF'lerin indirilmeden tarayıcıda görüntülenmesi için).

6. **Silme (POST `/delete/<filename>`)**:
L- Dosya adını güvenli hale getirir ve dosyayı dosya sisteminden kaldırır. la- Yönlendiren sayfaya geri döner.

### 4. UI Şablonları (`filemanager_templates/`)

#### `base.html`
- HTML5 iskeleti. la- "Dosya Yöneticisi" bağlantısını içeren bir navigasyon çubuğu ekleyin. la- Başarı/hata bildirimleri için bir flash mesaj alanı ekleyin. la- Düzen, tablolar, kartlar ve duyarlılık (responsiveness) için temel CSS ekleyin.

#### `index.html`
- **İstatistikler Bölümü**: Toplam Dosya, Toplam Boyut, Görseller, PDF'ler ve Diğerlerini gösteren 5 kart görüntüleyin. la- `enctype="multipart/form-data"`, `multiple` özniteliğine sahip bir dosya girişi ve bir yükleme butonu olan bir form ekleyin. l- Hepsi, Görseller, PDF'ler, Diğer şeklinde filtreleme butonları ekleyin. l- Simgeler, Dosya Adı, Boyut, Tarih ve İşlemler (Önizleme, İndirme, Silme) sütunlarını içeren bir dosya tablosu oluşturun. l- `files` listesi üzerinde yineleme yapmak için Jinja2 döngülerini kullanın.

#### `preview.html`
- Dosya simgesini ve adını belirgin şekilde görüntüleyin. la- Meta verileri gösterin: Boyut, Tarih, MIME türü. l- **İçerik Alanı**:
  - Görsel ise: `<img src="{{ url_for('serve_file', filename=filename) }}">` l- PDF ise: `<embed src="...">` veya bir indirme bağlantısı. l- Metin ise: İçeriği bir `<pre>` bloğu içinde görüntüleyin. la- İşlem butonlarını ekleyin: İndir, Sil. la- "Listeye Geri Dön" bağlantısını ekleyin.

---

## 🏃 Nasıl Çalıştırılır?

1. Bağımlılıkları yükleyin:
   ```bash
   pip install flask werkzeug
   ```
2. Uygulamayı çalıştırın:
   ```bash
   python filemanager_app.py
   ```
3. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **Flask Web Geliştirme**: Yönlendirme (routing), istek yönetimi, şablon oluşturma (Jinja2).
- **Dosya Yönetimi**: `werkzeug.utils.secure_filename` kullanarak dosyaları güvenli bir şekilde yükleme, kaydetme, silme ve sunma.
- **MIME Türü Tespiti**: Python'un `mimetypes` modülünü kullanma.
- **Statik Dosya Sunma**: Hem indirmeler hem de satır içi görüntüleme için `send_from_directory` kullanımı.
- **Kullanıcı Geri Bildirimi**: Başarı ve hata mesajlarını göstermek için Flask'ın `flash` sistemini kullanma.
- **Filtreleme ve Toplama**: İstatistikler ve kategori tabanlı filtreler oluşturmak için dosya listelerini işleme.

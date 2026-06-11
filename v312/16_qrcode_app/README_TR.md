# 📱 QR Kod Oluşturucu ve Okuyucu

**Python** ve **Flask** ile geliştirilmiş; kullanıcıların özelleştirilmiş QR kodlar oluşturmasına, mevcut QR kodları görsellerden veya canlı web kamerası akışı üzerinden çözmesine olanak tanıyan kapsamlı bir web uygulaması.

## 🚀 Özellikler

### 🎨 QR Kod Oluşturucu
- **Çoklu Formatlar**: Şunlar için QR kodları oluşturun:
  - Basit Metin veya URL'ler.
  - **vCard**: Dijital kartvizitler (İsim, Telefon, E-posta, Kuruluş, URL).
  - **WiFi**: Otomatik ağ bağlantısı/girişi (SSID, Şifre, Güvenlik).
- **Özelleştirme**:
  - **Boyut**: Çeşitli çözünürlükler arasından seçim yapın (örn. 200px ile 600px arası).
  - **Hata Düzeltme (Error Correction)**: Hasar veya gürültüyü yönetmek için düzeyi ayarlayın (L, M, Q, H).
  - **Temalar**: Farklı renk paletleri seçin (örn. Beyaz üzerine Siyah, Beyaz üzerine Mavi, Koyu üzerine Beyaz).
- **Hızlı Önizleme**: Oluşturulan QR kodu anında base64 görüntüsü olarak görüntüleyin.
- **İndirme**: Sonuçlanan QR kodu yüksek kaliteli bir PNG dosyası olarak kaydedin.

### 🔍 QR Kod Okuyucu
- **Görsel Yükleme**: Bir görsel (PNG, JPG, GIF, BMP, WebP) yükleyin ve içeriğini çözün.
- **Çoklu Stratejili Çözümleme**: Düşük kaliteli görsellerde bile yüksek doğruluk sağlamak için ön işleme (gri tonlama, eşikleme, keskinleştirme ve ölçek büyütme) ile birlikte `pyzbar` ve `OpenCV` kombinasyonunu kullanır.
- **Web Kamerası ile Tarama**: Tarayıcı üzerinden canlı tarama özelliği entegre edilmiştir (istemci tarafında `jsQR` ve sunucu tarafında `/scan_frame` uç noktası kullanılır).
- **Akıllı Eylemler**: Kolay navigasyon için çözülen içerikteki URL'leri otomatik olarak tespit eder.

---

## 📁 Proje Yapısı

```text
16_qrcode_app/
├── qrcode_app.py          # Ana giriş noktası ve Flask yapılandırması
├── qrcode_helpers.py       # QR oluşturma, çözümleme mantığı ve rota yöneticileri
├── qrcode_templates/       # HTML Kullanıcı Arayüzü şablonları
│   ├── base.html           # Ortak düzen ve CSS
│   ├── create.html         # Oluşturucu arayüzü
│   └── read.html           # Okuyucu ve yükleyici arayüzü
└── static/                 # (Opsiyonel) CSS/JS dosyaları
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Gereksinimler
Gerekli Python kütüphanelerini yükleyin:
```bash
pip install flask qrcode[pil] pyzbar pillow numpy opencv-python
```
*Not: `pyzbar` sisteminizde zbar paylaşılan kütüphanesini gerektirir.*
- **Ubuntu/Debian**: `sudo apt-get install libzbar0`
- **macOS**: `brew install zbar`

### 2. Uygulama Mantığı (`qrcode_helpers.py`)

#### A. QR İçerik Oluşturucular
Verileri standartlara göre formatlayan fonksiyonlar oluşturun:
- **vCard**: `BEGIN:VCARD...END:VCARD` şeklinde formatlayın.
- **WiFi**: `WIFI:T:[Güvenlik];S:[SSID];P:[Şifre];H:[Gizli];;` şeklinde formatlayın.

#### B. QR Oluşturma (`generate_qr`)
- `qrcode` kütüphanesini kullanarak bir `QRCode` nesnesi oluşturun.
- `box_size` (toplam piksellerden hesaplanan), `error_correction` ve `border` değerlerini ayarlayın.
- Veriyi ekleyin ve görüntüyü oluşturun.
- `PIL` (Pillow) kullanarak seçilen `fill_color` (dolgu rengi) ve `back_color` (arka plan rengi) değerlerini uygulayın.
- Piksellerin keskin kalması için görüntüyü `Image.NEAREST` kullanarak istenen boyutlara getirin.
- Görüntüyü bir `BytesIO` tamponuna kaydedin ve HTML içinde doğrudan göstermek için **base64 kodlanmış bir dize** döndürün.

#### C. QR Çözümleme Stratejisi (`read_qr_from_image`)
Çeşitli görüntü kalitelerini yönetmek için sağlam bir çözümleme hattı uygulayın:
1. **Standart**: Orijinal görüntü üzerinde `pyzbar.decode` çalıştırın.
2. **OpenCV Tespiti**: `cv2.QRCodeDetector().detectAndDecode()` kullanın.
3. **Ön İşleme**:
   - Gri tonlamaya çevir $\rightarrow$ Otsu eşikleme uygula $\rightarrow$ Çözümle.
   - Keskinleştirme filtresi uygula (Laplacian/özel kernel) $\rightarrow$ Çözümle.
   - Görüntüyü kübik interpolasyon kullanarak $2\times$ büyüt $\rightarrow$ Çözümle.

#### D. Flask Rota Yöneticileri
- **`/create`**:
  - **GET**: Oluşturucu formunu gösterir.
  - **POST**: Form verilerini (tür, boyut, renk, içerik) toplar, uygun dizeyi (Metin/WiFi/vCard) oluşturur, QR görüntüsünü üretir ve önizlemeyi sunar.
- **`/download`**: En son oluşturulan QR görüntü baytlarını `send_file` PNG eki olarak sunar.
- **`/read`**:
  - **GET**: Yükleme formunu gösterir.
  - **POST**: Yüklenen bir görüntüyü alır, çözümleme hattına gönderir ve sonucu görüntüler.
- **`/scan_frame`**: Web kamerası taraması için özelleştirilmiş bir uç noktadır. Tarayıcıdan gelen base64 görüntüsünü alır, çözer ve sonucu JSON olarak döndürür.

### 3. Uygulama Girişi (`qrcode_app.py`)
- Flask uygulamasını `qrcode_templates` klasörü ile başlatın.
- `qrcode_helpers` modülünü içe aktarın ve `setup_routes(app)` fonksiyonunu çağırın.
- Sunucuyu 8117 portunda başlatın.

### 4. Ön Yüz Uygulaması (`qrcode_templates/`)

- **`base.html`**: Navigasyon ve flaş mesajlar dahil olmak üzere genel görünümü tanımlayın.
- **`create.html`**:
  - QR türünü (Metin, URL, vCard, WiFi) seçmek için bir açılır menü içeren bir form.
  - Seçilen türe göre dinamik olarak beliren giriş alanları.
  - Boyut, hata düzeltme ve renk seçenekleri.
  - Oluşturulan QR kodu göstermek için bir önizleme alanı.
- **`read.html`**:
  - Sürükle-bırak destekli bir yükleme alanı.
  - Web kamerası görüntü alanı (bir `<video>` öğesi ve kare yakalama için bir `<canvas>` kullanılır).
  - Kareleri yakalayıp `/scan_frame` uç noktasına `fetch` ile gönderen JavaScript kodları.

---

## 🏃 Nasıl Çalıştırılır?

1. Tüm bağımlılıkların ve `zbar` kütüphanesinin kurulu olduğundan emin olun.
2. Uygulamayı çalıştırın:
   ```bash
   python qrcode_app.py
   ```
3. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **QR Standart Uygulaması**: vCard ve WiFi için özel formatların yönetimi.
- **Görüntü İşleme**: Yeniden boyutlandırma ve renklendirme için `Pillow`, gelişmiş görüntü ön işlemleri (eşikleme, keskinleştirme) için `OpenCV`.
- **Bilgisayarlı Görü (Computer Vision)**: QR kod tespiti ve çözümleme için `pyzbar` ve `cv2` kullanımı.
- **İkili Veri Yönetimi**: Görüntüleri diske kaydetmeden sunmak için `io.BytesIO` ve `base64` kullanımı.
- **Gerçek Zamanlı Etkileşim**: JavaScript web kamerası kare yakalama ile Python arka uç çözümlemesinin birleştirilmesi.
- **Web Çatıları**: Dinamik yönlendirme ve dosya sunumu ile çok fonksiyonlu bir araç oluşturmak için Flask kullanımı.
 la

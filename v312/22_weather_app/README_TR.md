# 🌤️ Hava Durumu Uygulaması - Python Sürümü

**Python**, **Flask** ve **OpenWeatherMap API** ile oluşturulmuş şık ve işlevsel bir hava durumu panosu. Bu uygulama, dinamik emoji simgeleri ve bir arama geçmişi özelliği ile dünya çapındaki herhangi bir şehir için gerçek zamanlı hava ve tahmin verileri sağlar.

## 🚀 Özellikler

- **Küresel Şehir Araması**: Dünya genelindeki herhangi bir şehir için mevcut hava durumu verilerini çekme.
- **Gerçek Zamanlı Hava Durumu Verisi**:
  - Sıcaklık ve "Hissedilen" sıcaklık.
  - Nem, rüzgar hızı, atmosfer basıncı ve görünürlük.
  - Yerel gün doğumu ve gün batımı saatleri.
  - Hava durumu açıklaması ve buna karşılık gelen emoji simgeleri.
- **5 Günlük Tahmin**: Minimum ve maksimum sıcaklıkları gösteren birleştirilmiş günlük tahminler.
- **Arama Geçmişi**: Flask oturumlarını kullanarak en son aramalarınızı hatırlama.
- **Duyarlı UI**: Hava durumu verilerini sezgisel bir şekilde gösteren temiz, modern bir pano.

---

## 📁 Proje Yapısı
```text
weather_app/
├── weather_app.py           # Application entry point & Flask config
├── weather_helpers.py       # API logic and route handlers
├── .env                     # API Key storage (Secret)
└── weather_templates/       # HTML UI templates
    ├── base.html            # Shared layout
    └── index.html           # Search and results dashboard
```
---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Koşullar
Gerekli kütüphaneleri kurun:
```bash
pip install flask requests
```
### 2. API Key Yapılandırması
Bu uygulama **OpenWeatherMap**'ten bir API anahtarı gerektirir.
1. Ücretsiz bir hesap için [openweathermap.org/api](https://openweathermap.org/api)'den kaydolun.
2. API anahtarınızı oluşturun.
3. Proje kök dizininde bir `.env` dosyası oluşturun ve anahtarınızı ekleyin:
   ```text
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
### 3. Uygulama Mantığı (`weather_helpers.py`)

Temel mantık, API çekme ve rota yönetimine ayrılmıştır.

#### A. Hava Verisi Çekme
Aşağıdaki yardımcı fonksiyonları uygulayın:
- **`weather_icon(code)`**: OpenWeatherMap durum kodlarını (örneğin, Açık için 800, Gök gürültülü fırtına için 200) karşılık gelen emojilere eşleştirin.
- **`fetch_current(city)`**:
  - `requests` kütüphanesini kullanarak `/weather` endpoint'ine çağrı yapın.
  - Celsius için `units='metric'` olarak ayarlayın.
  - `404` (Şehir bulunamadı) veya `401` (Geçersiz API anahtarı) gibi hataları ele alın.
  - UTC gün doğumu/gün batımı zaman damgalarını, şehrin saat dilimi ofsetini kullanarak yerel zamana dönüştürün.
- **`fetch_forecast(city)`**:
  - `/forecast` endpoint'ine çağrı yapın (bu endpoint 3 saatlik aralıklar döndürür).
  - Dönüş yapılan 40 veri noktasını tarihe göre gruplayın.
  - Günlük minimum/maksimum sıcaklıkları toplayın ve o gün için en sık görülen hava durumunu belirleyin.

#### B. Rota Yönetimi
Ana sayfayı yönetmek için bir `setup_routes(app)` fonksiyonu tanımlayın:
- **Index (`GET /`)**:
  - İstek parametrelerinden `city`'yi çıkarın.
  - Bir şehir sağlanmışsa, mevcut hava durumunu ve 5 günlük tahmini çekin.
  - Son 5 benzersiz şehri depolamak için `flask.session` içinde bir `recent` arama listesi yönetin.
  - Tüm çekilen hava verileriyle birlikte `index.html` şablonunu oluşturun.

### 4. Uygulama Girişi (`weather_app.py`)
- Flask uygulamasını başlatın ve `template_folder="weather_templates"` olarak belirtin.
- Oturum yönetimi için bir `secret_key` ayarlayın.
- `weather_helpers.setup_routes(app)` çağrısı yapın.
- Sunucuyu 8117 portunda başlatın.

### 5. Frontend Uygulaması (`weather_templates/`)
- **`base.html`**: HTML yapısını tanımlayın, temiz bir görünüm için CSS dahil edin ve alt şablonlar için bir düzen bloğu sağlayın.
- **`index.html`**:
  - Şehir adını sorgu parametresi olarak gönderen bir arama formu oluşturun.
  - Veri yoksa "Bir şehir arayın" mesajını göstermek için Jinja2 koşullu ifadeleri kullanın.
  - Esnek düzenler kullanarak bir "Mevcut Hava Durumu" kartı ve bir "5 Günlük Tahmin" ızgarası tasarlayın.
  - "Son Aramalar" listesini tıklanabilir bağlantılar kümesi olarak gösterin.

---

## 🏃 Nasıl Çalıştırılır

1. `.env` dosyanızın doğru şekilde yapılandırıldığından emin olun.
2. Uygulamayı çalıştırın:
   ```bash
 la python weather_app.py
   ```
3. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **REST API Entegrasyonu**: Genel bir API'den JSON verisi tüketmek için `requests` kütüphanesini kullanma.
- **Veri Toplama (Data Aggregation)**: Ham 3 saatlik aralık verisini temiz bir 5 günlük günlük tahmine dönüştürme.
- **Oturum Yönetimi (Session Management)**: Kullanıcı verilerini (son aramalar) sayfa yenilemeleri boyunca kalıcı hale getirmek için `flask.session` kullanma.
- **Dinamik UI**: API yanıtlarına göre içeriği koşullu olarak oluşturmak için Jinja2 şablonları kullanma.
- **Ortam Yapılandırması (Environmental Configuration)**: Hassas API anahtarlarını kaynak koddan uzak tutmak için `.env` dosyaları kullanma.
- **Saat Dilimi Yönetimi (Timezone Handling)**: UTC zaman damgalarından yerel gün doğumu/gün batımı saatlerini hesaplama.
# 🕷️ Genel Amaçlı Web Kazıyıcı

**Python**, **Flask** ve **BeautifulSoup** ile oluşturulmuş güçlü ve esnek bir web kazıma uygulaması. Bu araç, kullanıcılara herhangi bir genel URL'den yapılandırılmış veri çıkarmalarına olanak tanır ve geniş bir yelpazede seçilebilir veri türü ve gelişmiş kazıma seçenekleri sunar.

## 🚀 Özellikler

- **Esnek Veri Çıkarımı**: Bir sayfadan ne çıkarılacağını seçin:
  - **Meta Etiketler**: Sayfa başlığı, açıklama, OpenGraph etiketleri ve charset.
  - **Başlıklar**: Tüm h1-h6 etiketleri ve etiketleriyle birlikte.
  - **Bağlantılar**: Mutlak URL'lere ve bağlantı metinlerine sahip tüm `<a>` etiketleri.
  - **Görseller**: Mutlak kaynak URL'lere ve alt metinlere sahip tüm `<img>` etiketleri.
  - **Sayfa Metni**: Temizlenmiş metinsel içerik (script, style ve nav öğelerini kaldırır).
  - **Tablolar**: Başlıklar ve satırlar dahil olmak üzere `<table>` öğelerinden yapılandırılmış veri.
- **Gelişmiş İstek Seçenekleri**:
  - **User-Agent Seçimi**: Basit bot tespitini atlatmak için Chrome, Firefox, Googlebot veya varsayılan ajanlar arasında geçiş yapın.
  - **Zaman Aşımı Kontrolü**: Yavaş yanıt veren sunucuları ele almak için özel zaman aşımları ayarlayın.
  - **Sınırlayıcılar**: Çıkarılacak maksimum bağlantı ve görsel sayısını tanımlayın.
- **Sonuç Yönetimi**:
  - **Anında Önizleme**: Tüm çıkarılan verileri hemen bir sonuç sayfasında görüntüleyin.
  - **Oturum Geçmişi**: Mevcut oturum sırasında geçmiş kazımaları takip edin.
  - **JSON Dışa Aktarma**: Herhangi bir kazıma sonucunu biçimlendirilmiş bir JSON dosyası olarak indirin.

---

## 📁 Proje Yapısı
```text
scraper_app/
├── scraper_app.py             # Application entry point & Flask configuration
├── scraper_helpers.py         # Scraping logic and route handlers
└── scraper_templates/          # HTML UI templates
    ├── base.html               # Shared layout and CSS
    ├── index.html              # Scraper input form
    ├── result.html             # Data display page
    └── history.html            # List of past scrapes
```
---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Koşullar
Gerekli kütüphaneleri kurun:
```bash
pip install flask requests beautifulsoup4
```
### 2. Scraping Mantığını Uygulama (`scraper_helpers.py`)

Uygulamanın çekirdeği, çıkarma motorudur (extraction engine).

#### A. Sayfa Getirme (Page Fetching)
`fetch_page(url, timeout, user_agent)` fonksiyonunu oluşturun:
- Sayfayı getirmek için `requests.get()` kullanın.
- Önceden tanımlanmış bir sözlükten (Chrome, Firefox vb.) bir `User-Agent` başlığı uygulayın.
- `allow_redirects=True` ve özel bir zaman aşımı (timeout) kullanın.
- HTTP hatalarını ele almak için `raise_for_status()` çağırın.

#### B. Veri Çıkarma Yardımcıları (Data Extraction Helpers)
HTML'i ayrıştırmak (parse) için **BeautifulSoup** (`bs4`) kullanın:
- **Meta**: `<meta>` etiketlerini arayın ve `name`/`property` ile `content` değerlerini çıkarın.
- **Başlıklar (Headings)**: `['h1', 'h2', 'h3', 'h4', 'h5', 'h6']` içindeki tüm etiketleri bulun ve metinlerini çıkarın.
- **Bağlantılar (Links)**: `href` içeren tüm `<a>` etiketlerini bulun. Göreceli URL'leri mutlak URL'lere dönüştürmek için `urllib.parse.urljoin` kullanın.
- **Görseller (Images)**: `src` içeren tüm `<img>` etiketlerini bulun. Mutlak URL'ler için `urljoin` kullanın ve `alt` metnini çıkarın.
- **Metin (Text)**: `<script>`, `<style>`, `<nav>` ve `<footer>` gibi gürültü (noise) etiketlerini `tag.decompose()` kullanarak kaldırın, ardından yeni satır ayırıcı ile `soup.get_text()` kullanın.
- **Tablolar (Tables)**: Tüm `<table>` etiketlerini bulun. Başlıklar için `<th>` etiketleri ve satır verileri için `<tr>` içindeki `<td>` etiketleri üzerinde yineleme yapın.

#### C. Ana Scraping Orkestratörü (The Main Scrape Orchestrator)
`scrape(url, options)` fonksiyonunu uygulayın:
- `fetch_page()` çağırın.
- Temel bilgilerle bir `result` sözlüğü başlatın: `id` (uuid), `url`, `status_code`, `elapsed` zamanı ve `scraped_at` zaman damgası.
- Kullanıcı tarafından sağlanan `options`'a (onay kutuları aracılığıyla) bağlı olarak, ilgili çıkarma yardımcılarını çağırın ve verileri `result` sözlüğüne ekleyin.

### 3. Flask Rotalarını Uygulama (`scraper_helpers.py`)

- **Index (`GET /`)**: Giriş formunu render edin.
- **Scrape (`POST /scrape`)**:
  - Formdan URL'yi ve seçenekleri (meta, başlıklar, bağlantılar vb.) toplayın.
  - Yaygın istisnaları (`Timeout`, `ConnectionError`, `HTTPError`) ele alın.
  - Sonucu global bir `history` sözlüğünde saklayın ve `result.html` sayfasını render edin.
- **Sonucu Görüntüleme (`GET /result/<id>`)**: ID'sine göre `history`'den bir sonuç alın ve onu render edin.
- **İndirme (`GET /download/<id>`)**: `result` sözlüğünü bir JSON dizesine dönüştürün ve ona indirilebilir bir `.json` dosya olarak sağlamak için `send_file()` kullanın.
- **Geçmiş (`GET /history`)**: `history` sözlüğündeki tüm girişleri, tarihe göre sıralayarak gösterin.
- **Geçmişi Temizleme (`POST /history/clear`)**: `history` sözlüğünü boşaltın.

### 4. Uygulama Girişi (`scraper_app.py`)
- Flask uygulamasını `template_folder="scraper_templates"` ile başlatın.
- Rotaları `setup_routes(app)` aracılığıyla kaydedin.
- Sunucuyu 8117 portunda çalıştırın.

### 5. Frontend Uygulaması (`scraper_templates/`)

- **`base.html`**: Duyarlı bir düzen sağlayın ve bir navigasyon çubuğu ekleyin.
- **`index.html`**:
  - Bir URL giriş alanı.
  - Veri türlerini seçmek için bir onay kutusu grubu (Meta, Başlıklar, Bağlantılar, Görseller, Metin, Tablolar).
  - Zaman aşımı, maksimum bağlantı ve Kullanıcı-Agent için bir açılır menü içeren giriş alanları.
- **`result.html`**:
  - Bir özet kartı gösterin (Başlık, Durum Kodu, Yanıt Süresi).
  - Yalnızca istenen çıkarılmış veri türlerini göstermek için koşullu renderlama (Jinja2 `{% if %}`) kullanın.
  - Tabloları HTML `<table>` etiketleri kullanarak ve bağlantıları/görselleri meta verileriyle birlikte listeleyerek biçimlendirin.
- **`history.html`**: Önceki scraping işlemlerinin basit bir listesi, tam sonucu görüntülemek veya JSON'u indirmek için bağlantılar içerir.

---

## 🏃 Nasıl Çalıştırılır

1. Uygulamayı çalıştırın:
   ```bash
   python scraper_app.py
   ```
2. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **HTTP İstekleri**: Web sunlarıyla etkileşim kurmak için `requests` kütüphanesini kullanma.
- **HTML Ayrıştırma (Parsing)**: DOM'dan veri gezmek ve çıkarmak için `BeautifulSoup` kullanma.
- **URL Normalizasyonu**: Göreceli yolları `urljoin` kullanarak mutlak URL'lere dönüştürme.
- **Veri Serileştirme**: Yapılandırılmış veriyi JSON'a dışa aktarma.
- **User-Agent Taklidi (Spoofing)**: Temel anti-scraping engellerinden kaçınmak için farklı tarayıcıları taklit etme.
- **Hata Yönetimi (Error Handling)**: Ağla ilgili arızalar için sağlam `try-except` blokları uygulama.
- **Durum Yönetimi (State Management)**: Oturum tabanlı bir sonuç geçmişini yönetmek için basit bir bellek içi (in-memory) sözlük kullanma.
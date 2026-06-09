# 🤖 Gemini Sohbet Web Uygulaması

**Python**, **Flask** ve **Google Gemini API** kullanılarak oluşturulmuş gelişmiş bir yapay zeka sohbet arayüzü. Bu uygulama, çok turlu konuşma desteği ve harici araç çağırma (web araması ve kripto para fiyatları) özelliklerine sahip, gerçek zamanlı akışlı (streaming) bir sohbet deneyimi sunar.

## 🚀 Özellikler

- **Yapay Zeka Destekli Sohbet**: Google AI Studio API aracılığıyla Google Gemini modelleriyle doğrudan entegrasyon.
- **Akışlı Yanıtlar (Streaming)**: Sunucu Taraflı Olaylar (SSE) kullanılarak token'lar gerçek zamanlı olarak iletilir ve akıcı bir "yazma" deneyimi sağlanır.
- **Araç Çağırma (Fonksiyon Çağırma)**:
  - **Web Araması**: Web'den güncel bilgiler getirmek için Tavily API entegrasyonu.
  - **Kripto Para Fiyatları**: CoinGecko API aracılığıyla gerçek zamanlı kripto para verisi alma.
- **Konuşma Yönetimi**: Yapay zekanın önceki konuşmaları hatırlamasını sağlayan çok turlu sohbet geçmişi yönetimi.
- **Gelişmiş Model Kontrolleri**: Model seçimi, sistem istemleri (system prompts), sıcaklık (temperature) ve maksimum token limitleri dahil olmak üzere kullanıcı tarafından yapılandırılabilir ayarlar.
- **Performans Analitiği**: Yanıt süresi ve saniye başına token sayısının gerçek zamanlı takibi.

---

## 📁 Proje Yapısı

```text
gemini_chat_app/
├── gemini_chat_app.py    # Uygulama giriş noktası ve Flask yapılandırması
├── gemini_helpers.py     # Gemini API mantığı, araç çağırma ve rotalar
├── .env                  # API anahtarları (GEMINI_API_KEY, TAVILY_API_KEY)
└── gemini_templates/      # Kullanıcı arayüzü şablonları
    ├── base.html          # Ortak düzen ve CSS
    └── index.html         # Sohbet arayüzü ve JS mantığı
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Gereksinimler ve API Anahtarları
Şu anahtarlara ihtiyacınız olacaktır:
- **Gemini API Anahtarı**: [Google AI Studio](https://aistudio.google.com) adresinden ücretsiz olarak edinin.
- **Tavily API Anahtarı**: Web arama yetenekleri için [Tavily](https://tavily.com) adresine kayıt olun.

Bağımlılıkları yükleyin:
```bash
pip install flask requests
```

### 2. Yapılandırma (`.env`)
Ana dizinde anahtarlarınızı güvenli bir şekilde saklamak için bir `.env` dosyası oluşturun:
```text
GEMINI_API_KEY=gemini_api_anahtarınız_buraya
TAVILY_API_KEY=tavily_api_anahtarınız_buraya
```

### 3. Uygulama Mantığı (`gemini_helpers.py`)

Temel mantık, Flask sunucusu ile Gemini API arasındaki etkileşimi yönetir.

#### A. Araç Tanımları ve Entegrasyon
- **Araç Şeması**: OpenAI uyumlu formatta bir `TOOLS` listesi tanımlayın. Her araç; bir `name` (isim), `description` (açıklama) ve beklenen girdileri tanımlayan bir `parameters` nesnesine sahip olmalıdır.
- **Web Araması (Tavily)**: Tavily API'sini çağıran ve biçimlendirilmiş arama snippet'leri ile URL'leri döndüren bir fonksiyon uygulayın.
- **Kripto Para Fiyatları (CoinGecko)**: CoinGecko API'si üzerinden gerçek zamanlı fiyatlar ve piyasa verileri sorgulayan bir fonksiyon uygulayın.

#### B. Gemini API Köprüsü
- **Mesaj Eşleme**: Standart sohbet rollerini (`user`, `assistant`, `system`), Gemini'nin yerel `contents` formatına dönüştüren bir yardımcı oluşturun.
- **Yük (Payload) Oluşturma**: Konuşma geçmişini, `systemInstruction` (sistem istemi için) ve `generationConfig` (sıcaklık, maksimum token) bilgilerini içeren bir istek gövdesi oluşturun.
- **SSE Akışı**: `:streamGenerateContent` uç noktasına erişmek için `requests.post(..., stream=True)` kullanın. Ham SSE akışını ayrıştıran ve JSON parçaları döndüren bir jeneratör uygulayın.

#### C. Araç Çağırma Döngüsü (Agentic Loop)
Araç yürütmeyi yönetmek için özyinelemeli (recursive) benzeri bir döngü uygulayın:
1. **İstek**: Mevcut geçmişi Gemini'ye gönderin.
2. **Gözlem**: Model metin yerine bir `functionCall` döndürürse:
   - Fonksiyon adını ve argümanlarını belirleyin.
   - Karşılık gelen yerel Python fonksiyonunu (Arama veya Kripto) çalıştırın.
   - Aracın çıktısını geçmişe bir `tool` rolü mesajı olarak ekleyin.
   - Modelin araç sonuçlarını yorumlayabilmesi için 1. Adıma geri dönün.
3. **Final Yanıt**: Model metin döndürdüğünde, bunu istemciye akış olarak iletin.

#### D. Flask Rotaları
- **`/`**: Sohbet arayüzünü oluşturur ve desteklenen modellerin listesini sunar.
- **`/chat`**: POST isteklerini yönetir. Sohbet ayarlarını ayıklar ve `stream_with_context` ile araç çağırma jeneratörünü sarmalayan, `mimetype='text/event-stream'` değerine sahip bir `Response` nesnesi döndürür.

### 4. Uygulama Girişi (`gemini_chat_app.py`)
- Bir Flask uygulaması başlatın ve bir `secret_key` belirleyin.
- `template_folder` ayarını `gemini_templates` olarak yapılandırın.
- Tüm rotaları `gemini_helpers.setup_routes(app)` aracılığıyla kaydedin.
- Uygulamayı 8118 portunda çalıştırın.

### 5. Ön Yüz Uygulaması (`gemini_templates/`)
- **`base.html`**: Modern koyu tema CSS düzeni ve duyarlı (responsive) bir navigasyon çubuğu dahil olmak üzere HTML iskeletini tanımlayın.
- **`index.html`**: 
  - **Yan Panel**: Sistem istemi, sıcaklık ve maksimum tokenlar için bir ayarlar paneli oluşturun.
  - **Sohbet Penceresi**: Markdown benzeri render destekleyen bir mesaj akışı uygulayın.
  - **JS Entegrasyonu**: SSE uç noktasını tüketmek için `fetch` API ve `ReadableStream` kullanın. Token bazlı bir render döngüsü ve saniye başına token hesaplamak için bir zamanlayıcı uygulayın.

---

## 🏃 Nasıl Çalıştırılır?

1. `.env` dosyasının API anahtarlarınızla yapılandırıldığından emin olun.
2. Uygulamayı çalıştırın:
   ```bash
   python gemini_chat_app.py
   ```
3. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8118**

---

## 📚 Gösterilen Temel Kavramlar

- **Üretken YZ Entegrasyonu**: REST API'ler üzerinden büyük dil modelleriyle (LLM) etkileşim kurmak.
- **Araç Çağırma (Ajanlar)**: Bir YZ'nin fonksiyon yürütme yoluyla gerçek dünya ile etkileşime girmesini sağlamak.
- **Sunucu Taraflı Olaylar (SSE)**: Sunucudan istemciye gerçek zamanlı veri akışı uygulamak.
- **Bağlam Yönetimi**: Çok turlu etkileşimlerde konuşma durumunu korumak.
- **Hibrit API Mimarisi**: Birden fazla API'yi (Gemini, Tavily, CoinGecko) tek bir tutarlı uygulama altında birleştirmek.
- **Modern Ön Yüz**: Asenkron veri işleme özellikli, duyarlı bir YZ sohbet arayüzü oluşturmak.

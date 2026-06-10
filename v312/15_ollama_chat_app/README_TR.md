# 🦙 Ollama Sohbet Web Uygulaması

**Python**, **Flask** ve **Ollama** kullanılarak geliştirilmiş yüksek performanslı, yerel bir yapay zeka sohbet arayüzü. Bu uygulama; gerçek zamanlı akışlı yanıtlar, çok turlu konuşmalar ve harici araç çağırma yetenekleri ile yerel Büyük Dil Modelleriyle (LLM) etkileşim kurmak için modern, web tabanlı bir ön yüz sağlar.

## 🚀 Özellikler

- **Yerel Model Entegrasyonu**: Yerel Ollama örneğinize sorunsuz bir şekilde bağlanır.
- **Otomatik Model Keşfi**: Yerel Ollama sunucunuzda yüklü olan tüm modelleri dinamik olarak listeler.
- **Akışlı Yanıtlar (Streaming)**: Token'lar, "düşünme" (thinking) token'ları da dahil olmak üzere Sunucu Taraflı Olaylar (SSE) aracılığıyla gerçek zamanlı olarak iletilir.
- **Araç Çağırma (Ajanlar)**:
  - **Web Araması**: Web'den güncel bilgiler çekmek için Tavily API entegrasyonu.
  - **Kripto Para Fiyatları**: CoinGecko API aracılığıyla gerçek zamanlı kripto para verisi alma.
- **Konuşma Yönetimi**: Bağlam odaklı etkileşimler için tam geçmiş desteği.
- **Model Kontrolleri**: Sistem istemleri, sıcaklık (temperature) ve maksimum token limitleri için yapılandırmalar.
- **Oturum Analitiği**: Yanıt sürelerinin ve saniye başına token sayısının takibi.

---

## 📁 Proje Yapısı

```text
ollama_chat_app/
├── ollama_chat_app.py    # Uygulama giriş noktası ve Flask yapılandırması
├── ollama_helpers.py     # Ollama API mantığı, araç çağırma ve rotalar
├── .env                  # API anahtarları (TAVILY_API_KEY)
└── ollama_templates/      # Kullanıcı arayüzü şablonları
    ├── base.html          # Ortak düzen ve CSS
    └── index.html         # Sohbet arayüzü ve JS mantığı
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Gereksinimler

#### Ollama Kurulumu
1. Ollama'yı [ollama.com](https://ollama.com) adresinden indirin ve kurun.
2. Ollama sunucusunu başlatın: `ollama serve`.
3. Kullanmak istediğiniz bir modeli indirin (örneğin: `ollama pull llama3.2`).

#### Bağımlılıkların Kurulumu
```bash
pip install flask requests
```

### 2. Yapılandırma (`.env`)
Harici araçlar için API anahtarlarınızı saklamak üzere ana dizinde bir `.env` dosyası oluşturun:
```text
TAVILY_API_KEY=tavily_api_anahtarınız_buraya
```

### 3. Uygulama Mantığı (`ollama_helpers.py`)

Temel mantık, Flask sunucusu ile yerel Ollama API'si arasındaki etkileşimi yönetir.

#### A. Araç Tanımları ve Uygulama
- **Araç Şeması**: `web_search` ve `get_crypto_price` için fonksiyon deklarasyonlarını (isim, açıklama, parametreler) içeren bir `TOOLS` listesi tanımlayın.
- **Web Araması**: Tavily API'sine sorgu atan ve biçimlendirilmiş arama sonuçları döndüren bir fonksiyon uygulayın.
- **Kripto Para Fiyatları**: CoinGecko API'sinden gerçek zamanlı veriler çeken bir fonksiyon uygulayın.

#### B. Ollama API Etkileşimi
- **Model Keşfi**: Yüklü modellerin listesini almak için `requests.get("http://localhost:11434/api/tags")` kullanın.
- **Akışlı Jeneratör**: `/api/chat` uç noktasına `stream=True` ile istekler gönderen bir `chat_with_tools` jeneratörü oluşturun.
- **SSE Formatlama**: JSON verilerini Sunucu Taraflı Olaylar için `data: ...\n\n` formatında sarmalayan bir yardımcı fonksiyon uygulayın.

#### C. Ajan Döngüsü (Araç Çağırma)
Model güdümlü araç kullanımını yönetmek için bir döngü uygulayın:
1. **Token Akışı**: Ollama'dan gelen token'ları kullanıcıya iletin.
2. **Araç Çağrısını Tespit Etme**: Eğer `done` parçası `tool_calls` içeriyorsa, akışı durdurun ve fonksiyon adını ile argümanları ayıklayın.
3. **Yerel Araçları Çalıştırma**: İlgili Python fonksiyonunu (`web_search` veya `get_crypto_price`) çalıştırın.
4. **Sonuçları Geri Besleme**: Araç sonucunu mesaj geçmişine ekleyin ve final yanıtı almak için API'yi tekrar çağırın.
5. **Tekrar**: Her tur için en fazla 5 tur araç çağırma desteği sağlayın.

#### D. Flask Rotaları
- **`/`**: Sohbet arayüzünü oluşturur ve keşfedilen modellerin listesini sunar.
- **`/chat`**: POST isteklerini yönetir, konuşma geçmişini ve ayarları ayıklar ve `mimetype='text/event-stream'` değerine sahip bir `Response` nesnesi döndürür.

### 4. Uygulama Girişi (`ollama_chat_app.py`)
- Flask uygulamasını `template_folder="ollama_templates"` ile başlatın.
- `ollama_helpers.setup_routes(app)` çağrısı ile rotaları kaydedin.
- Uygulamayı 8117 portunda çalıştırın.

### 5. Ön Yüz Uygulaması (`ollama_templates/`)
- **`base.html`**: Modern CSS kullanan, temiz ve koyu temalı bir düzen.
- **`index.html`**: 
  - **Yan Panel**: Model seçici, sistem istemleri ve sıcaklık ayarları için kontrol paneli.
  - **Sohbet Penceresi**: SSE akışından gelen token'ları dinamik olarak ekleyen bir mesaj alanı.
  - **JS Mantığı**: `/chat` uç noktasından gelen parçaları işlemek ve kullanıcı arayüzünü gerçek zamanlı güncellemek için `fetch` API ve `ReadableStream` kullanın.

---

## 🏃 Nasıl Çalıştırılır?

1. Ollama'nın çalıştığından emin olun: `ollama serve`.
2. `.env` dosyanızı Tavily API anahtarı ile yapılandırın.
3. Uygulamayı çalıştırın:
   ```bash
   python ollama_chat_app.py
   ```
4. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **Yerel LLM Dağıtımı**: Yerel olarak barındırılan bir YZ modeliyle etkileşim kurmak.
- **Ajan Davranışı**: YZ'nin harici araçları kullanmasını sağlamak için fonksiyon çağırma (function calling) uygulamak.
- **Asenkron Akış**: YZ yanıtlarındaki gecikmeyi ortadan kaldırmak için SSE kullanmak.
- **Durum Yönetimi**: Yerel modeller için çok turlu konuşma geçmişini korumak.
- **Ön Yüz/Arka Yüz Entegrasyonu**: JavaScript tabanlı bir kullanıcı arayüzünü, Python tabanlı bir YZ orkestratörüne bağlamak.
- **Performans Takibi**: Yanıt sürelerini ve token verimliliğini ölçmek.

# 🌐 Python ile HTTP Temelleri

Python'un `requests` kütüphanesini kullanarak temel HTTP işlemlerini gösteren kapsamlı bir örnekler koleksiyonu. Bu proje; JSON veri çekme, API'lere veri gönderme, oturum yönetimi, kimlik doğrulama, dosya indirme ve yeniden deneme mantığı gibi temel konuları kapsar.

## 🚀 Özellikler

### 1. GET İstekleri (JSON API)
- Bir REST API'den kaynak listesi çekme
- Sorgu parametrelerini (query parameters) kullanarak sonuçları filtreleme
- ID ile tek bir kaynağı çekme
- Başarısız istekler için hata yönetimi

### 2. POST/PUT İstekleri
- POST ile yeni kaynaklar oluşturma
- PUT ile mevcut kaynakları güncelleme
- JSON veri gövdesi (payload) gönderme
- Yanıt durum kodlarını (201 Created, 200 OK) işleme

### 3. Oturum (Session) Yönetimi
- Çoklu istekler için TCP bağlantılarını yeniden kullanma
- Oturum düzeyinde başlıklar (headers) belirleme (tüm isteklere uygulanır)
- İstekler arasında otomatik çerez (cookie) kalıcılığı

### 4. Kimlik Doğrulama Yöntemleri
- Bearer Token kimlik doğrulaması (OAuth2, JWT)
- API Anahtarı kimlik doğrulaması (X-Api-Key gibi özel başlıklar)
- Temel Kimlik Doğrulama (Base64 kodlanmış kullanıcıadı:şifre)

### 5. Dosya İndirme
- Basit indirme (tüm dosyayı belleğe yükler)
- Akışlı (Streaming) indirme (büyük dosyalar için sabit bellek kullanımı)
- İlerleme göstergeli indirme

### 6. Zaman Aşımı ve Yeniden Deneme Mantığı
- Bağlantı ve okuma zaman aşımı (timeout) belirleme
- Sabit gecikmeli manuel yeniden deneme
- Üssel geri çekilme (Exponential backoff - her başarısızlıktan sonra bekleme süresini ikiye katlama)

---

## 📁 Proje Yapısı

```text
11_http_basics/
├── http_get_json_api.py       # GET istekleri ve JSON ayrıştırma
├── http_post_json.py          # POST ve PUT istekleri
├── http_session.py            # Oturum yönetimi
├── http_auth_headers.py       # Kimlik doğrulama kalıpları
├── http_download_streaming.py # Dosya indirme teknikleri
└── http_timeout_retry.py     # Zaman aşımı ve yeniden deneme stratejileri
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### Gereksinimler
Gerekli kütüphaneyi yükleyin:
```bash
pip install requests
```

---

### 1. HTTP GET İstekleri — `http_get_json_api.py`

**Hedef**: Genel bir REST API'den (JSONPlaceholder) veri çekmek ve bunu görüntülemek.

**Uygulama Adımları**:

1. **Modülleri içe aktarma**: `requests` ve `json` modüllerini import edin.
2. **Veri çekme fonksiyonunu tanımlama**:
   - API URL'sini oluşturun (örneğin: `https://jsonplaceholder.typicode.com/posts`).
   - `userId` değerine göre filtrelemek için bir sorgu parametreleri sözlüğü oluşturun.
   - `requests.get(url, params=params, timeout=10)` çağrısını yapın.
3. **Yanıtı işleme**:
   - `response.status_code == 200` olup olmadığını kontrol edin.
   - `response.json()` ile JSON verisini ayrıştırın.
   - Sonuçlar üzerinde döngü kurarak seçili alanları (id, başlık, gövde önizlemesi) yazdırın.
4. **Hata yönetimi**: Try/except blokları kullanarak bağlantı hatalarını yakalayın ve mesajlar yazdırın.
5. **Tekil kaynak çekme**:
   - ID'si eklenmiş bir URL oluşturun (örneğin: `/posts/7`).
   - Kaynak bulunamadığında 404 durumunu yönetin.
6. **Ana fonksiyon**: Her iki örneği de çağırarak gösterimi tamamlayın.

---

### 2. HTTP POST/PUT İstekleri — `http_post_json.py`

**Hedef**: Kaynak oluşturmak veya güncellemek için bir REST API'ye veri göndermek.

**Uygulama Adımları**:

1. **Post fonksiyonu oluşturma**:
   - API URL'sini belirleyin (POST uç noktası).
   - `userId`, `title`, `body` içeren bir veri gövdesi (payload) oluşturun.
   - Özel başlıklar belirleyin (`Content-Type`, `Accept`).
   - `requests.post(url, json=payload, headers=headers)` metodunu kullanın.
2. **Durumu kontrol etme**: Başarı durumunda 201 Created kodu beklenir.
3. **Yanıtı ayrıştırma**: API, atanan ID ile birlikte oluşturulan nesneyi geri döndürür.
4. **Güncelleme fonksiyonu** (PUT):
   - Tam kaynak URL'si ile `requests.put()` kullanın.
   - Tüm alanları veri gövdesine ekleyin (PUT tüm kaydı değiştirir).
5. **Ana fonksiyon**: `create_post()` ve `update_post()` fonksiyonlarını çağırın.

---

### 3. Oturum Yönetimi — `http_session.py`

**Hedef**: Bağlantıları yeniden kullanmak, başlıkları paylaşmak ve çerezleri otomatik olarak yönetmek.

**Uygulama Adımları**:

1. **Temel oturum**:
   - `session = requests.Session()` oluşturun.
   - `requests.get(url)` yerine `session.get(url)` kullanın.
   - Kaynakları serbest bırakmak için işiniz bittiğinde `session.close()` çağrısını yapın.
2. **Oturum başlıkları**:
   - Bir kez `session.headers["Authorization"] = "Bearer ..."` belirleyin.
   - Bu başlık, oturum üzerinden yapılan her isteğe otomatik olarak eklenir.
3. **Çerez yönetimi**:
   - Bir çerez ayarlamak için istek yapın (örneğin: `/cookies/set/session_id/...`).
   - İkinci bir istek yapın; oturum kayıtlı çerezi otomatik olarak gönderir.
   - Çerezin geri döndüğünü doğrulamak için httpbin.org kullanın.
4. **Ana fonksiyon**: Farklı oturum kalıplarını göstermek için tüm fonksiyonları çağırın.

---

### 4. Kimlik Doğrulama — `http_auth_headers.py`

**Hedef**: Çeşitli kimlik doğrulama yöntemlerini kullanarak korumalı API'lere erişmek.

**Uygulama Adımları**:

1. **Bearer Token**:
   - Başlık sözlüğünü oluşturun: `{"Authorization": "Bearer " + token}`.
   - Korumalı uç noktaya GET isteği gönderin.
   - Token geçersizse 401 Unauthorized hatasını yönetin.
2. **API Anahtarı (API Key)**:
   - Özel bir başlık adı kullanın (genellikle `X-Api-Key`).
   - İsteği gönderin ve httpbin.org'dan dönen başlıkları doğrulayın.
3. **Temel Kimlik Doğrulama (Basic Auth)**:
   - `requests.get(url, auth=(username, password))` kullanın.
   - `auth` parametresi kimlik bilgilerini otomatik olarak Base64 ile kodlar.
   - httpbin.org'un `/basic-auth/{user}/{pass}` uç noktasıyla test edin.
4. **En İyi Uygulama Notu**: Kimlik bilgilerini kodun içine gömmek yerine ortam değişkenleri (environment variables) kullanımını vurgulayın.

---

### 5. Dosya İndirme — `http_download_streaming.py`

**Hedef**: Dosyaları verimli bir şekilde indirmek, büyük dosyaları bellek sorunu yaşamadan yönetmek.

**Uygulama Adımları**:

1. **Basit indirme**:
   - `requests.get(url)` kullanın.
   - `response.content` içeriğini doğrudan ikili modda (`"wb"`) bir dosyaya yazın.
   - Sadece küçük dosyalar için uygundur.
2. **Akışlı (Streaming) indirme**:
   - İsteğe `stream=True` parametresini ekleyin.
   - Verileri parçalar halinde okumak için `response.iter_content(chunk_size=8192)` kullanın.
   - Her parçayı anında diske yazın; bellek kullanımı sabit kalır.
3. **İlerleme takibi**:
   - Toplam boyut için yanıttaki `Content-Length` başlığını okuyun.
   - İndirilen yüzdesi hesaplayın.
   - Her %10'da bir veya boyut bilinmiyorsa her 50KB'da bir ilerlemeyi yazdırın.
4. **Ana fonksiyon**: httpbin.org/bytes üzerinden test dosyalarını indirmek için fonksiyonları çağırın.

---

### 6. Zaman Aşımı ve Yeniden Deneme — `http_timeout_retry.py`

**Hedef**: Yavaş sunucuları ve geçici hataları yönetebilen dayanıklı HTTP istemcileri oluşturmak.

**Uygulama Adımları**:

1. **Zaman aşımı yönetimi**:
   - `requests.get()` fonksiyonuna `timeout=(connect_timeout, read_timeout)` parametresini geçirin.
   - Bağlantı zaman aşımı: Bağlantının kurulması için maksimum süre.
   - Okuma zaman aşımı: Verinin gelmesi için beklenen maksimum süre.
   - Zaman aşımı istisnalarını (exceptions) yakalayın ve uygun şekilde yönetin.
2. **Manuel yeniden deneme döngüsü**:
   - Bir yeniden deneme sayacı ile `while` döngüsü kullanın.
   - Hata durumunda, bir sonraki denemeden önce `time.sleep(delay)` ile bekleyin.
   - Başarıda çıkış yapın, hatada devam edin.
3. **Üssel geri çekilme (Exponential backoff)**:
   - Küçük bir gecikmeyle başlayın (örneğin: 1 saniye).
   - Her başarısızlıktan sonra gecikmeyi 2 ile çarpın (1s, 2s, 4s, 8s...).
   - Bu, zorlanan bir sunucuya aşırı yük binmesini önler.
4. **Ana fonksiyon**: Zaman aşımını tetiklemek için httpbin.org/delay ve yeniden denemeleri tetiklemek için /status/503 uç noktalarını test edin.

---

## 🏃 Betikleri Nasıl Çalıştırırsınız?

1. Proje dizinine gidin.
2. Herhangi bir betiği tek başına çalıştırın:
   ```bash
   python http_get_json_api.py
   python http_post_json.py
   python http_session.py
   python http_auth_headers.py
   python http_download_streaming.py
   python http_timeout_retry.py
   ```

---

## 📚 Gösterilen Temel Kavramlar

- **REST API'ler**: URL'ler, uç noktalar, metotlar (GET, POST, PUT) ve durum kodlarını anlamak.
- **JSON İşleme**: JSON yanıtlarını ayrıştırmak ve iç içe geçmiş verileri yönetmek.
- **Bağlantı Yeniden Kullanımı**: Performansı artırmak için Oturumların (Sessions) kullanımı.
- **Güvenlik**: Bearer, API Anahtarı ve Temel kimlik doğrulama uygulamaları.
- **Bellek Verimliliği**: Büyük dosyaların akışlı (streaming) indirilmesi.
- **Dayanıklılık (Resilience)**: Üretim kalitesinde kod için zaman aşımı ve yeniden deneme stratejileri.
- **API Testleri**: Güvenli ve ücretsiz testler için httpbin.org ve JSONPlaceholder kullanımı.

---

## ⚠️ Önemli Notlar

- **Test Servisleri**: Bu proje ücretsiz genel test servislerini (httpbin.org, jsonplaceholder.typicode.com) kullanır. Bu servislerde gerçek kimlik bilgilerini kullanmayın; bunlar sadece test amaçlıdır.
- **Ortam Değişkenleri**: Üretim kodunda API anahtarlarını veya tokenları asla kodun içine yazmayın. Bunun yerine `os.environ.get("API_KEY")` kullanın.
- **Hata Yönetimi**: Zaman aşımı, bağlantı hataları ve geçersiz yanıtları nazikçe yönetmek için ağ çağrılarını her zaman try/except bloklarına alın.

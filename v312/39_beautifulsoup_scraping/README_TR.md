# Proje 39: requests ve BeautifulSoup ile Web Scraping

Bir web sayfasını `requests` ile indirip `BeautifulSoup` ile ayrıştıran kısa bir veri kazıma (scraping) betiği. Sayfada blog yazısı bloklarını (`<article class="blog-post">`) arar ve her birinin başlığını, yazarını ve bağlantısını yazdırır. Sayfada böyle bir blok yoksa yedek yol olarak sayfanın `<title>` etiketini yazdırır.

## Nasıl Çalışır?
- `requests.get()` sayfayı tarayıcıya benzeyen bir `User-Agent` başlığıyla ve 10 saniyelik zaman aşımıyla indirir.
- Durum kodu `200` değilse betik kodu yazdırır ve durur. Ağ hataları (DNS hatası, zaman aşımı, reddedilen bağlantı) `requests.exceptions.RequestException` olarak yakalanır.
- `BeautifulSoup(response.text, "html.parser")` ayrıştırma ağacını Python'ın yerleşik HTML ayrıştırıcısıyla kurar; `lxml` gibi ek bir ayrıştırıcı gerekmez.
- `find_all("article", class_="blog-post")` yazı bloklarını toplar. Betik her bloğun içinden şunları okur:
  - `<h2 class="post-title">` metni (yoksa `No Title`),
  - ilk `<a>` etiketinin `href` değeri (yoksa `No Link`),
  - `<span class="post-author">` metni (yoksa `Anonymous`).
- Hiç yazı bloğu bulunamazsa onun yerine sayfa başlığını yazdırır.

Varsayılan hedef `https://example.com` adresidir ve bu sayfada `<article>` öğesi yoktur. Bu yüzden normal bir çalıştırma her zaman yedek yola düşer ve yalnızca sayfa başlığını yazdırır. Yazı çıkarma döngüsünü çalışırken görmek için `main.py` içindeki `target_sandbox_url` değişkenini bu yapıyı kullanan bir sayfaya yönlendirin. Kodda yorum satırı olarak duran `https://gurmezin.com` da bu yapıyı kullanmaz ve o da yedek yola düşer.

## Proje Yapısı
```text
39_beautifulsoup_scraping/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Güncel `requests` sürümü için Python 3.10 veya üstü (betiğin kendisi f-string'den yeni bir özellik kullanmaz). Python 3.12.3 ile test edildi.
- `requests` (2.34.2 ile test edildi) ve `beautifulsoup4` (4.15.0 ile test edildi).
- İnternet erişimi.

## Çalıştırma
Ubuntu 24.04'te sanal ortam dışında `pip install` komutu `externally-managed-environment` hatasıyla başarısız olur. Bu yüzden önce bir sanal ortam oluşturun:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
python3 main.py
```
Ubuntu'nun kendi `python3-requests` ve `python3-bs4` paketleri de (`sudo apt install python3-requests python3-bs4`) işe yarar; betik bu sürümlerle de (2.31.0 ve 4.12.3) test edildi.

## Örnek Çıktı (Python 3.12.3)
```text
--- Initiating Web Scraping Connection ---
Target URL: https://example.com

=== Extracted Article Elements ===
[Warning] No elements matched the target class layout.
Displaying raw page title instead as fallback:
Page Title Tag -> Example Domain
```

Sayfada eşleşen bloklar varsa her yazı şöyle yazdırılır:
```text
[Post #1]
 Title  : Hello
 Author : Ahmet
 Link   : /a
```
Bu ikinci çıktı, fonksiyona canlı bir site yerine küçük bir deneme HTML sayfası verilerek üretildi.

Hata durumları:
```text
[Error] Failed to connect. HTTP Status Code: 404
[Critical Network Error] Connection timed out or failed: HTTPSConnectionPool(host='nonexistent.invalid', port=443): ...
```
404 mesajının, bağlantı kurulduğu ve sunucu yanıt verdiği hâlde "Failed to connect" dediğine dikkat edin. Her iki hata durumunda da betik `0` çıkış koduyla sonlanır, yani bir kabuk betiği ya da zamanlanmış görev hatayı fark etmez.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/24/beautifulsoup-ile-web-scraping-html-corbasindan-anlamli-veri-cikarmak/
- Beautiful Soup belgeleri: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Requests belgeleri: https://requests.readthedocs.io/

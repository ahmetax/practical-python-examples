# Proje 27: Metin Normalizasyonu ve Türkçe I Sorunu

Saf Python ile yazılmış küçük bir metin temizleme örneği. Metni Türkçe kurallarına göre küçük harfe çevirir, noktalama işaretlerini ve rakamları `re.sub()` ile siler, art arda gelen boşlukları tek boşluğa indirir.

## Nasıl Çalışır?
- **`turkish_lower(text)`**: Python'un `str.lower()` metodu Türkçe kurallarını değil, Unicode'un varsayılan kurallarını uygular. `I` harfini `i` yapar (Türkçede `ı` olmalı), `İ` harfini ise `i` artı birleşik nokta (U+0307) yapar; bu yüzden `"İSTANBUL".lower()` 8 değil 9 karakter uzunluğundadır. Fonksiyon önce `İ` harfini `i`, `I` harfini `ı` ile değiştirir, kalan harfler için `.lower()` çağırır.
- **`turkish_upper(text)`**: Ters yön. `.upper()` çağırmadan önce `i` harfini `İ` ile değiştirir. (İçindeki `ı` → `I` değişimi zararsız ama gereksizdir: `"ı".upper()` zaten `I` döndürür.) Demo bu fonksiyonu çağırmaz.
- **`normalize_text(raw_text, remove_digits=False)`**:
  1. metni `turkish_lower()` ile küçük harfe çevirir,
  2. kelime karakteri ya da boşluk olmayan her karakteri siler (`[^\w\s]`); `remove_digits=True` verilirse rakamları da (`\d`) siler,
  3. art arda gelen boşluk, sekme ve satır sonlarını tek boşluğa indirir, baştaki ve sondaki boşlukları atar.

Dikkat edilmesi gerekenler:
- `\w` alt çizgiyi de kapsar; bu yüzden `Ahmet_Dev123` metni `ahmetdev` değil `ahmet_dev` olur.
- `turkish_lower()` her girdiye Türkçe kurallarını uygular. Büyük `I` içeren İngilizce metin de değişir: `"ISSUE"` metni `"ıssue"` olur.
- Python 3'te `str` desenleri için `re.UNICODE` zaten varsayılandır; koddaki bu bayrak hiçbir şeyi değiştirmez.

## Proje Yapısı
```text
27_text_normalization/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3. Kod yalnızca standart kütüphanedeki `re` modülünü ve f-string'leri kullanır; 3.12'ye özgü bir özellik yoktur. Python 3.12.3 (Ubuntu 24.04) ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
=== Testing Standard vs Custom Lowercasing ===
Original       : İSTANBUL IŞIKLARI
Naive .lower() : i̇stanbul işiklari  <- (Broken: notice the 'i' and 'ı' collision)
Custom Lower   : istanbul ışıkları  <- (Correctly preserved linguistic shapes)
------------------------------------------------------------

=== Running Comprehensive Pipeline ===
Raw Input : İSTANBUL, ISPARTA ve İZMİR şehirleri incelendi.
Normalized: istanbul ısparta ve izmir şehirleri incelendi
------------------------------------------------------------
Raw Input : Kullanıcı Adı: 'Ahmet_Dev123' - Giriş Tarihi: 2026!
Normalized: kullanıcı adı ahmet_dev giriş tarihi
------------------------------------------------------------
Raw Input : ılık su ile İYİCE yıkanmış,   temiz bir   yüzey.
Normalized: ılık su ile iyice yıkanmış temiz bir yüzey
------------------------------------------------------------
Raw Input : Mojo & Python dillerinin kararlılığı %100 test edildi.
Normalized: mojo python dillerinin kararlılığı test edildi
------------------------------------------------------------
```
`Naive .lower()` satırındaki ilk `i` harfinin üzerinde fazladan bir birleşik nokta (U+0307) vardır; terminal yazı tipinize göre düz bir `i` gibi görünebilir.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/20/python-ile-metin-normalizasyonu-turkce-karakter-tuzaklarindan-kurtulun/
- `re` belgeleri: https://docs.python.org/3/library/re.html
- `str.lower()` belgeleri: https://docs.python.org/3/library/stdtypes.html#str.lower

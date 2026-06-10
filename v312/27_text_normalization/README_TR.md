# Proje 27: Metin Normalizasyonu ve Dilsel Temizleme

Temiz bir metin ön işleme hattı tasarlamayı ve oluşturmayı gösteren özel bir yardımcı program projesi. Bu çerçeve, Doğal Dil İşleme (NLP) alanındaki kritik dilsel tuzakları ele alır; örneğin, yerel ayara özgü büyük/küçük harf dönüşümleri (örneğin, Türkçe `I/ı` ve `i/İ` matrisi) ve düzenli ifade güdümlü temizleme (sanitization).

## Mimari Amaç
Sistem, veri hattı (data pipeline) alım motorları, arama dizinleri veya NLP tokenizer'ları tipik bir metin normalizasyon katmanı görevi görür. Dağınık, kullanıcı tarafından gönderilmiş veya taranmış dizeleri kabul eder ve yerel ayar büyük/küçük harf kurallarını yöneterek, noktalama işaretlerini kaldırarak ve düzensiz boşlukları sıkıştırarak bunları standart formatlara dönüştürür.

## Proje Yapısı
```text
27_text_normalization/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-based distribution)

Runtime: Python 3.12+

Dependencies: None (Leverages standard library re module)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated folder for your project within your workspace repository:

```bash
mkdir 27_text_normalization
cd 27_text_normalization

### Adım 2: Temizleme Motorunu Uygulama
`main.py` adında bir dosya oluşturun. Sisteminizi katman katman inşa edin:

Yerel Ayara Duyarlı Küçük Harfe Dönüştürme (Locale-Safe Lowercasing) Uygulayın: Özel bir fonksiyon uygulayın (örneğin, `turkish_lower(text)`). Standart string dönüşümlerini tetiklemeden önce, karakter anormalliklerini açıkça `.replace()` yoluyla yakalayın. Büyük noktalı İ'yi küçük noktalı i'ye ve büyük noktası olmayan I'yı küçük noktası olmayan ı'ya dönüştürün. Python'ın yerel `.lower()` fonksiyonunu çağırmadan önce karakter çakışmalarını çözmek için bu deseni izleyin.

Yerel Ayara Duyarlı Büyük Harfe Dönüştürme (Locale-Safe Uppercasing) Uygulayın: Eşleştirilmiş bir fonksiyon uygulayın (örneğin, `turkish_upper(text)`). Son yerel `.upper()` geri dönüşünü çalıştırmadan önce, küçük noktası olmayan ı'yı büyük noktası olmayan I'ya ve küçük noktalı i'yi büyük noktalı İ'ye eşleyin.

İşleme Pipeline'ını Taslağını Çıkarma: Ana bir fonksiyon olan `normalize_text(raw_text, remove_digits)` oluşturun.

Özel küçük harfe dönüştürme fonksiyonunuzu ilk olarak uygulayın.

Noktalama işaretlerini düşürmek için düzenli ifadeleri (`re.sub()`) `re.UNICODE` bayrağı ile birleştirin. Noktalama işaretlerini düşürürken alfanümerik harfleri korumak için karakter kümeleri (örneğin, `[^\w\s]`) kullanarak esnek bir desen tasarlayın.

İstenildiğinde rakamları (`\d`) temiz bir şekilde hedefleyip ortadan kaldırmak için bir bayrak ekleyin.

Sondaki boşlukları kaldırın ve yapısal boşluk hatalarını (birden fazla boşluk, gizli tablar) tek bir boşluğa sıkıştırmak için `re.sub(r"\s+", " ", cleaned)` kullanın.

### Adım 3: Çalıştırma ve Doğrulama
`main.py` dosyasının en altına, karışık Türkçe karakterler, yoğun noktalama yapıları ve rakamlar içeren bir ham string örnekleri listesi kullanarak bir test çalıştırma dizisi ekleyin. Betiği yerel olarak çalıştırarak standart ve yerel ayara duyarlı normalleştirme arasındaki farkı gözlemleyin:
```bash
python main.py



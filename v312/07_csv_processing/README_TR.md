# 📊 CSV İşleme Projesi

Python kullanarak CSV verilerini okuma, filtreleme ve analiz etmenin pratik bir gösterimi. Bu proje iki farklı yaklaşımı sergilemektedir: Biri Python'un **standart kütüphanesini** (`csv` modülü) kullanan, diğeri ise daha gelişmiş veri manipülasyonu için popüler **Pandas** kütüphanesini kullanan yaklaşım.

## 🚀 Özellikler

- **Örnek Veri Üretimi**: Otomatik olarak bir test veri kümesi oluşturur (sütunları: product, category, quantity, unit_price, total olan satış verileri).
- **Standart Kütüphane Yaklaşımı**: Harici bağımlılıklar olmadan veri okumak, filtrelemek ve yazmak için Python'un yerleşik `csv` modülünü kullanır.
- **Pandas Yaklaşımı**: Grup tabanlı istatistiksel analizler için DataFrame'lerin gücünü gösterir.
- **Temel İşlemler**: Sütun değerlerine göre satırları filtreleme, sütun istatistiklerini (min, max, toplam, ortalama) hesaplama ve çıktıları yeni CSV dosyalarına yazma.

---

## 📁 Proje Yapısı

```text
07_csv_processing/
└── csv_processing.py    # Tüm mantığı içeren ana script
```

---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Gereksinimler
Python 3.12+ sürümünün yüklü olduğundan emin olun. Bu proje aşağıdaki kütüphaneyi gerektirir:
```bash
pip install pandas
```

### 2. Örnek Verilerin Oluşturulması
Test verileri içeren bir CSV dosyası üreten bir yardımcı fonksiyon oluşturarak başlayın.
- Dosya yolunu girdi olarak alan `create_sample_csv(path)` fonksiyonunu tanımlayın.
- Python'un yerleşik `open()` fonksiyonunu yazma modunda (`"w"`) kullanın.
- Sütun isimlerini içeren bir başlık satırı yazın: `product,category,quantity,unit_price,total`.
- Farklı ürün kategorilerini (Electronics, Furniture, Stationery) temsil eden birden fazla örnek satış verisi satırı ekleyin.
- Dosyayı kapatın ve oluşturulduğunu doğrulayın.

### 3. Yaklaşım 1: Python'un `csv` Modülünü Kullanma
Bu yaklaşım yalnızca standart kütüphaneyi kullanır, bu da onu hafif ve bağımlılıksız kılar.

#### CSV Okuma
- Dosyayı okuma modunda açan bir `read_csv_rows(path)` fonksiyonu oluşturun.
- Dosyayı ayrıştırmak için `csv.DictReader(f)` kullanın. Bu, anahtarların sütun başlıkları olduğu sözlüklerden oluşan bir yineleyici (iterable) döndürür.
- Okuyucuyu bir listeye dönüştürün ve dosyayı kapatın.
- Sözlüklerin listesini döndürün.

#### Verileri Görüntüleme
- Listeyi yineleyen ve her satırı biçimlendirilmiş tablo benzeri bir çıktıda yazdıran bir `print_rows(rows)` fonksiyonu oluşturun.
- Değerlere sözlük anahtarlarını kullanarak erişin (örneğin, `row["product"]`).

#### Verileri Filtreleme
- Satır listesini ve bir kategori dizesini alan `filter_by_category(rows, category)` fonksiyonunu uygulayın.
- Satırlar üzerinden geçin ve yalnızca `row["category"]` girdisiyle eşleşenleri yeni bir listeye ekleyin.
- Filtrelenmiş listeyi döndürün.

#### İstatistikleri Hesaplama
- Bir satır listesi ve sayısal bir sütun adı kabul eden `compute_stats(rows, column)` fonksiyonunu oluşturun.
- `min_val`, `max_val` ve `total` için değişkenleri başlatın.
- Her satır üzerinden geçin, sütun değerini float'a dönüştürün ve istatistikleri güncelleyin.
- Toplamı sayıma bölerek ortalamayı hesaplayın.
- Sonuçları yazdırın.

#### CSV'ye Yazma
- Filtrelenmiş verileri yeni bir dosyaya kaydeden `write_filtered_csv(rows, path)` fonksiyonunu yazın.
 idea- Alan adlarını listedeki ilk sözlüğün anahtarlarından çıkarın.
- Başlığı ve satırları yazmak için `csv.DictWriter(f, fieldnames=fieldnames)` kullanın.
- Yazma işleminden sonra dosyanın düzgün şekilde kapatıldığından emin olun.

### 4. Yaklaşım 2: Pandas Kullanımı
Pandas, veri toplama ve istatistikler için daha kısa bir yol sunar.

- CSV dosyasını `pd.read_csv(path)` kullanarak yükleyen bir `pandas_group_stats(path)` fonksiyonu uygulayın.
- Verileri kategoriye göre gruplandırmak ve "total" sütunu için toplu istatistikler hesaplamak için `df.groupby("category")["total"].agg(['sum', 'mean', 'count'])` kullanın.
- Sonuçlanan gruplandırılmış nesne üzerinden geçerek her kategori için istatistikleri yazdırın.

### 5. Ana Yürütme Akışı
- Tüm süreci yöneten bir `main()` fonksiyonu tanımlayın.
- Kaynak CSV ve filtrelenmiş çıktı dosyası için yolları belirleyin.
- Örnek CSV oluşturma fonksiyonunu çağırın.
- İş akışını göstermek için her fonksiyonu sırasıyla çağırın:
  1. CSV'yi oku.
  2. Verileri yazdır.
  3. Belirli bir kategoriye göre filtrele (örneğin, "Electronics").
  4. Filtrelenmiş veriler üzerinde istatistikleri hesapla.
  5. Filtrelenmiş sonuçları yeni bir dosyaya yaz.
  6. Grup tabanlı analizi göstermek için Pandas toplama örneğini çalıştır.

---

## 🏃 Nasıl Çalıştırılır?

1. Bağımlılıkların yüklü olduğundan emin olun:
   ```bash
   pip install pandas
   ```
2. Script'i çalıştırın:
   ```bash
   python csv_processing.py
   ```

---

## 📖 Gösterilen Temel Kavramlar

- **Dosya G/Ç (I/O)**: CSV dosyalarını okuma ve yazma.
- **Veri Yapıları**: Tablo verilerini temsil etmek için Python listeleri ve sözlüklerini kullanma.
- **Filtreleme**: Belirli alt kümeleri seçmek için koleksiyonlar üzerinde yineleme.
- **Toplama (Aggregation)**: İstatistiksel değerleri manuel olarak hesaplama.
- **Pandas DataFrame**: Pandas'ın DataFrame soyutlaması aracılığıyla veri manipülasyonunu nasıl basitleştirdiğini anlama.

# 📂 Dosya ve Kelime Sayacı

Belirli bir dizini özyinilemeli (recursive) olarak tarayan, tüm `.txt` dosyalarını bulan ve içlerindeki toplam dosya ve kelime sayısını hesaplayan basit bir Python aracı. Bu proje, dosya sistemi işlemleri için Python'un `pathlib` kütüphanesini ve dizin gezintisi için özyinleme kullanımını göstermektedir.

## 🚀 Özellikler

- **Özyinilemeli Dizin Gezintisi**: Verilen bir kök yolundaki tüm alt dizinleri tarar.
- **Dosya Filtreleme**: Yalnızca `.txt` uzantılı dosyaları işler.
- **Kelime Sayımı**: Her bir metin dosyasını okur ve toplam kelime sayısını hesaplar.
- **İlerleme Çıktısı**: Her dosya işlendikçe, o dosyaya ait kelime sayısını yazdırır.
- **Özet Rapor**: İşlem sonunda toplam dosya sayısını ve toplam kelime sayısını görüntüler.

---

## 📁 Proje Yapısı

```text
09_file_apps/
└── file_and_word_counter_01.py    # Tüm mantığı içeren ana script
```

---

## 🛠️ Adım Adım Uygulama Kılavuzu

### 1. Ön Gereksinimler
- **Python 3.12+** yüklü olmalıdır.
- Bu proje yalnızca Python'un standart kütüphanesini (`pathlib`) kullandığı için harici bir bağımlılık gerektirmez.

### 2. Script'in Oluşturulması

#### Adım 1: Gerekli Modülleri İçe Aktarma
Script'inizin en üstünde, `pathlib` modülünden `Path` sınıfını içe aktarın:
```python
from pathlib import Path
```

#### Adım 2: Bir Sayaç Sınıfı Oluşturma
Global sayaçları saklamak için bir sınıf tanımlayın:
- `FileCounter` adında bir sınıf oluşturun.
- `__init__` metodunda `count` (dosyalar için) ve `total_words` (kelimeler için) örnek değişkenlerini başlatın.

#### Adım 3: Bir Kelime Sayma Fonksiyonu Oluşturma
Tek bir dosyadaki kelimeleri saymak için bir yardımcı fonksiyon tanımlayın:
- Fonksiyon adı: `count_words_in_file(filepath)`.
- Dosyayı okuma modunda (`"r"`) açın.
- Tüm içeriği `f.read()` ile okuyun.
- Dosyayı kapatın.
- Kelimelerin bir listesini almak için içeriği `content.split()` ile boşluklara göre bölün.
- Kelime listesinin uzunluğunu döndürün.

#### Adım 4: Özyinilemeli İşleme Fonksiyonunu Oluşturma
Ana işleme fonksiyonunu tanımlayın:
- Fonksiyon adı: `process_txt_files(path, counter)`.
- **Adım A — Girişleri Listeleme**: Dizindeki tüm girişleri almak için `path.glob("*")` kullanın. Yalnızca dosyaları tutmak için filtreleyin (dizinleri değil).
- **Adım B — Yineleme**: Her bir giriş üzerinden döngü kurun.
- **Adım C — Özyinleme**: Eğer giriş bir dizinse, o alt dizin için `process_txt_files` fonksiyonunu özyinilemeli olarak çağırın.
- **Adım D — Dosya Kontrolü**: Eğer giriş bir dosyaysa, uzantısının `.txt` olup olmadığını kontrol edin.
- **Adım E — Sayma**:
  - `counter.count` değerini artırın.
  - Bu dosyanın kelime sayısını almak için kelime sayma fonksiyonunu çağırın.
  - Sonucu `counter.total_words` değerine ekleyin.
  - İlerlemeyi yazdırın: dosya numarası, dosya yolu ve kelime sayısı.

#### Adım 5: Ana Fonksiyonu Oluşturma
Giriş noktasını tanımlayın:
- Fonksiyon adı: `main()`.
- Bir `FileCounter()` nesnesi oluşturun.
- Taranacak hedef `Path`'i tanımlayın (örneğin, `/yol/klasorunuza` gibi bir klasör yolu).
- **Doğrulama**: Yolun mevcut olup olmadığını `path.exists()` ile kontrol edin. Mevcut değilse, bir hata mesajı yazdırın ve geri dönün.
- `process_txt_files(path, counter)` fonksiyonunu çağırın.
- İşleme bittikten sonra, toplam dosya sayısını ve toplam kelime sayısını gösteren bir özet bloğu yazdırın.

#### Adım 6: Ana Fonksiyonu Çalıştırma
Script'in en altında, programı başlatmak için `main()` fonksiyonunu çağırın:
```python
main()
```

---

## 🏃 Nasıl Çalıştırılır?

1. Analiz etmek istediğiniz `.txt` dosyalarını içeren bir dizine sahip olduğunuzdan emin olun (veya mevcut herhangi bir klasörü kullanın).
2. Script'i çalıştırın:
   ```bash
   python file_and_word_counter_01.py
   ```

---

## 📖 Örnek Çıktı

Script'i çalıştırdığınızda şuna benzer bir çıktı göreceksiniz:
```text
1 - /yol/klasore/dosya1.txt -> 1250 kelime
2 - /yol/klasore/altdizin/dosya2.txt -> 340 kelime
3 - /yol/klasore/altdizin/dosya3.txt -> 89 kelime

=== SONUÇLAR ===
Toplam dosya sayısı:  3
Toplam kelime sayısı:  1679
```

---

## 🔧 Özelleştirme İpuçları

- **Hedef Klasörü Değiştirme**: Taramak istediğiniz klasörü belirtmek için `main()` fonksiyonundaki `path` değişkenini değiştirin.
- **Farklı Uzantılar**: Diğer dosya türlerini saymak istiyorsanız, `entry_name.suffix == ".txt"` koşulunu istediğiniz uzantıyla (örneğin `.md`, `.csv`) değiştirin.
- **Büyük/Küçük Harf Duyarlılığı**: Mevcut uzantı kontrolü büyük/küçük harfe duyarlıdır. Bunu duyarsız hale getirmek için `entry_name.suffix.lower() == ".txt"` kullanın.

---

## 📚 Gösterilen Temel Kavramlar

- **Nesne Yönelimli Programlama (OOP)**: Özyinilemeli çağrılar arasında durumu korumak için bir sınıf kullanma.
- **Özyinleme (Recursion)**: Fonksiyonun, iç içe geçmiş dizinleri yönetmek için kendisini çağırması.
- **Dosya G/Ç (I/O)**: Metin dosyalarını okuma ve `pathlib` kullanarak yolları güvenli bir şekilde yönetme.
- **Dize Manipülasyonu**: Metni kelimelere ayırmak için `.split()` kullanımı.

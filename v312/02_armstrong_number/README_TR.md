# 🔢 Armstrong Sayısı Denetleyicisi

Belirli bir aralıktaki Armstrong sayılarını tespit eden basit ve verimli bir Python programı.

## 🧐 Armstrong Sayısı Nedir?
**Armstrong sayısı** (narsistik sayı olarak da bilinir), basamaklarının her birinin, toplam basamak sayısı kadar kuvvetinin toplamına eşit olan sayıdır.

**Örnek:**
$153$ sayısı için:
- Basamak sayısı = $3$
- Hesaplama: $1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153$
- Toplam orijinal sayıya eşit olduğu için $153$ bir Armstrong sayısıdır.

**Örnek:**
$9474$ sayısı için:
- Basamak sayısı = $4$
- Hesaplama: $9^4 + 4^4 + 7^4 + 4^4 = 6561 + 256 + 2401 + 256 = 9474$
- Toplam orijinal sayıya eşit olduğu için $9474$ bir Armstrong sayısıdır.

## 🛠️ Ön Gereksinimler
- **Python**: Versiyon 3.12
- **İşletim Sistemi**: Ubuntu 24.04 (üzerinde geliştirilmiştir)

## 🚀 Kurulum
Bu proje, tüm öğrenme modülleri arasında tutarlılığı sağlamak için Python projeleri dizininin kökünde bulunan paylaşılan bir sanal ortam (virtual environment) kullanır.

Paylaşılan ortamı etkinleştirmek için, proje klasörünün içindeyken şu komutu çalıştırın:
```bash
source ../../e312/bin/activate
```

## 💻 Kullanım
Sanal ortam etkinleştirildikten sonra, script'i şu komutla çalıştırabilirsiniz:
```bash
python check_armstrong_number.py
```

**Çalıştırdığınızda ne olur?**
Program, **0'dan 99.999'a** kadar olan tüm tam sayıları tarar ve Armstrong koşulunu sağlayan her sayıyı konsola yazdırır.

---

## 📖 Kod Ne Yapar?
Proje, aşağıdaki mantığı uygulayan `check_armstrong_number.py` adlı bir script'ten oluşur:
1. **Aralık Yinelemesi**: `main()` fonksiyonu, önceden tanımlanmış bir tam sayı aralığında döngü kurar.
2. **Armstrong Doğrulaması**: Her sayı için, `is_armstrong()` fonksiyonu sayının narsistik olup olmadığını belirler.
3. **Basamak İşleme**: Basamak sayısını belirlemek ve basamaklar üzerinde tek tek işlem yapmak için sayı bir dizeye (string) dönüştürülür.
4. **Toplam**: Her bir basamak, toplam basamak sayısı kadar kuvvete yükseltilir ve toplam değere eklenir.
5. **Doğrulama**: Eğer nihai toplam orijinal sayıya eşitse, sayı ekrana yazdırılır.

## 🎓 Temel Kavramlar
- **Dizeye Dönüştürme**: Basamaklar üzerinde kolayca yineleme yapabilmek için `str(n)` kullanarak sayıyı karakter dizisi olarak işleme.
- **Kuvvet Operatörü**: Python'da üssel hesaplama yapmak için `**` operatörünün kullanımı.
- **Boolean Mantığı**: Ana döngüyü temiz tutmak için bir doğrulama fonksiyonundan `True` veya `False` döndürmek.

## 🚀 Karmaşıklık Analizi
- **Zaman Karmaşıklığı**: $O(R \cdot D)$, burada $R$ kontrol edilen sayı aralığı, $D$ ise en büyük sayıdaki basamak sayısıdır.
- **Alan Karmaşıklığı**: Kontrol sırasında sayının dize temsilini saklamak için $O(D)$.

## 📦 Bağımlılıklar
- Yok (bu proje sadece Python Standart Kütüphanesini kullanır).

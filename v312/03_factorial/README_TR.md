# 🔢 Faktöriyel Hesaplama

Verilen bir sayının faktöriyelini hesaplamak için özyinilemeli (recursive) bir fonksiyon kullanan kısa bir Python projesi. Bu proje, Python'da özyinleme (recursion) temel kavramını göstermektedir.

## 🛠️ Genel Bakış
Bu proje, faktöriyel fonksiyonunun özyinleme kullanılarak basit bir uygulamasını sunar. Yeni başlayanların, bir matematiksel problemi çözmek için bir fonksiyonun kendisini nasıl çağırabileceğini anlamalarına yardımcı olmak için tasarlanmıştır.

## ⚙️ Ön Gereksinimler
- **Python**: Versiyon 3.12
- **İşletim Sistemi**: Ubuntu 24.04 (üzerinde geliştirilmiştir)

## 🚀 Kurulum
Bu proje, tüm öğrenme modülleri arasında tutarlılığı sağlamak için Python projeleri dizininin kökünde bulunan paylaşılan bir sanal ortam (virtual environment) kullanır.

Paylaşılan ortamı etkinleştirmek için, proje klasörünün içindeyken şu komutu çalıştırın:
```bash
source ../../e312/bin/activate
```

## 🏁 Hızlı Başlangıç
Bu projeyi çalıştırmak için `factorial.py` script'ini yürütün:
```bash
python factorial.py
```

**Kaynak Docstring:**
```python
"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""
```

**Beklenen Çıktı:**
`1307674368000`

## 📂 Proje Yapısı
```text
03_factorial/
└── factorial.py    # Özyinilemeli faktöriyel mantığını ve bir test vakasını uygular
```

## 📖 Nasıl Çalışır?
Proje, `factorial(i)` adında özyinilemeli bir fonksiyon kullanır.
1. **Temel Durum (Base Case)**: `i` değeri 0'a ulaştığında, fonksiyon 1 döndürür.
2. **Özyinleme Adımı (Recursive Step)**: Aksi takdirde, `i` değerini `factorial(i - 1)` çağrısının sonucuyla çarparak döndürür.
3. Program daha sonra 15'in faktöriyeli hesaplar ve yazdırır.

## 🎓 Temel Kavramlar
- **Docstring'ler**: Proje, yazar ve ortam gibi meta verileri sağlamak için modül düzeyinde bir docstring kullanır.
- **Özyinleme (Recursion)**: Bir fonksiyonun, problemi daha küçük alt problemlere bölerek kendisini tekrar çağırma tekniğidir.
- **Temel Durum (Base Case)**: Özyinlemenin sonsuz döngüye girmesini engelleyen temel koşuldur.
- **Tip Belirleme (Type Hinting)**: Daha iyi kod netliği sağlamak için giriş ve çıkış tiplerini belirtmek amacıyla `(i:int) -> int` kullanımı.

## 📦 Bağımlılıklar
- Yok (bu proje sadece Python Standart Kütüphanesini kullanır).

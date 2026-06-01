# Fibonacci Dizisi Projesi

Sayı dizisindeki her sayının kendisinden önceki iki sayının toplamı olduğu Fibonacci dizisini özyinilemeli (recursive) bir yaklaşımla uygulayan ve dizideki her sayı için yürütme süresini takip eden bir Python projesi. Bu proje, özyinilemeli fonksiyon çağrılarını ve temel performans ölçümünü göstermektedir.

## 🚀 Hızlı Başlangıç (Sıfırdan Oluşturma)

Bu projeyi kendi makinenizde yeniden oluşturmak için şu basit adımları izleyin:

### 1. Klasör Kurulumu
Proje için özel bir dizin oluşturun:
```bash
mkdir 04_fibonacci
cd 04_fibonacci
```

### 2. Kodu Oluşturma
`fibonacci.py` adında bir dosya oluşturun ve aşağıdaki uygulamayı içine yapıştırın:

```python
"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

from time import perf_counter

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def main():
    t0: int = perf_counter()
    t2 = t0
    for i in range(36):
        t1 = perf_counter()
        print(f"{i} : {fib(i)} ({(t1 - t2)*1000} ms)")
        t2 = t1

main()
```

### 3. Çalıştır ve Doğrula
Script'i Python kullanarak çalıştırın:
```bash
python3 fibonacci.py
```

**Beklenen Çıktı:**
Script, 0'dan 35'e kadar olan sayılar için indeksini, Fibonacci sayısını ve hesaplama için geçen süreyi milisaniye cinsinden yazdıracaktır. İndeks büyüdükçe sürenin üstel olarak arttığını fark edeceksiniz.

---

## 📂 Proje Yapısı
```text
04_fibonacci/
└── fibonacci.py    # Özyinilemeli Fibonacci mantığını ve zamanlamayı uygulayan ana script
```

## 🛠️ Gereksinimler
- **Python**: Versiyon 3.12 önerilir.
- **İşletim Sistemi**: Tüm ana işletim sistemleriyle uyumludur (Ubuntu 24.04 üzerinde geliştirilmiştir).

## 📖 Teknik Açıklama

### Özyinleme (Recursion)
Bu proje, Fibonacci dizisinin **özyinilemeli** bir uygulamasını kullanır:
- **Temel Durum (Base Case)**: Eğer $n < 2$ ise, $n$ döndürür.
- **Özyinleme Adımı (Recursive Step)**: $n \ge 2$ için, kendisinden önceki iki sayının toplamını döndürür: $fib(n-1) + fib(n-2)$.

### Performans Takibi
Script, hesaplamalar arasında geçen yüksek çözünürlüklü süreyi ölçmek için `time.perf_counter()` kullanır.

**Gözlem**: Bu uygulama, memoizasyon (hafızaya alma) olmadan basit özyinleme kullandığı için zaman karmaşıklığı üsteldir $O(2^n)$. Bu durum, $n$ arttıkça performansın önemli ölçüde düşmesine neden olur ve bu durum script'in çıktısında açıkça görülür.

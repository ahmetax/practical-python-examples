# λ Python'da Lambda Fonksiyonları

Python'daki **lambda fonksiyonlarının** (anonim fonksiyonlar) kullanımını gösteren kapsamlı bir örnekler koleksiyonu. Lambda fonksiyonları, resmi bir `def` ifadesi olmadan `lambda` anahtar kelimesi kullanılarak tanımlanan küçük, satır içi fonksiyonlardır. Özellikle `map()`, `filter()`, `sorted()` ve `reduce()` gibi yerleşik fonksiyonlarla birlikte kullanıldığında kısa süreli işlemler için oldukça kullanışlıdırlar.

---

## 📁 Proje Yapısı

```text
13_lambda_basics/
└── lambda_examples.py    # 20 adet lambda fonksiyonu örneği içeren ana betik
```

---

## 🛠️ Adım Adım Uygulama Rehberi

### Gereksinimler
- Python 3.12+ yüklü olmalı
- Harici bir bağımlılık gerekmez (yalnızca standart kütüphane kullanılır)

---

### Betiği Oluşturma

Bu proje, lambda fonksiyonları için 20 farklı kullanım durumunu göstermektedir. Her bir örneği sıfırdan oluşturmak için şu adımları izleyin.

---

### 1. Temel Kurulum

`lambda_examples.py` adında yeni bir dosya oluşturun ve şu importlarla başlayın:

```python
import operator
from functools import reduce
import math

def main():
    print("--- Python 3.12 Lambda Fonksiyon Örnekleri ---")
```

---

### 2. Örnek 1: Temel Toplama

İki argüman alan ve toplamlarını döndüren bir lambda oluşturun.

**Mantık**: `x` ve `y` değerlerini kabul eden ve `x + y` döndüren bir `add` lambda fonksiyonu tanımlayın. Bunu `add(5, 3)` ile çağırın.

---

### 3. Örnek 2: Sayının Karesini Alma

Bir argüman alan ve karesini döndüren bir lambda oluşturun.

**Mantık**: `square` fonksiyonunu `lambda x: x**2` olarak tanımlayın. Bunu `square(4)` ile çağırın.

---

### 4. Örnek 3: Koşullu (Ternary) İfade

Bir sayının çift mi yoksa tek mi olduğunu kontrol etmek için ternary operatörü içeren bir lambda kullanın.

**Mantık**: `check_even` fonksiyonunu `lambda x: "Çift" if x % 2 == 0 else "Tek"` olarak tanımlayın. Bunu `check_even(7)` ile çağırın.

---

### 5. Örnek 4: Tuple Listesini Sıralama

Bir tuple listesini, lambda'yı anahtar (key) olarak kullanarak ikinci elemana (string) göre sıralayın.

**Mantık**: `pairs = [(1, 'bir'), (2, 'iki'), ...]` şeklinde bir liste oluşturun. `pairs.sort(key=lambda pair: pair[1])` komutunu çağırın.

---

### 6. Örnek 5: Liste Filtreleme

Bir listeden sadece çift sayıları tutmak için `filter()` fonksiyonunu bir lambda ile kullanın.

**Mantık**: `nums = [1, 2, 3, 4, 5, 6]` listesini oluşturun. `filter(lambda x: x % 2 == 0, nums)` uygulayın ve listeye dönüştürün.

---

### 7. Örnek 6: Bir Fonksiyonu Listeye Eşleme (Mapping)

Bir listedeki her sayıyı iki katına çıkarmak için `map()` fonksiyonunu bir lambda ile kullanın.

**Mantık**: `map(lambda x: x * 2, nums)` uygulayın ve listeye dönüştürün.

---

### 8. Örnek 8: Currying (Lambda içinde Lambda)

Başka bir lambda döndüren bir "fabrika" fonksiyonu oluşturun — klasik bir currying kalıbı.

**Mantık**: `multiplier = lambda x: lambda y: x * y` şeklinde tanımlayın. `double_func = multiplier(2)` olarak atayın ve 20 sonucunu almak için `double_func(10)` şeklinde çağırın.

---

### 9. Örnek 9: Sözlüğü Değere Göre Sıralama

Bir sözlüğü, lambda anahtarını kullanarak değerlerine göre azalan sırada sıralayın.

**Mantık**: `scores = {'Alice': 88, 'Bob': 95, 'Charlie': 80}` şeklinde bir sözlük oluşturun. `sorted(scores.items(), key=lambda item: item[1], reverse=True)` komutunu kullanın.

---

### 10. Örnek 10: Basit String Formatlayıcı

Bir selamlama mesajı formatlamak için lambda kullanın.

**Mantık**: `greet = lambda name: f"Merhaba, {name}! Ubuntu 24.04'e hoş geldiniz."` şeklinde tanımlayın. Bunu `greet('Geliştirici')` ile çağırın.

---

### 11. Örnek 11: Sözlük Listesinden Veri Çıkarma

Bir sözlük listesinden belirli alanları çıkarmak için `map()` ve lambda kullanın.

**Mantık**: `users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]` listesini oluşturun. İsimleri `map(lambda u: u['name'], users)` ile çıkarın.

---

### 12. Örnek 12: Reduce ile Toplama

Bir listedeki tüm elemanları toplamak için `functools` modülünden `reduce()` fonksiyonunu bir lambda ile kullanın.

**Mantık**: `reduce` fonksiyonunu import edin. `reduce(lambda x, y: x + y, [1, 2, 3, 4])` uygulamasını yapın.

---

### 13. Örnek 13: Palindrom Kontrolü

Bir metnin tersten okunuşunun aynı olup olmadığını kontrol etmek için lambda kullanın.

**Mantık**: `is_palindrome = lambda s: s == s[::-1]` şeklinde tanımlayın. `'radar'` ile test edin.

---

### 14. Örnek 14: Daire Alanı Hesaplama

Dairenin alanını hesaplamak için `math.pi` ile birlikte bir lambda kullanın.

**Mantık**: `circle_area = lambda r: math.pi * (r**2)` şeklinde tanımlayın. `r=5` ile çağırın ve sonucu 2 ondalık basamağa formatlayın.

---

### 15. Örnek 15: Celsius'tan Fahrenheit'a Dönüştürme

Sıcaklıkları dönüştürmek için bir lambda kullanın.

**Mantık**: `c_to_f = lambda c: (c * 9/5) + 32` şeklinde tanımlayın. `c=25` ile çağırın.

---

### 16. Örnek 16: Ön Eke Göre Metin Filtreleme

Belirli bir harfle başlayan metinleri bulmak için `filter()` ve lambda kullanın.

**Mantık**: `fruit_list = ["apple", "apricot", "banana", "cherry"]` listesini oluşturun. `lambda f: f.startswith('a')` ile filtreleyin.

---

### 17. Örnek 17: Lambda ile Liste Üreteci (List Comprehension)

Bir liste üreteci içinde lambda kullanın (tipik bir kullanım olmasa da lambdanın çok yönlülüğünü gösterir).

**Mantık**: Kareler listesi oluşturmak için `[(lambda x: x**2)(x) for x in range(5)]` yapısını kullanın.

---

### 18. Örnek 18: Basit Mantık Kapısı (AND)

Mantıksal bir VE (AND) işlemini simüle etmek için lambda kullanın.

**Mantık**: `logic_and = lambda a, b: a and b` şeklinde tanımlayın. `(True, False)` ile test edin.

---

### 19. Örnek 19: Operatörleri Dinamik Olarak Uygulama

Bir operatör fonksiyonunu (`operator` modülünden) bir lambda'ya argüman olarak geçirin.

**Mantık**: `apply_op = lambda op, x, y: op(x, y)` şeklinde tanımlayın. Operatör olarak `operator.mul` kullanın.

---

### 20. Örnek 20: Aralık Doğrulama

Bir sayının belirli bir aralıkta olup olmadığını kontrol etmek için lambda kullanın.

**Mantık**: `in_range = lambda x, start, end: start <= x <= end` şeklinde tanımlayın. `in_range(15, 10, 20)` ile test edin.

---

### 3. Betiği Tamamlama

Tüm örnekleri ekledikten sonra, ana fonksiyonu kapatın ve çağırın:

```python
if __name__ == "__main__":
    main()
```

---

## 🏃 Nasıl Çalıştırılır?

1. Dosyayı `lambda_examples.py` olarak kaydedin.
2. Betiği çalıştırın:
   ```bash
   python lambda_examples.py
   ```

---

## 📖 Çıktı Örneği

Betiği çalıştırdığınızda şuna benzer bir çıktı göreceksiniz:

```text
--- Python 3.12 Lambda Fonksiyon Örnekleri ---
1. Toplama (5+3): 8
2. Kare (4): 16
3. Teklik/Çiftlik (7): Tek
4. İsime göre sıralanmış tuplelar: [(1, 'bir'), (3, 'üç'), (4, 'dört'), (2, 'iki')]
5. Filtrelenmiş çiftler: [2, 4, 6]
6. Eşlenmiş iki katları: [2, 4, 6, 8, 10, 12]
7. En uzun kelime: banana
8. Curried double (10): 20
9. Azalan sırada puanlar: [('Bob', 95), ('Alice', 88), ('Charlie', 80)]
10. Selamlama: Merhaba, Geliştirici! Ubuntu 24.04'e hoş geldiniz.
11. Çıkarılan isimler: ['Alice', 'Bob']
12. Reduce toplamı: 10
13. 'radar' palindrom mu? True
14. Daire alanı (r=5): 78.54
15. 25C'den F'ye: 77.0
16. 'a' ile başlayan meyveler: ['apple', 'apricot']
17. Liste üreteci lambda kareleri: [0, 1, 4, 9, 16]
18. Mantıksal VE (True, False): False
19. lambda üzerinden operator.mul kullanımı: 50
20. 15 sayısı 10-20 aralığında mı? True
```

---

## 🔑 Gösterilen Temel Kavramlar

1. **Anonim Fonksiyonlar**: `lambda` anahtar kelimesini kullanarak isimsiz fonksiyonlar oluşturmak.
2. **Tek Satırlı Mantık**: Basit işlemler için özlü fonksiyonlar yazmak.
3. **Fonksiyonel Programlama**: Lambda'yı `map()`, `filter()`, `sorted()`, `max()` ve `reduce()` ile kullanmak.
4. **Yüksek Mertebeli Fonksiyonlar**: Fonksiyonları argüman olarak geçirmek ve fonksiyon döndürmek (currying).
5. **Ternary İfadeler**: Lambda'lar içinde koşullu mantık kullanmak.
6. **Veri Dönüştürme**: Listeleri ve sözlükleri filtrelemek, dönüştürmek ve veri çıkarmak.
7. **Matematiksel İşlemler**: Lambda'lar kullanarak hesaplamalar yapmak.

---

## 💡 Lambda Ne Zaman Kullanılmalı?

- **Kısa süreli işlemler**: Bir fonksiyonun sadece bir kez kullanılması gerektiğinde.
- **Fonksiyonel programlama**: `map`, `filter`, `reduce`, `sorted` vb. kullanırken.
- **Geri çağırmalar (Callbacks)**: Küçük bir fonksiyonu başka bir fonksiyona argüman olarak gönderirken.
- **GUI olay yönetimi**: Basit olay geri çağırmaları için (örneğin Tkinter'da).

---

## ⚠️ Lambda Ne Zaman Kullanılmamalı?

- **Karmaşık mantık**: Fonksiyon birden fazla satır gerektiriyorsa, `def` kullanın.
- **Yeniden kullanılabilirlik**: Eğer fonksiyonu birden fazla yerden çağırmanız gerekiyorsa, `def` ile tanımlayın.
- **Hata Ayıklama (Debugging)**: Lambda'ların ismi olmadığı için hata ayıklamaları daha zordur.

---

## 🔧 Genişletme Fikirleri

- Yaygın görevler için kendi lambda ifadelerinizi yazın.
- `pandas` kütüphanesi ile DataFrame operasyonları için lambda'ları kullanın.
- Projeleriniz için lambda tabanlı bir yardımcı modül oluşturun.
- `map()` ve `filter()` alternatifleri olarak liste üreteçlerini (list comprehensions) keşfedin.

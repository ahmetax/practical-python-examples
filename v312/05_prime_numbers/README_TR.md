# 🔢 Asal Sayılar Üreteci

Belirli bir aralıktaki tüm asal sayıları bulan ve yazdıran basit ve verimli bir Python programı.

## 🧐 Asal Sayı Nedir?
**Asal sayı**, 1'den büyük olan ve 1 ile kendisinden başka hiçbir pozitif böleni olmayan doğal sayıdır.

**Örnekler:**
- **2**: Tek çift asal sayıdır.
- **3**: Asaldır, çünkü sadece 1 ve 3'e bölünebilir.
- **5**: Asaldır, çünkü sadece 1 ve 5'e bölünebilir.
- **4**: Asal değildir, çünkü 1, 2 ve 4'e bölünebilir.

---

## 📁 Proje Yapısı
```text
05_prime_numbers/
└── prime_numbers.py  # Ana mantık ve yürütme script'i
```

---

## 🛠️ Kurulum ve Yükleme

### 1. Ön Gereksinimler
- **Python 3.12+** yüklü olmalıdır.
- Bu proje standart Python kütüphanelerini kullanır ve harici bir bağımlılık gerektirmez.

### 2. Hızlı Başlangıç
1. `05_prime_numbers` adında bir klasör oluşturun.
2. İçine `prime_numbers.py` adında bir dosya oluşturun.
3. Kaynak dosyadaki kodu bu script'e kopyalayın.

---

## 🏃 Programı Çalıştırma

Script'i Python yorumlayıcısını kullanarak çalıştırın:

```bash
python prime_numbers.py
```

### Çalıştırdığınızda ne olur?
Program, **0'dan 127'ye kadar** olan tüm tam sayıları tarar ve bulunan her asal sayıyı konsola yazdırır.

---

## 📖 Kod Açıklaması

### Mantık Analizi
Program, asalları belirlemek için **Deneme Bölmesi (Trial Division)** adı verilen bir teknik kullanır:

1. **Aralık Tanımı**: Bir `lownum` (başlangıç) ve `highnum` (bitiş) tanımlar.
2. **Dış Döngü**: `[lownum, highnum]` aralığındaki her bir `n` sayısı üzerinden döner.
3. **Asal Filtreleme**:
    - Tanım gereği asal olmayan, 1'e eşit veya 1'den küçük sayıları atlar.
    - `n > 1` olan her sayı için, `2`den başlayıp `n-1`e kadar giden başka bir döngü başlatır.
4. **Bölünebilirlik Kontrolü**: Eğer `n`, bu aralıktaki herhangi bir `i` sayısına bölünebilirse (`n % i == 0`), sayı asal değildir ve iç döngü kırılır (`break`).
5. **`for...else` Bloğu**: Python'a özgü, bir `for` döngüsüne bağlı olan `else` yan cümleciği, **yalnızca döngü normal bir şekilde tamamlandığında** (yani `break` ifadesine hiç rastlanmadığında) çalışır. Eğer hiçbir bölen bulunamadıysa, sayı asaldır ve yazdırılır.

---

## 🚀 Karmaşıklık Analizi
- **Zaman Karmaşıklığı**: En kötü durumda $O(N^2)$'dir (burada $N$, `highnum` değeridir), çünkü her bir sayı için potansiyel olarak kendinden önceki tüm sayılar kontrol edilir.
- **Alan Karmaşıklığı**: $O(1)$'dir, çünkü aralık boyutuna bakılmaksızın sadece birkaç değişken kullanır.

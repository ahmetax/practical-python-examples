# Proje 31: Özel Sıralama Algoritmaları

Klasik sıralama algoritmalarını sıfırdan inşa ederek dizi sıralama mekaniklerini analiz eden teorik bir uygulama. Bu proje, iç içe döngü dizin gezintisini göstermek için Bubble Sort ve özyinelemeli böl-iş fethet stratejilerini örneklendirmek için Merge Sort içerir.

## Mimari Amaç
Proje, bellek adreslerinin, işaretçilerin (pointers) ve dizi indislerinin programatik olarak nasıl kaydırıldığını göstermek için Python'ın dahili, yüksek optimize edilmiş C tabanlı `Timsort` (`.sort()`) motorunu atlar. Kuadratik zaman yürütmesini ($O(n^2)$) lineer-logaritmik zaman yürütmesi ($O(n \log n)$) ile karşılaştırmak için bir kıyaslama görevi görür.

## Proje Yapısı
```text
31_custom_sorting_algorithms/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX environment)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Set up an isolated directory for this project inside your repository workspace:

```bash
mkdir 31_custom_sorting_algorithms
cd 31_custom_sorting_algorithms

### Adım 2: Sıralama Algoritmalarını Uygulama
main.py adında bir dosya oluşturun. Sıralama rutinlerinizi adım adım oluşturun:

Bubble Sort'u Uygulayın: bubble_sort(arr) adında bir fonksiyon yazın. Sıralama işleminin saf kalmasını ve orijinal dizi referansının istenmeyen şekilde değiştirilmesini önlemek için girdi listesinin `list(arr)` yoluyla sığ bir kopyasını oluşturun. Yan yana elemanları karşılaştırmak ve sırası bozuklarsa yer değiştirmek için iç içe döngüler kullanın. Bir geçiş herhangi bir değişiklik olmadan tamamlanırsa döngüden erken çıkmak için bir optimizasyon bayrağı (swapped = False) ekleyin, bu da zaten sıralanmış girdilerde runtime tasarrufu sağlar.

Merge Sort'u Uygulayın: merge_sort(arr) adında özyinelemeli (recursive) bir fonksiyon yazın. Uzunluğu 1 veya daha azsa koleksiyonu hemen döndüren bir temel durum (base case) oluşturun. Daha büyük listeler için, orta noktayı floor division (//) kullanarak bulun ve diziyi iki yarıya (arr[:mid] ve arr[mid:]) ayırın. Bu dilimleri özyinelemeli olarak tekrar merge_sort'a iletin.

Merge Birleştirici Yardımcı Programı Oluşturun: _merge(left, right) adında özel bir yardımcı fonksiyon oluşturun. Her iki sıralanmış listeyi aynı anda geçmek için sıfır ile başlatılmış iki indeks işaretçi değişkeni (i = j = 0) kullanın. Mevcut işaretçilerdeki elemanları karşılaştırın, daha düşük değeri yeni bir sonuç dizisine ekleyin ve o işaretçiyi ilerletin. Listelerden biri tükendiğinde kalan herhangi bir elemanı eklemek için .extend() kullanın.

### Adım 3: Çalıştırma ve Doğrulama
Betik (script) altına, rastgele sayılar (negatif değerler, sıfırlar ve yinelenen girişler dahil) içeren sıralanmamış bir liste kullanarak bir değerlendirme bloğu ekleyin. Her iki algoritmanın da mükemmel şekilde sıralanmış listeler döndürdüğünü doğrulamak için dosyayı terminalden çalıştırın:
```bash
python main.py



# Proje 32: İkili Arama Ağacı Veri Yapısı

Baştan sona yerel olarak oluşturulmuş, bağımsız bir İkili Arama Ağacı (BST) nesne yönelimli uygulaması. Bu proje, referans/pointer düğüm bağlantısını, koşullu dolaşım mekaniklerini ve derin özyinelemeli ağaç manipülasyon stratejilerini gösterir.

## Mimari Amaç
Uygulama, düz indeksleme tablolarına yapısal bir alternatif sağlar. Bir ebeveynin solundaki herhangi bir çocuk varlığının daha düşük bir değerlendirmeye, sağındaki herhangi bir çocuğun ise daha yüksek bir değere sahip olduğu hiyerarşik dal özelliklerini koruyarak, sistem arama işlemlerini ve düğüm güncellemelerini lineeritmik logaritmik zamanda ($O(\log n)$) çalıştırabilen yürütme çerçeveleri oluşturur.

## Proje Yapısı
```text
32_data_structures_bin_tree/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible ecosystem)
Runtime: Python 3.12+ (Leverages modern union notation Node | None)
Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated project directory structure within your repository workspace:
```bash
mkdir 32_data_structures_bin_tree
cd 32_data_structures_bin_tree

### Adım 2: Ağaç Sınıflarını Birleştirme
`main.py` adında bir dosya oluşturun. Hiyerarşik varlıklarınızı adım adım yapılandırın:
1. Bir Node Taslağı Tasarlama: `Node` adında temel bir yapı sınıfı oluşturun. Başlatıcısında (`__init__`), bir tamsayı `data` değişkeni kabul edin ve açıkça `None` olarak başlatılmış iki varsayılan çocuk işaretçi alanı (self.left ve self.right) eşleyin.
2. Ana Ağaç Kabuğunu Tasarlama: `BinarySearchTree` adında, boş tek bir giriş işaretçisi ile başlatılan (self.root = None) bir koordinasyon sınıfı oluşturun.
3. Özyinelemeli Ekleme Dahil Etme: Bir `insert(value)` genel metodu oluşturun. Eğer self.root mevcut değilse, yeni değeri hemen ona bağlayın. Aksi takdirde, düğümü dahili bir izleme metodu olan `_insert_recursive(current_node, value)`'a iletin. Yeni değeri mevcut düğüm değeriyle karşılaştırarak sola mı yoksa sağa mı dallanılacağına karar verin ve boş bir yaprak pozisyonu (`None`) bulunana kadar ağacı özyinelemeli olarak takip edin.
4. Uzmanlaşmış Arama Yönlendirmesi Dahil Etme: Ağaç dallarında özyinelemeli olarak adım atan bir `search(target)` fonksiyonu uygulayın. Veri organize edildiği için her düğümü taramanıza gerek yoktur; aramalar, değer karşılaştırmalarına dayanarak tüm alt ağaçların ötesine atlayabilir ve bu sayede ortalama $O(\log n)$ zaman karmaşıklığı elde edebilirsiniz.
5. Sıra İçi Sıralama Geçişi Uygulama: Bir sıra içi algoritma stratejisi kullanarak bir analitik görselleştirme dizisi oluşturun (`_inorder_recursive(node, list)`). Geçiş dizisi sırasını, önce sola adım atmak, ikinci olarak ebeveyn merkezi toplamak ve en son sağa geçiş yapmak üzere programlayın. Geçerli bir BST düzeni üzerinde gerçekleştirildiğinde, bu strateji doğal olarak değerleri mükemmel bir şekilde sıralanmış artan sırada çıktı verir.

### Adım 3: Çalıştırma ve Doğrulama
`main.py` dosyasının en altına bir sürücü değerlendirme betiği ekleyin. Sınıfınızın bir örneğini oluşturun, onu sıralanmamış bir sayı dizisiyle doldurun, bir sıra içi yazdırma araması çalıştırın ve izleme mantığınızı doğrulamak için hedeflenmiş değer sorgulamaları yapın. Betiği çalıştırın:
```bash
python main.py

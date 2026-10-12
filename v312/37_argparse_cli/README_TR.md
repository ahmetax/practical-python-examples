# Proje 37: argparse ile Komut Satırından Dosya Düzenleyici

Standart `argparse` modülüyle yazılmış küçük bir komut satırı aracı. Komut satırından bir kaynak ve bir hedef klasör alır; kaynak klasördeki her dosyayı uzantısına göre hedef klasörün altındaki bir kategori klasörüne (`Documents`, `Images`, `Code` veya `Others`) taşır. `--dry-run` bayrağıyla hiçbir şeyi taşımadan ne yapılacağını görebilirsiniz.

| Konu | Temel API |
|------|-----------|
| Yardım ekranındaki program açıklaması ve örnek satır | `ArgumentParser(description=..., epilog=...)` |
| Zorunlu konumsal argümanlar (`source`, `target`) | `add_argument("source")` |
| Kısa ve uzun adı olan açma/kapama bayrağı | `add_argument("-d", "--dry-run", action="store_true")` |
| Otomatik `--help` ve kullanım hataları | `parse_args()` |

## Nasıl Çalışır?
- `parse_args()`, `source`, `target` ve isteğe bağlı `-d` / `--dry-run` bayrağını okur. Konumsal argümanlardan biri eksikse argparse kullanım satırını yazar ve `2` çıkış koduyla sonlanır.
- `organize_files()`, kaynak klasörün doğrudan içindeki dosyaları dolaşır (alt klasörler atlanır) ve küçük harfe çevrilmiş uzantıyı sabit bir tabloda arar:
  - `.txt`, `.pdf`, `.docx` → `Documents`
  - `.jpg`, `.jpeg`, `.png` → `Images`
  - `.py`, `.sh`, `.js` → `Code`
  - diğer her şey → `Others`
- `--dry-run` yoksa kategori klasörü gerekirse oluşturulur ve dosya `shutil.move()` ile taşınır. `--dry-run` varsa yalnızca planlanan taşımalar yazdırılır; hiçbir şey oluşturulmaz ya da taşınmaz.

Dikkat etmeniz gereken birkaç nokta:
- Kaynak klasör yoksa betik bir hata mesajı yazar, ancak yine de `0` çıkış koduyla sonlanır.
- Hedef kategori klasöründe aynı adlı bir dosya varsa uyarı verilmeden üzerine yazılır.
- Dosyalar dosya sisteminin döndürdüğü sırayla listelenir; bu sıra alfabetik olmak zorunda değildir.

## Proje Yapısı
```text
37_argparse_cli/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.6 veya üstü (f-string ve `pathlib`). Python 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma

argparse'ın ürettiği yardım ekranını görüntüleyin:
```bash
python3 main.py --help
```
```text
usage: main.py [-h] [-d] source target

A robust CLI tool to organize directory files smoothly by category extensions.

positional arguments:
  source         Path to the unsorted source directory containing target
                 items.
  target         Path to the destination directory where categorized results
                 will be saved.

options:
  -h, --help     show this help message and exit
  -d, --dry-run  Simulates execution flow by printing layout actions without
                 moving any files.

Example: python3 main.py ./downloads ./sorted_archive --dry-run
```
Python 3.10'dan önceki sürümler `options:` yerine `optional arguments:` yazar.

Birkaç boş dosya içeren bir deneme klasörü oluşturun ve önce deneme çalıştırması yapın:
```bash
mkdir test_source && touch test_source/doc1.pdf test_source/photo2.png test_source/script3.py
python3 main.py ./test_source ./test_target --dry-run
```
```text
--- Initiating File Organization Layout ---
Source Location : /path/to/test_source
Target Location : /path/to/test_target
[Notice] DRY-RUN MODE ACTIVE: No files will actually be modified.

 -> Mapping: photo2.png -> [Images] folder
 -> Mapping: script3.py -> [Code] folder
 -> Mapping: doc1.pdf -> [Documents] folder
--------------------------------------------------
Execution complete. Total items logged/processed: 3
```
Deneme çalıştırmasında `test_target` oluşturulmaz. Dosyaları gerçekten taşımak için aynı komutu `--dry-run` olmadan çalıştırın:
```bash
python3 main.py ./test_source ./test_target
```
Bundan sonra `test_source` boşalır; dosyalar `test_target/Documents`, `test_target/Images` ve `test_target/Code` klasörlerine taşınmış olur.

Betiği argümansız çağırırsanız kullanım hatası görürsünüz:
```text
usage: main.py [-h] [-d] source target
main.py: error: the following arguments are required: source, target
```

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/17/pythonda-argparse-ile-gercek-bir-komut-satiri-araci-yazmak/
- `argparse` belgeleri: https://docs.python.org/3/library/argparse.html

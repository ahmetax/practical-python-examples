# Proje 57: Claude Olmayan Paket Öneriyor mu? PyPI Ad Denetçisi

Claude'a (Claude Code 2.1.330, `claude-opus-5-5`, araçlar kapalı) üçüncü taraf paket ya da Türkiye'ye özgü hizmet gerektiren 32 Python işi üçer kez yazdırıldı (PDF tablosu, HEIC, OCR, Türkçe kök bulma, IBAN, kargo takibi, MERNİS, merkez bankası kurları...). 96 yanıtta 134 `pip install` adı geçti (33 farklı paket); 134'ü de PyPI'da var. İçe aktarmalar, `from X import Y` adları (ağır paketler hariç) ve üç Hugging Face model kimliği de gerçekti. Ama varlık zayıf bir güvence: ayrıştırma sırasında kendi betiğimiz bir ara `python_version` adını paket sandı ve PyPI'da bu adla gerçek bir paket var.

Bu betik denetçinin kendisidir. Bir yanıt metni verilince (bir `python` bloğu ve `pip install` satırlı bir `bash` bloğu) `pip` adlarını çıkarır, her biri için PyPI JSON API'sine sorar, karşılığı olmayan bir üçüncü taraf `import` için uyarır. Argümansız çalıştırınca iki gömülü örneği denetler: gerçek paketler ve uydurma bir ad.

| Denetim | Kapsam | Sonuç |
|---|---|---|
| `pip install` adları | 134 geçiş, 33 farklı paket | 134/134 var |
| `import` ile `pip` adı uyumu | 96 yanıt | uyuşmazlık 0 |
| `from X import Y`, `X.a.b` zincirleri | 96 yanıt, 4 ağır paket hariç | eksik ad 0 |
| Hugging Face model kimlikleri | 3 farklı kimlik | 3/3 var |

## Nasıl Çalışır
- `pip_adlari`, `bash` bloklarındaki `pip install` satırlarını `shlex.split` ile okur; sürüm koşullarını ve ortam işaretçilerini (`;`) atar.
- `import_adlari`, `python` bloğunu `ast` ile ayrıştırır ve üst düzey üçüncü taraf modülleri tutar (`sys.stdlib_module_names` süzülür).
- `pypi_var_mi`, `https://pypi.org/pypi/<ad>/json` adresine GET gönderir: 200 = var, 404 = yok, başka kod ya da ağ hatası = belirsiz.
- Import adı ile pip adı farklı olanlar (`PIL`, `cv2`, `bs4`, `yaml`...) küçük bir tabloyla eşlenir.

## Sınırlar
- "PyPI'da var" ifadesi "doğru paket" ya da "güvenli paket" demek değil: kaydedilmiş bir ad bu denetimi geçer.
- Tek model, tek sürüm, iş başına üç deneme, araçlar kapalı (`pip`'i kendisi çalıştıran bir ajan ayrı bir senaryo).
- Betik adlara bakar; sürüm yaşı, indirme sayısı ya da bakımcıya bakmaz.

## Proje Yapısı
```text
57_package_name_check/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 ya da üstü (`sys.stdlib_module_names`). Python 3.12.3 ile denendi.
- Üçüncü taraf paket gerekmez. pypi.org'a ağ erişimi gerekir (salt okunur GET).

## Kullanım
```bash
python3 main.py                # gömülü iki örnek
python3 main.py yanit.md ...   # kendi yanıt dosyalarınız
```

## Örnek Çıktı (Python 3.12.3)
```text
== örnek: gerçek paketler
  pip hijridate                      var    2.6.0, 5 sürüm
  pip schwifty                       var    2026.11.3, 97 sürüm
  pip requests                       var    2.34.2, 163 sürüm
== örnek: uydurma paket
  pip turkce-kimlik-dogrula-pro      YOK    404
```
Sürüm numaraları, betiği çalıştırdığınız gün PyPI'da ne varsa onu gösterir.

# Proje 50: Sürüm Matrisi — "Python 3.12+ Gerekir" Doğru mu?

Bir proje klasörünü resmi `python:X-slim` Docker imajlarında (varsayılan olarak 3.8'den 3.15'e) çalıştıran ve her sürüm için kodun **derlenip derlenmediğini**, `main.py` dosyasının **çalışıp çalışmadığını** raporlayan küçük bir araç. Çalışan en düşük sürüm, projenin gerçek alt sınırıdır. README'deki sürüm satırıyla bu sonucu karşılaştırın.

Aracı bu depodaki 23–32, 35–38 ve 41 numaralı projelerde kullandık. Gerekçe veren üç iddia ("`match` için 3.10+", "`asyncio.TaskGroup` için 3.11+", "PEP 695 için 3.12+") doğru çıktı. Yalnızca "Runtime: Python 3.12+" yazan on iddianın hiçbiri doğru değildi: bu projelerin altısı 3.8'de, dördü 3.9'da çalışıyor.

## Nasıl Çalışıyor?
Araç her sürüm için ağı kapalı bir konteyner başlatır, projeyi `/src` altına salt okunur bağlar, `/tmp/app` altına kopyalar (dosya yazan betikler de çalışabilsin diye) ve şunları yapar:

1. Her `.py` dosyasını `compile()` fonksiyonuna verir. Burada çıkan `SyntaxError`, o sözdiziminin bu sürümde olmadığını gösterir.
2. `main.py` dosyasını çalıştırır (stdin kapalı, isteğe bağlı argümanlarla), çıkış kodunu ve stderr'in son satırını kaydeder.

| Sonuç | Anlamı |
|-------|--------|
| `ok` | çıkış kodu 0 |
| `SyntaxError` | bir dosya bu sürümde derlenmiyor |
| `ImportError`, `TypeError`, … | derleniyor ama çalışırken duruyor (ör. 3.8'de `list[str]`) |
| `timeout (no answer)` | `--timeout` süresinde sonuç yok; uyumsuzluk kanıtı **değil** |

## Proje Yapısı
```text
50_version_matrix/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.8 veya üstü (araç kendini `--args=--help` ile 3.8, 3.9 ve 3.15'te denedi; vermin 3.7 diyor). Yalnızca standart kütüphane.
- Docker. İmajlar ilk kullanımda indirilir (her biri diskte yaklaşık 120 MB).

## Kullanım
```bash
python3 main.py ../38_regex_validation
python3 main.py ../37_argparse_cli --args=--help
python3 main.py ../26_multiprocessing_vs_threading --versions 3.9,3.10 --timeout 600 -v
```

- `--versions` virgülle ayrılmış imaj etiketleri (varsayılan `3.8,…,3.15`; `3.15-rc` de olur)
- `--timeout` her çalıştırma için saniye (varsayılan 300)
- `--args` her `main.py`'ye geçirilen argümanlar
- `-v` ham hata satırını da gösterir

## Örnek Çıktı (Python 3.12.3 ana makine, Docker imajları 3.8–3.15.2)
```text
== 32_data_structures_bin_tree ==
  3.8    ImportError
  3.9    ImportError
  3.10   ImportError
  3.11   ok
  3.12   ok
  3.13   ok
  3.14   ok
  3.15   ok
  lowest version that runs: 3.11

== 24_advanced_type_hinting ==
  3.8    SyntaxError
  3.9    SyntaxError
  3.10   SyntaxError
  3.11   SyntaxError
  3.12   ok
  3.13   ok
  3.14   ok
  3.15   ok
  lowest version that runs: 3.12
```

## Sınırlamalar
- **"ok", "doğru" demek değil.** Araç yalnızca çıkış koduna bakar. 29 numaralı proje her sürümde 0 ile çıkıyor, ama Türkçe yerel ayarlı bir bilgisayarda Python 3.11 ve 3.12 yanlış veri bırakıyor (imajların yerel ayarı `C.UTF-8`). 26 numaralı proje ağ olmadan da 0 ile çıkıyor, çünkü her hatayı "404"e çeviriyor. Doğruluk gerekiyorsa projenin kendi testlerini her sürümde çalıştırın.
- **Üçüncü taraf paketler kurulmaz.** Bu tür projelerde paketleri konteynerin içinde kendiniz kurun. pip'in eski Python'da sessizce eski paket sürümü seçtiğini unutmayın (30 numaralı proje 3.8'de fastapi 0.124.4 ile çalıştı).
- Etkileşimli betikler kapalı bir stdin alır. Grafik arayüzlü programlar ve sunucular ayrı hazırlık ister.
- Aracın ilk sürümü klasörü kopyalamadan salt okunur bağlıyordu (29 "unable to open database file" ile düştü) ve 60 saniyelik bir sınır kullanıyordu (26, 3.8 ve 3.9'da zaman aşımına uğradı; oysa yalnızca daha yavaş çalışıyor: 3.9'da 79 sn). İkisi de düzeltildi. Kopyalama adımı ve "no answer" ifadesi bu yüzden var.

## Statik Kontrol
[vermin](https://github.com/netromdk/vermin), kodu çalıştırmadan en düşük sürümü tahmin eder. Buradaki projelerin hepsinde matrisle aynı sonucu verdi, 41 hariç: Python 3.12'de çalıştığı için 3.15 sözdizimini ayrıştıramıyor ve "~2, ~3" diyor.
```bash
pip install vermin
vermin --no-tips --eval-annotations main.py
```

## Bağlantılar
- Blog yazısı: https://gurmezin.com/2026/11/12/python-3-12-gerekir-dogru-mu-surum-iddialarini-dockerda-sinadik/
- Python sürümlerinin durumu: https://devguide.python.org/versions/

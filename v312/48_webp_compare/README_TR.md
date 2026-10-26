# Proje 48: WebP Karşılaştırma — Dönüştürmeden Önce Ölçün

Bir klasördeki her PNG/JPG dosyasını bellekte WebP'ye çevirir ve bir tablo yazar: özgün boyut, iki kalite ayarında kayıplı WebP (varsayılan q85 ve q75), kayıpsız WebP ve özgün görüntüye göre **PSNR** (dB; yüksek = kaynağa daha yakın). Aynı adlı bir PNG ve JPG varsa PNG kaynak kabul edilir, JPG de ona göre ölçülür. `--save` verilmedikçe diske hiçbir şey yazılmaz.

Bu araç, gurmezin.com'daki Ekim 2026 görsellerini WebP'ye çevirmeden önce yaptığımız ölçümden çıktı.

## Proje Yapısı
```text
48_webp_compare/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü ve Pillow (`pip install pillow`; Ubuntu'da `sudo apt install python3-pil`). Python 3.12.3 + Pillow 10.2.0 (Ubuntu 24.04) ve Docker `python:3.9-slim` + pip ile kurulan Pillow ile test edildi.
- numpy gerekmez; PSNR, Pillow'un `ImageChops` ve `ImageStat` modülleriyle hesaplanır.

## Çalıştırma
```bash
python3 main.py --demo                     # düz grafik ve fotoğraf benzeri görüntü
python3 main.py ./gorseller                # klasörü ölç
python3 main.py ./gorseller --quality 80   # farklı kalite
python3 main.py ./gorseller --save         # yanlarına .webp dosyalarını da yaz
```

## Örnek Çıktı: Demo
```text
Demo (JPG = quality 90; original = optimized PNG)

image                               original             JPG        WebP q85        WebP q75  lossless
demo: flat graphic                     13059   42850  37.7dB    8556  37.6dB    7242  37.3dB      1822
demo: photo-like                      494541  154146  49.5dB   54706  42.8dB   30080  40.7dB    337336

total JPG (or original): 196996 bytes, WebP q85: 63262 bytes (32%), lossless: 339158 bytes (172%)
```
Düz grafikte kayıpsız WebP en küçük dosya. Fotoğraf benzeri görüntüde ise JPG'nin iki katından büyük. Kalite ayarları biçimler arasında karşılaştırılamaz: JPG q90 ile WebP q85 aynı PSNR'ı vermez. (Kayıpsız boyut libwebp sürümüne göre birkaç bayt değişebilir.)

## Örnek Çıktı: gurmezin.com Ekim 2026 görselleri
```text
image                               original             JPG        WebP q85        WebP q75  lossless
claude-otomasyon-readme-bakimi.png    125406  137019  34.9dB   53334  35.0dB   40126  34.4dB     92716
claude-otomasyon-yayin-hatti.png      135912  131542  35.6dB   48924  35.6dB   36556  34.9dB    100182
dogru-gorunen-kod-yanlis-sonuc.png    133840  136922  34.5dB   52728  34.6dB   39654  34.0dB     97554
eylul-2026-yapay-zeka.png             160839  118599  36.2dB   48280  36.3dB   36270  35.3dB    109242
python-315-yenilikler.png             143438  134572  35.9dB   50318  35.8dB   37260  35.1dB    102720
python-dataclasses.png                140705  130739  34.6dB   50940  34.6dB   38412  34.1dB    100542
python-dekoratorler.png               149146  121580  35.9dB   45878  35.9dB   33948  35.2dB    105990

total JPG (or original): 910973 bytes, WebP q85: 350402 bytes (38%), lossless: 708946 bytes (78%)
```
Aynı kaynak PNG'den üretilen WebP q85, JPG ile aynı PSNR'ı dosya boyutunun %38'iyle veriyor. Yayındaki JPG'lerden dönüştürmek daha kötü sonuç veriyor: toplam 359 KB ve ortalama 33.8 dB (PNG'den: 350 KB ve 35.4 dB).

## Sınırlamalar
- PSNR basit bir piksel farkı ölçüsüdür, algılanan kaliteyi tam yansıtmaz. Aynı görüntünün farklı biçimlerini karşılaştırmak için yeterli, farklı görüntüleri karşılaştırmak için değil.
- Saydamlık (alfa kanalı) RGB'ye çevrilirken atılır.
- WordPress gibi sistemler küçük kopyaları kendi kalite ayarlarıyla yeniden üretir; buradaki oran yalnızca tam boyutlu dosya içindir.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/05/claude-ile-otomasyon-5-ekim-gorsellerini-webpye-cevirdik/
- Pillow WebP seçenekleri: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
- Google WebP sıkıştırma çalışması: https://developers.google.com/speed/webp/docs/webp_study

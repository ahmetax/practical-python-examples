# Project 48: WebP Compare — Measure Before You Convert

Converts every PNG/JPG in a folder to WebP in memory and prints a table: original size, lossy WebP at two qualities (default q85 and q75), lossless WebP, and **PSNR** against the original (dB; higher = closer to the source). When a PNG and a JPG share a name, the PNG is taken as the reference and the JPG is measured against it too. Nothing is written to disk unless `--save` is given.

This tool came out of the measurements we made before converting the October 2026 images on gurmezin.com to WebP.

## Project Structure
```text
48_webp_compare/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer and Pillow (`pip install pillow`; on Ubuntu `sudo apt install python3-pil`). Tested with Python 3.12.3 + Pillow 10.2.0 (Ubuntu 24.04) and Docker `python:3.9-slim` with Pillow from pip.
- No numpy; PSNR is computed with Pillow's `ImageChops` and `ImageStat`.

## Running
```bash
python3 main.py --demo                     # a flat graphic and a photo-like image
python3 main.py ./images                   # measure a folder
python3 main.py ./images --quality 80      # different quality
python3 main.py ./images --save            # also write .webp files next to them
```

## Sample Output: Demo
```text
Demo (JPG = quality 90; original = optimized PNG)

image                               original             JPG        WebP q85        WebP q75  lossless
demo: flat graphic                     13059   42850  37.7dB    8556  37.6dB    7242  37.3dB      1822
demo: photo-like                      494541  154146  49.5dB   54706  42.8dB   30080  40.7dB    337336

total JPG (or original): 196996 bytes, WebP q85: 63262 bytes (32%), lossless: 339158 bytes (172%)
```
For the flat graphic, lossless WebP is the smallest file. For the photo-like image it is more than twice the JPG. Quality settings are not comparable across formats: JPG q90 and WebP q85 do not give the same PSNR. (Lossless sizes may differ by a few bytes between libwebp versions.)

## Sample Output: gurmezin.com October 2026 images
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
WebP q85 made from the same source PNG matches the JPG's PSNR at 38% of the file size. Converting the published JPGs instead gives a worse result: 359 KB in total and 33.8 dB on average (from PNG: 350 KB and 35.4 dB).

## Limitations
- PSNR is a simple pixel-difference measure and does not fully reflect perceived quality. It is good enough for comparing formats of the same image, not for comparing different images.
- Transparency (alpha) is dropped when converting to RGB.
- Systems such as WordPress regenerate smaller copies with their own quality settings; the ratio here applies to the full-size file only.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/05/claude-ile-otomasyon-5-ekim-gorsellerini-webpye-cevirdik/
- Pillow WebP options: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
- Google WebP compression study: https://developers.google.com/speed/webp/docs/webp_study

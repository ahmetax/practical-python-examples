# Author: Ahmet Aksoy & Claude
# Date: 26.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.9+ and Pillow

"""
WebP Compare: Measure Before You Convert
Converts every PNG/JPG in a folder to WebP in memory and prints a table:
original size, lossy WebP at two qualities, lossless WebP, and PSNR (dB)
against the original. When a PNG and a JPG share a name, the PNG is taken as
the reference and the JPG is measured against it too. Nothing is written
unless --save is given.

    python3 main.py <folder> [--quality 85] [--save]
    python3 main.py --demo      # a flat graphic and a photo-like image
"""
import io
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat


def psnr(a: Image.Image, b: Image.Image) -> float:
    """Peak signal-to-noise ratio of two RGB images (higher = closer)."""
    diff = ImageChops.difference(a, b)
    mse = sum(ImageStat.Stat(diff).sum2) / (3 * a.width * a.height)
    return math.inf if mse == 0 else 10 * math.log10(255 ** 2 / mse)


def encode(img: Image.Image, fmt: str, **options) -> tuple:
    """Return (size in bytes, decoded image) for img saved as fmt."""
    buf = io.BytesIO()
    img.save(buf, fmt, **options)
    size = buf.tell()
    buf.seek(0)
    return size, Image.open(buf).convert("RGB")


def measure(name: str, ref: Image.Image, ref_bytes: int, jpg: Path = None, quality: int = 85) -> dict:
    row = {"name": name, "ref": ref_bytes}
    if jpg:
        row["jpg"] = jpg.stat().st_size
        row["jpg_psnr"] = psnr(ref, Image.open(jpg).convert("RGB"))
    for key, options in [("webp", {"quality": quality}), ("webp75", {"quality": 75}),
                         ("lossless", {"lossless": True})]:
        size, decoded = encode(ref, "WEBP", method=6, **options)
        row[key], row[key + "_psnr"] = size, psnr(ref, decoded)
    return row


def print_table(rows: list, quality: int) -> None:
    print(f"{'image':<34} {'original':>9} {'JPG':>15} {f'WebP q{quality}':>15} {'WebP q75':>15} {'lossless':>9}")
    for r in rows:
        jpg = f"{r['jpg']:>7} {r['jpg_psnr']:>5.1f}dB" if "jpg" in r else f"{'-':>15}"
        print(f"{r['name'][:34]:<34} {r['ref']:>9} {jpg} "
              f"{r['webp']:>7} {r['webp_psnr']:>5.1f}dB {r['webp75']:>7} {r['webp75_psnr']:>5.1f}dB {r['lossless']:>9}")
    base = sum(r.get("jpg", r["ref"]) for r in rows)
    print(f"\ntotal JPG (or original): {base} bytes, WebP q{quality}: {sum(r['webp'] for r in rows)} bytes "
          f"({sum(r['webp'] for r in rows) / base:.0%}), lossless: {sum(r['lossless'] for r in rows)} bytes "
          f"({sum(r['lossless'] for r in rows) / base:.0%})")


def scan(folder: Path, quality: int, save: bool) -> list:
    rows = []
    for path in sorted(folder.iterdir()):
        suffix = path.suffix.lower()
        if suffix == ".png" or (suffix in (".jpg", ".jpeg") and not path.with_suffix(".png").exists()):
            ref = Image.open(path).convert("RGB")
            jpg = path.with_suffix(".jpg") if suffix == ".png" and path.with_suffix(".jpg").exists() else None
            rows.append(measure(path.name, ref, path.stat().st_size, jpg, quality))
            if save:
                ref.save(path.with_suffix(".webp"), "WEBP", quality=quality, method=6)
    return rows


def demo_images() -> list:
    """A flat 'blog card' graphic and a noisy photo-like image, both 1200x900."""
    random.seed(1)
    card = Image.new("RGB", (1200, 900), (12, 24, 52))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([150, 120, 1050, 260], radius=24, fill=(30, 50, 100), outline=(255, 212, 59), width=4)
    for i in range(5):
        d.rounded_rectangle([150, 330 + i * 90, 1050, 394 + i * 90], radius=12, fill=(20, 34, 70))
        d.text((180, 350 + i * 90), f"row {i}: says OK / really NOT OK", fill=(240, 244, 255))
    photo = Image.effect_noise((1200, 900), 40).convert("RGB")
    photo = Image.blend(photo, Image.linear_gradient("L").resize((1200, 900)).convert("RGB"), 0.6)
    photo = photo.filter(ImageFilter.GaussianBlur(1.2))
    return [("demo: flat graphic", card), ("demo: photo-like", photo)]


def main() -> None:
    args = sys.argv[1:]
    quality = int(args[args.index("--quality") + 1]) if "--quality" in args else 85
    if "--demo" in args or not args:
        rows = []
        for name, img in demo_images():
            png_bytes, png = encode(img, "PNG", optimize=True)
            row = measure(name, png, png_bytes, quality=quality)
            row["jpg"], decoded = encode(png, "JPEG", quality=90)
            row["jpg_psnr"] = psnr(png, decoded)
            rows.append(row)
        print("Demo (JPG = quality 90; original = optimized PNG)\n")
        print_table(rows, quality)
        return
    folder = Path(args[0])
    if not folder.is_dir():
        sys.exit(f"not a folder: {folder}")
    rows = scan(folder, quality, "--save" in args)
    if not rows:
        sys.exit(f"no PNG/JPG files in {folder}")
    print_table(rows, quality)


if __name__ == "__main__":
    main()

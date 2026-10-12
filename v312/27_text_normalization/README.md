# Project 27: Text Normalization and the Turkish I Problem

A small text-cleaning example in pure Python. It lowercases text with Turkish rules, removes punctuation and digits with `re.sub()`, and collapses repeated whitespace into single spaces.

## How It Works
- **`turkish_lower(text)`**: Python's `str.lower()` follows Unicode default rules, not Turkish ones. It turns `I` into `i` (Turkish expects `ı`) and turns `İ` into `i` plus a combining dot (U+0307), so `"İSTANBUL".lower()` is 9 characters long instead of 8. The function replaces `İ` with `i` and `I` with `ı` first, then calls `.lower()` for the remaining letters.
- **`turkish_upper(text)`**: The reverse direction. It replaces `i` with `İ` before calling `.upper()`. (The `ı` → `I` replacement in it is harmless but redundant: `"ı".upper()` already returns `I`.) The demo does not call this function.
- **`normalize_text(raw_text, remove_digits=False)`**:
  1. lowercases with `turkish_lower()`,
  2. removes every character that is not a word character or whitespace (`[^\w\s]`); with `remove_digits=True` it also removes digits (`\d`),
  3. replaces runs of spaces, tabs and newlines with a single space and strips the ends.

Things to keep in mind:
- `\w` includes the underscore, so `Ahmet_Dev123` becomes `ahmet_dev`, not `ahmetdev`.
- `turkish_lower()` applies Turkish rules to every input. English text with a capital `I` changes too: `"ISSUE"` becomes `"ıssue"`.
- `re.UNICODE` is already the default for `str` patterns in Python 3; the flag in the code changes nothing.

## Project Structure
```text
27_text_normalization/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3. The code uses only the standard library `re` module and f-strings; nothing in it needs 3.12. Tested on Python 3.12.3 (Ubuntu 24.04).
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
=== Testing Standard vs Custom Lowercasing ===
Original       : İSTANBUL IŞIKLARI
Naive .lower() : i̇stanbul işiklari  <- (Broken: notice the 'i' and 'ı' collision)
Custom Lower   : istanbul ışıkları  <- (Correctly preserved linguistic shapes)
------------------------------------------------------------

=== Running Comprehensive Pipeline ===
Raw Input : İSTANBUL, ISPARTA ve İZMİR şehirleri incelendi.
Normalized: istanbul ısparta ve izmir şehirleri incelendi
------------------------------------------------------------
Raw Input : Kullanıcı Adı: 'Ahmet_Dev123' - Giriş Tarihi: 2026!
Normalized: kullanıcı adı ahmet_dev giriş tarihi
------------------------------------------------------------
Raw Input : ılık su ile İYİCE yıkanmış,   temiz bir   yüzey.
Normalized: ılık su ile iyice yıkanmış temiz bir yüzey
------------------------------------------------------------
Raw Input : Mojo & Python dillerinin kararlılığı %100 test edildi.
Normalized: mojo python dillerinin kararlılığı test edildi
------------------------------------------------------------
```
In the `Naive .lower()` line the first `i` carries an extra combining dot (U+0307); depending on your terminal font it may look like a plain `i`.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/20/python-ile-metin-normalizasyonu-turkce-karakter-tuzaklarindan-kurtulun/
- `re` documentation: https://docs.python.org/3/library/re.html
- `str.lower()` documentation: https://docs.python.org/3/library/stdtypes.html#str.lower

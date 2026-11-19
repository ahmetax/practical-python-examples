# Project 56: Turkish İ and ı: Testing Functions Claude Wrote

Claude (Claude Code 2.1.328, `claude-opus-5-5`, tools off) was asked five times each for twelve small Turkish text tasks: uppercasing, alphabetical sorting, case-insensitive comparison, slug, title case, word count, prefix search, username. The 60 answers passed 260 of 260 tests over three rounds. When the same text was given in decomposed (NFD) Unicode, `baslik_yap` (title case) returned `İzmı̇r` instead of `İzmir` in 10 of 10 answers: in the sequence `I` + U+0307 the `I` becomes `ı` when lowercased, and the combining dot stays on top of it.

This script embeds one answer per task (not all 60; the rest are in the blog post's folder). It runs 13 plain and 4 decomposed-input tests, then applies a one-line NFC fix to `baslik_yap`.

| Check | Tests | Passed |
|---|---|---|
| Round 1: prompt says "Turkish" (5 tasks) | 115 | 115 |
| Round 2: only Turkish example data (4 tasks) | 90 | 90 |
| Round 3: Turkish is a side issue (3 tasks) | 55 | 55 |
| Decomposed `İ`: `buyuk_harf`, `esles`, `slug` | 25 | 25 |
| Decomposed `İ`: `baslik_yap` | 10 | 0 |

## How It Works
- Each answer is loaded with `exec` in its own namespace; inputs are passed as a `deepcopy`, and exceptions are shown as results.
- Expected values follow Turkish rules. The most debatable one: `esles("ISPARTA", "isparta")` is expected to be `False`, because `ı` and `i` are different letters in Turkish.
- The decomposed test splits the same text with `unicodedata.normalize("NFD", ...)` and converts the output back to NFC before comparing.
- `duzelt_baslik` adds `unicodedata.normalize("NFC", metin)` at the top of the function.

## Limits
- One model, one version; a prompt with no hint at all was not tried.
- The decomposed check covers only four functions from rounds 1 and 2.
- Expected values are the author's choices; one round-3 test (the count of `izmir`) was written wrongly and removed.

## Project Structure
```text
56_turkish_i_pitfalls/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer. Tested with Python 3.12.3 and, in Docker, 3.9 and 3.14; same output.
- No third-party packages.

## Usage
```bash
python3 main.py
```

## Example Output (Python 3.12.3)
```text
Düz (NFC) girdi:
  GEÇTİ  buyuk_harf  i -> İ
  GEÇTİ  buyuk_harf  ı -> I
  GEÇTİ  buyuk_harf  karışık
  GEÇTİ  sirala      alfabe sırası
  GEÇTİ  sirala      boş liste
  GEÇTİ  esles       İSTANBUL ~ istanbul
  GEÇTİ  esles       ISPARTA ~ ısparta
  GEÇTİ  esles       ISPARTA !~ isparta
  GEÇTİ  slug        İstanbul Işık Şöleni
  GEÇTİ  slug        ÇIĞLIK
  GEÇTİ  baslik_yap  ısparta ılık
  GEÇTİ  baslik_yap  İZMİR IŞIK
  GEÇTİ  baslik_yap  iNEK
  13/13

Ayrışık (NFD) girdi:
  GEÇTİ  buyuk_harf  'İzmir ışık'
  GEÇTİ  esles       'İZMİR'
  GEÇTİ  slug        'İzmir Işık'
  KALDI  baslik_yap  'İZMİR'  -> 'İzmı̇r'

baslik_yap + NFC düzeltmesi:
  'İzmir'  (GEÇTİ)
```

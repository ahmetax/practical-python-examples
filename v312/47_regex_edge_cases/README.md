# Project 47: Regex Edge Cases — What Does a Validator Actually Accept?

We ran the email, phone and password patterns from project 38 against edge cases. In four places the pattern did something other than what it was written for. This project shows each case twice: the original pattern (**says**) and a fixed version (**checks**).

| # | Problem | Sample input | Check |
|---|---------|--------------|-------|
| 1 | `re.match` + `$` allows a trailing newline | `'a@x.com\n'` | `re.fullmatch` (or `\Z`) |
| 2 | `\d` matches every Unicode digit | `'5٥٥١٢٣٤٥٦٧'` | `[0-9]` or `re.ASCII` |
| 3 | `\s` also matches newlines and NBSP | `'0555\n123\n45\n67'` | normalize first, then full match with `[0-9]` |
| 4 | `[A-Z]` / `[a-z]` miss Turkish letters; `re.I` only adds `ı İ ſ K` | `'Şifre123!x'` | `str.isupper()`, `str.islower()`, `str.isalnum()` |

## Project Structure
```text
47_regex_edge_cases/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer. Tested on Python 3.12.3 (Ubuntu 24.04, `tr_TR.UTF-8`) and in Docker with `python:3.9-slim`, `3.13-slim`, `3.15-rc-slim` (`LC_ALL=C.UTF-8`); output is identical apart from the version line.
- No third-party packages, network or files (`sqlite3` runs in memory).

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3, Ubuntu 24.04)
```text
Python 3.12.3

== 1. '$' and a trailing newline ==
  'a@x.com'            says True   checks True
  'a@x.com\n'          says True   checks False
  'a@x.com\n\n'        says False  checks False
  says                 2 accounts for one address (UNIQUE did not help)
  checks               1 account

== 2. '\d' and Unicode digits ==
  input                '5٥٥١٢٣٤٥٦٧'  (Arabic-Indic digits)
  says                 ('5٥٥', '١٢٣', '٤٥', '٦٧')
  checks               None
  int()                5551234567  -> looks the same after conversion
  ==                   False  -> but not as text
  ascii                UnicodeEncodeError at position 1

== 3. '\s' is more than a space ==
  '0555 123 45 67'     says ('555', '123', '45', '67') checks ('555', '123', '45', '67')
  '0555\n123\n45\n67'  says ('555', '123', '45', '67') checks None
  '0555\xa0123\xa045\xa067' says ('555', '123', '45', '67') checks None
  '5551234567\n'       says ('555', '123', '45', '67') checks None

== 4. '[A-Z]' and Turkish letters ==
  Şifre123!x           says ['uppercase']              checks STRONG
  çğışöü12!A           says ['lowercase']              checks STRONG
  Passw0rd#            says ['special']                checks STRONG
  re.I                 [a-z] matches 'ıİſK' of 'ıİşŞğĞçÇöÖüÜſK'
```
- In section 1 the address with two trailing newlines is rejected even by the original pattern: `$` skips only **one** trailing newline.
- In section 2 `int()` silently turns the Arabic-Indic digits into 5551234567, while text comparison and ASCII encoding fail.
- The digit rule in section 4 deliberately allows Unicode digits (`isdecimal()`). Unlike a phone number, a password is not passed on to another system.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/02/regex-neyi-kabul-ediyor-turkce-harf-arapca-rakam-gorunmeyen-satir-sonu/
- Original code: 38_regex_validation in this repository
- `re` documentation: https://docs.python.org/3/library/re.html
- NIST SP 800-63B-4 (composition rules and Unicode passwords): https://pages.nist.gov/800-63-4/sp800-63b.html

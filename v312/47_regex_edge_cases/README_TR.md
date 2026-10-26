# Proje 47: Regex Kenar Durumları — Doğrulayıcı Gerçekte Neyi Kabul Ediyor?

38 numaralı projedeki e-posta, telefon ve şifre desenlerini kenar durumlarla çalıştırdık. Dört yerde desen, yazıldığı niyetten farklı bir şey yapıyordu. Bu proje her örneği iki kez gösteriyor: özgün desen (**says**) ve düzeltilmiş sürüm (**checks**).

| # | Sorun | Örnek girdi | Kontrol |
|---|-------|-------------|---------|
| 1 | `re.match` + `$` sondaki satır sonuna izin veriyor | `'a@x.com\n'` | `re.fullmatch` (ya da `\Z`) |
| 2 | `\d` her Unicode rakamıyla eşleşiyor | `'5٥٥١٢٣٤٥٦٧'` | `[0-9]` ya da `re.ASCII` |
| 3 | `\s` satır sonu ve NBSP ile de eşleşiyor | `'0555\n123\n45\n67'` | önce sadeleştir, sonra `[0-9]` ile tam eşleşme |
| 4 | `[A-Z]` / `[a-z]` Türkçe harfleri tanımıyor; `re.I` yalnızca `ı İ ſ K` ekliyor | `'Şifre123!x'` | `str.isupper()`, `str.islower()`, `str.isalnum()` |

## Proje Yapısı
```text
47_regex_edge_cases/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü. Python 3.12.3 (Ubuntu 24.04, `tr_TR.UTF-8`) ile ve Docker'da `python:3.9-slim`, `3.13-slim`, `3.15-rc-slim` (`LC_ALL=C.UTF-8`) ile test edildi; çıktı sürüm satırı dışında aynı.
- Üçüncü taraf paket, internet bağlantısı ya da dosya gerekmez (`sqlite3` bellekte çalışır).

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3, Ubuntu 24.04)
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
- 1. bölümde iki satır sonu olan adres özgün desenle de reddediliyor: `$` yalnızca **tek** bir sondaki satır sonunu atlıyor.
- 2. bölümde `int()` Arapça rakamları sessizce 5551234567'ye çeviriyor; metin karşılaştırması ve ASCII kodlaması ise başarısız oluyor.
- 4. bölümdeki rakam kuralı bilerek Unicode rakamlara izin veriyor (`isdecimal()`). Telefon numarasından farklı olarak şifre başka bir sisteme gönderilmiyor.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/02/regex-neyi-kabul-ediyor-turkce-harf-arapca-rakam-gorunmeyen-satir-sonu/
- Özgün kod: bu depodaki 38_regex_validation
- `re` belgeleri: https://docs.python.org/3/library/re.html
- NIST SP 800-63B-4 (bileşim kuralları ve Unicode şifreler): https://pages.nist.gov/800-63-4/sp800-63b.html

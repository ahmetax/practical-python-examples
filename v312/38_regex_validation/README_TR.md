# Proje 38: Regex ile E-posta, Telefon ve Şifre Doğrulama

Standart `re` modülüyle yazılmış, her biri birkaç örnek girdiyle denenen üç küçük doğrulayıcı:

| # | Doğrulayıcı | Yöntem |
|---|-------------|--------|
| 1 | E-posta adresi biçimi | `re.match()` ile tek bir çapalı (anchored) desen |
| 2 | Türkiye cep telefonu numarası ve parçalarına ayrılması | İsteğe bağlı önek `(?:\+90\|0)?`, yakalama grupları ve `match.groups()` |
| 3 | Şifre gücü, başarısız olan her kuralın listesiyle | Ayrı ayrı `re.search()` kontrolleri ve uzunluk kontrolü |

## Nasıl Çalışır?
- **E-posta:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` deseni bir kullanıcı adı, bir `@`, bir alan adı ve en az iki harfli bir üst düzey alan adı ister.
- **Telefon:** `^(?:\+90|0)?\s?([5]\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$` deseni isteğe bağlı `+90` veya `0` önekini ve bloklar arasında isteğe bağlı tek boşluğu kabul eder. Numara `5` ile başlamak zorunda olduğu için yalnızca cep telefonları geçer; `0212 123 45 67` gibi sabit hat numaraları reddedilir. Dört yakalama grubu düzenli bir biçimde yazdırılır. Çıktıda `Area` olarak etiketlenen ilk grup aslında operatör önekidir.
- **Şifre:** Birbirinden bağımsız beş kontrol yapılır: en az 8 karakter, bir büyük harf `[A-Z]`, bir küçük harf `[a-z]`, bir rakam `\d` ve `@$!%*?&` karakterlerinden biri. Başarısız olan her kontrol bir listede toplanır; böylece kullanıcı tüm sorunları tek seferde görür.

## Sınırlamalar
Bu desenler öğretim amaçlıdır ve göründüklerinden daha gevşek ya da daha katıdır:
- `$` sondaki satır sonu karakterinin hemen önünde de eşleşir; bu yüzden `"a@x.com\n"` geçerli e-posta sayılır. `re.fullmatch()` veya `\Z` bu açığı kapatır.
- E-posta deseni `a..b@x.com`, `.a@x.com` ve `a@x..com` gibi adresleri de kabul eder; `user@örnek.com` gibi ASCII dışı alan adlarını ise reddeder.
- `[A-Z]` yalnızca ASCII harfleri kapsar; bu yüzden `Şifre123!x` şifresi için "büyük harf yok" denir.
- `@$!%*?&` dışındaki özel karakterler sayılmaz: `Passw0rd#` reddedilir.
- Python'da `\d` her Unicode rakamıyla eşleşir; bu yüzden `5٥٥١٢٣٤٥٦٧` (Arap-Hint rakamları) telefon numarası olarak kabul edilir. Yalnızca 0–9'a izin vermek için `[0-9]` ya da `re.ASCII` bayrağını kullanın.

## Proje Yapısı
```text
38_regex_validation/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü (`list[str]` dönüş tipi gösterimi). Python 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Advanced Regular Expression Engine Initialized ---

=== 1. Email Pattern Ingestion ===
 -> Address [ahmet.aksoy@example.com]: VALID
 -> Address [invalid-email@domain]: INVALID
 -> Address [@missing-user.com]: INVALID
 -> Address [user@com]: INVALID
-----------------------------------------------------------------

=== 2. Phone Layout Mining & Normalization ===
 -> Parsing [+905551234567]:
   [Sanitized Output] Extracted -> Area: (555) Number: 123-45-67
 -> Parsing [0532 987 65 43]:
   [Sanitized Output] Extracted -> Area: (532) Number: 987-65-43
 -> Parsing [4440333]:
   [Result] Format Violation Detected.
 -> Parsing [5051112233]:
   [Sanitized Output] Extracted -> Area: (505) Number: 111-22-33
-----------------------------------------------------------------

=== 3. Password Security Assertions ===
 -> Password [12345]: WEAK / REJECTED
    x Fail Reason: Minimum length must be at least 8 characters.
    x Fail Reason: Must contain at least one uppercase letter [A-Z].
    x Fail Reason: Must contain at least one lowercase letter [a-z].
    x Fail Reason: Must contain at least one special character [@$!%*?&].
 -> Password [SecurePass123!]: STRONG / APPROVED
 -> Password [onlylowercase]: WEAK / REJECTED
    x Fail Reason: Must contain at least one uppercase letter [A-Z].
    x Fail Reason: Must contain at least one numerical digit [0-9].
    x Fail Reason: Must contain at least one special character [@$!%*?&].
 -> Password [UPPERCASE123]: WEAK / REJECTED
    x Fail Reason: Must contain at least one lowercase letter [a-z].
    x Fail Reason: Must contain at least one special character [@$!%*?&].
-----------------------------------------------------------------
```

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/21/pythonda-regex-sinir-bekciligi-e-posta-telefon-ve-sifre-dogrulama/
- `re` belgeleri: https://docs.python.org/3/library/re.html

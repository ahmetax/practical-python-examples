# Project 38: Validating Email, Phone and Password Input with Regex

Three small validators built with the standard `re` module, each run against a handful of sample inputs:

| # | Validator | Technique |
|---|-----------|-----------|
| 1 | Email address format | One anchored pattern with `re.match()` |
| 2 | Turkish mobile phone number, split into parts | Optional prefix `(?:\+90\|0)?`, capture groups and `match.groups()` |
| 3 | Password strength, listing every failed rule | Separate `re.search()` checks plus a length check |

## How It Works
- **Email:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` requires a local part, an `@`, a domain and a top-level domain of at least two letters.
- **Phone:** `^(?:\+90|0)?\s?([5]\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$` accepts an optional `+90` or `0` prefix and optional single spaces between the blocks. The number must start with `5`, so only mobile numbers pass; a landline such as `0212 123 45 67` is rejected. The four capture groups are printed in a normalized form. The first group (labelled `Area` in the output) is really the mobile operator prefix.
- **Password:** five independent checks: at least 8 characters, an uppercase letter `[A-Z]`, a lowercase letter `[a-z]`, a digit `\d` and one of the special characters `@$!%*?&`. Every failed check is collected in a list, so the user sees all problems at once instead of one at a time.

## Limitations
These patterns are meant for teaching and are looser or stricter than they look:
- `$` also matches just before a trailing newline, so `"a@x.com\n"` is accepted as a valid email. `re.fullmatch()` or `\Z` would close this gap.
- The email pattern also accepts addresses such as `a..b@x.com`, `.a@x.com` and `a@x..com`, and rejects non-ASCII domains such as `user@örnek.com`.
- `[A-Z]` only covers ASCII letters, so the password `Şifre123!x` is reported as having no uppercase letter.
- Special characters outside `@$!%*?&` do not count: `Passw0rd#` is rejected.
- In Python, `\d` matches any Unicode digit, so `5٥٥١٢٣٤٥٦٧` (Arabic-Indic digits) passes as a phone number. Use `[0-9]` or the `re.ASCII` flag to allow only 0–9.

## Project Structure
```text
38_regex_validation/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (the `list[str]` return annotation). Tested on 3.12.3.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
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

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/09/21/pythonda-regex-sinir-bekciligi-e-posta-telefon-ve-sifre-dogrulama/
- Follow-up on these limitations (Turkish blog post): https://gurmezin.com/2026/11/02/regex-neyi-kabul-ediyor-turkce-harf-arapca-rakam-gorunmeyen-satir-sonu/
- Fixed versions: 47_regex_edge_cases in this repository
- `re` documentation: https://docs.python.org/3/library/re.html

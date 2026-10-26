# Author: Ahmet Aksoy & Claude
# Date: 26.10.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - requires Python 3.9+

"""
Regex Edge Cases: What a Validator Actually Accepts
Four gaps found in project 38 (regex validation), each shown twice: the
original pattern that only *looks* strict and a version that checks what it
claims to check. Standard library only, no network, no files.
"""
import re
import sqlite3
import sys


def show(label: str, value: object) -> None:
    print(f"  {label:<20} {value}")


# --- 1. '$' bir satır sonuna izin verir (e-posta) ---------------------------------
EMAIL_SAYS = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
EMAIL_CHECKS = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def email_says(email: str) -> bool:
    return bool(re.match(EMAIL_SAYS, email))


def email_checks(email: str) -> bool:
    return EMAIL_CHECKS.fullmatch(email) is not None


def register(addresses: list, validate) -> int:
    """Insert every address that passes validation into a UNIQUE column."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (email TEXT UNIQUE)")
    for address in addresses:
        if validate(address):
            try:
                conn.execute("INSERT INTO users VALUES (?)", (address,))
            except sqlite3.IntegrityError:
                pass
    count = conn.execute("SELECT count(*) FROM users").fetchone()[0]
    conn.close()
    return count


def demo_newline() -> None:
    print("== 1. '$' and a trailing newline ==")
    for address in ["a@x.com", "a@x.com\n", "a@x.com\n\n"]:
        show(repr(address), f"says {email_says(address)!s:<6} checks {email_checks(address)}")
    same_user = ["ahmet@gurmezin.com", "ahmet@gurmezin.com\n"]
    show("says", f"{register(same_user, email_says)} accounts for one address (UNIQUE did not help)")
    show("checks", f"{register(same_user, email_checks)} account")


# --- 2. '\d' her Unicode rakamını kabul eder (telefon) ----------------------------
PHONE_SAYS = r"^(?:\+90|0)?\s?([5]\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$"
PHONE_CHECKS = re.compile(r"(?:\+90|0)?(5[0-9]{2})([0-9]{3})([0-9]{2})([0-9]{2})")


def phone_says(phone: str):
    match = re.match(PHONE_SAYS, phone)
    return match.groups() if match else None


def phone_checks(phone: str):
    # Only ordinary spaces are removed on purpose; newlines and NBSP are rejected.
    match = PHONE_CHECKS.fullmatch(phone.replace(" ", ""))
    return match.groups() if match else None


def demo_digits() -> None:
    print("\n== 2. '\\d' and Unicode digits ==")
    arabic = "5٥٥١٢٣٤٥٦٧"
    show("input", f"{arabic!r}  (Arabic-Indic digits)")
    show("says", phone_says(arabic))
    show("checks", phone_checks(arabic))
    show("int()", f"{int(arabic)}  -> looks the same after conversion")
    show("==", f"{arabic == '5551234567'}  -> but not as text")
    try:
        arabic.encode("ascii")
    except UnicodeEncodeError as exc:
        show("ascii", f"UnicodeEncodeError at position {exc.start}")


# --- 3. '\s' yalnızca boşluk değildir (telefon) -----------------------------------
def demo_whitespace() -> None:
    print("\n== 3. '\\s' is more than a space ==")
    cases = ["0555 123 45 67", "0555\n123\n45\n67", "0555 123 45 67", "5551234567\n"]
    for phone in cases:
        show(repr(phone), f"says {phone_says(phone)!s:<26} checks {phone_checks(phone)}")


# --- 4. '[A-Z]' Türkçe harfleri tanımaz (şifre) -----------------------------------
def password_says(password: str) -> list:
    missing = []
    if len(password) < 8:
        missing.append("length")
    if not re.search(r"[A-Z]", password):
        missing.append("uppercase")
    if not re.search(r"[a-z]", password):
        missing.append("lowercase")
    if not re.search(r"\d", password):
        missing.append("digit")
    if not re.search(r"[@$!%*?&]", password):
        missing.append("special")
    return missing


def password_checks(password: str) -> list:
    missing = []
    if len(password) < 8:
        missing.append("length")
    if not any(c.isupper() for c in password):
        missing.append("uppercase")
    if not any(c.islower() for c in password):
        missing.append("lowercase")
    if not any(c.isdecimal() for c in password):
        missing.append("digit")
    if all(c.isalnum() or c.isspace() for c in password):
        missing.append("special")
    return missing


def demo_letters() -> None:
    print("\n== 4. '[A-Z]' and Turkish letters ==")
    for password in ["Şifre123!x", "çğışöü12!A", "Passw0rd#"]:
        says = password_says(password) or "STRONG"
        checks = password_checks(password) or "STRONG"
        show(password, f"says {str(says):<26} checks {checks}")
    letters = "ıİşŞğĞçÇöÖüÜſK"
    matched = "".join(c for c in letters if re.fullmatch(r"[a-z]", c, re.IGNORECASE))
    show("re.I", f"[a-z] matches {matched!r} of {letters!r}")


if __name__ == "__main__":
    print(f"Python {sys.version.split()[0]}\n")
    demo_newline()
    demo_digits()
    demo_whitespace()
    demo_letters()

# Author: Ahmet Aksoy
# Date: 27.05.2026
# Python3.12 Ubuntu 24.04

"""
Advanced Regex Validation Engine
Demonstrates complex text pattern matching, formatting compliance checks, 
and input extraction using Python's native 're' standard library.
"""

import re


def validate_email(email: str) -> bool:
    r"""
    Validates an email address layout using structural boundary tracking.
    Pattern breakdown:
    - ^[a-zA-Z0-9._%+-]+ : Starts with one or more alphanumeric/allowed special chars
    - @                  : Must contain exactly one literal '@' symbol
    - [a-zA-Z0-9.-]+     : Followed by a domain name alphanumeric segment
    - \.[a-zA-Z]{2,}$    : Concludes with a period and at least a 2-character Top-Level Domain
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))


def validate_turkish_phone(phone: str) -> bool:
    """
    Validates Turkish phone numbers (with or without +90/0 prefixes and spaces).
    Matches formats like: +905551234567, 0555 123 45 67, 5551234567
    """
    phone_pattern = r"^(?:\+90|0)?\s?([5]\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$"
    match = re.match(phone_pattern, phone)
    
    if match:
        # Demonstrates how regex groups can extract sanitized segments from raw text
        area_code, part1, part2, part3 = match.groups()
        print(f"   [Sanitized Output] Extracted -> Area: ({area_code}) Number: {part1}-{part2}-{part3}")
        return True
    return False


def assess_password_strength(password: str) -> list[str]:
    """
    Evaluates password security thresholds using multiple targeted lookups.
    Returns a list of missing requirement statements. Secure passwords require:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one numerical digit
    - At least one special character (@$!%*?&)
    """
    failed_criteria = []
    
    if len(password) < 8:
        failed_criteria.append("Minimum length must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        failed_criteria.append("Must contain at least one uppercase letter [A-Z].")
    if not re.search(r"[a-z]", password):
        failed_criteria.append("Must contain at least one lowercase letter [a-z].")
    if not re.search(r"\d", password):
        failed_criteria.append("Must contain at least one numerical digit [0-9].")
    if not re.search(r"[@$!%*?&]", password):
        failed_criteria.append("Must contain at least one special character [@$!%*?&].")
        
    return failed_criteria


if __name__ == "__main__":
    print("--- Advanced Regular Expression Engine Initialized ---\n")

    # 1. Email Verification Testing
    print("=== 1. Email Pattern Ingestion ===")
    emails = ["ahmet.aksoy@example.com", "invalid-email@domain", "@missing-user.com", "user@com"]
    for email in emails:
        status = "VALID" if validate_email(email) else "INVALID"
        print(f" -> Address [{email}]: {status}")
    print("-" * 65)

    # 2. Phone Verification and Data Extraction Testing
    print("\n=== 2. Phone Layout Mining & Normalization ===")
    phone_numbers = ["+905551234567", "0532 987 65 43", "4440333", "5051112233"]
    for phone in phone_numbers:
        print(f" -> Parsing [{phone}]:")
        if not validate_turkish_phone(phone):
            print("   [Result] Format Violation Detected.")
    print("-" * 65)

    # 3. Complex Multi-layered Password Enforcement Testing
    print("\n=== 3. Password Security Assertions ===")
    passwords = ["12345", "SecurePass123!", "onlylowercase", "UPPERCASE123"]
    for pwd in passwords:
        issues = assess_password_strength(pwd)
        if not issues:
            print(f" -> Password [{pwd}]: STRONG / APPROVED")
        else:
            print(f" -> Password [{pwd}]: WEAK / REJECTED")
            for issue in issues:
                print(f"    x Fail Reason: {issue}")
    print("-" * 65)

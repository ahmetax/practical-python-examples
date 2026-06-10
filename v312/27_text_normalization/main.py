# Author: Ahmet Aksoy
# Date: 22.05.2026
# Python3.12 Ubuntu 24.04

"""
Text Normalization and Linguistic Sanitization Example
Demonstrates how to process raw text data, clean special characters using regex,
and properly handle locale-specific casing anomalies (e.g., Turkish I/ı and i/İ)
which frequently break naive string manipulation functions.
"""

import re


def turkish_lower(text: str) -> str:
    """
    Converts a string to lowercase following Turkish linguistic rules.
    Standard Python .lower() converts 'İ' to 'i\u0307' (combining dot) or 'i',
    and incorrectly maps 'I' to 'i' instead of 'ı'.
    """
    # Map capital dotted I (İ) to lowercase dotted i (i)
    text = text.replace("İ", "i")
    # Map capital dotless I (I) to lowercase dotless ı (ı)
    text = text.replace("I", "ı")
    return text.lower()


def turkish_upper(text: str) -> str:
    """
    Converts a string to uppercase following Turkish linguistic rules.
    Standard Python .upper() incorrectly maps 'ı' to 'I' instead of 'I',
    and 'i' to 'I' instead of 'İ'.
    """
    # Map lowercase dotless ı (ı) to capital dotless I (I)
    text = text.replace("ı", "I")
    # Map lowercase dotted i (i) to capital dotted I (İ)
    text = text.replace("i", "İ")
    return text.upper()


def normalize_text(raw_text: str, remove_digits: bool = False) -> str:
    """
    Sanitizes raw text strings by fixing casing anomalies, stripping
    punctuation, normalizing erratic whitespace, and optionally removing digits.
    """
    if not raw_text:
        return ""

    # 1. Apply locale-aware lowercasing
    cleaned = turkish_lower(raw_text)

    # 2. Strip punctuation and structural noise using regular expressions
    # Retains alphanumeric characters and basic space across Unicode ranges
    if remove_digits:
        # Match everything except letters and spaces
        cleaned = re.sub(r"[^\w\s]|\d", "", cleaned, flags=re.UNICODE)
    else:
        # Match everything except letters, digits, and spaces
        cleaned = re.sub(r"[^\w\s]", "", cleaned, flags=re.UNICODE)

    # 3. Collapse multiple consecutive spaces, tabs, or newlines into a single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Text Normalization Engine Started ---\n")

    # Sample texts containing mixed Turkish characters, punctuation, and digits
    sample_phrases = [
        "İSTANBUL, ISPARTA ve İZMİR şehirleri incelendi.",
        "Kullanıcı Adı: 'Ahmet_Dev123' - Giriş Tarihi: 2026!",
        "ılık su ile İYİCE yıkanmış,   temiz bir   yüzey.",
        "Mojo & Python dillerinin kararlılığı %100 test edildi."
    ]

    print("=== Testing Standard vs Custom Lowercasing ===")
    test_word = "İSTANBUL IŞIKLARI"
    print(f"Original       : {test_word}")
    print(f"Naive .lower() : {test_word.lower()}  <- (Broken: notice the 'i' and 'ı' collision)")
    print(f"Custom Lower   : {turkish_lower(test_word)}  <- (Correctly preserved linguistic shapes)")
    print("-" * 60)

    print("\n=== Running Comprehensive Pipeline ===")
    for phrase in sample_phrases:
        print(f"Raw Input : {phrase}")
        print(f"Normalized: {normalize_text(phrase, remove_digits=True)}")
        print("-" * 60)

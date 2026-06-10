# Project 27: Text Normalization & Linguistic Sanitization

A specialized utility project demonstrating how to design and build a clean text-preprocessing pipeline. This framework addresses critical linguistic pitfalls in Natural Language Processing (NLP), such as locale-specific casing conversions (e.g., the Turkish `I/ı` and `i/İ` matrix) and regular expression-driven sanitization.

## Architectural Goal
The system acts as a text normalization layer typical of data pipelines ingestion engines, search indexes, or NLP tokenizers. It accepts messy, user-submitted, or crawled strings and transforms them into standard formats by managing locale casing rules, removing punctuations, and compressing erratic whitespace.

## Project Structure
```text
27_text_normalization/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-based distribution)

Runtime: Python 3.12+

Dependencies: None (Leverages standard library re module)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated folder for your project within your workspace repository:

```bash
mkdir 27_text_normalization
cd 27_text_normalization

### Step 2: Implement the Cleaning Engine
Create a file named main.py. Build your system layer by layer:

Incorporate Locale-Safe Lowercasing: Implement a specialized function (e.g., turkish_lower(text)). Before triggering standard string transformations, explicitly intercept character anomalies via .replace(). Convert capital dotted İ to lowercase dotted i, and capital dotless I to lowercase dotless ı. Follow this pattern to resolve character collisions before calling Python's native .lower().

Incorporate Locale-Safe Uppercasing: Implement a paired function (e.g., turkish_upper(text)). Map lowercase dotless ı to capital dotless I, and lowercase dotted i to capital dotted İ before running the final native .upper() fallback.

Draft the Processing Pipeline: Create a master function normalize_text(raw_text, remove_digits).

Apply your custom lowercasing function first.

Use regular expressions (re.sub()) combined with the re.UNICODE flag to drop punctuation marks. Design a flexible pattern using character sets (like [^\w\s]) to drop punctuation while retaining alphanumeric letters.

Include a flag to cleanly target and eliminate digits (\d) when requested.

Strip trailing spaces and compress structural spacing bugs (multiple spaces, hidden tabs) down to a single space using re.sub(r"\s+", " ", cleaned).

### Step 3: Run and Verify
Add a testing execution sequence at the bottom of main.py using a list of raw string examples that contain mixed Turkish characters, dense punctuation structures, and digits. Execute the script natively to observe the difference between standard and locale-aware normalization:

```bash
python main.py



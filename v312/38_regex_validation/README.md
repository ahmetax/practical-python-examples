# Project 38: Text Pattern Recognition and Validation with Regex

A comprehensive data compliance and text extraction utility engineered using Python's native regular expressions (`re`) engine. This project covers complex pattern matching, input sanitation, group token mining, and multi-layered credential security enforcement.

## Architectural Goal
The system establishes a deterministic boundary guard layer for processing raw inputs. By verifying structure formats (such as formal emails, region-specific telecom routing channels, or algorithmic passkeys) at the application entrance, it prevents corrupted strings from reaching core service layers or polluting data persistence storage layers.

## Project Structure
```text
38_regex_validation/
└── main.py
System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
Step 1: Directory Setup
Create a dedicated project folder structure within your workspace repository:

Bash
mkdir 38_regex_validation
cd 38_regex_validation
Step 2: Implement Regex Rule Definitions
Create a file named main.py. Build your pattern constraints step-by-step using Python's standard re module:

Design an Email Structure Mask: Use anchors (^ for line start, $ for line end) to prevent partial matching. Use character sets ([a-zA-Z0-9._%+-]+) to match allowed email headers, require a literal @ symbol, map domain segments, and mandate a suffix TLD via \.[a-zA-Z]{2,}. Match inputs against this blueprint using re.match().

Design a Telecom Extractor Pattern: Build a flexible pattern using optional non-capturing prefix tokens (?:\+90|0)? alongside conditional spaces \s?. Use structural grouping parentheses () around digits (\d) to isolate Area Codes from local sub-blocks. Access these isolated strings via .groups() to achieve runtime text normalization.

Design Sequential Security Scanners: Instead of one monolithic regex rule, map separate scanning steps using re.search(). Check the string for individual character classes sequentially: [A-Z] for uppercase, [a-z] for lowercase, \d for numeric units, and [@$!%*?&] for cryptographic special flag parameters. Collect failing conditions into an errors array.

Step 3: Run and Verify
Execute your test matrix suite directly via your terminal prompt:

Bash
python3 main.py
Examine the terminal feedback meticulously. Verify that valid emails pass securely, phone variations normalize correctly into standard segments, and weak passwords explicitly list all broken criteria rules before rejection.


---

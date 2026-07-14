# Proje 38: Regex ile Metin Örüntü Tanıma ve Doğrulama

Python'ın yerel düzenli ifadeler (`re`) motoru kullanılarak tasarlanmış kapsamlı bir veri uyumluluğu ve metin çıkarma yardımcı programı. Bu proje, karmaşık örüntü eşleştirme, girdi temizleme (sanitation), grup belirteci madenciliği (group token mining) ve çok katmanlı kimlik bilgisi güvenliği uygulamalarını kapsamaktadır.

## Mimari Hedef
Sistem, ham girdileri işlemek için deterministik bir sınır koruma katmanı oluşturur. Uygulama girişinde yapı formatlarını (örneğin, resmi e-postalar, bölgeye özgü telekom yönlendirme kanalları veya algoritmik geçiş anahtarları) doğrulayarak, bozulmuş dizelerin çekirdek hizmet katmanlarına ulaşmasını veya veri kalıcılık depolama katmanlarını kirletmesini engeller.

## Proje Yapısı
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

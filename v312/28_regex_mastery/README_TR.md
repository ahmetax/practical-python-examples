# Proje 28: Regex Uzmanlığı ve Log Ayrıştırma Motoru

Python'ın standart `re` motoru aracılığıyla gelişmiş desen eşleştirme stratejileri gösteren, sağlam, kurumsal düzeyde bir yardımcı program. Bu mimari, ham, biçimlendirilmemiş metin dökümlerini nasıl tarayacağınızı ve adlandırılmış yakalama parametreleri, koşullu lookaround'lar ve çok satırlı pipeline yapılandırma bayrakları kullanarak bunları temiz yapılara nasıl deserilize edeceğinizi özetlemektedir.

## Mimari Amaç
Motor, analitik bir log toplayıcı veya denetim hattı görevi görür. Düz metin akışlarını (üretim sistemi dökümleri gibi) alır, katı sınırları yapısal parametrelere (Zaman Damgaları, Seviyeler, IP Ayak İzleri, Alt Bileşenler ve Durum Kodları) eşler ve ağır üçüncü taraf ayrıştırma ajanlarına ihtiyaç duymadan aranabilir Python sözlükleri döndürür.

## Proje Yapısı
```text
28_regex_mastery/
└── main.py
System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-based system environment)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated folder for your project within your workspace:

Bash
mkdir 28_regex_mastery
cd 28_regex_mastery
### Step 2: Assemble the Pattern Matching Engine
Create a file named main.py. Build out your processing routines sequentially:

Construct Named Groups: Implement an ingestion routine (e.g., parse_system_logs(raw_log_data)). Draft a compiled regex object (re.compile) that sets explicit variable key signatures onto individual slices of text via the (?P<name>...) syntax.

Handle Optional Tokens: Account for parameters that might not occur on every line (like HTTP or exception error codes) by grouping the sub-pattern and appending the non-greedy optional operator (?), for instance: (?:\s+\[code:(?P<status_code>\d+)\])?$.

Loop Over Stream Iterations: Run the .finditer() method across target logs. Inside the iteration block, invoke .groupdict() on each individual match element to transform text instantly into structured key-value maps.

Incorporate Lookahead Assertions: Implement an analytical filtration function using Lookarounds (e.g., extract_critical_failures_with_lookahead). Design a pattern utilizing non-consuming assertions like (?=.*\[database\]) to ensure lines belong to a specific category before checking for strings like denied or failed.

### Step 3: Run and Verify
Add a sample multi-line mock text log layout at the bottom of the script. Run the script via the terminal to confirm that the text blocks are correctly parsed into clean JSON schemas and filtered appropriately.

```bash
python main.py
# Proje 37: Argparse ile Komut Satırı Arayüzleri (CLI)

Python'ın standart `argparse` modülü kullanılarak oluşturulmuş, üretim düzeyinde bir komut satırı arayüzü (CLI) yardımcı programı. Bu mimari, kabuk parametrelerini güvenli bir şekilde nasıl alacağınızı, tür dönüşümlerini nasıl zorlayacağınızı, koşullu bayrak parametrelerini nasıl yapılandıracağınızı ve etkileşimli metin araçlarını sıfırdan yerel olarak nasıl yapılandıracağınızı gösterir.

## Mimari Hedef
Uygulama, kullanıcı operasyonel yapılandırmalarını statik yapılandırma değişkenlerinden veya etkileşimli komut istemi sorularından (`input()`) uzaklaştırır. Argümanları doğrudan işletim sistemi kabuk sınırından yönlendirerek, yardımcı program bash pipeline rutinleri, cron görevleri veya otomatik devops betik paketleri içine sorunsuz bir şekilde zincirlenebilen, yüksek düzeyde betiklenebilir bir bileşen haline gelir.

## Proje Yapısı
```text
37_argparse_cli/
└── main.py
System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
Step 1: Directory Setup
Create a dedicated project directory structure within your workspace repository:

Bash
mkdir 37_argparse_cli
cd 37_argparse_cli
Step 2: Implement the CLI Parser Engine
Create a file named main.py. Build your command parameters step-by-step:

Instantiate the Argument Parser Object: Import argparse and create a schema shell via argparse.ArgumentParser(). Pass helpful system documentation context strings like description and epilog to make terminal user discovery highly intuitive.

Configure Positional Fields: Use .add_argument() without any dash prefixes (e.g., "source", "target") to mandate positional parameters. These must be supplied by the end-user in exact order for the script execution to proceed.

Configure Flag Options: Introduce configuration switches by prefixing with hyphens (e.g., "-d", "--dry-run"). Leverage the action="store_true" property to build non-blocking toggles that act as native booleans (True if typed in command lines, False if completely omitted).

Parse and Delegate Values: Call parser.parse_args() to capture execution tokens from shell streams. Route those mapped properties cleanly directly into core data manipulation operations.

Step 3: Run and Verify
Test the capabilities of your freshly engineered CLI system using the following steps:

Invoke Automatic Documentation Screen:

Bash
python3 main.py --help
The engine automatically captures metadata, compiling a comprehensive, fully formatted user manual sheet on the fly.

Simulate File Relocation Layout (Dry-Run):
Create a dummy source directory with temporary files, and run a safe test pass:

Bash
mkdir test_source && touch test_source/doc1.pdf test_source/photo2.png test_source/script3.py
python3 main.py ./test_source ./test_target --dry-run
Verify that the workflow prints correct structural grouping blueprints without modifying any elements on the active disk engine layout.


---

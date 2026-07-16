# Proje 40: Üretim Ortamı İzolasyonu ve Dağıtımı

Modern üretim sunucuları için güvenli, izole sanal ortamların (`virtualenv`) nasıl oluşturulacağını, kilitleneceğini, doğrulanacağını ve dağıtılacağını gösteren son kilometre taşı projesi. Bu kurulum, küresel bağımlılık kirliliğini önlemek için gerçek dünya otomatik dağıtım (CI/CD) boru hatlarını modellemektedir.

## Mimari Hedef
Sistem, kurumsal düzeyde dağıtımlar için mutlak sınır kısıtlamasını oluşturur. Çalışma zamanı gereksinimlerini (runtime requirements) deterministik yapısal kilitlere (`requirements.txt`) dönüştürerek ve ana orkestrasyon katmanlarına titiz sağlık kontrol döngüleri gömerek, eksik dosyalardan kaynaklanan küresel ana makine paket kontaminasyonu veya bozuk üretim boru hatları riskini tamamen azaltır.

## Proje Yapısı
```text
40_virtualenv_deployment/
├── main.py
└── requirements.txt
System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX host environment)

Runtime: Python 3.12+

Core Tool: Python native venv standard module

How to Recreate This Project From Scratch
Step 1: Directory Setup
Create a dedicated project directory structure within your workspace repository:

Bash
mkdir 40_virtualenv_deployment
cd 40_virtualenv_deployment
Step 2: Formulate the Manifest and Deployment Target
Create the Script Target: Create a file named main.py. Build a defensive guard routine that actively compares sys.prefix with sys.base_prefix to determine environmental isolation dynamically on the fly.

Draft the Manifest Dependency Sheet: Create a file named requirements.txt. Specify your exact pinning definitions for downstream deployment routines:

Plaintext
requests==2.31.0
Step 3: Run and Verify the Deployment Simulation
Follow this multi-step terminal verification sequence to simulate a live production delivery setup on your Ubuntu host:

Verify Fallback Safeguards (Running Globally):
Run the file directly via your global system command lines:

Bash
python3 main.py
The engine immediately catches that no virtual environment layer bounds the execution memory address space and triggers a calculated sys.exit(1) block to protect your production lines from failure.

Spin Up an Isolated Production Virtualenv:
Construct a local, hidden standalone execution container directory:

Bash
python3 -m venv .venv
Activate the Layer Context:
Inject the freshly mapped environment paths directly into your current shell thread session:

Bash
source .venv/bin/init  # or source .venv/bin/activate
(Your terminal prompt will change to show a (.venv) prefix header)

Synchronize Packages via Lock Manifest:
Install all pinned production-grade dependencies securely into the active sub-context shell:

Bash
pip install --upgrade pip
pip install -r requirements.txt
Execute Final Release Verification Pass:
With your .venv context actively bound, execute your master sanity manager:

Bash
python3 main.py
The application logic will confirm isolation layer activation, ensure all tracking variables are explicitly resolved, and declare the server state SUCCESS for target data traffic!

---

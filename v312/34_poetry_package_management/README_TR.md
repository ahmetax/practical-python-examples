# Proje 34: Poetry ile Modern Paket Yönetimi

Python üçüncü taraf bağımlılıklarının, alt bağımlılık çözümleme izolasyonunun ve sanal ortamların modern endüstri standardı olan `Poetry` kullanılarak nasıl yönetileceğini gösteren bir üretim düzeyinde örnektir. Bu proje, `pip` ve `requirements.txt` gibi geleneksel eski iş akışlarını tamamen ortadan kaldırmaktadır.

## Mimari Hedef
Sistem, bağımlılık çözümlemesine deterministik bir plan şeması tasarlamaktadır. Gevşek eşleştirilmiş gereksinim sayfalarını, katı, tekrarlanabilir kilit manifestoları (`poetry.lock`) ile değiştirerek, tam yazılım bileşen ağaçlarının tüm yerel geliştirici makinelerinde, staging kümelerinde ve otomatik sürekli dağıtım (CD) iş akışlarında aynı şekilde kopyalanmasını garanti eder.

## Proje Yapısı
```text
34_poetry_package_management/
├── pyproject.toml
└── src/
    └── main.py

## System Requirements
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)
- Runtime: Python 3.12+
- Global Dependency: Poetry engine installed globally or user-wide on your system.

## Setting Up Poetry on Ubuntu
If you do not have Poetry installed on your host system, install it using the official standard installation script:

```bash
curl -sSL https://install.python-poetry.org | python3 -

Kurulumu, sürüm izini kontrol ederek doğrulayın:
```bash
poetry --version

## How to Recreate This Project From Scratch
### Step 1: Directory and Package Initialisation
Create a dedicated folder for this project inside your repository workspace:

```bash
mkdir 34_poetry_package_management
cd 34_poetry_package_management

Yapılandırma şemalarını manuel olarak yazmak yerine, standart bir düzeni yerel olarak şu yolla başlatabilirsiniz:
```bash
poetry init --no-interaction

This generates your fundamental structure mapping blueprint, pyproject.toml.

### Step 2: Configuring Dependencies and Source Code
- Define the pyproject.toml Layout: Ensure your pyproject.toml lists target constraints, including specific runtime platforms (e.g., python = "^3.12"), core packages (like requests and rich), and isolated developer groups (pytest).

- Add Dependencies Programmatically: Instead of editing raw files, add libraries using Poetry's interactive CLI. This triggers immediate cryptographic calculation checks and resolves sub-dependency graphs cleanly:

```bash
poetry add rich requests
poetry add pytest --group dev

- Uygulama Giriş Noktasını Taslağını Oluşturma: Bir `src/` dizini oluşturun ve `main.py` ekleyin. Kodunuzun, `runtime` sırasında izole edilmiş paket yapılarına temiz bir şekilde erişebildiğini doğrulamak için yeni yönettiğiniz bağımlılıkları—örneğin `rich.table`—içe aktarın.

### Adım 3: Çalıştırma ve Doğrulama
Poetry, tüm bağımlılıkları özel bir sanal ortam katmanı içinde izole eder. Uygulama kodunu bu korumalı bağlam içinde çalıştırmak için `poetry run` komut sarmalını (wrapper) kullanın:
```bash
poetry run python3 src/main.py

This activates the runtime layer seamlessly on the fly and outputs a beautifully formatted system visualization matrix inside your Ubuntu CLI interface.


---


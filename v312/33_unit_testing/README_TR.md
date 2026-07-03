# Proje 33: Pytest ile Otomatik Birim Testi

Üretim ortamına hazır bir test örneği olup, iş mantığını nasıl izole edeceğinizi ve `pytest` kullanarak otomatik test yürütme paketleri uygulayacağınızı göstermektedir. Bu proje, temel onaylamaları (assertions), uç durumları (edge cases) kontrol etmeyi ve beklenen istisna durumlarını doğrulamayı kapsar.

## Mimari Hedef
Uygulama, kod deposu içinde resmi bir test güdümlü katman oluşturur. Yürütme fonksiyonlarını test betiklerinden ayırarak, sürekli entegrasyon (CI) çalışanlarının veya pre-commit hook'larının gelen değişikliklerin yerleşik iş alanlarına regresyonlar sokmadığından emin olarak yürütme durumlarını otomatik olarak ayrıştırmasına olanak tanır.

## Proje Yapısı
```text
33_unit_testing/
├── math_operations.py
└── test_math_operations.py

System Requirements
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)
- Runtime: Python 3.12+

Setup & Dependencies
Pytest is an external framework package that needs to be installed inside your virtual environment. Run the following command:

```bash
```
pip install pytest
```

Bu Projeyi Sıfırdan Nasıl Yeniden Oluşturulur
Adım 1: Dizin Kurulumu
Bu proje için özel bir klasör oluşturun:
```bash
mkdir 33_unit_testing
cd 33_unit_testing

### Step 2: Implement Core Functions and Test Suits
1. Create the Target Module: Create a file named math_operations.py. Inside, implement core utility tasks like a division function (divide_numbers) that explicitly guards boundaries by raising a ValueError during division-by-zero attempts, and an array calculation function (calculate_average) that safely manages empty inputs.

2. Create the Testing Module: Create a file named test_math_operations.py. Note: Pytest depends on naming conventions to automatically discover tests; your file name must start with test_ and your interior test functions must also start with the test_ prefix.

3. Draft Target Verifications: Implement clear test blocks using plain Python assert statements.

  - Write standard path evaluations (e.g., verifying divide_numbers(10, 2) == 5.0).

  - Use the with pytest.raises(ValueError): context manager block to verify that your system components actively intercept and raise expected exceptions on forbidden input parameters.

### Step 3: Run and Verify
Instead of running Python directly on the script, invoke the pytest engine from your terminal inside the project directory:

```bash
pytest -v

-v (verbose) bayrağı, runner'a her test senaryosunu eşleşen doğrulama durumuyla birlikte listelemesini emreder ve temiz, yeşil bir geçiş özeti profili çıktısı verir.
# Proje 33: pytest ile Birim Testi

`pytest` ile birim testi yazmaya küçük bir örnek. Test edilen kod ile testler ayrı dosyalardadır:

| Dosya | İçerik |
|-------|--------|
| `math_operations.py` | `divide_numbers()` payda sıfırsa `ValueError` fırlatır; `calculate_average()` boş liste için `0.0` döndürür |
| `test_math_operations.py` | Beş test: normal sonuçlar, hata durumu ve uç durumlar (boş liste, tek elemanlı liste) |

## Nasıl Çalışır?
- pytest testleri adlarından bulur: `test_` ile başlayan dosyalar ve bu dosyalarda `test_` ile başlayan fonksiyonlar.
- Testler düz `assert` ifadeleri kullanır; bir doğrulama başarısız olursa pytest karşılaştırılan değerleri gösterir.
- `pytest.raises(ValueError)`, sıfıra bölmenin beklenen hatayı fırlattığını denetler. Test ayrıca hata mesajını da karşılaştırır (`str(exc_info.value)`).
- `math_operations.py` içinde `if __name__ == "__main__":` bloğu yoktur; `python3` ile çalıştırırsanız hiçbir şey yazdırmaz. Proje pytest ile çalıştırılır.

## Proje Yapısı
```text
33_unit_testing/
├── math_operations.py
├── test_math_operations.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü (pytest 9, 3.10+ ister; kodun kendisi 3.9 gerektiren `list[float]` kullanır). Python 3.12.3 ile test edildi.
- Üçüncü taraf paket: `pytest`. pytest 9.1.1 ile test edildi.

## Çalıştırma
Komutları `33_unit_testing` klasörünün içinde çalıştırın:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -v
```
`-v` (ayrıntılı) seçeneği her testi sonucuyla birlikte listeler.

## Örnek Çıktı (Python 3.12.3)
```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /path/to/.venv/bin/python3
rootdir: /path/to/33_unit_testing
collecting ... collected 5 items

test_math_operations.py::test_divide_numbers_success PASSED              [ 20%]
test_math_operations.py::test_divide_numbers_by_zero PASSED              [ 40%]
test_math_operations.py::test_calculate_average_normal_list PASSED       [ 60%]
test_math_operations.py::test_calculate_average_empty_list PASSED        [ 80%]
test_math_operations.py::test_calculate_average_single_element PASSED    [100%]

============================== 5 passed in 0.03s ===============================
```
Yollar ve çalışma süresi sizin makinenizde farklı olur. pytest proje klasöründe `.pytest_cache/` ve `__pycache__/` klasörleri oluşturur; bunları güvenle silebilirsiniz.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/05/pythonda-kodunuzu-kirilmaktan-koruyun-pytest-ile-birim-testi-yazmak/
- pytest belgeleri: https://docs.pytest.org/

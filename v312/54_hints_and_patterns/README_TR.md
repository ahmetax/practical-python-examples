# Proje 54: Tip İpuçları Çalışmaz, Desenler Yanılır — mypy ve pyright Yapay Zekânın Kodunda Neyi Görüyor?

Proje 23'ü (yapısal desen eşleme) ve proje 24'ü (gelişmiş tip ipuçları) bir yapay zekâ yazdı. İkisi de çalışıyor ve beklenen örnek çıktıyı veriyor. Proje 24'ün yorumları mypy'nin tipleri "tam olarak bileceğini" söylüyor. mypy gerçekten biliyor ve aynı dosyada bir hata buluyor. Bu betik, ipuçlarının ve desenlerin ne vaat ettiğini, Python'ın çalışma anında ne yaptığını ve tip denetleyicilerinin neyi görüp neyi göremediğini gösteriyor.

| Sorun | Örnek | mypy --strict | pyright |
|---|---|---|---|
| `data: T` için `data=None` (proje 24) | `APIResponse(status="fail", data=None)` | hata | hata |
| Durum yazım hatası, `status: str` | `is_successful("Success")` | ok | ok |
| Dataclass birleşiminde unutulan `case` | `assert_never(cmd)` | hata | hata |
| `float` değer üzerinde `case float()` | `kind(1250)` | ok (kaçırıyor) | hata |
| `TypedDict` üzerinde sözlük deseni | `assert_never(inv)` | kod doğruyken bile hata | kod doğruyken bile hata |
| `int` yerine `True` | `add("Laptop", True)` | ok | ok |

## Nasıl Çalışır?
- 1. bölüm, proje 24'ün `User` ve `APIResponse` sınıflarını ipuçlarının yasakladığı değerlerle çalıştırıyor. Python hepsini kabul ediyor. Hata çıkacaksa daha sonra, başka bir yerde çıkıyor.
- 2. bölüm, proje 23'ün `process_command` fonksiyonunu ("says") ve düzeltilmiş sürümünü ("checks") çalıştırıyor. `float(amt)` bir `isinstance` denetimi olduğu için JSON'dan gelen `1250` (`int`) tutarı reddediliyor. `bool`, `int`'in alt sınıfı olduğu için `int(qty)` deseni `True` ile eşleşiyor. Düzeltilmiş sürüm önce `bool()` desenini deniyor, tutar için koşullu `int() | float()` kullanıyor ve kimlikleri `type(i) is int` ile denetliyor.
- 3. bölüm, on küçük örnek kodu geçici bir klasöre yazıyor, her birini `mypy --strict --python-version 3.12` ve `pyright --pythonversion 3.12` ile denetliyor ve ilk hata kodunu yazdırıyor. İki araç da kurulu değilse bu bölüm atlanıyor.
- `d` örneği, proje 24 için akla ilk gelen düzeltme (`data: T | None`). `is_successful()` tipi daraltmadığı için iki denetleyici de `r.data.upper()` satırına hata veriyor. `e` örneği (`match` ile `Ok[T] | Err`) ikisinden de geçiyor.
- `j` örneği, Claude'un 12.11.2026'da yazdığı beş proje 24 sürümünün dördündeki hatayı yeniden üretiyor. PEP 695'te varyans çıkarılıyor; `T`'yi parametre olarak alan bir metot (`ok(cls, data: T)`) sınıfı değişmez (invariant) yapıyor. Bu yüzden `APIResponse[int]` ve `APIResponse[str]` karışık bir liste `describe[T]` fonksiyonuna verilemiyor.

## Proje Yapısı
```text
54_hints_and_patterns/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü. Python 3.12.3 ile ve Docker'da 3.10 ve 3.14 ile test edildi (1. ve 2. bölüm aynı).
- 1. ve 2. bölüm üçüncü taraf paket gerektirmiyor. 3. bölüm için `mypy` ve/veya `pyright` gerekiyor (mypy 2.4.1 ve pyright 1.1.414 ile test edildi; başka sürümler farklı kodlar verebilir).

## Çalıştırma
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mypy pyright
python3 main.py
```
pyright ilk çalıştırmada kendi Node.js ortamını indirebilir.

## Örnek Çıktı (Python 3.12.3)
```text
Python 3.12.3

== 1. Type hints do not run (project 24) ==
  User(id=3.5, username=None, email=42)        -> User(id=3.5, username=None, email=42)
  APIResponse(status="success", data=None)     -> AttributeError: 'NoneType' object has no attribute 'id'
  APIResponse(status="Success", data=User(...)) -> Error occurred: None

== 2. match patterns at runtime (project 23) ==
  {'type': 'invoice', 'amount': 1250.5}
    says     Invoice processed. Amount: $1250.50
    checks   Invoice processed. Amount: $1250.50
  {'type': 'invoice', 'amount': 1250}
    says     Invalid or unrecognized command format: {'type': 'invoice', 'amount': 1250}
    checks   Invoice processed. Amount: $1250.00
  {'type': 'invoice', 'amount': True}
    says     Invalid or unrecognized command format: {'type': 'invoice', 'amount': True}
    checks   Rejected: amount must be a number, not True/False
  ['add', 'Laptop', 2]
    says     Stock updated: Added 2 units of 'Laptop'.
    checks   Stock updated: Added 2 units of 'Laptop'.
  ['add', 'Laptop', True]
    says     Stock updated: Added True units of 'Laptop'.
    checks   Rejected: quantity must be a number, not True/False
  ['add', 'Laptop', -3]
    says     Stock updated: Added -3 units of 'Laptop'.
    checks   Rejected: use ['add', name, quantity > 0]
  ['delete', True, False]
    says     Deleting products with IDs: [True, False]
    checks   Invalid or unrecognized command format: ['delete', True, False]

== 3. What mypy (--strict) and pyright (default mode) see ==
  snippet                 mypy                              pyright                           
  a_none_data             error [arg-type]                  error [reportAssignmentType]      
  b_status_typo_str       ok                                ok                                
  c_status_typo_literal   error [arg-type]                  error [reportArgumentType]        
  d_optional_data         error [union-attr]                error [reportOptionalMemberAccess]
  e_result_union          ok                                ok                                
  f_forgotten_case        error [arg-type]                  error [reportArgumentType]        
  g_float_pattern         ok                                error [reportArgumentType]        
  h_mapping_pattern       error [arg-type]                  error [reportArgumentType]        
  i_bool_as_int           ok                                ok                                
  j_mixed_generic_list    error [misc]                      error [reportArgumentType]        
```

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/30/tip-ipuclari-calismaz-desenler-yanilir-mypy-pyright/
- Özgün projeler: `v312/23_structural_pattern_matching`, `v312/24_advanced_type_hinting`
- PEP 695, varyans çıkarımı: https://peps.python.org/pep-0695/#variance-inference
- PEP 634, yapısal desen eşleme: https://peps.python.org/pep-0634/
- typing.assert_never: https://docs.python.org/3/library/typing.html#typing.assert_never

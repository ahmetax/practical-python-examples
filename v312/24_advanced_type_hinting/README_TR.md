# Proje 24: Python 3.12 Sözdizimiyle Tip İpuçları ve Jenerikler

Python 3.12 ile gelen tip parametresi sözdizimine (PEP 695) kısa bir örnek. Kod, `type` ifadesiyle bir tip takma adı (alias) ve `TypeVar` tanımlamadan `class APIResponse[T]:` biçiminde jenerik bir sınıf oluşturur. İki veri sınıfı (`User`, `Product`) `APIResponse` içine sarılır; işleyici fonksiyonlar hangi tür yanıtı kabul ettiklerini açıkça belirtir.

| # | Konu | Koddaki örnek |
|---|------|---------------|
| 1 | Tip takma adı (PEP 695) | `type Identifier = int \| str` |
| 2 | `TypeVar` olmadan jenerik sınıf (PEP 695) | `class APIResponse[T]:` |
| 3 | `\|` ile birleşim ve isteğe bağlı değer | `error: str \| None = None` |
| 4 | İmzada parametreli jenerik | `def process_user_response(response: APIResponse[User]) -> None:` |

## Proje Yapısı
```text
24_advanced_type_hinting/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.12 veya üstü. `type` ifadesi ve `class Ad[T]:` sözdizimi 3.12'den önce yoktur; dosya 3.11'de `type Identifier = int | str` satırında `SyntaxError: invalid syntax` hatası verir. 3.12.3 ile test edildi.
- Üçüncü taraf paket gerekmez. `mypy` isteğe bağlıdır, yalnızca aşağıdaki tip kontrolü için.

## Çalıştırma
```bash
python3 main.py
```

## Örnek Çıktı (Python 3.12.3)
```text
--- Advanced Type Hinting Test Started ---

Success: Processing User #101 -> ahmet_dev (ahmet@example.com)
--------------------------------------------------
Success: Processing Product #PROD-99X -> Mechanical Keyboard costs $89.99
--------------------------------------------------
Error occurred: User not found
```

## mypy ile Kontrol
Tip ipuçları çalışma anında denetlenmez; onları statik bir tip denetleyicisi okur. Denemek için:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mypy
mypy main.py
```
mypy 2.4.0 ile sonuç şudur:
```text
main.py:88: error: Argument "data" to "APIResponse" has incompatible type "None"; expected "User"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```
Başarısız yanıt örneği, `APIResponse[User]` nesnesine `data=None` verir; oysa `data` parametresi `T | None` değil `T` olarak tanımlanmıştır. Python bunu sorunsuz çalıştırır, mypy ise hata olarak bildirir. Parametreyi `data: T | None` yapmak (ve işleyicilerde `None` durumunu ele almak) hatayı giderir.

## Nasıl Çalışır?
- `type Identifier = int | str` tembel değerlendirilen bir tip takma adı oluşturur; `User.id` ve `Product.id` tam sayı da metin de olabilir.
- `class APIResponse[T]:` tip parametresi `T`'yi doğrudan sınıf başlığında tanımlar. mypy, `APIResponse(status="success", data=user_data)` ifadesinden `APIResponse[User]` türünü çıkarır; böylece `response.data` değerinin `User` olduğunu bilir.
- `process_user_response()` yalnızca `APIResponse[User]` kabul eder; ona `APIResponse[Product]` vermek mypy için tip hatasıdır, ama çalışma anında hata vermez.
- Dosya hâlâ `typing` modülünden `Generic` ve `TypeVar` içe aktarır (11. satır) ama bunları kullanmaz; yeni sözdizimi burada onları gereksiz kılar.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/05/python-3-12-ile-tip-sisteminde-yeni-bir-donem-pep-695-ve-gelismis-jenerikler/
- PEP 695: Tip parametresi sözdizimi: https://peps.python.org/pep-0695/
- `typing` belgeleri: https://docs.python.org/3/library/typing.html

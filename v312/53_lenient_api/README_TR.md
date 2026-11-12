# Proje 53: Sessizce Kabul Eden API — limit=-1, "12.5" Fiyat ve Listeyi Kilitleyen "inf"

Proje 30'u (FastAPI temelleri) bir yapay zekâ yazdı. Belgelenen bütün istekler çalışıyor, README'deki geçersiz gövdeleri de Pydantic reddediyor. Bu betik, kimsenin belgelemediği istekleri önce özgün uygulamaya, sonra düzeltilmiş uygulamaya gönderiyor.

| İstek | Özgün ("says") | Düzeltilmiş ("checks") |
|---|---|---|
| `GET /items?limit=-1` / `skip=-1` | 200, yanlış kayıtlar (liste dilimleme) | 422 (`Query(ge=...)`) |
| `GET /items?limit=1000000000` | 200, üst sınır yok | 422 (`le=100`) |
| `"price": "12.5"` ya da `true` | 201, 12.5 / 1.0 olarak kaydediliyor | 422 (`strict=True`) |
| `"name": "   "`, fazladan `"discount"` alanı | 201, boş ad / alan atılıyor | 422 (`str_strip_whitespace`, `extra="forbid"`) |
| `"price": "inf"` | 500, **kayıt ekleniyor**, sonra `GET /items` 500 veriyor | 422 |
| tırnaksız `NaN`, `Infinity`, `1e999` | 500 | 422, ancak özel bir doğrulama hatası işleyicisiyle |

## Nasıl Çalışır?
- `build_says()` proje 30'daki modeli ve iki uç noktayı değiştirmeden içeriyor. `build_checks()` düzeltilmiş sürüm. Her istek yeni bir uygulamaya gidiyor. Yalnızca 3. bölüm, hatalı istekten sonra aynı uygulamaya ne olduğunu gösteriyor.
- İstekler FastAPI'nin `TestClient` aracıyla `raise_server_exceptions=False` ayarıyla gönderiliyor. Böylece sunucu hatası, gerçek bir istemcinin gördüğü gibi 500 yanıtı olarak görünüyor.
- 3. bölüm: Esnek kipteki Pydantic `"inf"` metnini `float("inf")` değerine çeviriyor ve bu değer `gt=0` kuralını geçiyor. Kayıt ekleniyor, sonra Starlette yanıtı yazamıyor (`ValueError: Out of range float values are not JSON compliant: inf`). O kayda ulaşan sonraki her listeleme de çöküyor.
- 4. bölüm: Python'ın `json` modülü tırnaksız `NaN`, `Infinity` ve `1e999` değerlerini kabul ediyor. Düzeltilmiş model bunları reddediyor ve hiçbir şey kaydedilmiyor. Ama FastAPI'nin varsayılan 422 yanıtı reddedilen girdiyi geri gönderiyor, bu yanıt JSON'a çevrilemiyor ve istemci yine 500 alıyor. `build_checks()`, hata listesinden `input` ve `ctx` alanlarını çıkaran bir `RequestValidationError` işleyicisi kuruyor.
- 5. bölüm: `Query(strict=True)` her değeri reddediyor, çünkü adres satırındaki değerler her zaman metindir. Sorgu parametrelerinde `ge`/`le` kullanın.

## Proje Yapısı
```text
53_lenient_api/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.9 veya üstü. Python 3.12.3 ile ve Docker'da 3.9, 3.10, 3.14 ile test edildi (3.9'da fastapi 0.128.8 / pydantic 2.13.5 kuruluyor); çıktı aynı.
- Üçüncü taraf paketler: `fastapi` ve `httpx` (`TestClient` için). fastapi 0.162.5 ve pydantic 2.14.3 ile test edildi; 3. ve 4. bölüm fastapi 0.143.0 / pydantic 2.14.1 ile de aynı.

## Çalıştırma
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi httpx
python3 main.py
```
Sunucu başlatılmıyor.

## Örnek Çıktı (Python 3.12.3)
```text
Python 3.12.3, fastapi 0.162.5, pydantic 2.14.3

== 1. Pagination ==
  GET /items?limit=-1
  says      200  ids [1]
  checks    422  greater_than_equal at query.limit
  GET /items?skip=-1
  says      200  ids [2]
  checks    422  greater_than_equal at query.skip
  GET /items?limit=1000000000
  says      200  ids [1, 2]
  checks    422  less_than_equal at query.limit

== 2. Lax types ==
  POST {"sku":"SKU-A1","name":"Cable","price":"12.5"}
  says      201  {"id":3,"sku":"SKU-A1","name":"Cable","price":12.5}
  checks    422  float_type at body.price
  POST {"sku":"SKU-A2","name":"Cable","price":true}
  says      201  {"id":3,"sku":"SKU-A2","name":"Cable","price":1.0}
  checks    422  float_type at body.price
  POST {"sku":"SKU-A3","name":"Cable","price":12}
  says      201  {"id":3,"sku":"SKU-A3","name":"Cable","price":12.0}
  checks    201  {"id":3,"sku":"SKU-A3","name":"Cable","price":12.0}
  POST {"sku":"SKU-A4","name":"   ","price":5}
  says      201  {"id":3,"sku":"SKU-A4","name":"   ","price":5.0}
  checks    422  string_too_short at body.name
  POST {"sku":"SKU-A5","name":"Cable","price":5,"discount":90}
  says      201  {"id":3,"sku":"SKU-A5","name":"Cable","price":5.0}
  checks    422  extra_forbidden at body.discount
  POST {"sku":" SKU-MECH-01","name":"Cable","price":5}
  says      201  {"id":3,"sku":" SKU-MECH-01","name":"Cable","price":5.0}
  checks    400  {"detail":"An item with SKU 'SKU-MECH-01' already exist...

== 3. "inf" passes gt=0 ==
  says      500  Internal Server Error
            records now: 3
  GET       500  Internal Server Error
  GET       200  ids [1, 2]
  checks    422  float_type at body.price
            records now: 2
  GET       200  ids [1, 2]
  GET       200  ids [1, 2]

== 4. Bare NaN / Infinity in the body ==
  POST {"sku":"SKU-N1","name":"Cable","price":NaN}
  says      500  Internal Server Error                    records: 2
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  POST {"sku":"SKU-N2","name":"Cable","price":Infinity}
  says      500  Internal Server Error                    records: 3
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  POST {"sku":"SKU-N3","name":"Cable","price":1e999}
  says      500  Internal Server Error                    records: 3
  model     500  Internal Server Error                    records: 2
  checks    422  finite_number at body.price              records: 2
  (model = corrected model without the error handler)

== 5. Query(strict=True) ==
  strict    422  int_type at query.limit
  checks    200  ids [1, 2]
```

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/11/26/sessizce-kabul-eden-api-fastapi-limit-fiyat-inf/
- Özgün proje: `v312/30_fastapi_basics`
- FastAPI sayısal doğrulama: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
- FastAPI, doğrulama hatası işleyicisini değiştirmek: https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
- Pydantic strict mod: https://docs.pydantic.dev/latest/concepts/strict_mode/
- Python json, sonsuz ve NaN değerleri: https://docs.python.org/3/library/json.html#infinite-and-nan-number-values

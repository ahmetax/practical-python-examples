# Proje 30: FastAPI Temelleri

FastAPI ile yazılmış küçük bir REST API. Ürün envanterini bir Python sözlüğünde (bellekte) tutar ve FastAPI'nin temel özelliklerini dört uç noktada gösterir:

| Uç nokta | Gösterdiği konu |
|----------|-----------------|
| `GET /` | Basit bir durum mesajı |
| `GET /items?limit=10&skip=0` | Varsayılan değerli sorgu parametreleri (sayfalama) |
| `GET /items/{item_id}` | Tipli yol parametresi ve `HTTPException` ile `404` hatası |
| `POST /items` | Pydantic modeliyle istek gövdesi doğrulama, `201` ve `400` durum kodları |

## Nasıl Çalışır?
- `ItemSchema` bir Pydantic modelidir. `sku` en az 3, `name` en az 1 karakter olmalı, `price` ise 0'dan büyük olmalıdır. FastAPI istek gövdesini fonksiyon çalışmadan önce bu modele göre denetler ve geçersiz isteklere kendiliğinden `422` ile yanıt verir.
- Yoldaki `item_id: int` tamsayıya dönüştürülür. `abc` gibi bir değer `422` ile reddedilir.
- `POST /items`, aynı `sku` ile gelen ikinci kaydı `400` ile reddeder. Yeni kayıtlar bir sonraki tamsayı kimliği alır (`max + 1`).
- Veriler `INVENTORY_DB` sözlüğünde durur; sunucu yeniden başlayınca eklediğiniz her şey kaybolur.
- `limit` ve `skip` doğrulanmaz. Negatif değerler doğrudan Python liste dilimlemesine gider: `/items?limit=-1` sonuncusu hariç bütün kayıtları döndürür.
- FastAPI, `/docs` (Swagger UI) ve `/redoc` adreslerinde etkileşimli belgeleri kendisi üretir.

## Proje Yapısı
```text
30_fastapi_basics/
├── main.py
├── README.md
└── README_TR.md
```

## Gereksinimler
- Python 3.10 veya üstü (FastAPI, Pydantic ve Uvicorn'un güncel sürümleri 3.10+ istiyor; kodun kendisi daha yeni bir sözdizimi kullanmıyor). Python 3.12.3 ile test edildi.
- Üçüncü taraf paketler: `fastapi` ve `uvicorn` (`pydantic`, FastAPI ile birlikte kurulur). fastapi 0.143.0, pydantic 2.14.1, uvicorn 0.54.0 ile test edildi.

## Çalıştırma
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python3 main.py
```
Sunucu, otomatik yeniden yükleme açık olarak `http://127.0.0.1:8000` adresinde başlar. `Ctrl+C` ile durdurabilirsiniz.

İkinci bir terminalden uç noktaları `curl` ile çağırabilir ya da tarayıcınızda `http://127.0.0.1:8000/docs` adresini açabilirsiniz.

## Örnek Çıktı (Python 3.12.3)
Sunucu terminali:
```text
INFO:     Will watch for changes in these directories: ['/path/to/30_fastapi_basics']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [435840] using StatReload
Launching API Web Server locally...
INFO:     Started server process [435849]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

İstekler ve yanıtları (HTTP durum kodu `200` değilse parantez içinde eklenmiştir):
```bash
curl http://127.0.0.1:8000/
curl "http://127.0.0.1:8000/items?limit=1&skip=1"
curl http://127.0.0.1:8000/items/99
curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" \
     -d '{"sku":"SKU-MON-03","name":"27-inch Monitor","price":199.9}'
curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" \
     -d '{"sku":"AB","name":"","price":0}'
```
```text
{"status":"online","message":"Welcome to the FastAPI Inventory System"}
[{"id":2,"sku":"SKU-MOUS-02","name":"Ergonomic Wireless Mouse","price":49.5}]
{"detail":"Item with ID 99 does not exist."}                                   (HTTP 404)
{"id":3,"sku":"SKU-MON-03","name":"27-inch Monitor","price":199.9}             (HTTP 201)
{"detail":[{"type":"string_too_short","loc":["body","sku"],"msg":"String should have at least 3 characters","input":"AB","ctx":{"min_length":3}},{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1}},{"type":"greater_than","loc":["body","price"],"msg":"Input should be greater than 0","input":0,"ctx":{"gt":0.0}}]}   (HTTP 422)
```
Aynı `SKU-MON-03` kaydını tekrar gönderirseniz `400` durum koduyla `{"detail":"An item with SKU 'SKU-MON-03' already exists."}` yanıtını alırsınız. İşlem numaraları ve yollar sizin makinenizde farklı olur.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/08/26/fastapi-ile-tanisin-modern-hizli-ve-tip-guvenli-apiler-gelistirmek/
- FastAPI belgeleri: https://fastapi.tiangolo.com/

# Proje 30: FastAPI Temelleri

FastAPI ve Pydantic kullanarak yüksek performanslı, asenkron REST API'leri nasıl oluşturulacağını gösteren temel bir mikroservis web framework örneği. Bu uygulama, tip doğrulama şemalarını, path/query parametre işleme, durum kodlarını ve istisna yönetimini kapsar.

## Mimari Hedef
Uygulama, geleneksel senkron paradigmalardan (standart Flask yönlendirmesi gibi) modern bir ASGI tabanlı mimariye geçiş yapar. `async/await` non-blocking işlemlerini Pydantic veri modelleme katmanlarıyla birleştirerek, runtime trafik yüklerinin çekirdek uygulama alanlarına ulaşmadan önce anında doğrulandığından emin olur.

## Proje Yapısı
```text
30_fastapi_basics/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)

Runtime: Python 3.12+

Setup & Dependencies
Unlike previous standard library examples, FastAPI requires an external routing framework engine and an ASGI web server runner (uvicorn). Pip install them directly into your virtual environment:

```bash
pip install fastapi uvicorn pydantic

How to Recreate This Project From Scratch
### Adım 1: Dizin Kurulumu
Bu proje için, depo çalışma alanınızın içine izole bir dizin kurun:
```bash
mkdir 30_fastapi_basics
cd 30_fastapi_basics

### Step 2: Formulate the Web Service
Create a file named main.py. Build your API structure step-by-step:

Instantiate the Core Application Instance: Import FastAPI and create an instance variable (e.g., app = FastAPI()). You can optionally pass metadata like title, description, and version to customize the automated openAPI documentation context.

Design Data Validation Schemas: Define your input constraints by inheriting from Pydantic's BaseModel. Use field attributes (Field(...)) to mandate basic requirements, string length boundaries, or positive math validations (e.g., enforcing that price values stay strictly greater than zero via gt=0.0).

Draft Non-Blocking Asynchronous Routes: Implement standard REST verb decorators over asynchronous target routines (async def).

Use plain routing paths for broad actions (e.g., @app.get("/items")).

Use bracket formatting tokens for explicit inline routing parameters (e.g., @app.get("/items/{item_id}")), capturing variables natively as strongly typed function inputs.

Map parameter variables directly inside function declarations (e.g., limit: int = 10) to handle query parameters and pagination effortlessly.

Enforce Error Boundaries: Guard edge cases by raising instances of HTTPException alongside valid status components imported directly from fastapi.status.

### Step 3: Run and Verify
Add a driver block to launch your application using uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True). Run the server script from your terminal:

```bash
python main.py

Tarayıcınızı açın ve aşağıdaki etkileşimli uç noktalara gidin:

API Durum Kontrolü: http://127.0.0.1:8000/

Etkileşimli Swagger Dokümantasyonu: http://127.0.0.1:8000/docs

Alternatif ReDoc Arayüzü: http://127.0.0.1:8000/redoc
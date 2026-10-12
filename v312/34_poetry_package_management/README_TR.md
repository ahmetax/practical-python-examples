# Proje 34: Poetry ile Paket Yönetimi

Bir projenin bağımlılıklarını `pip` ve `requirements.txt` dosyası yerine [Poetry](https://python-poetry.org/) ile yönetmeyi gösteren küçük bir örnek. Bağımlılıklar `pyproject.toml` dosyasında tanımlanır. Poetry'nin çözümlediği tam sürümler (alt bağımlılıklar ve özet değerleri dahil) `poetry.lock` dosyasında sabitlenir. Bu klasörde `poetry install` komutunu çalıştıran herkes aynı paket sürümlerini kurar.

`src/main.py`, üçüncü taraf `rich` paketini kullanarak hangi Python yorumlayıcısıyla çalıştığını gösteren bir tablo yazdırır. Betiği `poetry run` ile başlattığınızda bu yorumlayıcı, Poetry'nin proje için oluşturduğu sanal ortamdaki yorumlayıcıdır.

## Nasıl Çalışır?
- `pyproject.toml` iki çalışma zamanı bağımlılığı (`rich >=15,<16` ve `requests >=2.34.2,<3`) ile `dev` grubunda bir geliştirme bağımlılığı (`pytest >=9.0.3,<10`) tanımlar. `requests` ve `pytest` kodda kullanılmaz; çalışma zamanı ve geliştirme gruplarını göstermek için eklenmiştir. Projede test dosyası yoktur.
- `poetry.lock` toplam 14 paketi sabitler (yukarıdaki üç paket ve `certifi`, `urllib3`, `markdown-it-py`, `pygments` gibi alt bağımlılıkları).
- `poetry install` bir sanal ortam oluşturur ve kilit dosyasındaki sürümleri birebir kurar. `poetry run <komut>` ise bir komutu, ortamı etkinleştirmenize gerek kalmadan o ortamın içinde çalıştırır.
- Çıktıdaki "Successfully Resolved via Poetry" yazısı kodda sabit bir metindir. Tablo yalnızca `rich` paketinin içe aktarılabildiğini gösterir, nasıl kurulduğunu değil.

## Proje Yapısı
```text
34_poetry_package_management/
├── poetry.lock
├── pyproject.toml
├── README.md
├── README_TR.md
└── src/
    └── main.py
```

## Gereksinimler
- Python 3.12 veya üstü (`pyproject.toml` içinde `requires-python = ">=3.12"`; kilitli paketlerin kendisi 3.10+ ister). Python 3.12.3 ile test edilmiştir.
- Poetry 2.3 veya üstü. Kilit dosyası Poetry 2.4.1 ile oluşturulmuştur ve geliştirme grubu standart `[dependency-groups]` tablosunu kullanır. Poetry 2.1 ve 2.2 bu kilit dosyasını "pyproject.toml changed significantly since poetry.lock was last generated" hatasıyla reddeder. Poetry 2.3.0, 2.4.0 ve 2.5.1 ile test edilmiştir.

Poetry'yi `pipx` ile kurun (önerilen yol):
```bash
sudo apt install pipx
pipx install poetry
poetry --version
```
ya da resmî kurulum betiğiyle:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Çalıştırma
```bash
cd 34_poetry_package_management
poetry install --no-root
poetry run python3 src/main.py
```
`--no-root` seçeneğini kullanın. Bu klasör kurulabilir bir paket değildir. Bu yüzden düz `poetry install` önce tüm bağımlılıkları kurar, sonra hata vererek durur (çıkış kodu 1):
```text
Error: The current project could not be installed: No file/folder found for package 34-poetry-package-management
If you do not want to install the current project use --no-root.
```
Diğer bir yol da `pyproject.toml` dosyasına bir `[tool.poetry]` tablosu ekleyip altına `package-mode = false` yazmaktır. Bundan sonra düz `poetry install` de çalışır.

## Örnek Çıktı (Python 3.12.3)
```text
                      Poetry Managed Environment Metadata                       
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter              ┃ Value                                               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Python Executable Path │ /home/you/.cache/pypoetry/virtualenvs/34-poetry-pa… │
│ Python Version         │ 3.12.3                                              │
│ Rich Library Status    │ Successfully Resolved via Poetry                    │
└────────────────────────┴─────────────────────────────────────────────────────┘
```
Yorumlayıcı yolu makinenize ve Poetry ayarlarınıza göre değişir. Rich, terminal genişliğine sığmayan değerleri `…` ile kısaltır.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/08/requirements-txtye-veda-poetry-ile-python-paket-yonetimi/
- Poetry belgeleri: https://python-poetry.org/docs/
- Rich belgeleri: https://rich.readthedocs.io/

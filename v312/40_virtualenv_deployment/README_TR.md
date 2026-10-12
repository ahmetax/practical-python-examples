# Proje 40: Dağıtım Öncesi Sanal Ortam Kontrolü

Küçük bir dağıtım öncesi sağlık kontrolü. `main.py`, bir sanal ortamın (`venv`) içinde çalışmıyorsa ya da ihtiyaç duyduğu üçüncü taraf paket (`requests`) kurulu değilse çalışmayı reddeder. Bir servisin yanlışlıkla sistemin genel Python kurulumuyla çalışmasını önlemek için dağıtım hattının (pipeline) başına konacak türden bir kontroldür.

## Nasıl Çalışır?
- **İzolasyon kontrolü:** Sanal ortamın içinde `sys.prefix` ortamın klasörünü, `sys.base_prefix` ise temel Python kurulumunu gösterir. İkisi eşitse betik genel ortamda çalışıyor demektir ve `1` çıkış koduyla sonlanır.
- **Bağımlılık kontrolü:** Betik `import requests` satırını dener. İçe aktarma başarısız olursa `1` çıkış koduyla sonlanır ve gereksinimleri kurmanızı ister.
- İki kontrol de geçilirse başarı mesajı yazar ve `0` çıkış koduyla sonlanır. Böylece bir CI/CD adımı çıkış koduna güvenebilir.

## Proje Yapısı
```text
40_virtualenv_deployment/
├── main.py
├── README.md
└── README_TR.md
```
`requirements.txt` projeye dahil değildir. Aşağıdaki 2. adımda siz oluşturursunuz.

## Gereksinimler
- Python 3.12+ (yerleşik `venv` modülü olan her Python 3 sürümü çalışır)
- Ubuntu 24.04 veya herhangi bir Linux/macOS sistemi. Windows'ta `source .venv/bin/activate` yerine `.venv\Scripts\activate` kullanın.
- Ubuntu'da `venv` için sistem paketi gerekebilir: `sudo apt install python3-venv`

## Çalıştırma

**1. Genel ortamda çalıştırın (başarısız olması beklenir):**
```bash
python3 main.py
```
```text
--- Running Production Deployment Sanity Monitor ---
 -> Isolation Layer Status   : INACTIVE (GLOBAL)
 -> Python Interpreter Path   : /usr/bin/python3
 -> Python Core Version       : 3.12.3
 -> Third-Party Requirements : RESOLVED
-------------------------------------------------------
[Critical Danger] Application is running globally! Aborting pipeline to prevent host pollution.
```

**2. Sanal ortamı ve gereksinim dosyasını oluşturun:**
```bash
python3 -m venv .venv
source .venv/bin/activate
echo "requests==2.32.3" > requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
```
Komut satırınız artık `(.venv)` ile başlar. Sürümü tam olarak sabitlemek (`==`) her dağıtımda aynı paketin kurulmasını sağlar.

**3. Sanal ortamın içinde çalıştırın (başarılı olması beklenir):**
```bash
python3 main.py
```
```text
--- Running Production Deployment Sanity Monitor ---
 -> Isolation Layer Status   : ACTIVE (.venv)
 -> Python Interpreter Path   : /path/to/40_virtualenv_deployment/.venv/bin/python3
 -> Python Core Version       : 3.12.3
 -> Third-Party Requirements : RESOLVED
-------------------------------------------------------
[SUCCESS] Environment sanity check passed. The container/host is safe for heavy web routing operations.
```

`pip install -r requirements.txt` adımını atlarsanız betik etkin ortamı tanır, ancak gereksinimler için `UNRESOLVED (CRITICAL)` yazar ve `1` çıkış koduyla sonlanır.

İşiniz bittiğinde `deactivate` komutuyla ortamdan çıkabilirsiniz.

## Kaynaklar
- Blog yazısı: https://gurmezin.com/2026/09/28/pythonda-sanal-ortam-kontrolu-uretime-cikmadan-once-son-guvenlik-adimi/
- `venv` belgeleri: https://docs.python.org/3/library/venv.html

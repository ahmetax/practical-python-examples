# 🧩 Sudoku Oluşturucu ve Çözücü

**Python** ve **Flask** ile oluşturulmuş eksiksiz bir Sudoku uygulaması. Bu proje, bir bulmaca oluşturucu, adım adım animasyonlu bir geri izleme (backtracking) çözücü ve bulmacaları oynamak ve çözmek için bir web arayüzünü bir araya getiriyor.

## 🚀 Özellikler

- **Bulmaca Oluşturma**: Üç zorluk seviyesinde (Kolay, Orta, Zor) geçerli Sudoku bulmacaları oluşturma.
- **Deterministik Bulmacalar**: Aynı bulmacayı yeniden oluşturmak için rastgele bir tohum (seed) desteği.
- **Animasyonlu Çözücü**: Her denemeyi kaydeden ve kullanıcıların çözme sürecini adım adım izlemesine olanak tanıyan bir geri izleme (backtracking) çözücü.
- **Alt Süreç (Subprocess) Çalıştırma**: Çözücü bağımsız bir script olarak uygulanmıştır ve performans karşılaştırması için bir subprocess aracılığıyla çağrılabilir.
- **Etkileşimli Arayüz (UI)**:
  - Numpad ve klavye girişi.
  - Gerçek zamanlı tahta doğrulama (çakışmaları tespit eder).
  - Çözücü animasyonu için Oynat/Duraklat/Adım kontrolleri.
  - Değişken animasyon hızı.
- **Tahta Yönetimi**: Orijinal bulmacaya sıfırlama veya tahtayı temizleme seçenekleri.

---

## 📁 Proje Yapısı
```text
18_sudoku_app/
├── sudoku_app.py         # Flask startup and server configuration
├── sudoku_engine.py      # Core logic: Generator, Validator, and Solver
├── sudoku_solver.py      # Standalone solver script for subprocess calls
├── sudoku_helpers.py     # Flask routes and API logic
└── sudoku_templates/      # UI templates
    ├── base.html         # Shared layout and styling
    └── index.html        # Game board and control panel
```
---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Koşullar
Flask'ı Kurun:
```bash
pip install flask
```
### 2. Core Logic: The Engine (`sudoku_engine.py`)

Motor, Sudoku'nun matematiksel mantığını yönetir.

#### A. Validation Logic
`is_valid(board, row, col, num)` fonksiyonunu uygulayın:
- **Satırı** kontrol ederek sayının zaten var olup olmadığını kontrol edin.
- **Sütunu** kontrol ederek sayının zaten var olup olmadığını kontrol edin.
- **3x3 kutuyu** hesaplayarak kutu başlangıç indekslerini `(row // 3) * 3` ve `(col // 3) * 3` ile kontrol edin.

#### B. Backtracking Solver
`solve(board)` fonksiyonunu uygulayın:
1. İlk boş hücreyi (değeri 0) bulun. Eğer hiçbiri yoksa, tahta çözülmüştür.
2. 1'den 9'a kadar sayılar üzerinde döngü yapın.
3. Eğer bir sayı o hücrede geçerliyse, yerleştirin ve özyinelemeli olarak `solve()` çağırın.
4. Özyinelemeli çağrı `False` döndürürse, hücreyi 0'a sıfırlayın (backtrack) ve bir sonraki sayıyı deneyin.

#### C. Step-Recording Solver
`solve_with_steps(board)` fonksiyonunu uygulayın:
- Geri izleme çözücüye benzer, ancak sadece bir boolean döndürmek yerine, bir sayı yerleştirildiğinde veya kaldırıldığında bir nesneyi bir `steps` listesine ekleyin.
- Her adım şunları içermelidir: `row`, `col`, `num` ve `action` ('place' veya 'backtrack').

#### D. Puzzle Generator
`generate(difficulty, seed)` fonksiyonunu uygulayın:
1. Boş bir tahtayla başlayın ve `solve()` fonksiyonunu kullanarak tamamen doldurun (karıştırılmış sayılar rastgeleliği sağlar).
2. Zorluğa göre kaç tane "ipucu" tutulacağını belirleyin (örneğin, Easy=36, Medium=27, Hard=22).
3. Hücreleri rastgele tek tek kaldırın.
4. **Kritik**: Bir hücre kaldırıldıktan sonra, bulmacanın hala benzersiz bir çözümü olup olmadığını doğrulayın. Eğer değilse, hücreyi geri yükleyin ve başka bir tane deneyin.

---

### 3. Standalone Solver (`sudoku_solver.py`)

Ayrı bir script oluşturun ki:
- Bir komut satırı argümanı olarak 81 karakterlik bir puzzle string'i alsın.
- String'i 9x9 bir tahtaya dönüştürsün.
- Tahtayı çözsün ve geçen süreyi ölçsün (`time.perf_counter_ns()`).
- Sonucu bir JSON string'i olarak yazdırsın: `{"solution": "...", "elapsed_ns": ..., "solved": ...}`.

---

### 4. Flask API Integration (`sudoku_helpers.py`)

Frontend'i motorla bağlamak için endpoint'leri tanımlayın:

- **`/generate` (POST)**: `engine.generate()` çağırır, tahtayı düz bir listeye dönüştürür ve bulmacayı ile çözümü JSON olarak döndürür.
- **`/solve` (POST)**:
  - Animasyon için veri sağlamak amacıyla adım kaydeden çözücüyü çalıştırır.
  - İsteğe bağlı olarak, bağımsız script'in performansı ile süreç içi çözücünün performansını karşılaştırmak için `subprocess.run()` aracılığıyla `sudoku_solver.py` çağırır.
- **`/validate` (POST)**: Mevcut tahta durumunu alır ve `engine.is_valid()` kullanarak tüm boş olmayan hücreler üzerinde döngü yaparak çakışma kontrolü yapar.

---

### 5. Application Entry (`sudoku_app.py`)
- Flask'ı başlatın.
- Rotaları `sudoku_helpers.setup_routes(app)` kullanarak kaydedin.
- Uygulamayı 8117 portunda çalıştırın.

### 6. Frontend Development (`sudoku_templates/`)
- **`base.html`**: Duyarlı bir ızgara ile koyu temalı bir düzen kurun.
- **`index.html`**:
  - **The Board (Tahta)**: Girişlerden oluşan 9x9 bir ızgara. 3x3 blokların görsel olarak farklı (örneğin, daha kalın kenarlıklarla) görünmesi için stil verin.
  - **Numpad (Sayısal Tuş Takımı)**: Kolay giriş sağlamak için 1–9 sayılarına ait düğmeler.
  - **Controls (Kontroller)**: Generate, Solve, Validate ve Clear düğmeleri.
  - **Animation Logic (Animasyon Mantığı)**: `/solve` yanıtındaki `steps` dizisini okuyan ve belirtilen bir aralıkta tahta hücrelerini tek tek güncelleyen JavaScript.

---

## 🏃 Nasıl Çalıştırılır

1. Sunucuyu çalıştırın:
   ```bash
   python sudoku_app.py
   ```
2. Tarayıcınızı açın ve şu adrese gidin:
   **http://localhost:8117**

---

## 📚 Gösterilen Temel Kavramlar

- **Geri İzleme Algoritması (Backtracking Algorithm)**: Kısıtlı tatmin problemleri (constraint satisfaction problems) çözmek için derinlik öncelikli arama (depth-first search) yaklaşımı.
- **Özyinelemeli Problem Çözme (Recursive Problem Solving)**: Tüm olası sayı kombinasyonlarını keşfetmek için özyineleme (recursion) kullanmak.
- **Bulmaca Üretim Mantığı (Puzzle Generation Logic)**: Tek bir çözümü olan çözülebilir bir bulmaca oluşturma süreci.
- **Alt Süreç Yönetimi (Subprocess Management)**: Harici betiklerle (external scripts) çalışmak ve iletişim kurmak için Python'ın `subprocess` modülünü kullanmak.
- **Gerçek Zamanlı Web Animasyonu (Real-time Web Animation)**: Algoritmik adımların kaydedilmiş bir dizisini oynatmak için JavaScript kullanmak.
- **Karmaşıklık Analizi (Complexity Analysis)**: Algoritma karşılaştırması için yürütme süresini nanosaniyede ölçmek.
# 🐍 Yapay Zeka Modlu Yılan Oyunu

Python'da `tkinter` kütüphanesi kullanılarak uygulanmış klasik bir Yılan oyunu. Bu proje, oyun durumu yönetimini, klavye olay işleme mekanizmasını ve Breadth-First Search (BFS) algoritması kullanılarak temel bir yapay zeka uygulamasını göstermektedir.

## 🚀 Özellikler

- **Klasik Oynanış**: Yılanı yiyecek yemek ve daha uzun büyütmek için hareket ettirin.
- **Dinamik Skorlama**: Yenilen her yiyecek parçası için 10 puan kazanın.
- **Oyun Bitiş Koşulları**: Oyun, yılan ızgaranın sınırlarına veya kendi vücuduna çarparsa sona erer.
- **Otomatik Mod (AI)**: BFS algoritmasını kullanarak yiyeceğe en kısa yolu otomatik olarak bulan yerleşik bir yapay zeka.
- **Kontrol Sistemi**:
  - **Ok Tuşları**: Yılan yönünü değiştirir.
  - **'R' Tuşu**: Oyun bittikten sonra oyunu yeniden başlatır.
  - **'Q' Tuşu**: Uygulamadan çıkar.
  - **'A' Tuşu**: Manuel ve Otomatik mod arasında geçiş yapar.

---

## 📁 Proje Yapısı
```text
17_snake_game/
├── snake_game.py    # Main game loop, state management, and rendering
└── snake_helpers.py # Keyboard handlers and AI (BFS) logic
```
---

## 🛠️ Adım Adım Uygulama Rehberi

### 1. Ön Gereksinimler
Bu proje, Python standart kütüphanesinde bulunan `tkinter` kullanmaktadır. Harici bir pakete gerek yoktur.

### 2. Oyun Durumu Yönetimi (`snake_game.py`)

#### Adım 1: Sabitleri ve Durumu Tanımlama
Yönler için (`UP=0, DOWN=1, LEFT=2, RIGHT=3`) sabitler ve aşağıdaki sözlüğü döndüren bir `make_state` fonksiyonu oluşturun:
- **Vücut Konumu**: Segmentleri temsil eden iki liste (`body_x`, `body_y`), indeks 0 başı temsil eder.
- **Hareket**: Mevcut yön ve buna karşılık gelen koordinat deltaları (`dx`, `dy`).
- **Oyun Durumu**: `score` ve bir `alive` boolean değeri.
- **Yiyecek Konumu**: Rastgele oluşturulmuş `food_x` ve `food_y`.
- **Izgara Boyutu**: Oyun alanının boyutları.

#### Adım 2: Temel Oyun Mantığı
Aşağıdaki fonksiyonları uygulayın:
- **`place_food(state)`**: Yiyecek için rastgele koordinatlar oluşturur. Yiyeceğin, `body_x` ve `body_y` listelerine karşı kontrol edilerek yılanın vücudu üzerinde spawn olmadığından emin olun.
- **`set_direction(state, new_dir)`**: Yılanın yönünü günceller. **Çok Önemli**: "180 derecelik" dönüşleri engelleyin (örneğin, yukarı hareket ediyorsa, yılan hemen aşağı dönemez).
- **`move_snake(state)`**: 
  1. Yeni baş konumunu hesaplar.
  2. Duvarlarla veya yılanın kendi vücuduyla çarpışma kontrolü yapar.
  3. Yiyecek yenirse: Skoru artırır ve `place_food()` çağırır.
  4. Yiyecek yenmezse: Kuyruğun son segmentini kaldırır.
  5. Yeni baş konumunu vücut listelerinin başına ekler.

#### Adım 3: Rendering Motoru
`tkinter.Canvas` kullanarak şunları çizen bir `render` fonksiyonu oluşturun:
- Yiyecek (kırmızı dikdörtgen).
- Yılan vücudu (yeşil/cyan dikdörtgenler).
- Mevcut skor.
- `alive` False olduğunda bir "GAME OVER" katmanı.

---

### 3. Yapay Zeka ve Giriş Yardımcıları (`snake_helpers.py`)

#### Adım 1: Klavye İşleme
`root.bind("<KeyPress>", ...)` için bir geri çağırma (callback) döndüren `make_handler` fonksiyonu oluşturun. Bu handler şunları yapmalıdır:
- Ok tuşlarına göre `next_dir` değişkenini günceller.
- Yeniden başlatma ('R'), çıkış ('Q') ve otomatik mod değiştirme ('A') için bayraklar ayarlar.

#### Adım 2: Yapay Zeka Mantığı (BFS Algoritması)
Yiyeceğe en kısa yolu bulmak için `bfs_next_dir(state)` uygulayın:
- **Engeller**: Tüm yılan vücudu segmentlerini (kuyruk hariç) duvar olarak kabul edin.
- **Kuyruk (Queue)**: Bir Breadth-First Search yapmak için `collections.deque` kullanın.
- **Gezinme (Traversal)**: Dört yönü de keşfedin. Bir hücreye ulaşmak için alınan ilk yönü saklayın.
- **Hedef**: Yiyecek konumu ulaşılırsa, o ilk yönü döndürün.
- **Geri Dönüş (Fallback)**: Yol bulunamazsa, -1 döndürün (düz devam et).

---

### 4. Ana Oyun Döngüsü (`snake_game.py`)

1. **Pencere Kurulumu**: `tk.Tk()` başlatın, bir `Canvas` oluşturun ve klavye handler'ını bağlayın.
2. **Oyun Döngüsü**: Aşağıdakileri tekrarlamak için bir `while True` döngüsü kullanın:
   - Giriş bayraklarını kontrol edin (Yeniden Başlatma, Çıkış, Otomatik Mod değiştirme).
   - Eğer `alive` True ise:
     - **Auto Mode**'da: Yönü ayarlamak için `bfs_next_dir()` çağırın.
     - **Manual Mode**'da: Klavye tarafından yakalanan `next_dir`'i uygulayın.
     - `move_snake()` çağırın.
   - Canvas'ı güncellemek için `render()` çağırın.
   - UI olaylarını işlemek için `root.update()` kullanın.
   - `time.sleep()` kullanarak bir kare gecikmesi uygulayın (örneğin, manuel için 120ms, yapay zeka için 50ms).

---

## 🏃 Nasıl Çalıştırılır

1. Dosyaları bir klasöre kaydedin.
2. Ana betiği çalıştırın:
   ```bash
   python snake_game.py
   ```
3. **Kontroller**:
   - Yön değiştirmek için **Ok Tuşlarını** kullanın.
   - Yapay Zeka (AI) modunu etkinleştirmek için **A** tuşuna basın.
   - Ölümden sonra yeniden başlamak için **R** tuşuna basın.
   - Çıkmak için **Q** tuşuna basın.

---

## 📚 Gösterilen Temel Kavramlar

- **Game Loop Architecture**: Durumu yönetme $\rightarrow$ mantığı güncelleme $\rightarrow$ görselleştirme.
- **Coordinate Geometry**: Hareket ve çarpışma tespiti için bir ızgara sistemi kullanma.
- **BFS (Breadth-First Search)**: Ağırlıksız bir ızgarada en kısa yolu bulma.
- **Event-Driven Programming**: Bir GUI'de asenkron klavye girdilerini işleme.
- **Time Management**: Uyku aralıkları (sleep intervals) aracılığıyla oyun hızını kontrol etme.
- **State Machines**: "Alive", "Game Over" ve "AI Mode" arasındaki geçişleri yönetme.
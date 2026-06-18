# 21 ML Algoritması — Saf Python'da Sıfırdan

**Saf Python** kullanılarak sıfırdan uygulanmış 17 (21'e çıkacak) klasik makine öğrenimi algoritması koleksiyonu — NumPy yok, scikit-learn yok, harici ML kütüphanesi yok. Her algoritma tek bir dosyada kendi kendine yeterli ve yalnızca Python standart kütüphanesi ile çalıştırılabilir.

---

## Proje Hedefleri

- Her algoritmanın matematiksel olarak nasıl çalıştığını anlamak, sadece API'sini nasıl çağıracağını değil
- Her hesaplamayı elle uygulamak: matris işlemleri, optimizasyon döngüleri, olasılık hesaplamaları
- Her algoritma için çalışan bir demo sağlamak, böylece sonuçlar hemen doğrulanabilir

---

## Proje Yapısı
```
21_ml_algorithms/
├── 01_linear_regression.py
├── 02_logistic_regression.py
├── 03_knn.py
├── 04_kmeans.py
├── 05_decision_tree.py
├── 06_naive_bayes.py
├── 07_neural_network.py
├── 08_random_forest.py
├── 09_svm.py
├── 10_pca.py
├── 11_gradient_boosting.py
├── 12_dbscan.py
├── 13_lda.py
├── 14_xgboost.py
├── 15_tsne.py
├── 16_ensemble.py
└── 17_hmm.py
```
Her dosya bağımsızdır. İstediğiniz herhangi birini doğrudan çalıştırabilirsiniz:
```bash
python 01_linear_regression.py
```
---

## Gereksinimler

- Python 3.8 veya üzeri
- Harici paket yok (yalnızca standart kütüphaneden `math`, `random`)

---

## Her Algoritmayı Nasıl Oluşturulur

Aşağıda, her dosyayı sıfırdan oluşturmak için bir rehber bulunmaktadır. Açıklanan deseni, matematiği ve yapıyı takip edin.

---

### 01 — Linear Regression (Doğrusal Regresyon)

**Konsept:** Gradyan İniş (Gradient Descent) kullanarak Ortalama Kare Hata'yı (Mean Squared Error) minimize ederek bir veri kümesi üzerinden `y = w * x + b` doğrusunu uydurmak.

**Uygulama Adımları:**

1. Bir listenin ortalamasını hesaplayan bir `mean(data)` yardımcı fonksiyonu yazın.
2. `mse(y_true, y_pred)` yazın — kare farkların toplamının n'e bölünmesi.
3. `r2_score(y_true, y_pred)` yazın — `1 - SS_res / SS_tot` (burada `SS_res` kare artıkların toplamı ve `SS_tot` ortalama etrafındaki toplam karelerdir).
4. Min-max ölçeklendirme kullanarak bir `normalize(data)` fonksiyonu yazın: `(x - min) / (max - min)`. Tahminlerin daha sonra de-normalize edilebilmesi için normalize edilmiş veriyi, `min_val` ve `max_val` ile birlikte döndürün.
5. Şu bileşenlere sahip bir `LinearRegression` sınıfı oluşturun:
   - `__init__(lr, epochs)` — `weight = 0.0` ve `bias = 0.0` başlatın
   - `fit(x, y)` — gradyan inişi döngüsü: tahminleri hesaplayın, MSE'yi hesaplayın, `dw` ve `db` gradyanlarını hesaplayın, ağırlıkları güncelleyin
   - `predict(x)` — her girdi için `w * x + b` uygulayın
6. Demo'da (`if __name__ == "__main__"`), bir ev büyüklüğü vs fiyat veri kümesi kullanın, her iki ekseni de normalize edin, modeli eğitin, ardından gerçek dünya değerlerini göstermek için tahminleri de-normalize edin.

**Ana formül:** `dw = (2/n) * Σ (ŷ - y) * x`, `db = (2/n) * Σ (ŷ - y)`

---

### 02 — Logistic Regression (Lojistik Regresyon)

**Konsept:** Sigmoid fonksiyonu ve İkili Çapraz-Entropi (Binary Cross-Entropy) kaybı kullanılarak, gradyan inişi ile eğitilmiş ikili sınıflandırma.

**Uygulama Adımları:**

1. `math`'i içe aktarın. `sigmoid(z)` yazın — `1 / (1 + exp(-z))` döndürür.
2. `binary_cross_entropy(y_true, y_pred)` yazın — `-y * log(ŷ) - (1-y) * log(1-ŷ)` ortalaması. `log(0)`'dan kaçınmak için tahminleri kırpın (Clip).
3. `normalize(data)` ve `accuracy(y_true, y_pred)`'i yeniden kullanın veya yeniden yazın.
4. Bir `LogisticRegression` sınıfı oluşturun:
   - `__init__(lr, epochs)` — ağırlık vektörü `w` ve `bias = 0.0` başlatın
   - `fit(X, y)` — her epoch için: ağırlıklar ile her girdi arasındaki nokta çarpımını hesaplayın, sigmoid uygulayın, BCE kaybını hesaplayın, ardından gradyanları hesaplayın ve `w` ile `bias`'ı güncelleyin
   - `predict(X)` — sigmoid çıktısı > 0.5 ise 1, değilse 0 döndürün
5. Demo: Bir veri kümesini sınıflandırın (örneğin, çalışma saatleri vs sınav geçme/kalma).

**Ana formül:** `dw_j = (1/n) * Σ (ŷ_i - y_i) * x_ij`

---

### 03 — K-Nearest Neighbors (KNN)

**Konsept:** Bir noktayı, en yakın K eğitim örneğine bakarak ve çoğunluk oyu alarak sınıflandırmak.

**Uygulama Adımları:**

1. `math`'i içe aktarın. Çok boyutlu noktalar için `euclidean(x1, x2)` ve isteğe bağlı olarak `manhattan(x1, x2)` uzaklık fonksiyonları yazın.
2. `majority_vote(labels, num_classes)` yazın — bir listedeki her sınıfın oluşum sayısını sayar ve en yaygın olanı döndürür.
3. `accuracy(y_true, y_pred)` yazın.
4. Bir `KNNClassifier` sınıfı oluşturun:
   - `__init__(k, metric)` — K'yı ve uzaklık fonksiyonu seçimini saklayın
   - `fit(X, y)` — sadece eğitim verisini saklar (KNN tembeldir/lazy)
   - `predict_single(x)` — tüm eğitim noktalarına uzaklığı hesaplar, en küçük K'yı seçer, çoğunluk oyu döndürür
   - `predict(X)` — her örnek için `predict_single` çağırır
5. Demo: Iris veri kümesi (basitlik için yalnızca 2 özellik kullanın), K değerleri 1, 3, 5'i deneyin.

---

### 04 — K-Means Clustering (K-Ortalamalar Kümeleme)

**Konsept:** n veri noktasını, her noktayı yinelemeli olarak en yakın merkezcilere atayarak ve ardından merkezcilere yeniden hesaplayarak K kümesine bölmek.

**Uygulama Adımları:**

1. Yardımcı fonksiyonlar yazın: `euclidean_sq(x1, x2)` (kare uzaklık karşılaştırmalar için daha hızlıdır), `copy_point(src)`, yakınsama kontrolü için `points_equal(a, b, tol)`.
2. Bir `KMeans` sınıfı oluşturun:
   - `__init__(k, max_iter, tol)` — hiperparametreleri saklayın; merkezciler boş başlar
   - `_init_centroids(X)` — X'ten K rastgele nokta seçerek başlangıç merkezcileri olarak belirleyin
   - `_assign(X)` — her nokta için en yakın merkezcilere indeksini bulun
   - `_update(X, labels)` — her merkezcilere atanan tüm noktaların ortalaması olarak yeniden hesaplayın
   - `fit(X)` — yineleyin: ata → güncelle → yakınsama kontrolü
   - `predict(X)` — yeni noktaları en yakın merkezcilere atayın
3. Kümeleme kalitesini değerlendirmek için `inertia`'yı (atanan merkezcilere olan kare uzaklıkların toplamı) takip edin.
4. Demo: 3 doğal küme içeren 2D sentetik veri. Her noktanın hangi kümeye ait olduğunu yazdırın ve küme sembollerini gösterin (örneğin, `●`, `■`, `▲`).

---

### 05 — Decision Tree Classifier (Karar Ağacı Sınıflandırıcı)

**Konsept:** Gini saflığını en çok azaltan özellik ve eşik değeri üzerinde veriyi özyinelemeli olarak bölerek ikili bir ağaç oluşturmak.

**Uygulama Adımları:**

1. `gini_impurity(labels, indices, n_classes)` yazın — her sınıf c için `1 - Σ (count_c / n)²`.
2. Yaprak tahminleri için `majority_class(labels, indices, n_classes)` yazın.
3. Saf düğümleri tespit etmek için `all_same_class(labels, indices)` yazın.
4. Aday bölme eşiklerini almak için `unique_values(x, feature, indices)` yazın.
5. Dahili bir düğüm listesi ( `feat`, `threshold`, `left`, `right`, `leaf_class` için paralel diziler) kullanarak bir `DecisionTree` sınıfı oluşturun:
   - `__init__(max_depth, min_samples_split)`
   - `_best_split(x, y, indices)` — her özellik × eşik kombinasyonunu dener, en düşük ağırlıklı Gini'yi döndürür
   - `_build(x, y, indices, depth)` — ağacı özyinelemeli olarak büyütür; maksimum derinlikte, saf düğümlerde veya çok az örnekte durur
   - `fit(x, y)` — kökten `_build` çağrılır
   - `predict_single(x)` — ağacı dolaşır: eğer `x[feat] <= threshold` ise sola, değilse sağa gider
6. Demo: Tenis veri kümesi — 4 kategorik benzeri özellik (hava durumu, nem, rüzgar, sıcaklık) tamsayı olarak kodlanmıştır.

---

### 06 — Gaussian Naive Bayes (Gauss Naif Bayes)

**Konsept:** Her sınıf için her özelliği bir Gauss dağılımı olarak modellemek. En yüksek olası koşullu olasılığa sahip sınıfı seçerek tahmin yapmak.

**Uygulama Adımları:**

1. `math`'ı import edin. `mean(data)` ve `variance(data, mu)` — popülasyon varyansı yazın.
2. `gaussian_log_prob(x, mu, var)` — Gaussian PDF'nin logaritması: `-0.5 * log(2π * var) - (x - mu)² / (2 * var)`. Log alanını kullanmak underflow'u önler.
3. Bir `GaussianNB` sınıfı oluşturun:
   - `__init__()` — sınıf başına prior ve sınıf başına, özellik başına (ortalama, varyans) çiftleri için depolama
   - `fit(X, y)` — örnekleri sınıfa göre gruplayın; log prior = `log(count / n)` hesaplayın; her sınıf için her özellik için ortalama ve varyansı hesaplayın
   - `predict_single(x)` — her sınıf için, log prior + Σ gaussian_log_prob'yi her özellik için toplayın; en yüksek puana sahip sınıfı döndürün
4. Demo: Iris veri seti, yaprak uzunluğu ve yaprak genişliği özelliklerini kullanarak.

---

### 07 — Sinir Ağı (Neural Network)

**Konsept:** Tek bir gizli katman ve sigmoid aktivasyonları ile beslemeli bir ağ (feedforward network), backpropagation yoluyla eğitilir.

**Uygulama Adımları:**

1. `math`'ı import edin. Tüm matris işlemlerini iç içe listeler kullanarak sıfırdan uygulayın: `mat_mul(A, B, m, k, n)`, `mat_transpose(A)`, `mat_add_bias(A, b)`, `mat_sigmoid(A)`, `mat_scale(A, s)`.
2. `sigmoid(z)`, `sigmoid_deriv(a)` (z'ye değil, aktivasyona göre verilir) ve `clip(v, lo, hi)` yazın.
3. Bir `NeuralNetwork` sınıfı oluşturun:
   - `__init__(n_input, n_hidden, lr, epochs)` — `W1` (n_hidden × n_input) ve `W2` (1 × n_hidden) başlangıç ağırlıklarını Xavier tarzı ölçeklendirme ile başlatın: `scale = sqrt(2 / fan_in)`; bias'ları `b1`, `b2` sıfıra başlatın
   - `forward(x)` — `z1 = x @ W1.T + b1`, `a1 = sigmoid(z1)`, `z2 = a1 @ W2.T + b2`, `a2 = sigmoid(z2)` hesaplayın; `a1, a2`'yi döndürün
   - `fit(x, y)` — eğitim döngüsü: forward pass → Binary Cross-Entropy loss hesapla → `W2`, `b2`, `W1`, `b1` üzerinden backprop gradientleri hesapla → tüm ağırlıkları güncelle
   - `predict(x)` — `a2 > 0.5` eşiğiyle tahmin yap
4. Demo: XOR problemi — 4 örnek, 2 giriş, 1 çıkış. Lineer bir model XOR'u çözemez; gizli katman bunu mümkün kılar.

**Temel backprop denklemleri:**
- `dz2 = a2 - y`
- `dW2 = (1/n) * dz2.T @ a1`
- `dz1 = (dz2 @ W2) * sigmoid_deriv(a1)`
- `dW1 = (1/n) * dz1.T @ x`

---

### 08 — Random Forest

**Konsept:** Veri ve özelliklerin rastgele alt kümeleri üzerinde birçok karar ağacı eğitilir; tahminler çoğunluk oyuyla birleştirilir.

**Uygulama Adımları:**

1. `math`, `random`'ı import edin. Karar Ağacından `gini_impurity`, `majority_class`, `all_same_class`'ı yeniden kullanın veya yeniden yazın.
2. `best_split(x, y, indices, n_classes, n_features, max_features)` yazın — Karar Ağacındaki en iyi bölme ile aynı, ancak her düğümde dikkate alınacak `max_features` kadar özelliği rastgele örnekler (bu, düz bir karar ağacından temel farktır).
3. `DecisionTreeNode` ve `DecisionTree` sınıflarını oluşturun (dosya 05'e benzer, ancak özellik örneklemeli bölme kullanılarak).
4. Bir `RandomForest` sınıfı oluşturun:
   - `__init__(n_trees, max_depth, min_samples_split, max_features, seed)`
   - `_bootstrap(X, y)` — eğitim kümesinden yerine koyarak n indeks örnekle
   - `fit(X, y)` — her ağaç için: veriyi bootstrapla, bir `DecisionTree` eğit, sakla
   - `predict(X)` — her örnek için, tüm ağaçlardan tahminleri topla ve çoğunluk oyu al
5. Demo: Iris veri seti (3 sınıf, 4 özellik). Tek ağaç ile orman doğruluğunu karşılaştırın.

---

### 09 — Destek Vektör Makinesi (SVM)

**Konsept:** İki sınıf arasındaki marjı maksimize eden hiper düzlemi bulur. Hinge loss + SGD kullanır. One-vs-Rest ile çok sınıfa genişletilir.

**Uygulama Adımları:**

1. `math`'ı import edin. `dot(w, x)` — iki listenin nokta çarpımını yazın. Özellik ölçeklendirmesi için `normalize_data(data)` yazın (SVM'lerin iyi çalışması için gereklidir).
2. Bir `LinearSVM` sınıfı oluşturun (ikili):
   - `__init__(lr, C, epochs)` — `C` düzenlileştirme parametresidir; `w` ve `bias`'ı başlatın
   - `fit(X, y)` — y {-1, +1} olmalıdır; her epoch için, her örnek için: eğer `y * (w·x + b) < 1` (hinge bölgesi) ise, hem düzenlileştirme hem de kayıp terimleri ile gradient güncellemesi uygula; aksi takdirde sadece düzenlileştirme güncellemesini uygula
   - `predict(X)` — `sign(w·x + b)`'yi döndür
3. Bir `SVM_OvR` sınıfı oluşturun (çok sınıf için One-vs-Rest):
   - `fit(X, y)` — her sınıf için bir `LinearSVM` eğit, o sınıfı +1 ve diğer tüm sınıfları -1 olarak kodlayarak
   - `predict(X)` — her örnek için, her ikili SVM'den ham skoru `w·x + b` al; en yüksek skora sahip sınıfı döndür
4. Demo: İkili XOR tarzı veri seti, ardından Iris 3-sınıflı.

---

### 10 — Temel Bileşen Analizi (PCA)

**Konsept:** Kovaryans matrisinin özvektörlerini kullanarak maksimum varyansın ortogonal yönlerini bulur. Veriyi en iyi K bileşenlerine yansıtır.

**Uygulama Adımları:**

1. `math`'ı import edin. Sıfırdan matris yardımcıları yazın: `mat_zeros`, `mat_copy`, `mat_transpose`, `mat_mul`.
2. `power_iteration(A, n_iter)` — simetrik bir matrisin baskın özvektörünü, rastgele bir vektörü tekrar tekrar çarparak ve normalize ederek bulur. Bu, tam bir özdekompozisyon uygulamaktan kaçınır.
3. Bir `PCA` sınıfı oluşturun:
   - `__init__(n_components)`
   - `fit(X)` — sütun ortalamalarını hesapla; X'i merkezle; kovaryans matrisini `C = X_centered.T @ X_centered / (n-1)` hesapla; azaltma (bulunan bileşeni bir sonrakiyi bulmadan önce C'den çıkarmak) ile power iteration kullanarak `n_components` özvektörünü çıkar
   - `transform(X)` — X'i merkezle ve depolanan bileşenlere yansıt: `Z = X_centered @ components.T`
4. Demo: Iris 4D → 2D. Her bileşen için açıklanan varyans oranını yazdırın.

---

### 11 — Gradyan Artırımlı Regresör (Gradient Boosting Regressor)

**Konsept:** Yüzeysel regresyon ağaçları eğitilerek bir topluluk oluşturulur; her biri bir önceki topluluğun kalıntılarını (hata) uygun hale getirir.

**Uygulama Adımları:**

### 12 — DBSCAN

**Konsept:** Yoğunluk tabanlı kümeleme yöntemidir; birbirine yakın olan noktaları gruplar ve aykırı değerleri (outliers) gürültü (noise) olarak işaretler. Önceden K değerini belirtmeyi gerektirmez.

**Uygulama Adımları:**

1. `math`'ı içe aktarın. `euclidean(a, b)` fonksiyonunu yazın.
2. `region_query(X, idx, eps)` yazın — `idx` noktasından `eps` mesafesi içindeki tüm noktaların indekslerini döndürür.
3. Bir `DBSCAN` sınıfı oluşturun:
   - `__init__(eps, min_samples)` — `eps` komşuluk yarıçapıdır; `min_samples` ise bir çekirdek (core) nokta olmak için gereken minimum sayıdır.
   - `fit(X)` — tüm etiketleri -1 (gürültü) olarak başlatın. Her ziyaret edilmemiş nokta için: komşularını alın; eğer `min_samples`'tan azsa, gürültü olarak işaretleyin; aksi takdirde yeni bir küme başlatın ve BFS/queue yoluyla tüm yoğunluk-ulaşılabilir (density-reachable) noktaları ekleyerek genişletin.
   - `labels_` — küme atamalarının listesi (-1 = gürültü, 0, 1, 2, ...)
4. Demo: 3 küme ve dağınık gürültü noktaları içeren 2D sentetik veri.

**Uygulanması Gereken Ana Konsept:** "Sınır noktaları" (border points), kendileri yeterli komşuya sahip olmasalar bile, bir çekirdek noktanın komşuluğunda bulunmaları durumunda bir kümeye aitlerdir.

---

### 13 — Lineer Diskriminant Analizi (LDA)

**Konsept:** Sınıflar arası saçılımın (between-class scatter) sınıf içi saçılığa (within-class scatter) oranını maksimize eden özelliklerin lineer kombinasyonlarını bulur. Hem sınıflandırma hem de boyut indirgeme için kullanılır.

**Uygulama Adımları:**

1. `math`'ı içe aktarın. Matris yardımcı fonksiyonları yazın: `mat_zeros`, `mat_add`, `mat_scale`, `mat_mul`, `mat_transpose`.
2. Özvektörleri çıkarmak için `power_iteration(M, n_iter)` yazın.
3. `deflate(M, v)` yazın — matris M'den bileşen `v`'yi çıkarır: `M = M - (v @ v.T) * (v.T @ M @ v)`.
4. Gauss-Jordan eliminasyonu kullanarak `mat_inv_nxn(M)` — n×n matris tersini yazın.
5. Bir `LDA` sınıfı oluşturun:
   - `__init__(n_components)`
   - `fit(X, y)` — genel ortalamayı ve sınıf bazlı ortalamaları hesaplayın; sınıf içi saçılım matrisi `S_W` ve sınıf arası saçılım matrisi `S_B`'yi hesaplayın; `S_W⁻¹ @ S_B`'yi hesaplayın; güç yinelemesi (power iteration) + deflasyon kullanarak en üst `n_components` özvektörünü çıkarın.
   - `transform(X)` — X'i öğrenilen bileşenlere yansıtın.
   - `predict(X)` — X'i yansıtın; yansıtılmış uzaydaki en yakın sınıf merkezine göre sınıflandırın.
6. Demo: Iris 4D → 2D ile 3-sınıflı sınıflandırma.

---

### 14 — XGBoost Sınıflandırıcı

**Konsept:** Kaybın ikinci dereceden Taylor yaklaşımı ile yapılan gradient boosting. Temel öğrenici olarak regresyon saplamaları (shallow trees) kullanır ve çok sınıflı problem için softmax kullanır.

**Uygulama Adımları:**

1. `math`'ı içe aktarın. `softmax(scores)` yazın — `max` çıkarma işlemi kullanılarak sayısal olarak kararlı hale getirilir.
2. Bir `RegressionStump` sınıfı oluşturun (maksimum derinlik sınırlı regresyon ağacı):
   - Önceki ağaçlar gibi aynı özyinelemeli yapıyı kullanır, ancak düğümleri düğüm kimliği ile indekslenmiş paralel düz dizilerde (`feat`, `thr`, `left`, `right`, `val`) depolar.
   - `fit(X, residuals)` — sözde-kalıntılara (pseudo-residuals) göre uyum sağlar.
   - `predict_single(x)` — düğüm dizisinde gezinir.
3. Bir `XGBoostClassifier` sınıfı oluşturun:
   - `__init__(n_estimators, lr, max_depth, n_classes)`
   - `fit(X, y)` — her sınıf için skorları 0 olarak başlatın; her tur için: mevcut skorlardan softmax olasılıklarını hesaplayın; sözde-kalıntıları `p - one_hot(y)` olarak hesaplayın; her sınıf için bir saplamaya (stump) uyum sağlayın; o sınıfın skorlarını `lr * stump.predict(X)` ile güncelleyin.
   - `predict(X)` — `argmax(softmax(scores))` değerini döndürür.
4. Demo: Iris 3-sınıflı. Sınıfa özel ağaç sayılarını ve test doğruluğunu yazdırın.

---

### 15 — t-SNE

**Konsept:** Yüksek boyutlu veriyi yerel komşuluk yapısını koruyarak 2D'ye eşler. Olasılıksal bir benzerlik ölçüsü ve gradient descent kullanır.

**Uygulama Adımları:**

1. `math`, `random`'ı içe aktarın. `pairwise_sq_dist(X)` yazın — kare Euclidean mesafelerinin n×n matrisi.
2. `compute_row_prob(D_row, i, n, target_perp, perplexity)` yazın — hedef perplexity'yi sağlayan bant genişliği `sigma` için ikili arama yapar; koşullu olasılık satırı `p(j|i)`'yi döndürür.
3. Bir `TSNE` sınıfı oluşturun:
   - `__init__(n_components, perplexity, lr, n_iter, seed)`
   - `fit_transform(X)`:
     - Çift boyutlu yüksek boyutlu olasılıkları P hesaplayın (simetrizasyon: `P_ij = (p_j|i + p_i|j) / 2n`)
     - 2D gömülmesini `Y` rastgele başlatın.
     - Her yineleme için: çift boyutlu düşük boyutlu Student-t benzerliklerini Q hesaplayın; gradyanı `dY = 4 * Σ_j (P_ij - Q_ij) * (Y_i - Y_j) * (1 + ||Y_i - Y_j||²)⁻¹` hesaplayın; Y'yi gradient descent ve momentum ile güncelleyin.
   - Nihai 2D gömülmesini döndürün.
4. Demo: Iris 4D → 2D. 2D koordinatları yazdırın ve her noktanın hangi sınıfa ait olduğunu gösterin.

**Not:** Bu, büyük veri kümelerinde saf Python'da hesaplama açısından yavaştır. Demo'yu ~150 örnek ve ~500 yinelemeyle sınırlı tutun.

---

### 16 — Ensemble Methods (Oylama ve Stacking)

**Konsept:** Birden fazla temel sınıflandırıcıyı birleştirerek herhangi bir bireysel modelden daha iyi tahminler üretmek.

**Uygulama Adımları:**

1. `math`'ı İçe Aktar. `euclidean(a, b)` yaz.
2. `fit`, `predict_single` ve `predict_proba_single` (stacking için gerekli) içeren minimal bir `KNN` sınıfı uygula.
3. Bir `VotingClassifier` sınıfı oluştur (Hard Voting):
   - `__init__(classifiers)` — temel sınıflandırıcı örnekleri listesi
   - `fit(X, y)` — her sınıflandırıcıyı aynı veri üzerinde eğit
   - `predict(X)` — her örnek için her sınıflandırıcıdan bir tahmin topla ve çoğunluk oyu döndür
4. Bir `StackingClassifier` sınıfı oluştur:
   - `__init__(base_classifiers, meta_classifier, n_classes)`
   - `fit(X, y)` — tüm temel sınıflandırıcıları eğit; her eğitim örneği için tüm temel sınıflandırıcıların olasılık çıktılarını birleştirerek "meta-özellikler" oluştur; meta-sınıflandırıcıyı bu meta-özellikler üzerinde eğit
   - `predict(X)` — tüm temel sınıflandırıcılardan olasılık vektörleri al; meta-özellikler oluşturmak için birleştir; meta-sınıflandırıcı ile tahmin yap
5. Demo: Iris 3-sınıflı. Bireysel sınıflandırıcılar vs Voting vs Stacking doğruluğunu karşılaştır.

---

### 17 — Hidden Markov Model (HMM)

**Konsept:** Gizli durumları olan sıralı veriler için olasılıksal bir model. Dört klasik HMM algoritmasını uygular.

**Uygulama Adımları:**

1. `math`'ı İçe Aktar. `LOG_ZERO = -1e18` tanımla. `log_add(a, b)` yaz — sayısal olarak kararlı log-sum-exp: `max(a, b) + log(1 + exp(min - max))`.
2. Bir `HMM` sınıfı oluştur:
   - `__init__(n_states, n_obs)` — üniform geçiş matrisi `A` (n_states × n_states), emisyon matrisi `B` (n_states × n_obs) ve başlangıç dağılımı `pi`'yi başlat
   - `forward(obs)` — Forward algoritması: `alpha[t][s]` = t'ye kadar gözlemlerin ve s durumunda olmanın olasılığı; `log P(obs | model)`'i döndür
   - `backward(obs)` — Backward algoritması: `beta[t][s]` = t'deki s durumuna bağlı gelecekteki gözlemlerin olasılığı
   - `viterbi(obs)` — Viterbi algoritması: geri izleme (traceback) ile dinamik programlama kullanarak en olası gizli durum dizisini bul
   - `baum_welch(obs_seqs, n_iter)` — Etiketlenmemiş dizilerden A, B, pi öğrenmek için EM algoritması: E-adımı forward/backward hesaplar; M-adımı durum işgal sayılarından parametreleri yeniden tahmin eder
3. Demo 1 — Dürüst Olmayan Kumarhane: 2 durum (Adil zar / Yüklenmiş zar), 6 gözlem; A ve B'yi manuel olarak ayarla, ardından bir zar atma dizisi üzerinde Viterbi çalıştır.
4. Demo 2 — Iris yaprak sırası: yaprak uzunluklarını kutulara ayrıştır, 2 durumlu bir HMM öğrenmek için Baum-Welch çalıştır, eğitim öncesi ve sonrası log-olasılığını karşılaştır.

---

## Tüm Süreç Boyunca Kullanılan Design Patterns

**Ağaçlar için düz düğüm dizileri:** Özyinelemeli `TreeNode` nesneleri yerine, ağaçlar düğümleri düğüm kimliği ile indekslenmiş paralel listeler (`feat`, `thr`, `left_child`, `right_child`, `leaf_value`) olarak depolar. Bu, nesne yükünden kaçınır ve yinelemeli olarak dolaşması kolaydır.

**Log-uzay olasılığı:** Çarpılan olasılıkları içeren herhangi bir algoritma (Naive Bayes, HMM) kayan nokta alt taşmasına (floating point underflow) kaçınmak için log-uzayda çalışır.

**Özdeğerler için Power iteration:** Tam bir özdeğer çözücü (eigensolver) uygulamaktan kaçınılır. Baskın özvektör çıkarılır, ardından matris deflat edilir ve sonraki bileşenler için tekrarlanır (PCA, LDA).

**Ön işleme sözleşmesi olarak Normalizasyon:** Gradyan iniş kullanan her demo, girdileri önce [0, 1]'e normalleştirir, ardından tahminleri okunabilir birimlerde göstermek için de-normalize eder.

**`if __name__ == "__main__"` demoları:** Her dosya doğrudan çalıştırıldığında tamamen çalışmış bir örnek çalıştırır. Demo, ayrı bir betik değil, dosyanın bir parçasıdır.

---

## Önerilen Yapılandırma Sırası

Bu projeyi sıfırdan inşa ediyorsanız, daha sonraki algoritmalar önceki olanlardan desenler oluşturduğu için dosyaları bu sırayla uygulayın:

1. Linear Regression → gradyan inişi desenini oluşturur
2. Logistic Regression → sigmoid ve BCE kaybını ekler
3. KNN → uzaklık fonksiyonlarını ve çok boyutlu veriyi tanıtır
4. Decision Tree → özyinelemeli bölmeyi ve Gini saflığını tanıtır
5. Naive Bayes → olasılıksal, log-uzay sınıflandırmayı tanıtır
6. K-Means → yinelemeli merkez tabanlı kümelemeyi tanıtır
7. PCA → matris matematiğini ve power iteration'ı tanıtır
8. Neural Network → matris işlemleriyle forward/backward geçişi tanıtır
9. Random Forest → Decision Tree'yi bootstrapping ile genişletir
10. SVM → marj tabanlı optimizasyonu tanıtır
11. LDA → PCA'yı sınıf farkındalıklı projeksiyonlarla genişletir
12. DBSCAN → yoğunluk tabanlı kümelemeyi tanıtır
13. Gradient Boosting → sıralı ensemble öğrenmeyi tanıtır
14. XGBoost → ikinci dereceden gradyanlarla Gradient Boosting'i genişletir
15. Ensemble (Voting/Stacking) → daha önce oluşturulmuş sınıflandırıcıları birleştirir
16. t-SNE → doğrusal olmayan boyut indirgemeyi tanıtır
17. HMM → sıralı olasılıksal modellemeyi tanıtır

---

## Tüm Algoritmaları Çalıştırma
```bash
for f in *.py; do
    echo "=== Running $f ==="
    python "$f"
    echo
done
```
## Lisans

MIT — kullanmak, incelemek ve değiştirmek için ücretsizdir.
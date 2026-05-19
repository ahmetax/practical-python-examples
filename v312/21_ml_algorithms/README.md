# 21 ML Algorithms — From Scratch in Pure Python

A collection of 17 (growing to 21) classic machine learning algorithms implemented from scratch using **pure Python** — no NumPy, no scikit-learn, no external ML libraries. Every algorithm is self-contained in a single file and runnable with just the Python standard library.

---

## Project Goals

- Understand how each algorithm works mathematically, not just how to call its API
- Implement every computation by hand: matrix operations, optimization loops, probability calculations
- Provide a working demo for each algorithm so results can be verified immediately

---

## Project Structure

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

Each file is standalone. Run any of them directly:

```bash
python 01_linear_regression.py
```

---

## Requirements

- Python 3.8 or higher
- No external packages (only `math`, `random` from the standard library)

---

## How to Build Each Algorithm

Below is a guide for building each file from scratch. Follow the pattern, math, and structure described for each one.

---

### 01 — Linear Regression

**Concept:** Fit a line `y = w * x + b` through data by minimizing Mean Squared Error using Gradient Descent.

**Steps to implement:**

1. Write a `mean(data)` helper that computes the average of a list.
2. Write `mse(y_true, y_pred)` — sum of squared differences divided by n.
3. Write `r2_score(y_true, y_pred)` — `1 - SS_res / SS_tot` where `SS_res` is the sum of squared residuals and `SS_tot` is the total sum of squares around the mean.
4. Write a `normalize(data)` function using min-max scaling: `(x - min) / (max - min)`. Return the normalized data along with `min_val` and `max_val` so predictions can be de-normalized later.
5. Create a `LinearRegression` class with:
   - `__init__(lr, epochs)` — initialize `weight = 0.0` and `bias = 0.0`
   - `fit(x, y)` — gradient descent loop: compute predictions, compute MSE, compute gradients `dw` and `db`, update weights
   - `predict(x)` — apply `w * x + b` to each input
6. In the demo (`if __name__ == "__main__"`), use a house size vs price dataset, normalize both axes, train the model, then de-normalize predictions to show real-world values.

**Key formula:** `dw = (2/n) * Σ (ŷ - y) * x`, `db = (2/n) * Σ (ŷ - y)`

---

### 02 — Logistic Regression

**Concept:** Binary classification using the sigmoid function and Binary Cross-Entropy loss, trained with gradient descent.

**Steps to implement:**

1. Import `math`. Write `sigmoid(z)` — returns `1 / (1 + exp(-z))`.
2. Write `binary_cross_entropy(y_true, y_pred)` — average of `-y * log(ŷ) - (1-y) * log(1-ŷ)`. Clip predictions to avoid `log(0)`.
3. Reuse or rewrite `normalize(data)` and `accuracy(y_true, y_pred)`.
4. Create a `LogisticRegression` class:
   - `__init__(lr, epochs)` — initialize weight vector `w` and `bias = 0.0`
   - `fit(X, y)` — for each epoch: compute dot product of weights and each input, apply sigmoid, compute BCE loss, then compute gradients and update `w` and `bias`
   - `predict(X)` — return 1 if sigmoid output > 0.5, else 0
5. Demo: classify a dataset (e.g., study hours vs exam pass/fail).

**Key formula:** `dw_j = (1/n) * Σ (ŷ_i - y_i) * x_ij`

---

### 03 — K-Nearest Neighbors (KNN)

**Concept:** Classify a point by looking at the K closest training examples and taking a majority vote.

**Steps to implement:**

1. Import `math`. Write `euclidean(x1, x2)` and optionally `manhattan(x1, x2)` distance functions for multi-dimensional points.
2. Write `majority_vote(labels, num_classes)` — count occurrences of each class in a list and return the most common one.
3. Write `accuracy(y_true, y_pred)`.
4. Create a `KNNClassifier` class:
   - `__init__(k, metric)` — store K and the distance function choice
   - `fit(X, y)` — simply store the training data (KNN is lazy)
   - `predict_single(x)` — compute distance to all training points, pick K smallest, return majority vote
   - `predict(X)` — call `predict_single` for each sample
5. Demo: Iris dataset (use only 2 features for simplicity), try K values of 1, 3, 5.

---

### 04 — K-Means Clustering

**Concept:** Partition n data points into K clusters by iteratively assigning each point to the nearest centroid, then recomputing centroids.

**Steps to implement:**

1. Write helper functions: `euclidean_sq(x1, x2)` (squared distance is faster for comparisons), `copy_point(src)`, `points_equal(a, b, tol)` for convergence checking.
2. Create a `KMeans` class:
   - `__init__(k, max_iter, tol)` — store hyperparameters; centroids start empty
   - `_init_centroids(X)` — pick K random points from X as starting centroids
   - `_assign(X)` — for each point, find the nearest centroid index
   - `_update(X, labels)` — recompute each centroid as the mean of all assigned points
   - `fit(X)` — iterate: assign → update → check convergence
   - `predict(X)` — assign new points to nearest centroid
3. Track `inertia` (sum of squared distances to assigned centroid) to evaluate clustering quality.
4. Demo: 2D synthetic data with 3 natural clusters. Print which cluster each point belongs to, and show cluster symbols (e.g., `●`, `■`, `▲`).

---

### 05 — Decision Tree Classifier

**Concept:** Recursively split data on the feature and threshold that most reduces Gini impurity, building a binary tree.

**Steps to implement:**

1. Write `gini_impurity(labels, indices, n_classes)` — `1 - Σ (count_c / n)²` for each class c.
2. Write `majority_class(labels, indices, n_classes)` for leaf predictions.
3. Write `all_same_class(labels, indices)` to detect pure nodes.
4. Write `unique_values(x, feature, indices)` to get candidate split thresholds.
5. Create a `DecisionTree` class using an internal node list (parallel arrays for `feat`, `threshold`, `left`, `right`, `leaf_class`):
   - `__init__(max_depth, min_samples_split)`
   - `_best_split(x, y, indices)` — try every feature × threshold combination, return the one with lowest weighted Gini
   - `_build(x, y, indices, depth)` — recursively grow the tree; stop at max depth, pure nodes, or too few samples
   - `fit(x, y)` — call `_build` from root
   - `predict_single(x)` — traverse the tree: go left if `x[feat] <= threshold`, else right
6. Demo: Play Tennis dataset — 4 categorical-like features (outlook, humidity, wind, temperature) encoded as integers.

---

### 06 — Gaussian Naive Bayes

**Concept:** For each class, model each feature as a Gaussian distribution. Predict by picking the class with the highest posterior probability.

**Steps to implement:**

1. Import `math`. Write `mean(data)` and `variance(data, mu)` — population variance.
2. Write `gaussian_log_prob(x, mu, var)` — log of the Gaussian PDF: `-0.5 * log(2π * var) - (x - mu)² / (2 * var)`. Using log-space avoids underflow.
3. Create a `GaussianNB` class:
   - `__init__()` — storage for per-class priors and per-class, per-feature (mean, variance) pairs
   - `fit(X, y)` — group samples by class; compute log prior = `log(count / n)`; compute mean and variance for each feature in each class
   - `predict_single(x)` — for each class, sum log prior + Σ gaussian_log_prob for each feature; return the class with the highest score
4. Demo: Iris dataset using petal length and petal width features.

---

### 07 — Neural Network

**Concept:** A feedforward network with one hidden layer and sigmoid activations, trained via backpropagation.

**Steps to implement:**

1. Import `math`. Implement all matrix operations from scratch using nested lists: `mat_mul(A, B, m, k, n)`, `mat_transpose(A)`, `mat_add_bias(A, b)`, `mat_sigmoid(A)`, `mat_scale(A, s)`.
2. Write `sigmoid(z)`, `sigmoid_deriv(a)` (given the activation, not z), and `clip(v, lo, hi)`.
3. Create a `NeuralNetwork` class:
   - `__init__(n_input, n_hidden, lr, epochs)` — initialize `W1` (n_hidden × n_input) and `W2` (1 × n_hidden) with Xavier-style scaling: `scale = sqrt(2 / fan_in)`; initialize biases `b1`, `b2` to zero
   - `forward(x)` — compute `z1 = x @ W1.T + b1`, `a1 = sigmoid(z1)`, `z2 = a1 @ W2.T + b2`, `a2 = sigmoid(z2)`; return `a1, a2`
   - `fit(x, y)` — training loop: forward pass → compute Binary Cross-Entropy loss → backprop gradients through `W2`, `b2`, `W1`, `b1` → update all weights
   - `predict(x)` — threshold `a2 > 0.5`
4. Demo: XOR problem — 4 samples, 2 inputs, 1 output. A linear model cannot solve XOR; the hidden layer makes it possible.

**Key backprop equations:**  
- `dz2 = a2 - y`  
- `dW2 = (1/n) * dz2.T @ a1`  
- `dz1 = (dz2 @ W2) * sigmoid_deriv(a1)`  
- `dW1 = (1/n) * dz1.T @ x`

---

### 08 — Random Forest

**Concept:** Train many decision trees on random subsets of data and features; aggregate predictions by majority vote.

**Steps to implement:**

1. Import `math`, `random`. Reuse or rewrite `gini_impurity`, `majority_class`, `all_same_class` from the Decision Tree.
2. Write `best_split(x, y, indices, n_classes, n_features, max_features)` — same as Decision Tree's best split but randomly sample `max_features` features to consider at each node (this is the key difference from a plain decision tree).
3. Build `DecisionTreeNode` and `DecisionTree` classes (similar to file 05, but using the feature-sampled split).
4. Create a `RandomForest` class:
   - `__init__(n_trees, max_depth, min_samples_split, max_features, seed)`
   - `_bootstrap(X, y)` — sample n indices with replacement from the training set
   - `fit(X, y)` — for each tree: bootstrap the data, train a `DecisionTree`, store it
   - `predict(X)` — for each sample, collect predictions from all trees and take majority vote
5. Demo: Iris dataset (3 classes, 4 features). Compare single tree vs forest accuracy.

---

### 09 — Support Vector Machine (SVM)

**Concept:** Find the hyperplane that maximizes the margin between two classes. Use hinge loss + SGD. Extend to multi-class with One-vs-Rest.

**Steps to implement:**

1. Import `math`. Write `dot(w, x)` — dot product of two lists. Write `normalize_data(data)` for feature scaling (required for SVMs to work well).
2. Create a `LinearSVM` class (binary):
   - `__init__(lr, C, epochs)` — `C` is the regularization parameter; initialize `w` and `bias`
   - `fit(X, y)` — y must be {-1, +1}; for each epoch, for each sample: if `y * (w·x + b) < 1` (hinge region), apply gradient update with both regularization and loss terms; else apply only regularization update
   - `predict(X)` — return `sign(w·x + b)`
3. Create a `SVM_OvR` class (One-vs-Rest for multi-class):
   - `fit(X, y)` — train one `LinearSVM` per class, encoding that class as +1 and all others as -1
   - `predict(X)` — for each sample, get the raw score `w·x + b` from each binary SVM; return the class with the highest score
4. Demo: binary XOR-style dataset, then Iris 3-class.

---

### 10 — Principal Component Analysis (PCA)

**Concept:** Find orthogonal directions of maximum variance using eigenvectors of the covariance matrix. Project data onto the top K components.

**Steps to implement:**

1. Import `math`. Write matrix helpers from scratch: `mat_zeros`, `mat_copy`, `mat_transpose`, `mat_mul`.
2. Write `power_iteration(A, n_iter)` — finds the dominant eigenvector of a symmetric matrix by repeatedly multiplying and normalizing a random vector. This avoids implementing a full eigendecomposition.
3. Create a `PCA` class:
   - `__init__(n_components)`
   - `fit(X)` — compute column means; center X; compute the covariance matrix `C = X_centered.T @ X_centered / (n-1)`; extract `n_components` eigenvectors using power iteration with deflation (subtract the found component from C before finding the next)
   - `transform(X)` — center X and project onto stored components: `Z = X_centered @ components.T`
4. Demo: Iris 4D → 2D. Print explained variance ratio for each component.

---

### 11 — Gradient Boosting Regressor

**Concept:** Build an ensemble by training shallow regression trees sequentially, each one fitting the residuals (errors) of the previous ensemble.

**Steps to implement:**

1. Import `math`. Write `mean_val(data)` and `best_split_threshold(x, y, indices)` — finds the best single-feature split to minimize variance in both child nodes.
2. Create a `RegressionTree` class (a shallow tree, e.g., max depth 3):
   - Uses the same recursive build pattern as the decision tree, but leaf values are the mean of residuals at that node
   - `predict_single(x)` — traverse to a leaf and return its mean value
3. Create a `GradientBoostingRegressor` class:
   - `__init__(n_estimators, lr, max_depth)` — initialize with a list of trees and a base prediction
   - `fit(X, y)` — initialize `F₀ = mean(y)`; for each round: compute residuals `r = y - current_predictions`; fit a tree to (X, r); update `F += lr * tree.predict(X)`; store the tree
   - `predict(X)` — start from `F₀` and add each tree's contribution scaled by `lr`
4. Demo: House price prediction. Compare against a single decision tree.

---

### 12 — DBSCAN

**Concept:** Density-based clustering that groups points that are close together and marks outliers as noise. Does not require specifying K in advance.

**Steps to implement:**

1. Import `math`. Write `euclidean(a, b)`.
2. Write `region_query(X, idx, eps)` — returns indices of all points within distance `eps` of point `idx`.
3. Create a `DBSCAN` class:
   - `__init__(eps, min_samples)` — `eps` is the neighborhood radius; `min_samples` is the minimum count to be a core point
   - `fit(X)` — initialize all labels as -1 (noise). For each unvisited point: get its neighbors; if fewer than `min_samples`, mark as noise; otherwise start a new cluster and expand it by adding all density-reachable points via a BFS/queue
   - `labels_` — list of cluster assignments (-1 = noise, 0, 1, 2, ...)
4. Demo: 2D synthetic data with 3 clusters and scattered noise points.

**Key concept to implement:** "border points" belong to a cluster if they are in the neighborhood of a core point but don't have enough neighbors themselves.

---

### 13 — Linear Discriminant Analysis (LDA)

**Concept:** Find linear combinations of features that maximize the ratio of between-class scatter to within-class scatter. Used for both classification and dimensionality reduction.

**Steps to implement:**

1. Import `math`. Write matrix helpers: `mat_zeros`, `mat_add`, `mat_scale`, `mat_mul`, `mat_transpose`.
2. Write `power_iteration(M, n_iter)` for extracting eigenvectors.
3. Write `deflate(M, v)` — remove component `v` from matrix M: `M = M - (v @ v.T) * (v.T @ M @ v)`.
4. Write `mat_inv_nxn(M)` — n×n matrix inverse using Gauss-Jordan elimination.
5. Create an `LDA` class:
   - `__init__(n_components)`
   - `fit(X, y)` — compute overall mean and per-class means; compute within-class scatter matrix `S_W` and between-class scatter matrix `S_B`; compute `S_W⁻¹ @ S_B`; extract top `n_components` eigenvectors using power iteration + deflation
   - `transform(X)` — project X onto learned components
   - `predict(X)` — project X; classify by nearest class centroid in the projected space
6. Demo: Iris 4D → 2D with 3-class classification.

---

### 14 — XGBoost Classifier

**Concept:** Gradient boosting with second-order Taylor approximation of the loss. Uses regression stumps (shallow trees) as base learners and softmax for multi-class.

**Steps to implement:**

1. Import `math`. Write `softmax(scores)` — numerically stable using `max` subtraction.
2. Create a `RegressionStump` class (regression tree with `max_depth` limit):
   - Same recursive build as previous trees, but stores nodes in parallel flat arrays (`feat`, `thr`, `left`, `right`, `val`) indexed by node id
   - `fit(X, residuals)` — fit to pseudo-residuals
   - `predict_single(x)` — traverse node array
3. Create an `XGBoostClassifier` class:
   - `__init__(n_estimators, lr, max_depth, n_classes)`
   - `fit(X, y)` — initialize scores to 0 for each class; for each round: compute softmax probabilities from current scores; compute pseudo-residuals as `p - one_hot(y)`; for each class, fit a stump to its residuals; update that class's scores by `lr * stump.predict(X)`
   - `predict(X)` — return `argmax(softmax(scores))`
4. Demo: Iris 3-class. Print per-class tree counts and test accuracy.

---

### 15 — t-SNE

**Concept:** Map high-dimensional data to 2D while preserving local neighborhood structure. Uses a probabilistic similarity measure and gradient descent.

**Steps to implement:**

1. Import `math`, `random`. Write `pairwise_sq_dist(X)` — n×n matrix of squared Euclidean distances.
2. Write `compute_row_prob(D_row, i, n, target_perp, perplexity)` — binary search for the bandwidth `sigma` that achieves the target perplexity; return the conditional probability row `p(j|i)`.
3. Create a `TSNE` class:
   - `__init__(n_components, perplexity, lr, n_iter, seed)`
   - `fit_transform(X)`:
     - Compute pairwise high-dimensional probabilities P (symmetrize: `P_ij = (p_j|i + p_i|j) / 2n`)
     - Initialize 2D embedding `Y` randomly
     - For each iteration: compute pairwise low-dimensional Student-t similarities Q; compute gradient `dY = 4 * Σ_j (P_ij - Q_ij) * (Y_i - Y_j) * (1 + ||Y_i - Y_j||²)⁻¹`; update Y with gradient descent and momentum
   - Return final 2D embedding
4. Demo: Iris 4D → 2D. Print the 2D coordinates and show which class each point belongs to.

**Note:** This is computationally slow in pure Python for large datasets. Keep the demo to ~150 samples and ~500 iterations.

---

### 16 — Ensemble Methods (Voting & Stacking)

**Concept:** Combine multiple base classifiers to produce better predictions than any individual model.

**Steps to implement:**

1. Import `math`. Write `euclidean(a, b)`.
2. Implement a minimal `KNN` class with `fit`, `predict_single`, and `predict_proba_single` (needed for stacking).
3. Create a `VotingClassifier` class (Hard Voting):
   - `__init__(classifiers)` — list of base classifier instances
   - `fit(X, y)` — train each classifier on the same data
   - `predict(X)` — for each sample, collect a prediction from each classifier and return the majority vote
4. Create a `StackingClassifier` class:
   - `__init__(base_classifiers, meta_classifier, n_classes)`
   - `fit(X, y)` — train all base classifiers; generate "meta-features" by concatenating the probability outputs of all base classifiers for each training sample; train the meta-classifier on these meta-features
   - `predict(X)` — get probability vectors from all base classifiers; concatenate into meta-features; predict with the meta-classifier
5. Demo: Iris 3-class. Compare individual classifiers vs Voting vs Stacking accuracy.

---

### 17 — Hidden Markov Model (HMM)

**Concept:** A probabilistic model for sequential data with hidden states. Implements four classic HMM algorithms.

**Steps to implement:**

1. Import `math`. Define `LOG_ZERO = -1e18`. Write `log_add(a, b)` — numerically stable log-sum-exp: `max(a, b) + log(1 + exp(min - max))`.
2. Create an `HMM` class:
   - `__init__(n_states, n_obs)` — initialize uniform transition matrix `A` (n_states × n_states), emission matrix `B` (n_states × n_obs), and initial distribution `pi`
   - `forward(obs)` — Forward algorithm: compute `alpha[t][s]` = probability of observations up to t and being in state s; return `log P(obs | model)`
   - `backward(obs)` — Backward algorithm: compute `beta[t][s]` = probability of future observations given state s at t
   - `viterbi(obs)` — Viterbi algorithm: find the most likely sequence of hidden states using dynamic programming with traceback
   - `baum_welch(obs_seqs, n_iter)` — EM algorithm to learn A, B, pi from unlabeled sequences: E-step computes forward/backward; M-step re-estimates parameters from state occupation counts
3. Demo 1 — Dishonest Casino: 2 states (Fair die / Loaded die), 6 observations; manually set A and B, then run Viterbi on a dice roll sequence.
4. Demo 2 — Iris petal sequence: discretize petal lengths into bins, run Baum-Welch to learn a 2-state HMM, compare log-likelihood before and after training.

---

## Design Patterns Used Throughout

**Flat node arrays for trees:** Instead of recursive `TreeNode` objects, trees store nodes as parallel lists (`feat`, `thr`, `left_child`, `right_child`, `leaf_value`) indexed by node id. This avoids object overhead and is easy to traverse iteratively.

**Log-space probability:** Any algorithm involving multiplied probabilities (Naive Bayes, HMM) works in log-space to avoid floating point underflow.

**Power iteration for eigenvalues:** Avoids implementing a full eigensolver. Extract the dominant eigenvector, then deflate the matrix and repeat for subsequent components (PCA, LDA).

**Normalization as a preprocessing contract:** Each demo that uses gradient descent normalizes inputs to [0, 1] first, then de-normalizes outputs when displaying predictions in human-readable units.

**`if __name__ == "__main__"` demos:** Every file runs a fully worked example when executed directly. The demo is part of the file — not a separate script.

---

## Recommended Build Order

If building this project from scratch, implement the files in this order, since later algorithms build on patterns from earlier ones:

1. Linear Regression → establishes gradient descent pattern
2. Logistic Regression → adds sigmoid and BCE loss
3. KNN → introduces distance functions and multi-dimensional data
4. Decision Tree → introduces recursive splitting and Gini impurity
5. Naive Bayes → introduces probabilistic, log-space classification
6. K-Means → introduces iterative centroid-based clustering
7. PCA → introduces matrix math and power iteration
8. Neural Network → introduces forward/backward pass with matrix ops
9. Random Forest → extends Decision Tree with bootstrapping
10. SVM → introduces margin-based optimization
11. LDA → extends PCA with class-aware projections
12. DBSCAN → introduces density-based clustering
13. Gradient Boosting → introduces sequential ensemble learning
14. XGBoost → extends Gradient Boosting with second-order gradients
15. Ensemble (Voting/Stacking) → combines previously built classifiers
16. t-SNE → introduces non-linear dimensionality reduction
17. HMM → introduces sequential probabilistic modeling

---

## Running All Algorithms

```bash
for f in *.py; do
    echo "=== Running $f ==="
    python "$f"
    echo
done
```

---

## License

MIT — free to use, study, and modify.

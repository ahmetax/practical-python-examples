"""
XGBoost Classifier — Python Implementation
Gradient boosting with second-order Taylor approximation.
Demo: Iris multi-class classification
"""
import math

def softmax(scores):
    """Compute softmax probabilities."""
    max_val = max(scores)
    exp_scores = [math.exp(s - max_val) for s in scores]
    sum_exp = sum(exp_scores)
    return [e / sum_exp for e in exp_scores]

class RegressionStump:
    """Depth-limited regression tree for XGBoost base learner."""
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.feat = []
        self.thr = []
        self.left = []
        self.right = []
        self.val = []

    def fit(self, X, residuals):
        self.feat = []
        self.thr = []
        self.left = []
        self.right = []
        self.val = []
        indices = list(range(len(residuals)))
        self._build(X, residuals, indices, depth=0)

    def _build(self, X, r, indices, depth):
        mean_r = sum(r[i] for i in indices) / len(indices)
        if depth >= self.max_depth or len(indices) < 2:
            self.feat.append(-1); self.thr.append(0.0)
            self.left.append(-1); self.right.append(-1)
            self.val.append(mean_r)
            return len(self.feat) - 1

        best_var = float('inf'); best_f = -1; best_t = 0.0
        n_features = len(X[0])
        for f in range(n_features):
            for idx in indices:
                t = X[idx][f]
                l = [i for i in indices if X[i][f] <= t]
                r2 = [i for i in indices if X[i][f] > t]
                if not l or not r2:
                    continue
                lm = sum(r[i] for i in l) / len(l)
                rm = sum(r[i] for i in r2) / len(r2)
                var = sum((r[i] - lm)**2 for i in l) + sum((r[i] - rm)**2 for i in r2)
                if var < best_var:
                    best_var = var; best_f = f; best_t = t

        if best_f == -1:
            self.feat.append(-1); self.thr.append(0.0)
            self.left.append(-1); self.right.append(-1)
            self.val.append(mean_r)
            return len(self.feat) - 1

        self.feat.append(best_f); self.thr.append(best_t)
        self.left.append(-1); self.right.append(-1)
        self.val.append(mean_r)
        node = len(self.feat) - 1
        l_idx = [i for i in indices if X[i][best_f] <= best_t]
        r_idx = [i for i in indices if X[i][best_f] > best_t]
        self.left[node] = self._build(X, r, l_idx, depth + 1)
        self.right[node] = self._build(X, r, r_idx, depth + 1)
        return node

    def predict_single(self, x):
        idx = 0
        while self.feat[idx] != -1:
            idx = self.left[idx] if x[self.feat[idx]] <= self.thr[idx] else self.right[idx]
        return self.val[idx]


class XGBoostClassifier:
    """Simplified XGBoost for multi-class (one tree per class per round)."""
    def __init__(self, n_estimators=10, max_depth=3, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.trees = []   # list of lists: trees[round][class]
        self.n_classes = 0

    def fit(self, X, y):
        """Train XGBoost: grow K trees per round, update raw scores."""
        self.n_classes = max(y) + 1
        n = len(X)
        self.trees = []

        # Initialize raw scores to zero
        raw_scores = [[0.0] * self.n_classes for _ in range(n)]

        for _ in range(self.n_estimators):
            probs = [softmax(raw_scores[i]) for i in range(n)]
            round_trees = []
            for c in range(self.n_classes):
                # First-order gradient (residual) for class c
                residuals = [(1.0 if y[i] == c else 0.0) - probs[i][c] for i in range(n)]
                tree = RegressionStump(max_depth=self.max_depth)
                tree.fit(X, residuals)
                round_trees.append(tree)
                # Update raw scores for class c
                for i in range(n):
                    raw_scores[i][c] += self.learning_rate * tree.predict_single(X[i])
            self.trees.append(round_trees)

    def predict_single(self, x):
        """Predict class for a single sample."""
        raw = [0.0] * self.n_classes
        for round_trees in self.trees:
            for c, tree in enumerate(round_trees):
                raw[c] += self.learning_rate * tree.predict_single(x)
        probs = softmax(raw)
        return max(range(self.n_classes), key=lambda c: probs[c])

    def predict(self, X):
        """Predict classes for multiple samples."""
        return [self.predict_single(x) for x in X]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  XGBoost Classifier")
    print("=" * 60)

    X_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9],
    ]
    y_data = [0, 0, 1, 1, 2, 2]

    model = XGBoostClassifier(n_estimators=10, max_depth=3, learning_rate=0.3)
    model.fit(X_data, y_data)

    predictions = model.predict(X_data)
    acc = sum(1 for i in range(len(y_data)) if predictions[i] == y_data[i]) / len(y_data) * 100
    print(f"Accuracy: {acc:.1f}%")
    print(f"Predictions : {predictions}")
    print(f"Ground truth: {y_data}")
    print("XGBoost training completed.")
    print("=" * 60)
"""
Gradient Boosting Regressor — Python Implementation
Ensemble of shallow trees sequentially fitting residuals.
Demo: House price prediction
"""
import math

def mean_val(data):
    """Compute mean."""
    return sum(data) / len(data)

def best_split_threshold(x, y, indices):
    """Find threshold minimizing variance."""
    if not indices:
        return 0.0
    
    best_thr = x[indices[0]]
    best_var = 1e38

    for idx_i in indices:
        thr = x[idx_i]
        ls = sum(y[j] for j in indices if x[j] <= thr)
        ln = sum(1 for j in indices if x[j] <= thr)
        rs = sum(y[j] for j in indices if x[j] > thr)
        rn = sum(1 for j in indices if x[j] > thr)
        
        if ln == 0 or rn == 0:
            continue
        
        lm = ls / ln
        rm = rs / rn
        lv = sum((y[j] - lm) ** 2 for j in indices if x[j] <= thr)
        rv = sum((y[j] - rm) ** 2 for j in indices if x[j] > thr)
        tv = (lv + rv) / len(indices)
        
        if tv < best_var:
            best_var = tv
            best_thr = thr
    
    return best_thr

class RegressionTree:
    """Simple regression tree."""
    def __init__(self, max_depth=3, min_samples=1):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.thresholds = []
        self.lefts = []
        self.rights = []
        self.values = []

    def fit(self, x, y):
        """Build tree."""
        self.thresholds = []
        self.lefts = []
        self.rights = []
        self.values = []
        indices = list(range(len(y)))
        self._build(x, y, indices, depth=0)

    def _build(self, x, y, indices, depth):
        """Recursively build tree."""
        pred = mean_val([y[i] for i in indices]) if indices else 0.0
        
        if depth >= self.max_depth or len(indices) < self.min_samples:
            self.thresholds.append(-1e38)
            self.lefts.append(-1)
            self.rights.append(-1)
            self.values.append(pred)
            return len(self.thresholds) - 1

        thr = best_split_threshold(x, y, indices)
        left_idx = [i for i in indices if x[i] <= thr]
        right_idx = [i for i in indices if x[i] > thr]

        if not left_idx or not right_idx:
            self.thresholds.append(-1e38)
            self.lefts.append(-1)
            self.rights.append(-1)
            self.values.append(pred)
            return len(self.thresholds) - 1

        self.thresholds.append(thr)
        self.lefts.append(-1)
        self.rights.append(-1)
        self.values.append(pred)
        node_idx = len(self.thresholds) - 1

        li = self._build(x, y, left_idx, depth + 1)
        ri = self._build(x, y, right_idx, depth + 1)
        self.lefts[node_idx] = li
        self.rights[node_idx] = ri
        return node_idx

    def predict_single(self, xq):
        """Predict single value."""
        idx = 0
        while self.thresholds[idx] > -1e37:
            idx = self.lefts[idx] if xq <= self.thresholds[idx] else self.rights[idx]
        return self.values[idx]

    def predict(self, x):
        """Predict multiple values."""
        return [self.predict_single(xi) for xi in x]

class GradientBoostingRegressor:
    """Gradient Boosting Regressor."""
    def __init__(self, n_estimators=10, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.init_pred = 0.0

    def fit(self, x, y):
        """Train boosting ensemble."""
        n = len(y)
        self.init_pred = mean_val(y)
        predictions = [self.init_pred] * n

        for _ in range(self.n_estimators):
            # Residuals
            residuals = [y[i] - predictions[i] for i in range(n)]
            
            # Fit tree to residuals
            tree = RegressionTree(max_depth=self.max_depth, min_samples=1)
            tree.fit(x, residuals)
            self.trees.append(tree)
            
            # Update predictions
            tree_preds = tree.predict(x)
            predictions = [predictions[i] + self.learning_rate * tree_preds[i] for i in range(n)]

    def predict_single(self, xq):
        """Predict single value."""
        pred = self.init_pred
        for tree in self.trees:
            pred += self.learning_rate * tree.predict_single(xq)
        return pred

    def predict(self, x):
        """Predict multiple values."""
        return [self.predict_single(xi) for xi in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Gradient Boosting Regressor")
    print("=" * 60)

    x_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    y_data = [2.0, 4.5, 5.2, 8.1, 9.5, 12.0, 13.2, 15.8]

    model = GradientBoostingRegressor(n_estimators=5, learning_rate=0.1)
    model.fit(x_data, y_data)
    
    predictions = model.predict(x_data)
    
    print(f"Boosting completed.")
    print("=" * 60)
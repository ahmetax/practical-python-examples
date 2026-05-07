"""
Random Forest Classifier — Python Implementation
Ensemble of decision trees trained on random data and feature subsets.
Demo: Iris flower classification (3 classes)
"""
import math
import random

def gini_impurity(labels, indices, n_classes):
    """Compute Gini impurity."""
    n = len(indices)
    if n == 0:
        return 0.0
    counts = [0] * n_classes
    for i in indices:
        counts[labels[i]] += 1
    return 1.0 - sum((counts[c] / n) ** 2 for c in range(n_classes))

def majority_class(labels, indices, n_classes):
    """Get most common class."""
    counts = [0] * n_classes
    for i in indices:
        counts[labels[i]] += 1
    return max(range(n_classes), key=lambda c: counts[c])

def all_same_class(labels, indices):
    """Check if all samples have same label."""
    return len(set(labels[i] for i in indices)) <= 1

def best_split(x, y, indices, n_classes, n_features, max_features):
    """Find best feature-threshold split."""
    best_gain = 0.0
    best_f = -1
    best_thr = 0.0
    n = len(indices)
    parent_gini = gini_impurity(y, indices, n_classes)

    feat_idx = list(range(n_features))
    random.shuffle(feat_idx)
    feat_idx = feat_idx[:min(max_features, n_features)]

    for f in feat_idx:
        for idx_i in indices:
            thr = x[idx_i][f]
            left = [i for i in indices if x[i][f] <= thr]
            right = [i for i in indices if x[i][f] > thr]
            
            if not left or not right:
                continue
            
            gini_l = gini_impurity(y, left, n_classes)
            gini_r = gini_impurity(y, right, n_classes)
            weighted = (len(left) * gini_l + len(right) * gini_r) / n
            gain = parent_gini - weighted

            if gain > best_gain:
                best_gain = gain
                best_f = f
                best_thr = thr

    return best_f, best_thr

class DecisionTreeNode:
    """Decision tree node for random forest."""
    def __init__(self):
        self.feature = -1
        self.threshold = 0.0
        self.left = None
        self.right = None
        self.pred = 0

class DecisionTree:
    """Simple decision tree."""
    def __init__(self, max_depth=5, min_samples=1, n_classes=3, max_features=None):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.n_classes = n_classes
        self.max_features = max_features
        self.root = None
        self.n_features = 0

    def fit(self, x, y):
        """Build tree."""
        self.n_features = len(x[0])
        max_f = self.max_features if self.max_features else self.n_features
        indices = list(range(len(y)))
        self.root = self._build(x, y, indices, depth=0, max_features=max_f)

    def _build(self, x, y, indices, depth, max_features):
        """Recursively build tree."""
        node = DecisionTreeNode()
        node.pred = majority_class(y, indices, self.n_classes)
        
        if depth >= self.max_depth or len(indices) < self.min_samples or all_same_class(y, indices):
            return node

        f, thr = best_split(x, y, indices, self.n_classes, self.n_features, max_features)
        if f == -1:
            return node

        left_idx = [i for i in indices if x[i][f] <= thr]
        right_idx = [i for i in indices if x[i][f] > thr]

        if not left_idx or not right_idx:
            return node

        node.feature = f
        node.threshold = thr
        node.left = self._build(x, y, left_idx, depth + 1, max_features)
        node.right = self._build(x, y, right_idx, depth + 1, max_features)
        
        return node

    def predict_single(self, x_sample):
        """Predict single sample."""
        node = self.root
        while node.feature != -1:
            if x_sample[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.pred

    def predict(self, x):
        """Predict multiple samples."""
        return [self.predict_single(sample) for sample in x]

class RandomForest:
    """Random Forest Classifier."""
    def __init__(self, n_trees=10, max_depth=5, min_samples=1, n_classes=3, max_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.n_classes = n_classes
        self.max_features = max_features
        self.trees = []

    def fit(self, x, y):
        """Train forest."""
        n = len(x)
        random.seed(42)
        for _ in range(self.n_trees):
            # Bootstrap sample
            indices = [random.randint(0, n - 1) for _ in range(n)]
            x_boot = [x[i] for i in indices]
            y_boot = [y[i] for i in indices]
            
            # Train tree
            tree = DecisionTree(self.max_depth, self.min_samples, self.n_classes, self.max_features)
            tree.fit(x_boot, y_boot)
            self.trees.append(tree)

    def predict(self, x):
        """Predict with voting."""
        predictions = []
        for sample in x:
            votes = [0] * self.n_classes
            for tree in self.trees:
                pred = tree.predict_single(sample)
                votes[pred] += 1
            predictions.append(max(range(self.n_classes), key=lambda c: votes[c]))
        return predictions

# Demo (simple)
if __name__ == "__main__":
    print("=" * 60)
    print("  Random Forest Classifier")
    print("=" * 60)
    
    # Simple dataset
    x_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5], [6.9, 3.1, 4.9, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9], [7.1, 3.0, 5.9, 2.1],
    ]
    y_data = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    model = RandomForest(n_trees=5, max_depth=3, n_classes=3)
    model.fit(x_data, y_data)
    
    predictions = model.predict(x_data)
    acc = sum(1 for i in range(len(y_data)) if predictions[i] == y_data[i]) / len(y_data) * 100
    
    print(f"Accuracy: {acc:.1f}%")
    print("Random Forest completed.")
    print("=" * 60)
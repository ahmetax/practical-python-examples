"""
K-Nearest Neighbors (KNN) in Python
Simple non-parametric classifier using K closest training samples.
"""

import math

def euclidean(x1, x2):
    """Euclidean distance between two points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(x1, x2)))

def manhattan(x1, x2):
    """Manhattan distance between two points."""
    return sum(abs(a - b) for a, b in zip(x1, x2))

def majority_vote(labels, num_classes):
    """Return most frequent label."""
    counts = [0] * num_classes
    for label in labels:
        counts[label] += 1
    return counts.index(max(counts))

def accuracy(y_true, y_pred):
    """Compute classification accuracy (%)."""
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true) * 100.0

class KNNClassifier:
    """K-Nearest Neighbors Classifier."""
    def __init__(self, k=3, metric="euclidean", num_classes=3):
        self.k = k
        self.metric = metric
        self.num_classes = num_classes
        self.x_train = []
        self.y_train = []

    def fit(self, x, y):
        """Store training data (no training step for KNN)."""
        self.x_train = [list(row) for row in x]
        self.y_train = list(y)

    def predict_single(self, x_query):
        """Predict class for single point."""
        dist_func = manhattan if self.metric == "manhattan" else euclidean
        dists = [(dist_func(x_query, x), label) 
                 for x, label in zip(self.x_train, self.y_train)]
        dists.sort(key=lambda x: x[0])
        k_labels = [label for _, label in dists[:self.k]]
        return majority_vote(k_labels, self.num_classes)

    def predict(self, x):
        """Predict classes for multiple points."""
        return [self.predict_single(xi) for xi in x]

# Demo
if __name__ == "__main__":
    print("=" * 65)
    print("  K-Nearest Neighbors (KNN) Classifier")
    print("  Demo: Iris Flower Classification")
    print("  Features: petal length, petal width")
    print("  Classes : 0=Setosa, 1=Versicolor, 2=Virginica")
    print("=" * 65)

    # Dataset
    x_data = [
        # Setosa (label=0)
        [1.4, 0.2], [1.3, 0.2], [1.5, 0.2], [1.4, 0.3], [1.7, 0.4],
        [1.5, 0.1], [1.6, 0.2], [1.1, 0.1], [1.2, 0.2], [1.5, 0.3],
        # Versicolor (label=1)
        [4.7, 1.4], [4.5, 1.5], [4.9, 1.5], [4.0, 1.3], [4.6, 1.5],
        [4.5, 1.3], [4.7, 1.6], [3.3, 1.0], [4.6, 1.3], [3.9, 1.4],
        # Virginica (label=2)
        [6.0, 2.5], [5.1, 1.9], [5.9, 2.1], [5.6, 1.8], [5.8, 2.2],
        [6.6, 2.1], [6.3, 1.8], [6.1, 2.5], [6.4, 2.0], [5.6, 2.1]
    ]
    y_data = [0]*10 + [1]*10 + [2]*10

    classes = {0: "Setosa    ", 1: "Versicolor", 2: "Virginica "}
    
    print(f"\nDataset: {len(y_data)} samples (10 per class)")
    print("Features: petal length (cm), petal width (cm)")

    # Test K values
    print("\n--- Accuracy vs K (Euclidean) ---")
    print("K     Accuracy")
    print("-" * 20)
    for k in range(1, 8):
        model = KNNClassifier(k=k, metric="euclidean", num_classes=3)
        model.fit(x_data, y_data)
        preds = model.predict(x_data)
        acc = accuracy(y_data, preds)
        print(f"K={k}   {acc:.1f}%")

    # Main model with K=3
    print("\n--- Predictions (K=3, Euclidean) ---")
    print("PetalLen  PetalWid  Actual        Predicted     Correct?")
    print("-" * 62)

    model = KNNClassifier(k=3, metric="euclidean", num_classes=3)
    model.fit(x_data, y_data)
    preds = model.predict(x_data)

    for i, (x, y_true, y_pred) in enumerate(zip(x_data, y_data, preds)):
        actual = classes[y_true]
        predicted = classes[y_pred]
        correct = "Yes" if y_pred == y_true else "No "
        print(f"{x[0]:7.1f}   {x[1]:7.1f}   {actual}   {predicted}   {correct}")

    acc = accuracy(y_data, preds)
    print(f"\nAccuracy (K=3, Euclidean): {acc:.1f}%")

    # Compare metrics
    print("\n--- Euclidean vs Manhattan (K=3) ---")
    model_m = KNNClassifier(k=3, metric="manhattan", num_classes=3)
    model_m.fit(x_data, y_data)
    preds_m = model_m.predict(x_data)
    acc_m = accuracy(y_data, preds_m)
    print(f"Euclidean : {acc:.1f}%")
    print(f"Manhattan : {acc_m:.1f}%")

    # New predictions
    print("\n--- New Flower Predictions (K=3) ---")
    print("PetalLen  PetalWid  ->  Predicted")
    print("-" * 40)
    test_points = [[1.3, 0.2], [4.5, 1.4], [5.8, 2.0], [3.8, 1.2], [5.0, 1.7]]
    for x in test_points:
        pred = model.predict_single(x)
        print(f"{x[0]:7.1f}   {x[1]:7.1f}   ->  {classes[pred]}")

    print("\nKNN Classification completed.")
    print("=" * 65)
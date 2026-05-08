"""
Support Vector Machine (SVM) — Python Implementation
Finds hyperplane maximizing margin between classes using SGD on hinge loss.
Demo: Binary and multi-class classification
"""
import math

def dot(w, x):
    """Compute dot product."""
    return sum(a * b for a, b in zip(w, x))

def normalize_data(data):
    """Min-Max normalize each feature to [0, 1]."""
    n = len(data)
    nf = len(data[0])
    mins = [data[0][f] for f in range(nf)]
    maxs = [data[0][f] for f in range(nf)]
    
    for i in range(n):
        for f in range(nf):
            mins[f] = min(mins[f], data[i][f])
            maxs[f] = max(maxs[f], data[i][f])
    
    result = []
    for i in range(n):
        row = []
        for f in range(nf):
            rng = maxs[f] - mins[f]
            if rng == 0.0:
                row.append(0.0)
            else:
                row.append((data[i][f] - mins[f]) / rng)
        result.append(row)
    return result

def accuracy_int(y_true, y_pred):
    """Compute accuracy (%)."""
    return sum(1 for i in range(len(y_true)) if y_true[i] == y_pred[i]) / len(y_true) * 100

class LinearSVM:
    """Binary Linear SVM trained with SGD."""
    def __init__(self, C=1.0, lr=0.01, epochs=100):
        self.C = C
        self.lr = lr
        self.epochs = epochs
        self.w = []
        self.b = 0.0

    def fit(self, x, y):
        """Train SVM (labels must be +1 or -1)."""
        n = len(x)
        nf = len(x[0])
        self.w = [0.1] * nf
        self.b = 0.0

        for _ in range(self.epochs):
            for i in range(n):
                decision = y[i] * (dot(self.w, x[i]) + self.b)
                
                if decision >= 1:
                    # Correct classification with margin
                    dw = [wi for wi in self.w]
                    db = 0.0
                else:
                    # Margin violation
                    dw = [self.w[j] - self.C * y[i] * x[i][j] for j in range(nf)]
                    db = -self.C * y[i]
                
                self.w = [self.w[j] - self.lr * dw[j] for j in range(nf)]
                self.b -= self.lr * db

    def predict_single(self, x_sample):
        """Predict for single sample."""
        decision = dot(self.w, x_sample) + self.b
        return 1 if decision >= 0 else -1

    def predict(self, x):
        """Predict for multiple samples."""
        return [self.predict_single(sample) for sample in x]

class SVM_OvR:
    """Multi-class SVM using One-vs-Rest."""
    def __init__(self, n_classes=3, C=1.0, lr=0.01, epochs=100):
        self.n_classes = n_classes
        self.C = C
        self.lr = lr
        self.epochs = epochs
        self.svms = []

    def fit(self, x, y):
        """Train OvR SVMs."""
        for c in range(self.n_classes):
            # One-vs-Rest: class c vs all others
            y_binary = [1 if label == c else -1 for label in y]
            svm = LinearSVM(self.C, self.lr, self.epochs)
            svm.fit(x, y_binary)
            self.svms.append(svm)

    def predict_single(self, x_sample):
        """Predict class with highest decision score."""
        scores = [self.svms[c].predict_single(x_sample) for c in range(self.n_classes)]
        return max(range(self.n_classes), key=lambda c: scores[c])

    def predict(self, x):
        """Predict multiple samples."""
        return [self.predict_single(sample) for sample in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Support Vector Machine")
    print("=" * 60)

    x_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5], [6.9, 3.1, 4.9, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9], [7.1, 3.0, 5.9, 2.1],
    ]
    y_data = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    x_data = normalize_data(x_data)
    
    model = SVM_OvR(n_classes=3, C=1.0, lr=0.01, epochs=100)
    model.fit(x_data, y_data)
    
    predictions = model.predict(x_data)
    acc = accuracy_int(y_data, predictions)
    
    print(f"Accuracy: {acc:.1f}%")
    print("SVM training completed.")
    print("=" * 60)
"""
Logistic Regression in Python
Binary classification with sigmoid and BCE loss.
"""

import math

class NormResult:
    def __init__(self, data, min_val, max_val):
        self.data = data
        self.min_val = min_val
        self.max_val = max_val

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def binary_cross_entropy(y_true, y_pred):
    total = 0
    for yt, yp in zip(y_true, y_pred):
        p = max(min(yp, 1 - 1e-9), 1e-9)
        total += yt * math.log(p) + (1 - yt) * math.log(1 - p)
    return -total / len(y_true)

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val
    normalized = [(x - min_val) / range_val if range_val != 0 else 0 for x in data]
    return NormResult(normalized, min_val, max_val)

def accuracy(y_true, y_pred):
    correct = sum(1 if (yp >= 0.5) == yt else 0 for yp, yt in zip(y_pred, y_true))
    return correct / len(y_true) * 100

class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.weight = 0.0
        self.bias = 0.0
        self.lr = lr
        self.epochs = epochs
        self.loss_history = []

    def fit(self, x, y):
        n = len(x)
        for _ in range(self.epochs):
            y_pred = [sigmoid(self.weight * xi + self.bias) for xi in x]
            loss = binary_cross_entropy(y, y_pred)
            self.loss_history.append(loss)
            dw = sum((yp - yt) * xi for yp, yt, xi in zip(y_pred, y, x)) / n
            db = sum(yp - yt for yp, yt in zip(y_pred, y)) / n
            self.weight -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, x):
        return sigmoid(self.weight * x + self.bias)

    def predict(self, x):
        return [self.predict_proba(xi) for xi in x]

    def predict_class(self, x):
        return 1 if self.predict_proba(x) >= 0.5 else 0

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Logistic Regression Demo")
    print("=" * 60)

    x_raw = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    y_raw = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    print(f"Dataset: {len(x_raw)} students")

    xn = normalize(x_raw)

    model = LogisticRegression(lr=0.5, epochs=2000)
    model.fit(xn.data, y_raw)

    y_pred = model.predict(xn.data)
    acc = accuracy(y_raw, y_pred)
    final_loss = model.loss_history[-1]

    print(f"Epochs: {model.epochs}, LR: {model.lr}, Loss: {final_loss:.4f}, Acc: {acc:.1f}%")
    print(f"Weight: {model.weight:.4f}, Bias: {model.bias:.4f}")

    print("\nPredictions:")
    for i in range(len(x_raw)):
        prob = y_pred[i]
        pred_cls = 1 if prob >= 0.5 else 0
        actual = int(y_raw[i])
        correct = "Yes" if pred_cls == actual else "No"
        print(f"{x_raw[i]:4.1f}h: {actual} -> {prob:.3f} -> {pred_cls} ({correct})")

    x_range = xn.max_val - xn.min_val
    boundary_norm = -model.bias / model.weight
    boundary_hours = boundary_norm * x_range + xn.min_val
    print(f"\nDecision boundary at {boundary_hours:.2f}h")

    test_hours = [2.0, 4.0, 5.5, 7.0, 9.0]
    print("\nNew predictions:")
    for h in test_hours:
        h_norm = (h - xn.min_val) / x_range
        prob = model.predict_proba(h_norm)
        cls = model.predict_class(h_norm)
        label = "PASS" if cls == 1 else "FAIL"
        print(f"{h:.1f}h -> P={prob:.3f} -> {label}")
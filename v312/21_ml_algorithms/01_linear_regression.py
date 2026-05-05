"""
Linear Regression in Python
Model: y = w * x + b
Trained with Gradient Descent.
"""

class NormResult:
    def __init__(self, data, min_val, max_val):
        self.data = data
        self.min_val = min_val
        self.max_val = max_val

def mean(data):
    return sum(data) / len(data)

def mse(y_true, y_pred):
    return sum((p - t) ** 2 for p, t in zip(y_pred, y_true)) / len(y_true)

def r2_score(y_true, y_pred):
    y_mean = mean(y_true)
    ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    ss_tot = sum((t - y_mean) ** 2 for t in y_true)
    return 1 - ss_res / ss_tot if ss_tot != 0 else 1.0

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val
    normalized = [(x - min_val) / range_val if range_val != 0 else 0.0 for x in data]
    return NormResult(normalized, min_val, max_val)

class LinearRegression:
    def __init__(self, lr=0.01, epochs=1000):
        self.weight = 0.0
        self.bias = 0.0
        self.lr = lr
        self.epochs = epochs
        self.loss_history = []

    def fit(self, x, y):
        n = len(x)
        for _ in range(self.epochs):
            y_pred = [self.weight * xi + self.bias for xi in x]
            loss = mse(y, y_pred)
            self.loss_history.append(loss)
            dw = sum((yp - yt) * xi for yp, yt, xi in zip(y_pred, y, x)) * 2 / n
            db = sum(yp - yt for yp, yt in zip(y_pred, y)) * 2 / n
            self.weight -= self.lr * dw
            self.bias -= self.lr * db

    def predict_single(self, x):
        return self.weight * x + self.bias

    def predict(self, x):
        return [self.predict_single(xi) for xi in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Linear Regression Demo")
    print("=" * 60)

    x_raw = [50, 65, 70, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 250]
    y_raw = [450, 520, 580, 620, 680, 720, 750, 800, 870, 950, 1020, 1100, 1180, 1250, 1420, 1600, 1780, 2050]

    print(f"Dataset: {len(x_raw)} houses")

    xn = normalize(x_raw)
    yn = normalize(y_raw)

    model = LinearRegression(lr=0.1, epochs=2000)
    model.fit(xn.data, yn.data)

    y_pred_norm = model.predict(xn.data)
    r2 = r2_score(yn.data, y_pred_norm)
    final_loss = model.loss_history[-1]

    print(f"Epochs: {model.epochs}, LR: {model.lr}, Loss: {final_loss:.4f}, R2: {r2:.4f}")
    print(f"Weight: {model.weight:.4f}, Bias: {model.bias:.4f}")

    print("\nPredictions:")
    y_range = yn.max_val - yn.min_val
    x_range = xn.max_val - xn.min_val
    for i in range(len(x_raw)):
        pred_norm = model.predict_single(xn.data[i])
        pred_real = pred_norm * y_range + yn.min_val
        real = y_raw[i]
        error = abs(pred_real - real) / real * 100
        print(f"{x_raw[i]:3} m2: {real:4}K -> {pred_real:4.0f}K ({error:3.0f}%)")

    test_sizes = [75, 115, 175, 300]
    print("\nNew predictions:")
    for m2 in test_sizes:
        m2_norm = (m2 - xn.min_val) / x_range
        pred_norm = model.predict_single(m2_norm)
        pred_real = pred_norm * y_range + yn.min_val
        print(f"{m2} m2 -> {pred_real:.0f}K TL")
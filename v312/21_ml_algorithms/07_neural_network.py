"""
Neural Network — Python Implementation
Feedforward network with backpropagation for binary classification.
Architecture: Input -> Hidden -> Output (sigmoid activations)
"""
import math

def sigmoid(z):
    """Sigmoid activation function."""
    return 1.0 / (1.0 + math.exp(-z))

def sigmoid_deriv(a):
    """Derivative of sigmoid given its output."""
    return a * (1.0 - a)

def clip(v, lo, hi):
    """Clip value to range."""
    return max(lo, min(hi, v))

def float_str(val, decimals):
    """Format float."""
    return f"{val:.{decimals}f}"

def mat_mul(A, B, m, k, n):
    """Matrix multiply A(m×k) × B(k×n) -> C(m×n)."""
    C = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            s = 0.0
            for p in range(k):
                s += A[i][p] * B[p][j]
            C[i][j] = s
    return C

def mat_sigmoid(A):
    """Apply sigmoid element-wise."""
    return [[sigmoid(x) for x in row] for row in A]

def mat_add_bias(A, b):
    """Add bias vector to each row."""
    m = len(A)
    n = len(A[0])
    return [[A[i][j] + b[j] for j in range(n)] for i in range(m)]

def mat_transpose(A):
    """Transpose matrix."""
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_scale(A, s):
    """Scale matrix by scalar."""
    return [[x * s for x in row] for row in A]

class NeuralNetwork:
    """Simple 2-layer neural network for binary classification."""
    def __init__(self, n_input=2, n_hidden=4, lr=0.1, epochs=1000):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.lr = lr
        self.epochs = epochs
        # Xavier-style initialization for better convergence
        import random as _rnd
        _rnd.seed(42)
        scale1 = (2.0 / n_input) ** 0.5
        scale2 = (2.0 / n_hidden) ** 0.5
        self.W1 = [[(_rnd.random() * 2 - 1) * scale1 for _ in range(n_input)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[(_rnd.random() * 2 - 1) * scale2 for _ in range(n_hidden)]]
        self.b2 = [0.0]
        self.loss_history = []

    def forward(self, x):
        """Forward pass."""
        # x: batch_size x n_input
        z1 = mat_add_bias(mat_mul(x, mat_transpose(self.W1), len(x), self.n_input, self.n_hidden), self.b1)
        a1 = mat_sigmoid(z1)
        z2 = mat_add_bias(mat_mul(a1, mat_transpose(self.W2), len(a1), self.n_hidden, 1), self.b2)
        a2 = mat_sigmoid(z2)
        return a1, a2

    def fit(self, x, y):
        """Train the network."""
        n = len(x)
        for epoch in range(self.epochs):
            # Forward pass
            a1, a2 = self.forward(x)
            
            # Loss
            loss = sum(-(y[i][0] * math.log(clip(a2[i][0], 1e-10, 1.0)) + 
                        (1 - y[i][0]) * math.log(clip(1 - a2[i][0], 1e-10, 1.0))) 
                      for i in range(n)) / n
            self.loss_history.append(loss)
            
            # Backprop
            # dz2: [n x 1]
            dz2 = [[a2[i][0] - y[i][0]] for i in range(n)]

            # dW2: [1 x n_hidden] — gradient w.r.t. W2
            dW2 = [[sum(dz2[i][0] * a1[i][j] for i in range(n)) / n
                    for j in range(self.n_hidden)]]
            db2 = [sum(dz2[i][0] for i in range(n)) / n]

            # dz1: [n x n_hidden]
            dz1 = [[(dz2[i][0] * self.W2[0][j]) * sigmoid_deriv(a1[i][j])
                    for j in range(self.n_hidden)] for i in range(n)]

            # dW1: [n_hidden x n_input]
            dW1 = [[sum(dz1[i][h] * x[i][f] for i in range(n)) / n
                    for f in range(self.n_input)] for h in range(self.n_hidden)]
            db1 = [sum(dz1[i][j] for i in range(n)) / n for j in range(self.n_hidden)]

            # Update weights
            self.W2 = [[self.W2[0][j] - self.lr * dW2[0][j] for j in range(self.n_hidden)]]
            self.b2 = [self.b2[0] - self.lr * db2[0]]
            self.W1 = [[self.W1[i][j] - self.lr * dW1[i][j] for j in range(self.n_input)] for i in range(self.n_hidden)]
            self.b1 = [self.b1[j] - self.lr * db1[j] for j in range(self.n_hidden)]

    def predict_single(self, x_sample):
        """Predict for single sample."""
        _, a2 = self.forward([x_sample])
        return 1 if a2[0][0] > 0.5 else 0

    def predict(self, x):
        """Predict for multiple samples."""
        return [self.predict_single(sample) for sample in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Neural Network (2-Layer)")
    print("  Demo: XOR Problem")
    print("=" * 60)

    # XOR dataset
    x_data = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    y_data = [[0.0], [1.0], [1.0], [0.0]]

    print(f"\nDataset  : {len(x_data)} samples")
    print("Features : x1, x2")
    print("Problem  : XOR (non-linearly separable)")

    model = NeuralNetwork(n_input=2, n_hidden=4, lr=0.5, epochs=2000)
    model.fit(x_data, y_data)

    predictions = model.predict(x_data)
    
    print(f"\n--- Training Results ---")
    print(f"Final Loss: {float_str(model.loss_history[-1], 4)}")

    print("\nNeural Network training completed.")
    print("=" * 60)
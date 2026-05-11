"""
t-SNE — Python Implementation
Maps high-dimensional data to 2D while preserving local neighborhood structure.
Demo: Iris visualization
"""
import math
import random

def pairwise_sq_dist(X):
    """Compute pairwise squared distances."""
    n = len(X)
    d = len(X[0])
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = sum((X[i][k] - X[j][k]) ** 2 for k in range(d))
            D[i][j] = s
            D[j][i] = s
    return D

def compute_row_prob(D_row, i, n, target_perp, perplexity=30.0):
    """Compute conditional probabilities via binary search."""
    target_H = math.log(target_perp)
    sigma_lo, sigma_hi = 1e-5, 1e5
    p = [0.0] * n

    for _ in range(50):
        sigma = (sigma_lo + sigma_hi) / 2.0
        two_sig2 = 2.0 * sigma * sigma

        sum_p = 0.0
        for j in range(n):
            if j == i:
                p[j] = 0.0
            else:
                p[j] = math.exp(-D_row[j] / two_sig2)
                sum_p += p[j]

        if sum_p < 1e-12:
            sum_p = 1e-12

        for j in range(n):
            p[j] /= sum_p

        H = -sum(p[j] * math.log(p[j] + 1e-10) for j in range(n))

        if abs(H - target_H) < 0.01:
            break
        
        if H > target_H:
            sigma_hi = sigma
        else:
            sigma_lo = sigma

    return p

class TSNE:
    """t-SNE Dimensionality Reduction."""
    def __init__(self, n_components=2, perplexity=30.0, n_iter=1000, learning_rate=200.0):
        self.n_components = n_components
        self.perplexity = perplexity
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.embedding = []

    def fit_transform(self, X):
        """Fit and transform data."""
        n = len(X)
        d = len(X[0])
        
        # Pairwise distances
        D = pairwise_sq_dist(X)
        
        # Joint probabilities P_ij
        P = [[0.0] * n for _ in range(n)]
        for i in range(n):
            p_i = compute_row_prob([D[i][j] for j in range(n)], i, n, self.perplexity)
            for j in range(n):
                P[i][j] = (p_i[j] + p_i[j]) / (2.0 * n)
        
        # Initialize embedding randomly
        random.seed(42)
        Y = [[random.gauss(0, 1e-4) for _ in range(self.n_components)] for _ in range(n)]
        
        # Gradient descent
        for _ in range(self.n_iter):
            # Compute low-dim distances
            Q = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    sq_d = sum((Y[i][k] - Y[j][k]) ** 2 for k in range(self.n_components))
                    Q[i][j] = 1.0 / (1.0 + sq_d)
            
        # Normalize Q
        Q_sum = sum(Q[i][j] for i in range(n) for j in range(n) if i != j)
        Q_sum = max(Q_sum, 1e-12)
        Q_norm = [[Q[i][j] / Q_sum if i != j else 0.0 for j in range(n)] for i in range(n)]

        # Gradient descent step
        lr = self.learning_rate
        momentum = [[0.0] * self.n_components for _ in range(n)]

        for i in range(n):
            grad = [0.0] * self.n_components
            for j in range(n):
                if i == j:
                    continue
                pq_diff = P[i][j] - Q_norm[i][j]
                q_ij = Q[i][j]
                for k in range(self.n_components):
                    grad[k] += 4.0 * pq_diff * (Y[i][k] - Y[j][k]) * q_ij
            momentum[i] = [grad[k] for k in range(self.n_components)]

        for i in range(n):
            for k in range(self.n_components):
                Y[i][k] -= lr * momentum[i][k]

        # Zero-center
        for k in range(self.n_components):
            mean_k = sum(Y[i][k] for i in range(n)) / n
            for i in range(n):
                Y[i][k] -= mean_k
        
        self.embedding = Y
        return Y

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  t-SNE Dimensionality Reduction")
    print("=" * 60)

    X_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9],
    ]

    tsne = TSNE(n_components=2, n_iter=200, learning_rate=50.0, perplexity=3.0)
    Z = tsne.fit_transform(X_data)

    print(f"\n2D Embedding (first 6 points):")
    print(f"{'Point':<8} {'PC1':>8} {'PC2':>8}")
    print("-" * 28)
    labels = ['Setosa', 'Setosa', 'Versicolor', 'Versicolor', 'Virginica', 'Virginica']
    for i, z in enumerate(Z):
        print(f"{labels[i]:<14} {z[0]:>8.4f} {z[1]:>8.4f}")

    print(f"\nt-SNE projection completed.")
    print("=" * 60)
"""
Linear Discriminant Analysis (LDA) — Python Implementation
Finds linear combinations of features maximizing class separability.
Demo: Iris classification (4D -> 2D)
"""
import math

def mat_zeros(r, c):
    return [[0.0] * c for _ in range(r)]

def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mat_scale(A, s):
    return [[A[i][j] * s for j in range(len(A[0]))] for i in range(len(A))]

def mat_mul(A, B):
    m, k, n = len(A), len(A[0]), len(B[0])
    C = mat_zeros(m, n)
    for i in range(m):
        for j in range(n):
            C[i][j] = sum(A[i][p] * B[p][j] for p in range(k))
    return C

def power_iteration(M, n_iter=200):
    """Find dominant eigenvector via power iteration."""
    d = len(M)
    v = [1.0 / d**0.5] * d
    for _ in range(n_iter):
        u = [sum(M[i][j] * v[j] for j in range(d)) for i in range(d)]
        norm = sum(x**2 for x in u) ** 0.5
        if norm < 1e-12:
            break
        v = [x / norm for x in u]
    return v

def deflate(M, v):
    """Remove component along v (Hotelling deflation)."""
    d = len(M)
    Av = [sum(M[i][j] * v[j] for j in range(d)) for i in range(d)]
    lam = sum(Av[i] * v[i] for i in range(d))
    return [[M[i][j] - lam * v[i] * v[j] for j in range(d)] for i in range(d)]

def mat_inv_nxn(M):
    """Gauss-Jordan inversion."""
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)]
         for i, row in enumerate(M)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[pivot] = A[pivot], A[col]
        if abs(A[col][col]) < 1e-12:
            continue
        factor = A[col][col]
        A[col] = [x / factor for x in A[col]]
        for row in range(n):
            if row != col:
                f = A[row][col]
                A[row] = [A[row][k] - f * A[col][k] for k in range(2 * n)]
    return [row[n:] for row in A]


class LDA:
    """Linear Discriminant Analysis — maximises between-class / within-class scatter."""
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components = []   # shape: [n_components][d]

    def fit(self, X, y):
        n_classes = max(y) + 1
        n = len(X)
        d = len(X[0])

        # Per-class means and counts
        class_means = [mat_zeros(1, d)[0] for _ in range(n_classes)]
        class_counts = [0] * n_classes
        for i in range(n):
            for j in range(d):
                class_means[y[i]][j] += X[i][j]
            class_counts[y[i]] += 1
        for c in range(n_classes):
            for j in range(d):
                class_means[c][j] /= class_counts[c]

        overall_mean = [sum(X[i][j] for i in range(n)) / n for j in range(d)]

        # Between-class scatter Sb
        Sb = mat_zeros(d, d)
        for c in range(n_classes):
            diff = [class_means[c][j] - overall_mean[j] for j in range(d)]
            for i in range(d):
                for j in range(d):
                    Sb[i][j] += class_counts[c] * diff[i] * diff[j]

        # Within-class scatter Sw
        Sw = mat_zeros(d, d)
        for i in range(n):
            diff = [X[i][j] - class_means[y[i]][j] for j in range(d)]
            for r in range(d):
                for cc in range(d):
                    Sw[r][cc] += diff[r] * diff[cc]

        # Regularise Sw to avoid singularity
        for i in range(d):
            Sw[i][i] += 1e-6

        Sw_inv = mat_inv_nxn(Sw)
        M = mat_mul(Sw_inv, Sb)   # M = Sw^{-1} Sb

        # Extract top n_components eigenvectors via power iteration + deflation
        self.components = []
        M_temp = [row[:] for row in M]
        for _ in range(min(self.n_components, n_classes - 1)):
            v = power_iteration(M_temp)
            self.components.append(v)
            M_temp = deflate(M_temp, v)

    def transform(self, X):
        """Project data onto LDA components."""
        d = len(X[0])
        return [[sum(X[i][j] * self.components[c][j] for j in range(d))
                 for c in range(len(self.components))]
                for i in range(len(X))]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Linear Discriminant Analysis")
    print("=" * 60)

    X_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5], [6.9, 3.1, 4.9, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9], [7.1, 3.0, 5.9, 2.1],
    ]
    y_data = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    lda = LDA(n_components=2)
    lda.fit(X_data, y_data)
    Z = lda.transform(X_data)

    print(f"\n{'Sample':<10} {'LD1':>10} {'LD2':>10}  Class")
    print("-" * 40)
    class_names = ['Setosa', 'Versicolor', 'Virginica']
    for i, (z, label) in enumerate(zip(Z, y_data)):
        print(f"  {i:<8} {z[0]:>10.4f} {z[1]:>10.4f}  {class_names[label]}")

    print(f"\nProjection completed.")
    print("=" * 60)
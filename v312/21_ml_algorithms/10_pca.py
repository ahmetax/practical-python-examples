"""
Principal Component Analysis (PCA) — Python Implementation
Finds directions of maximum variance and projects data to lower dimensions.
Demo: Iris 4D -> 2D projection
"""
import math

def mat_zeros(rows, cols):
    """Create zero matrix."""
    return [[0.0] * cols for _ in range(rows)]

def mat_copy(src):
    """Copy matrix."""
    return [row[:] for row in src]

def mat_transpose(A):
    """Transpose matrix."""
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_mul(A, B):
    """Matrix multiply."""
    m, k = len(A), len(A[0])
    n = len(B[0])
    C = mat_zeros(m, n)
    for i in range(m):
        for j in range(n):
            C[i][j] = sum(A[i][p] * B[p][j] for p in range(k))
    return C

def power_iteration(A, n_iter=100):
    """Power iteration to find dominant eigenvector."""
    n = len(A)
    v = [1.0 / math.sqrt(n)] * n
    
    for _ in range(n_iter):
        # Av
        u = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        # Norm
        norm = math.sqrt(sum(x**2 for x in u))
        if norm < 1e-10:
            break
        v = [x / norm for x in u]
    
    return v

class PCA:
    """Principal Component Analysis."""
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.mean = []
        self.components = []
        self.explained_variance = []

    def fit(self, X):
        """Fit PCA model."""
        n = len(X)
        d = len(X[0])
        
        # Center data
        self.mean = [sum(X[i][j] for i in range(n)) / n for j in range(d)]
        X_centered = [[X[i][j] - self.mean[j] for j in range(d)] for i in range(n)]
        
        # Covariance matrix
        X_T = mat_transpose(X_centered)
        cov = mat_mul(X_T, X_centered)
        for i in range(d):
            for j in range(d):
                cov[i][j] /= n
        
        # Extract components via power iteration + deflation
        self.components = []
        self.explained_variance = []
        cov_temp = mat_copy(cov)
        
        for _ in range(self.n_components):
            v = power_iteration(cov_temp)
            # Eigenvalue
            Av = [sum(cov_temp[i][j] * v[j] for j in range(d)) for i in range(d)]
            eigenval = sum(Av[i] * v[i] for i in range(d))
            
            self.components.append(v)
            self.explained_variance.append(eigenval)
            
            # Deflate
            vv = [[v[i] * v[j] for j in range(d)] for i in range(d)]
            for i in range(d):
                for j in range(d):
                    cov_temp[i][j] -= eigenval * vv[i][j]

    def transform(self, X):
        """Project data onto components."""
        d = len(X[0])
        X_centered = [[X[i][j] - self.mean[j] for j in range(d)] for i in range(len(X))]
        
        Z = []
        for x in X_centered:
            z = [sum(x[j] * self.components[c][j] for j in range(d)) 
                 for c in range(self.n_components)]
            Z.append(z)
        return Z

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Principal Component Analysis")
    print("  Demo: Iris 4D -> 2D Projection")
    print("=" * 60)

    X_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5], [6.9, 3.1, 4.9, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9], [7.1, 3.0, 5.9, 2.1],
    ]

    pca = PCA(n_components=2)
    pca.fit(X_data)
    
    Z = pca.transform(X_data)
    
    print(f"\nDataset  : {len(X_data)} samples")
    print("Features : 4D -> 2D projection")
    print(f"Explained variance: {pca.explained_variance}")
    
    print("\nPCA projection completed.")
    print("=" * 60)
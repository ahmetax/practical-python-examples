"""
K-Means Clustering — Python Implementation
Partitions data into K groups by iteratively assigning points to the nearest
centroid and updating centroids.
Demo: 2D synthetic data with 3 natural clusters
"""
import math

def euclidean_sq(x1, x2):
    """Squared Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(x1, x2))

def euclidean(x1, x2):
    """Euclidean distance."""
    return math.sqrt(euclidean_sq(x1, x2))

def copy_point(src):
    """Copy a point."""
    return list(src)

def points_equal(a, b, tol):
    """Check if two points are within tolerance."""
    return all(abs(ai - bi) <= tol for ai, bi in zip(a, b))

def float_str(val, decimals):
    """Format float to fixed decimal places."""
    return f"{val:.{decimals}f}"

def cluster_symbol(label):
    """Return a symbol for each cluster."""
    return ['A', 'B', 'C'][label] if label < 3 else 'D'

class KMeans:
    """K-Means Clustering using squared Euclidean distance."""
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = []
        self.labels = []
        self.inertia = 0.0
        self.n_iters = 0

    def fit(self, x):
        """Run K-Means on dataset x."""
        n = len(x)
        dims = len(x[0])

        # K-Means++ initialization
        mean_pt = [sum(x[i][d] for i in range(n)) / n for d in range(dims)]
        best_dist = -1.0
        best_idx = 0
        for i in range(n):
            dist = euclidean_sq(x[i], mean_pt)
            if dist > best_dist:
                best_dist = dist
                best_idx = i
        self.centroids = [copy_point(x[best_idx])]

        for _ in range(1, self.k):
            max_min_dist = -1.0
            next_idx = 0
            for i in range(n):
                min_dist = min(euclidean_sq(x[i], c) for c in self.centroids)
                if min_dist > max_min_dist:
                    max_min_dist = min_dist
                    next_idx = i
            self.centroids.append(copy_point(x[next_idx]))

        self.labels = [0] * n

        # EM loop
        for iteration in range(self.max_iters):
            self.n_iters = iteration + 1

            # E-step: assign to nearest centroid
            for i in range(n):
                best_dist = euclidean_sq(x[i], self.centroids[0])
                best_k = 0
                for c in range(1, self.k):
                    dist = euclidean_sq(x[i], self.centroids[c])
                    if dist < best_dist:
                        best_dist = dist
                        best_k = c
                self.labels[i] = best_k

            # M-step: update centroids
            new_centroids = []
            for c in range(self.k):
                cluster_pts = [x[i] for i in range(n) if self.labels[i] == c]
                if cluster_pts:
                    new_centroids.append([sum(pt[d] for pt in cluster_pts) / len(cluster_pts) 
                                         for d in range(dims)])
                else:
                    new_centroids.append(copy_point(self.centroids[c]))

            # Check convergence
            if all(points_equal(self.centroids[c], new_centroids[c], self.tol) 
                   for c in range(self.k)):
                self.centroids = new_centroids
                break
            self.centroids = new_centroids

        # Compute inertia
        self.inertia = sum(euclidean_sq(x[i], self.centroids[self.labels[i]]) 
                          for i in range(n))

    def predict_single(self, x_query):
        """Assign a new point to nearest centroid."""
        best_dist = euclidean_sq(x_query, self.centroids[0])
        best_k = 0
        for c in range(1, self.k):
            dist = euclidean_sq(x_query, self.centroids[c])
            if dist < best_dist:
                best_dist = dist
                best_k = c
        return best_k

# Demo
if __name__ == "__main__":
    print("=" * 65)
    print("  K-Means Clustering")
    print("  Demo: 2D Synthetic Data with 3 Natural Clusters")
    print("=" * 65)

    # Dataset: 3 clusters
    x_data = [
        # Cluster A (bottom-left)
        [1.0, 1.5], [1.5, 2.0], [2.0, 2.5], [2.5, 1.8],
        [1.8, 1.2], [3.0, 2.0], [2.2, 3.0], [1.2, 2.8],
        # Cluster B (top-center)
        [4.5, 7.5], [5.0, 8.0], [5.5, 8.5], [4.8, 9.0],
        [5.2, 7.8], [6.0, 8.2], [4.2, 8.8], [5.8, 7.2],
        # Cluster C (right)
        [8.5, 3.5], [9.0, 4.0], [9.5, 4.5], [8.8, 5.0],
        [9.2, 3.2], [10.0, 4.2], [8.2, 4.8], [9.8, 3.8],
    ]

    n = len(x_data)
    print(f"\nDataset  : {n} points (8 per cluster)")
    print("Features : x, y coordinates")
    print("Expected : 3 natural clusters (A, B, C)")

    model = KMeans(k=3, max_iters=100, tol=1e-4)
    model.fit(x_data)

    print(f"\n--- Training Results ---")
    print(f"Iterations : {model.n_iters}")
    print(f"Inertia    : {float_str(model.inertia, 2)}")

    print(f"\n--- Final Centroids ---")
    print("Cluster   X        Y")
    print("-" * 30)
    for c in range(model.k):
        print(f"  {cluster_symbol(c)}     {float_str(model.centroids[c][0], 3):>7}  {float_str(model.centroids[c][1], 3):>7}")

    print(f"\n--- Cluster Sizes ---")
    for c in range(model.k):
        count = sum(1 for i in range(n) if model.labels[i] == c)
        print(f"Cluster {cluster_symbol(c)} : {count} points")

    print("\nK-Means Clustering completed.")
    print("=" * 65)
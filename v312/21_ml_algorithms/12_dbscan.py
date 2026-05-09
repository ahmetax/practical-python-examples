"""
DBSCAN — Density-Based Clustering
Groups closely-packed points and marks low-density regions as noise.
Demo: 2D synthetic data with noise
"""
import math

def euclidean(a, b):
    """Euclidean distance."""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

def region_query(x, idx, eps):
    """Return indices of points within eps radius."""
    return [i for i in range(len(x)) if i != idx and euclidean(x[idx], x[i]) <= eps]

class DBSCAN:
    """DBSCAN Clustering. Labels: -1=noise, 0..k=cluster id."""
    def __init__(self, eps=0.5, min_samples=3):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = []
        self.n_clusters = 0

    def fit(self, x):
        """Run DBSCAN."""
        n = len(x)
        self.labels = [-2] * n  # -2 = unvisited
        cluster_id = -1

        for i in range(n):
            if self.labels[i] != -2:
                continue

            neighbors = region_query(x, i, self.eps)

            if len(neighbors) < self.min_samples:
                self.labels[i] = -1  # noise
                continue

            # Start new cluster
            cluster_id += 1
            self.labels[i] = cluster_id

            # BFS expand
            queue = neighbors[:]
            while queue:
                q = queue.pop(0)

                if self.labels[q] == -1:
                    self.labels[q] = cluster_id

                if self.labels[q] != -2:
                    continue

                self.labels[q] = cluster_id
                q_neighbors = region_query(x, q, self.eps)
                if len(q_neighbors) >= self.min_samples:
                    for nb in q_neighbors:
                        if self.labels[nb] == -2 or self.labels[nb] == -1:
                            queue.append(nb)

        self.n_clusters = cluster_id + 1

    def predict_single(self, x, query):
        """Assign new point to nearest cluster or mark as noise."""
        best_label = -1
        best_dist = 1e38
        for i in range(len(x)):
            if self.labels[i] >= 0:
                dist = euclidean(x[i], query)
                if dist <= self.eps and dist < best_dist:
                    best_dist = dist
                    best_label = self.labels[i]
        return best_label

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  DBSCAN Clustering")
    print("=" * 60)

    x_data = [
        [1.0, 1.0], [1.1, 1.1], [1.2, 0.9],
        [5.0, 5.0], [5.1, 5.2], [5.2, 5.0],
        [9.0, 9.0], [9.1, 9.1], [9.2, 8.9],
        [2.0, 8.0],  # noise
    ]

    model = DBSCAN(eps=1.0, min_samples=2)
    model.fit(x_data)

    print(f"Clusters found: {model.n_clusters}")
    print(f"Labels: {model.labels}")
    
    print("DBSCAN clustering completed.")
    print("=" * 60)
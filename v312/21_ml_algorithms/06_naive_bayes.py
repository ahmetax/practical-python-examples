"""
Gaussian Naive Bayes — Python Implementation
Probabilistic classifier using Bayes' theorem with feature independence assumption.
Demo: Iris flower classification (petal features)
"""
import math

PI = math.pi

def mean(data):
    """Compute mean of a list."""
    return sum(data) / len(data)

def variance(data, mu):
    """Compute variance given mean."""
    return sum((x - mu) ** 2 for x in data) / len(data)

def gaussian_log_prob(x, mu, var_):
    """Log probability of x under Gaussian(mu, var_)."""
    eps = 1e-9
    v = var_ + eps
    return -0.5 * math.log(2.0 * PI * v) - ((x - mu) ** 2) / (2.0 * v)

def accuracy(y_true, y_pred):
    """Compute classification accuracy (%)."""
    return sum(1 for i in range(len(y_true)) if y_true[i] == y_pred[i]) / len(y_true) * 100

class GaussianNB:
    """Gaussian Naive Bayes Classifier."""
    def __init__(self, n_classes=3, n_features=2):
        self.n_classes = n_classes
        self.n_features = n_features
        self.class_prior = []
        self.class_mean = []
        self.class_var = []

    def fit(self, x, y):
        """Compute per-class priors, means and variances."""
        n = len(y)
        self.class_prior = []
        self.class_mean = []
        self.class_var = []

        for c in range(self.n_classes):
            idx = [i for i in range(n) if y[i] == c]
            self.class_prior.append(math.log(len(idx) / n))

            for f in range(self.n_features):
                feature_data = [x[i][f] for i in idx]
                mu = mean(feature_data) if feature_data else 0.0
                var = variance(feature_data, mu) if feature_data else 1.0
                self.class_mean.append(mu)
                self.class_var.append(var)

    def predict_single(self, x_sample):
        """Predict class for a single sample."""
        scores = []
        for c in range(self.n_classes):
            score = self.class_prior[c]
            for f in range(self.n_features):
                mu = self.class_mean[c * self.n_features + f]
                var = self.class_var[c * self.n_features + f]
                score += gaussian_log_prob(x_sample[f], mu, var)
            scores.append(score)
        return max(range(self.n_classes), key=lambda c: scores[c])

    def predict(self, x):
        """Predict classes for samples."""
        return [self.predict_single(sample) for sample in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Gaussian Naive Bayes")
    print("  Demo: Iris Petal Features (2D)")
    print("=" * 60)

    # Iris petal_len, petal_wid
    # 0=Setosa, 1=Versicolor, 2=Virginica
    x_data = [
        [1.4, 0.2], [1.4, 0.2], [1.3, 0.2], [1.5, 0.2], [1.4, 0.2],
        [1.7, 0.4], [1.4, 0.3], [1.5, 0.2], [1.4, 0.2], [1.5, 0.1],
        [4.7, 1.4], [4.5, 1.5], [4.9, 1.5], [4.0, 1.3], [4.6, 1.5],
        [4.5, 1.3], [4.7, 1.6], [3.3, 1.0], [4.6, 1.3], [3.9, 1.4],
        [6.0, 2.5], [5.1, 1.9], [5.9, 2.1], [5.6, 1.8], [5.8, 2.2],
        [6.6, 2.1], [4.5, 1.7], [6.3, 1.8], [5.8, 1.8], [6.1, 2.5],
    ]
    
    y_data = [0]*10 + [1]*10 + [2]*10

    print(f"\nDataset  : {len(x_data)} samples (2 features, 3 classes)")
    print("Features : Petal Length, Petal Width")
    print("Classes  : 0=Setosa, 1=Versicolor, 2=Virginica")

    model = GaussianNB(n_classes=3, n_features=2)
    model.fit(x_data, y_data)

    predictions = model.predict(x_data)
    acc = accuracy(y_data, predictions)
    
    print(f"\n--- Training Results ---")
    print(f"Accuracy : {acc:.1f}%")

    print("\nGaussian Naive Bayes classification completed.")
    print("=" * 60)
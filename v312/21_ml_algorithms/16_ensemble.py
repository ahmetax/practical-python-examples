"""
Ensemble Methods: Voting & Stacking — Python Implementation
Combines multiple base classifiers for improved predictions.
Demo: Iris classification (3 classes)
"""
import math

def euclidean(a, b):
    """Euclidean distance."""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

class KNN:
    """K-Nearest Neighbors classifier."""
    def __init__(self, k=5):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        """Store training data."""
        self.X_train = X
        self.y_train = y

    def predict_single(self, x):
        """Predict single sample."""
        dists = [euclidean(x, xt) for xt in self.X_train]
        indices = sorted(range(len(dists)), key=lambda i: dists[i])[:self.k]
        votes = [self.y_train[i] for i in indices]
        return max(set(votes), key=votes.count)

    def predict_proba_single(self, x, n_classes):
        """Predict probabilities."""
        dists = [euclidean(x, xt) for xt in self.X_train]
        indices = sorted(range(len(dists)), key=lambda i: dists[i])[:self.k]
        votes = [self.y_train[i] for i in indices]
        probs = [votes.count(c) / self.k for c in range(n_classes)]
        return probs

class VotingClassifier:
    """Hard Voting Ensemble."""
    def __init__(self, estimators, method='hard'):
        self.estimators = estimators
        self.method = method
        self.n_classes = 0

    def fit(self, X, y):
        """Train all base classifiers."""
        self.n_classes = max(y) + 1
        for name, clf in self.estimators:
            clf.fit(X, y)

    def predict(self, X):
        """Predict with majority voting."""
        predictions = []
        for x in X:
            votes = [clf.predict_single(x) for _, clf in self.estimators]
            pred = max(set(votes), key=votes.count)
            predictions.append(pred)
        return predictions

class StackingClassifier:
    """Stacking Ensemble with meta-learner."""
    def __init__(self, base_estimators, meta_estimator):
        self.base_estimators = base_estimators
        self.meta_estimator = meta_estimator
        self.n_classes = 0

    def fit(self, X, y):
        """Train base estimators and meta-estimator."""
        self.n_classes = max(y) + 1
        for clf in self.base_estimators:
            clf.fit(X, y)

        # Generate meta-features
        meta_X = []
        for x in X:
            features = []
            for clf in self.base_estimators:
                probs = clf.predict_proba_single(x, self.n_classes)
                features.extend(probs)
            meta_X.append(features)

        self.meta_estimator.fit(meta_X, y)

    def predict(self, X):
        """Predict with stacking."""
        meta_X = []
        for x in X:
            features = []
            for clf in self.base_estimators:
                probs = clf.predict_proba_single(x, self.n_classes)
                features.extend(probs)
            meta_X.append(features)
        return self.meta_estimator.predict(meta_X)

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Ensemble Methods: Voting & Stacking")
    print("=" * 60)

    X_data = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2],
        [7.0, 3.2, 4.7, 1.4], [6.4, 3.2, 4.5, 1.5],
        [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9],
    ]
    y_data = [0, 0, 1, 1, 2, 2]

    knn = KNN(k=3)
    
    estimators = [("knn", knn)]
    voting = VotingClassifier(estimators)
    voting.fit(X_data, y_data)
    
    predictions = voting.predict(X_data)
    
    print(f"Ensemble predictions completed.")
    print("=" * 60)
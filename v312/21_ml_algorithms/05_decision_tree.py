"""
Decision Tree Classifier — Python Implementation
Splits data recursively by feature-threshold pairs minimizing Gini impurity.
Demo: Play Tennis classification
"""

def gini_impurity(labels, indices, n_classes):
    """Compute Gini impurity for a subset."""
    n = len(indices)
    if n == 0:
        return 0.0
    counts = [0] * n_classes
    for i in indices:
        counts[labels[i]] += 1
    impurity = 1.0
    for c in range(n_classes):
        p = counts[c] / n
        impurity -= p * p
    return impurity

def majority_class(labels, indices, n_classes):
    """Return the most common class in a subset."""
    counts = [0] * n_classes
    for i in indices:
        counts[labels[i]] += 1
    return max(range(n_classes), key=lambda c: counts[c])

def all_same_class(labels, indices):
    """Check if all samples have the same label."""
    if not indices:
        return True
    first = labels[indices[0]]
    return all(labels[i] == first for i in indices)

def unique_values(x, feature, indices):
    """Get unique values of a feature in a subset."""
    seen = []
    for i in indices:
        val = x[i][feature]
        if val not in seen:
            seen.append(val)
    return seen

class DecisionTree:
    """Decision Tree Classifier using Gini Impurity."""
    def __init__(self, max_depth=5, min_samples=1, n_classes=2):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.n_classes = n_classes
        self.n_features = 0
        self.node_feature = []
        self.node_threshold = []
        self.node_left = []
        self.node_right = []
        self.node_pred = []

    def fit(self, x, y):
        """Build the tree."""
        self.n_features = len(x[0])
        self.node_feature = []
        self.node_threshold = []
        self.node_left = []
        self.node_right = []
        self.node_pred = []
        
        indices = list(range(len(y)))
        self._build_tree(x, y, indices, depth=0)

    def _build_tree(self, x, y, indices, depth):
        """Recursively build tree nodes."""
        pred = majority_class(y, indices, self.n_classes)
        
        if depth >= self.max_depth or len(indices) < self.min_samples or all_same_class(y, indices):
            self.node_feature.append(-1)
            self.node_threshold.append(0.0)
            self.node_left.append(-1)
            self.node_right.append(-1)
            self.node_pred.append(pred)
            return len(self.node_feature) - 1

        best_gain = 0.0
        best_feature = -1
        best_threshold = 0.0
        parent_gini = gini_impurity(y, indices, self.n_classes)

        for f in range(self.n_features):
            for threshold in unique_values(x, f, indices):
                left = [i for i in indices if x[i][f] <= threshold]
                right = [i for i in indices if x[i][f] > threshold]
                
                if not left or not right:
                    continue
                
                gini_left = gini_impurity(y, left, self.n_classes)
                gini_right = gini_impurity(y, right, self.n_classes)
                weighted_gini = (len(left) * gini_left + len(right) * gini_right) / len(indices)
                gain = parent_gini - weighted_gini

                if gain > best_gain:
                    best_gain = gain
                    best_feature = f
                    best_threshold = threshold

        if best_feature == -1:
            self.node_feature.append(-1)
            self.node_threshold.append(0.0)
            self.node_left.append(-1)
            self.node_right.append(-1)
            self.node_pred.append(pred)
            return len(self.node_feature) - 1

        self.node_feature.append(best_feature)
        self.node_threshold.append(best_threshold)
        self.node_left.append(-1)
        self.node_right.append(-1)
        self.node_pred.append(pred)
        node_idx = len(self.node_feature) - 1

        left = [i for i in indices if x[i][best_feature] <= best_threshold]
        right = [i for i in indices if x[i][best_feature] > best_threshold]

        left_idx = self._build_tree(x, y, left, depth + 1)
        right_idx = self._build_tree(x, y, right, depth + 1)
        
        self.node_left[node_idx] = left_idx
        self.node_right[node_idx] = right_idx
        
        return node_idx

    def predict_single(self, x_sample):
        """Predict class for a single sample."""
        idx = 0
        while self.node_feature[idx] != -1:
            if x_sample[self.node_feature[idx]] <= self.node_threshold[idx]:
                idx = self.node_left[idx]
            else:
                idx = self.node_right[idx]
        return self.node_pred[idx]

    def predict(self, x):
        """Predict classes for samples."""
        return [self.predict_single(sample) for sample in x]

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Decision Tree Classifier")
    print("  Demo: Play Tennis Dataset")
    print("=" * 60)

    # Features: Outlook (0=Sunny, 1=Overcast, 2=Rain),
    #           Temp (0=Hot, 1=Mild, 2=Cool),
    #           Humidity (0=High, 1=Normal),
    #           Wind (0=Weak, 1=Strong)
    # Label: 0=No Play, 1=Play
    x_data = [
        [0, 0, 0, 0],  # Sunny, Hot, High, Weak -> No Play
        [0, 0, 0, 1],  # Sunny, Hot, High, Strong -> No Play
        [1, 0, 0, 0],  # Overcast, Hot, High, Weak -> Play
        [2, 1, 0, 0],  # Rain, Mild, High, Weak -> Play
        [2, 2, 1, 0],  # Rain, Cool, Normal, Weak -> Play
        [2, 2, 1, 1],  # Rain, Cool, Normal, Strong -> No Play
        [1, 2, 1, 1],  # Overcast, Cool, Normal, Strong -> Play
        [0, 1, 0, 0],  # Sunny, Mild, High, Weak -> No Play
        [0, 2, 1, 0],  # Sunny, Cool, Normal, Weak -> Play
        [2, 1, 1, 0],  # Rain, Mild, Normal, Weak -> Play
    ]
    
    y_data = [0, 0, 1, 1, 1, 0, 1, 0, 1, 1]

    print(f"\nDataset  : {len(x_data)} samples (4 features, 2 classes)")
    print("Features : Outlook, Temp, Humidity, Wind")
    print("Classes  : 0=No Play, 1=Play")

    model = DecisionTree(max_depth=4, min_samples=1, n_classes=2)
    model.fit(x_data, y_data)

    predictions = model.predict(x_data)
    accuracy = sum(1 for i in range(len(y_data)) if predictions[i] == y_data[i]) / len(y_data) * 100
    
    print(f"\n--- Training Results ---")
    print(f"Accuracy : {accuracy:.1f}%")
    print(f"Tree nodes: Feature={len(model.node_feature)}")

    print("\nDecision Tree classification completed.")
    print("=" * 60)
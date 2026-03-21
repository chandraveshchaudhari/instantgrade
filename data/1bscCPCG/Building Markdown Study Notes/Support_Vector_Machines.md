# Support Vector Machines (SVM): A Comprehensive Guide

## Table of Contents
1. [Introduction to SVM](#introduction-to-svm)
2. [Mathematical Foundations](#mathematical-foundations)
3. [Linear SVMs](#linear-svms)
4. [Non-Linear SVMs and Kernel Trick](#non-linear-svms-and-kernel-trick)
5. [Soft Margin Classification](#soft-margin-classification)
6. [Multi-Class Classification](#multi-class-classification)
7. [SVM Regression](#svm-regression)
8. [Implementation with Python](#implementation-with-python)
9. [Hyperparameter Tuning](#hyperparameter-tuning)
10. [Performance Evaluation](#performance-evaluation)
11. [Advantages and Disadvantages](#advantages-and-disadvantages)
12. [Applications](#applications)
13. [Best Practices](#best-practices)

---

## Introduction to SVM

### What is Support Vector Machine?

Support Vector Machine (SVM) is a supervised machine learning algorithm used for classification and regression tasks. It finds the optimal hyperplane that maximally separates different classes in the training data.

### Historical Context

- Developed by Vladimir Vapnik and colleagues in the 1990s
- Initially designed for binary classification
- Extended to multi-class and regression problems
- One of the most powerful machine learning algorithms

### Key Concept

SVM searches for the **maximum margin hyperplane** - the decision boundary that maximizes the distance between classes. The data points closest to this boundary are called **support vectors**.

```
Binary Classification Example:

        * * (Class 2)
           |
           | Margin
    -------+---------  <- Hyperplane
           | Margin
        o o o (Class 1)
        
Support vectors are marked with circles/stars closest to the hyperplane
```

---

## Mathematical Foundations

### Hyperplane

A hyperplane in n-dimensional space is defined as:

$$w \cdot x + b = 0$$

Where:
- $w$ = weight vector (coefficients)
- $x$ = feature vector
- $b$ = bias term
- $\cdot$ = dot product

### Classification Function

The decision function classifies a point $x$ as:

$$f(x) = \text{sign}(w \cdot x + b)$$

- If $f(x) > 0$: point belongs to class +1
- If $f(x) < 0$: point belongs to class -1

### Margin

The margin is the distance between the hyperplane and the nearest data points:

$$\text{Margin} = \frac{2}{||w||}$$

To maximize the margin, we minimize $||w||^2$.

### Optimization Problem

For linearly separable data, SVM solves:

$$\min_{w,b} \frac{1}{2}||w||^2$$

Subject to constraint (for each training sample $i$):

$$y_i(w \cdot x_i + b) \geq 1$$

Where $y_i \in \{-1, +1\}$ is the class label.

---

## Linear SVMs

### Hard Margin SVM

Used when data is perfectly linearly separable.

```python
# Example: Linearly separable data

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_classification

# Generate linearly separable data
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, 
                           n_informative=2, random_state=42)

# Train SVM with linear kernel
svm = SVC(kernel='linear', C=float('inf'))  # Hard margin
svm.fit(X, y)

# Get support vectors
support_vectors = svm.support_vectors_

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(X[y==0, 0], X[y==0, 1], c='red', label='Class 0', alpha=0.6)
plt.scatter(X[y==1, 0], X[y==1, 1], c='blue', label='Class 1', alpha=0.6)
plt.scatter(support_vectors[:, 0], support_vectors[:, 1], 
            s=200, linewidth=1.5, facecolors='none', edgecolors='green', 
            label='Support Vectors')

# Plot decision boundary
xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-1, X[:, 0].max()+1, 100),
                      np.linspace(X[:, 1].min()-1, X[:, 1].max()+1, 100))
Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black')
plt.contour(xx, yy, Z, levels=[-1, 1], linewidths=1, colors='black', linestyles='--')

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.title('SVM with Linear Kernel (Hard Margin)')
plt.show()
```

### Support Vectors

Points that define the decision boundary. Only these points matter for the solution - other points can be removed without changing the SVM.

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris

# Load data
iris = load_iris()
X, y = iris.data[:, :2], iris.target
X = X[(y == 0) | (y == 1)]  # Binary classification
y = y[(y == 0) | (y == 1)]

# Train SVM
svm = SVC(kernel='linear', C=1.0)
svm.fit(X, y)

# Analyze support vectors
print(f"Number of support vectors: {len(svm.support_vectors_)}")
print(f"Support vector indices: {svm.support_}")
print(f"Support vectors per class: {svm.n_support_}")
```

### Weight Vector and Bias

```python
from sklearn.svm import SVC

# For linear kernel
svm = SVC(kernel='linear')
svm.fit(X, y)

# Get coefficients (weights) and bias
w = svm.coef_[0]  # Weight vector
b = svm.intercept_[0]  # Bias

print(f"Weight vector: {w}")
print(f"Bias: {b}")

# Decision function: w·x + b
decision_value = X[0] @ w + b
print(f"Decision value for first sample: {decision_value}")
```

---

## Non-Linear SVMs and Kernel Trick

### The Kernel Trick

When data is not linearly separable, SVM uses **kernel trick** to map data to higher dimensions implicitly.

```
Original (Non-separable):        Transformed (Separable):

    * o *                            * * *
    o * *              φ                 |
    * o *         ---------->           ---|---
    * * o                               o o o
    o o *                               
```

### Mathematical Formulation

Instead of computing $w \cdot x$ directly, we use kernel function $K(x_i, x_j)$:

$$K(x_i, x_j) = \phi(x_i) \cdot \phi(x_j)$$

Where $\phi$ implicitly maps data to higher dimensions.

### Common Kernel Functions

#### 1. **Linear Kernel**

$$K(x_i, x_j) = x_i \cdot x_j$$

Best for: Linearly separable data, high-dimensional data

```python
from sklearn.svm import SVC

svm = SVC(kernel='linear')
```

#### 2. **Polynomial Kernel**

$$K(x_i, x_j) = (x_i \cdot x_j + c)^d$$

Where:
- $d$ = degree of polynomial
- $c$ = constant (coef0)

Best for: Polynomial relationships between features

```python
from sklearn.svm import SVC

# Degree 2 polynomial
svm = SVC(kernel='poly', degree=2, coef0=1)

# Degree 3 polynomial
svm = SVC(kernel='poly', degree=3, coef0=1)
```

#### 3. **Radial Basis Function (RBF) Kernel**

$$K(x_i, x_j) = \exp(-\gamma ||x_i - x_j||^2)$$

Where $\gamma$ controls the influence of each training example.

Best for: Non-linear problems, most flexible

```python
from sklearn.svm import SVC

# Default gamma='scale' = 1/(n_features * X.var())
svm = SVC(kernel='rbf', gamma='scale')

# Custom gamma
svm = SVC(kernel='rbf', gamma=0.1)  # Smaller gamma = smoother boundary
svm = SVC(kernel='rbf', gamma=10)   # Larger gamma = more complex boundary
```

#### 4. **Sigmoid Kernel**

$$K(x_i, x_j) = \tanh(\gamma x_i \cdot x_j + c)$$

Best for: Neural network-like decision boundaries (rarely used)

```python
from sklearn.svm import SVC

svm = SVC(kernel='sigmoid', gamma=0.1, coef0=1)
```

### Kernel Comparison Example

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_circles

# Generate non-linearly separable data
X, y = make_circles(n_samples=300, noise=0.1, factor=0.3, random_state=42)

# Create different SVM models
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, kernel in zip(axes.ravel(), kernels):
    svm = SVC(kernel=kernel, degree=2 if kernel == 'poly' else 3)
    svm.fit(X, y)
    
    # Create mesh
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-0.5, X[:, 0].max()+0.5, 200),
                         np.linspace(X[:, 1].min()-0.5, X[:, 1].max()+0.5, 200))
    
    # Decision boundary
    Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    
    # Plot
    ax.contourf(xx, yy, Z, levels=20, cmap='RdBu_r', alpha=0.6)
    ax.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black')
    ax.scatter(X[y==0, 0], X[y==0, 1], c='red', alpha=0.6)
    ax.scatter(X[y==1, 0], X[y==1, 1], c='blue', alpha=0.6)
    ax.set_title(f'SVM with {kernel.upper()} Kernel')
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

plt.tight_layout()
plt.show()
```

---

## Soft Margin Classification

### The Problem with Hard Margin

Hard margin SVM fails when:
- Data has noise or outliers
- Perfect separation is impossible
- Overfitting occurs

### Soft Margin Solution

Introduces slack variables $\xi_i$ to allow some misclassification:

$$y_i(w \cdot x_i + b) \geq 1 - \xi_i$$

Where $\xi_i \geq 0$ represents the margin violation.

### Optimization Problem with Regularization

$$\min_{w,b,\xi} \frac{1}{2}||w||^2 + C\sum_{i=1}^{n} \xi_i$$

Where $C$ is the regularization parameter (penalty for misclassification).

### C Parameter (Regularization)

The parameter $C$ in scikit-learn controls the trade-off:

```python
from sklearn.svm import SVC

# Large C: stricter, more support vectors, potential overfitting
svm_strict = SVC(kernel='rbf', C=100)

# Medium C: balanced
svm_balanced = SVC(kernel='rbf', C=1.0)

# Small C: more tolerance, fewer support vectors, potential underfitting
svm_loose = SVC(kernel='rbf', C=0.01)
```

### Visualization of C Effect

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_classification

# Generate data with some noise
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                          n_informative=2, random_state=42)

# Different C values
C_values = [0.1, 1, 10, 100]
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, C in zip(axes.ravel(), C_values):
    svm = SVC(kernel='rbf', C=C)
    svm.fit(X, y)
    
    # Mesh
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-1, X[:, 0].max()+1, 100),
                         np.linspace(X[:, 1].min()-1, X[:, 1].max()+1, 100))
    
    Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, levels=20, cmap='RdBu_r', alpha=0.6)
    ax.scatter(X[y==0, 0], X[y==0, 1], c='red', alpha=0.6)
    ax.scatter(X[y==1, 0], X[y==1, 1], c='blue', alpha=0.6)
    ax.scatter(svm.support_vectors_[:, 0], svm.support_vectors_[:, 1],
              s=100, linewidth=1, facecolors='none', edgecolors='green')
    ax.set_title(f'C = {C} (SVs: {len(svm.support_vectors_)})')

plt.tight_layout()
plt.show()
```

---

## Multi-Class Classification

### Strategies for Multi-Class SVM

#### 1. One-vs-Rest (OvR)

Creates K binary classifiers for K classes. Each classifier separates one class from all others.

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

# SVM automatically uses OvR for multi-class
svm = SVC(kernel='rbf', decision_function_shape='ovr')
svm.fit(X, y)

# Predictions
predictions = svm.predict(X[:5])
print(f"Predictions: {predictions}")
```

#### 2. One-vs-One (OvO)

Creates $\frac{K(K-1)}{2}$ binary classifiers for all pairs of classes.

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

# Use OvO strategy
svm = SVC(kernel='rbf', decision_function_shape='ovo')
svm.fit(X, y)

predictions = svm.predict(X[:5])
print(f"Predictions: {predictions}")
```

### Example: Multi-Class Classification

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load Iris dataset (3 classes)
X, y = load_iris(return_X_y=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train SVM for multi-class
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)

# Evaluate
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

---

## SVM Regression

### SVR (Support Vector Regression)

Extends SVM to regression tasks by finding the hyperplane that best fits the data while maximizing margin.

### Epsilon-Insensitive Loss

Only penalizes errors outside the epsilon-tube:

$$L = \max(0, |y - \hat{y}| - \epsilon)$$

Where $\epsilon$ defines the acceptable error range.

### SVR Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR

# Generate data
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 2 * X.ravel() + 1 + np.random.normal(0, 2, 100)

# Create SVR models with different kernels
models = {
    'linear': SVR(kernel='linear', C=100, epsilon=1),
    'poly': SVR(kernel='poly', degree=2, C=100, epsilon=1),
    'rbf': SVR(kernel='rbf', C=100, epsilon=1, gamma=0.1)
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (name, model) in zip(axes, models.items()):
    model.fit(X, y)
    y_pred = model.predict(X)
    
    ax.scatter(X, y, color='red', alpha=0.5, label='Training data')
    ax.plot(X, y_pred, color='blue', label='Prediction')
    ax.set_title(f'SVR with {name.upper()} Kernel')
    ax.set_xlabel('X')
    ax.set_ylabel('y')
    ax.legend()

plt.tight_layout()
plt.show()
```

### SVR Parameters

```python
from sklearn.svm import SVR

svr = SVR(
    kernel='rbf',      # Kernel type
    C=100,             # Regularization parameter
    epsilon=0.1,       # Epsilon-tube width
    gamma='scale',     # Kernel coefficient
    degree=3           # Polynomial degree (if kernel='poly')
)
```

---

## Implementation with Python

### Installation

```bash
pip install scikit-learn numpy pandas matplotlib scipy
```

### Basic Binary Classification

```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Generate data
X, y = make_classification(n_samples=200, n_features=2, n_redundant=0,
                          n_informative=2, random_state=42)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train SVM
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)

# Predictions
y_pred = svm.predict(X_test)

# Evaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

### Feature Scaling (Important!)

SVM is sensitive to feature scaling. Always normalize features:

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline

# Create pipeline with scaling and SVM
svm_pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Normalize features
    ('svm', SVC(kernel='rbf', C=1.0))
])

svm_pipeline.fit(X_train, y_train)
y_pred = svm_pipeline.predict(X_test)
```

### Probability Estimates

```python
from sklearn.svm import SVC

# Enable probability estimates
svm = SVC(kernel='rbf', probability=True)
svm.fit(X_train, y_train)

# Get probability estimates
probabilities = svm.predict_proba(X_test)
print(f"Probabilities for first sample: {probabilities[0]}")

# Predict with confidence
y_pred = svm.predict(X_test)
confidence = svm.predict_proba(X_test).max(axis=1)
```

### Custom Kernel

```python
from sklearn.svm import SVC
import numpy as np

# Define custom kernel function
def custom_kernel(X, Y):
    """Custom Gaussian-like kernel"""
    return np.exp(-10 * np.sum((X[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=2))

# Use custom kernel
svm = SVC(kernel=custom_kernel)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)
```

---

## Hyperparameter Tuning

### Key Hyperparameters

| Parameter | Effect | Range |
|-----------|--------|-------|
| **C** | Regularization strength | [0.001, 0.01, 0.1, 1, 10, 100, 1000] |
| **kernel** | Type of kernel | ['linear', 'poly', 'rbf', 'sigmoid'] |
| **gamma** | Kernel coefficient (RBF) | [0.0001, 0.001, 0.01, 0.1, 1, 10] |
| **degree** | Polynomial degree | [1, 2, 3, 4, 5] |
| **epsilon** (SVR) | Epsilon-tube width | [0.01, 0.1, 0.5, 1.0] |

### Grid Search

```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
    'kernel': ['rbf', 'poly']
}

# Grid search
grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")

# Use best model
best_svm = grid_search.best_estimator_
y_pred = best_svm.predict(X_test)
```

### Randomized Search

```python
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, uniform

# Parameter distribution
param_dist = {
    'C': loguniform(0.1, 1000),
    'gamma': loguniform(0.0001, 10),
    'kernel': ['rbf', 'poly']
}

# Randomized search
random_search = RandomizedSearchCV(SVC(), param_dist, n_iter=20, cv=5, n_jobs=-1, random_state=42)
random_search.fit(X_train, y_train)

print(f"Best parameters: {random_search.best_params_}")
print(f"Best CV score: {random_search.best_score_:.4f}")
```

### Cross-Validation

```python
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_validate
import numpy as np

svm = SVC(kernel='rbf', C=1.0)

# Simple cross-validation
scores = cross_val_score(svm, X_train, y_train, cv=5, scoring='accuracy')
print(f"CV Scores: {scores}")
print(f"Mean CV Score: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Multiple metrics
scoring = {'accuracy': 'accuracy', 'precision': 'precision', 'recall': 'recall'}
results = cross_validate(svm, X_train, y_train, cv=5, scoring=scoring)
print(f"Average accuracy: {np.mean(results['test_accuracy']):.4f}")
print(f"Average precision: {np.mean(results['test_precision']):.4f}")
print(f"Average recall: {np.mean(results['test_recall']):.4f}")
```

---

## Performance Evaluation

### Classification Metrics

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix, roc_auc_score, 
                           roc_curve, precision_recall_curve)
import matplotlib.pyplot as plt

# Predictions
y_pred = svm.predict(X_test)
y_pred_proba = svm.decision_function(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(cm)

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
auc = roc_auc_score(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.title('ROC Curve')
plt.show()
```

### Regression Metrics

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Predictions
y_pred = svr.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE:  {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R²:   {r2:.4f}")
```

---

## Advantages and Disadvantages

### Advantages

| Advantage | Description |
|-----------|-------------|
| **Effective in high dimensions** | Works well with many features |
| **Memory efficient** | Uses only support vectors for prediction |
| **Versatile kernels** | Can solve linear and non-linear problems |
| **Good generalization** | Robust to overfitting with proper regularization |
| **Robust** | Works well with both classification and regression |
| **Handles outliers** | Soft margin tolerates some misclassification |
| **Proven theory** | Strong mathematical foundation |

### Disadvantages

| Disadvantage | Description |
|--------------|-------------|
| **Slow with large datasets** | $O(n^3)$ complexity for training |
| **Feature scaling required** | Sensitive to feature normalization |
| **Hyperparameter tuning** | Requires careful tuning of C and gamma |
| **Not interpretable** | Black-box model, difficult to explain |
| **Memory usage** | Can be memory-intensive with many support vectors |
| **Probability calibration** | Probability estimates are not well-calibrated |
| **Binary focus** | Multi-class needs workarounds |

---

## Applications

### 1. **Image Classification**

```python
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# Load digit dataset (images)
digits = load_digits()
X, y = digits.data, digits.target

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train SVM
svm = SVC(kernel='rbf', gamma=0.001)
svm.fit(X_train, y_train)

# Evaluate
accuracy = svm.score(X_test, y_test)
print(f"Digit Recognition Accuracy: {accuracy:.4f}")
```

### 2. **Text Classification**

```python
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# Text data
documents = [
    "This movie is great",
    "I loved this film",
    "This movie is terrible",
    "I hated it"
]
labels = [1, 1, 0, 0]  # 1: positive, 0: negative

# Create pipeline
svm_text = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=100)),
    ('svm', SVC(kernel='linear'))
])

svm_text.fit(documents, labels)

# Predict
new_text = ["This movie is amazing"]
prediction = svm_text.predict(new_text)
print(f"Sentiment: {'Positive' if prediction[0] == 1 else 'Negative'}")
```

### 3. **Medical Diagnosis**

```python
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load medical data
cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM
svm = SVC(kernel='rbf', C=1, gamma='scale')
svm.fit(X_train_scaled, y_train)

# Evaluate
accuracy = svm.score(X_test_scaled, y_test)
print(f"Cancer Detection Accuracy: {accuracy:.4f}")
```

### 4. **Fraud Detection**

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load credit card fraud dataset (example)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train with weighted classes (fraud is rare)
svm = SVC(kernel='rbf', C=1, class_weight='balanced')
svm.fit(X_train_scaled, y_train)

# Predictions
y_pred = svm.predict(X_test_scaled)
```

---

## Best Practices

### 1. **Always Scale Features**

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline

# Good: Use pipeline for automatic scaling
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf'))
])
pipeline.fit(X_train, y_train)

# Bad: Forgetting to scale
svm = SVC(kernel='rbf')
svm.fit(X_train, y_train)  # Features may have different scales
```

### 2. **Start with RBF Kernel**

```python
# Good: Start with RBF (most versatile)
svm = SVC(kernel='rbf', C=1, gamma='scale')

# Alternative: Try linear for initial experiments
svm = SVC(kernel='linear')

# Avoid: Using sigmoid without specific reason
svm = SVC(kernel='sigmoid')
```

### 3. **Use Cross-Validation for Tuning**

```python
from sklearn.model_selection import GridSearchCV

# Good: Use cross-validation
grid = GridSearchCV(SVC(), param_grid, cv=5)
grid.fit(X_train, y_train)

# Avoid: No cross-validation
svm = SVC(C=100, gamma=0.1)  # Arbitrary values
```

### 4. **Handle Class Imbalance**

```python
from sklearn.svm import SVC

# Good: Use class_weight for imbalanced data
svm = SVC(kernel='rbf', class_weight='balanced')

# Also good: Specify weights
class_weights = {0: 1, 1: 10}  # More weight to minority class
svm = SVC(kernel='rbf', class_weight=class_weights)

# Avoid: Ignoring class imbalance
svm = SVC(kernel='rbf')
```

### 5. **Monitor Training Progress**

```python
from sklearn.svm import SVC
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

svm = SVC(kernel='rbf')

# Learning curve
train_sizes, train_scores, val_scores = learning_curve(
    svm, X, y, cv=5, scoring='accuracy',
    train_sizes=np.linspace(0.1, 1.0, 10)
)

train_mean = np.mean(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)

plt.plot(train_sizes, train_mean, label='Training')
plt.plot(train_sizes, val_mean, label='Validation')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
```

### 6. **Use Probability Calibration for Imbalanced Data**

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC

# Base SVM
svm = SVC(kernel='rbf', probability=False)

# Calibrate probabilities
calibrated_svm = CalibratedClassifierCV(svm, method='sigmoid', cv=5)
calibrated_svm.fit(X_train, y_train)

# Better probability estimates
probs = calibrated_svm.predict_proba(X_test)
```

### 7. **Save and Load Models**

```python
import joblib
from sklearn.svm import SVC

# Train
svm = SVC(kernel='rbf')
svm.fit(X_train, y_train)

# Save
joblib.dump(svm, 'svm_model.pkl')

# Load
loaded_svm = joblib.load('svm_model.pkl')
predictions = loaded_svm.predict(X_test)
```

### 8. **Document Hyperparameters**

```python
from sklearn.svm import SVC
import json

# Store hyperparameters
hyperparameters = {
    'kernel': 'rbf',
    'C': 1.0,
    'gamma': 'scale',
    'cv': 5,
    'notes': 'Best model after grid search on validation set'
}

with open('hyperparameters.json', 'w') as f:
    json.dump(hyperparameters, f, indent=2)

# Recreate model
svm = SVC(**hyperparameters)
```

---

## Summary Table: When to Use SVM

| Scenario | Best Choice | Notes |
|----------|-------------|-------|
| Binary classification | SVM with RBF | Good baseline, fast training |
| Multi-class (3-10 classes) | SVM with OvR | Works well |
| High dimensions | Linear SVM | Efficient for sparse data |
| Non-linear patterns | RBF or Poly SVM | Requires tuning |
| Regression | SVR with RBF | Competitive with other methods |
| Imbalanced data | SVM with class_weight | Handle minority class |
| Real-time prediction | Linear SVM | Fast inference |
| Interpretability needed | Different model | SVM is black-box |
| Large datasets (>100k) | Linear SVM or neural nets | SVM can be slow |

---

## Comparison with Other Algorithms

| Algorithm | Speed | Accuracy | Interpretability | Scalability |
|-----------|-------|----------|------------------|-------------|
| **SVM** | Medium | High | Low | Medium |
| **Logistic Regression** | Fast | Medium | High | High |
| **Decision Trees** | Fast | Medium | High | High |
| **Random Forest** | Medium | High | Medium | High |
| **Neural Networks** | Slow | Very High | Low | High |
| **Naive Bayes** | Very Fast | Medium | High | Very High |

---

## Conclusion

Support Vector Machines are powerful algorithms for classification and regression. Key takeaways:

1. **Theory**: SVM finds the maximum margin hyperplane
2. **Kernels**: Enable handling of non-linear problems
3. **Regularization**: C parameter controls overfitting
4. **Practical**: Use scaling, proper evaluation, and hyperparameter tuning
5. **Trade-offs**: Good accuracy but slower training on large datasets

### When to Choose SVM
- ✅ High-dimensional data
- ✅ Clear margin separation
- ✅ Binary or small multi-class problems
- ✅ Need good generalization

### When to Choose Alternatives
- ❌ Very large datasets (>100k samples)
- ❌ Need interpretability
- ❌ Many classes (>50)
- ❌ Need real-time training

---

## Additional Resources

- [Scikit-learn SVM Documentation](https://scikit-learn.org/stable/modules/svm.html)
- [StatQuest: Support Vector Machines Playlist](https://www.youtube.com/watch?v=efR1C6CvhmE)
- [Understanding SVM through Geometry](https://www.youtube.com/watch?v=N1vOgolbjSc)
- [LibSVM: A Library for SVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)
- [Paper: Support Vector Networks by Boser, Guyon, Vapnik](https://dl.acm.org/doi/10.1145/130385.130401)

"""
Script 4: Train and Validate Models
Train multiple models and VALIDATE for overfitting

CRITICAL CHECKS:
- If training accuracy = 100%, something is WRONG (data leakage)
- Training vs Test accuracy should be reasonable (not > 15% difference)
- Use cross-validation to ensure robustness
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import json
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("MODEL TRAINING AND VALIDATION")
print("=" * 80)

# Load engineered data
df = pd.read_csv('kepler/kepler_engineered.csv')

print(f"\nDataset: {df.shape}")
print(f"Target distribution:")
print(df['is_exoplanet'].value_counts())
print(f"  Positive rate: {df['is_exoplanet'].mean()*100:.1f}%")

# Prepare data
X = df.drop(['is_exoplanet'], axis=1)
y = df['is_exoplanet']

print(f"\nFeatures: {X.shape[1]}")
print(f"Samples: {len(y)}")

# Clean data - replace inf and very large values
print(f"\nCleaning data...")
print(f"  Inf values: {np.isinf(X).sum().sum()}")
print(f"  NaN values: {np.isnan(X).sum().sum()}")

# Replace inf with NaN, then fill with median
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.median())

# Clip extreme values (beyond 99.9th percentile)
for col in X.columns:
    q99 = X[col].quantile(0.999)
    q01 = X[col].quantile(0.001)
    X[col] = X[col].clip(q01, q99)

print(f"  After cleaning - Inf: {np.isinf(X).sum().sum()}, NaN: {np.isnan(X).sum().sum()}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# Train multiple models
# ============================================================================

print(f"\n" + "=" * 80)
print("TRAINING MODELS")
print("=" * 80)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, max_depth=5, random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\n>>> Training {name}...")

    # Train
    model.fit(X_train_scaled, y_train)

    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # Accuracy
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    # Cross-validation (reduced folds for speed)
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=3, n_jobs=-1)
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    # OVERFITTING CHECK
    overfit_gap = train_acc - test_acc

    print(f"  Train Accuracy: {train_acc*100:.2f}%")
    print(f"  Test Accuracy:  {test_acc*100:.2f}%")
    print(f"  CV Accuracy:    {cv_mean*100:.2f}% (+/- {cv_std*100:.2f}%)")
    print(f"  Overfit Gap:    {overfit_gap*100:.2f}%")

    # WARNING FLAGS
    if train_acc >= 0.99:
        print(f"  [WARNING] Train accuracy = {train_acc*100:.1f}% - POSSIBLE DATA LEAKAGE!")
    if overfit_gap > 0.15:
        print(f"  [WARNING] Large overfit gap ({overfit_gap*100:.1f}%) - Model may be overfitting")
    if test_acc < 0.70:
        print(f"  [WARNING] Low test accuracy ({test_acc*100:.1f}%) - Model not learning well")

    results[name] = {
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'cv_mean': cv_mean,
        'cv_std': cv_std,
        'overfit_gap': overfit_gap
    }

# ============================================================================
# Detailed analysis of best model
# ============================================================================

print(f"\n" + "=" * 80)
print("BEST MODEL ANALYSIS")
print("=" * 80)

best_model_name = max(results, key=lambda x: results[x]['test_accuracy'])
best_model = models[best_model_name]

print(f"\nBest Model: {best_model_name}")
print(f"  Test Accuracy: {results[best_model_name]['test_accuracy']*100:.2f}%")

# Predictions
y_test_pred = best_model.predict(X_test_scaled)

# Classification report
print(f"\nClassification Report:")
print(classification_report(y_test, y_test_pred, target_names=['Not Exoplanet', 'Exoplanet']))

# Confusion matrix
cm = confusion_matrix(y_test, y_test_pred)
print(f"\nConfusion Matrix:")
print(f"                Predicted")
print(f"              Not  Exoplanet")
print(f"Actual Not    {cm[0,0]:<6} {cm[0,1]:<6}")
print(f"Actual Exo    {cm[1,0]:<6} {cm[1,1]:<6}")

# ============================================================================
# Feature importance (for tree-based models)
# ============================================================================

if hasattr(best_model, 'feature_importances_'):
    print(f"\n" + "=" * 80)
    print("FEATURE IMPORTANCE")
    print("=" * 80)

    importances = best_model.feature_importances_
    feature_names = X.columns

    # Sort
    indices = np.argsort(importances)[::-1]

    print(f"\nTop 20 Most Important Features:")
    print(f"{'Rank':<6} {'Feature':<35} {'Importance':<12}")
    print("-" * 60)
    for i, idx in enumerate(indices[:20], 1):
        print(f"{i:<6} {feature_names[idx]:<35} {importances[idx]:<12.6f}")

    # Save feature importance plot
    plt.figure(figsize=(10, 8))
    plt.barh(range(20), importances[indices[:20]][::-1])
    plt.yticks(range(20), feature_names[indices[:20]][::-1])
    plt.xlabel('Feature Importance')
    plt.title(f'Top 20 Features - {best_model_name}')
    plt.tight_layout()
    plt.savefig('kepler/feature_importance.png', dpi=150)
    print(f"\n[+] Saved feature importance plot: kepler/feature_importance.png")

# ============================================================================
# Save results
# ============================================================================

print(f"\n" + "=" * 80)
print("SAVING RESULTS")
print("=" * 80)

# Save model comparison
comparison_df = pd.DataFrame(results).T
comparison_df.to_csv('kepler/model_comparison.csv')
print(f"[+] Saved: kepler/model_comparison.csv")

# Save detailed results
detailed_results = {
    'best_model': best_model_name,
    'model_results': results,
    'classification_report': classification_report(y_test, y_test_pred,
                                                   target_names=['Not Exoplanet', 'Exoplanet'],
                                                   output_dict=True),
    'confusion_matrix': cm.tolist(),
    'dataset_info': {
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'num_features': X.shape[1],
        'positive_rate': float(df['is_exoplanet'].mean())
    }
}

with open('kepler/training_results.json', 'w') as f:
    json.dump(detailed_results, f, indent=2)

print(f"[+] Saved: kepler/training_results.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print(f"\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

print(f"\n[OK] All models trained and validated")
print(f"[OK] Best model: {best_model_name} ({results[best_model_name]['test_accuracy']*100:.2f}%)")
print(f"[OK] No data leakage detected" if results[best_model_name]['train_accuracy'] < 0.99 else "[X] POSSIBLE DATA LEAKAGE")
print(f"[OK] Overfitting controlled" if results[best_model_name]['overfit_gap'] < 0.15 else "[X] HIGH OVERFITTING")
print(f"\nAll results saved to kepler/ directory")
print("=" * 80)

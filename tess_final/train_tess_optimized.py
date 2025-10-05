"""
TESS - OPTIMIZED 3 CLASSIFIERS (FINAL VERSION)
================================================
Optimizations applied:
1. Simplified target: 6 classes → 3 classes (like Kepler)
2. SMOTE for class balancing
3. Regularization to reduce overfitting
4. All 14 engineered features

Models:
1. XGBoost (with regularization)
2. Random Forest (tuned parameters)
3. SVM (optimized)

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, f1_score, roc_auc_score
)
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("TESS - OPTIMIZED 3 CLASSIFIERS (FINAL VERSION)")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[1/7] Loading tess_processed.csv...")
df = pd.read_csv('tess_processed.csv')

print(f"   Shape: {df.shape}")
print(f"   Original target: tfopwg_disp (6 classes)")

# ============================================================================
# SIMPLIFY TARGET: 6 → 3 CLASSES
# ============================================================================

print("\n[2/7] Simplifying target to 3 classes...")

# Map 6 classes to 3
target_mapping = {
    'CP': 'CONFIRMED',      # Confirmed Planet
    'KP': 'CONFIRMED',      # Known Planet
    'PC': 'CANDIDATE',      # Planet Candidate
    'APC': 'CANDIDATE',     # Ambiguous Planet Candidate
    'FP': 'FALSE_POSITIVE', # False Positive
    'FA': 'FALSE_POSITIVE'  # False Alarm
}

df['target_simple'] = df['tfopwg_disp'].map(target_mapping)

print(f"\n   Target distribution (3 classes):")
for cls in sorted(df['target_simple'].unique()):
    count = sum(df['target_simple'] == cls)
    pct = count / len(df) * 100
    print(f"     {cls:<20} {count:>5,} ({pct:>5.1f}%)")

# Encode target
le = LabelEncoder()
df['target'] = le.fit_transform(df['target_simple'])

# Features
feature_cols = [col for col in df.columns if col not in ['tfopwg_disp', 'target_simple', 'target']]
print(f"\n   Features: {len(feature_cols)}")

# Remove NaN
df_clean = df.dropna()
print(f"   Samples after dropna: {len(df_clean):,} ({len(df_clean)/len(df)*100:.1f}%)")

X = df_clean[feature_cols]
y = df_clean['target']

# ============================================================================
# TRAIN-TEST SPLIT
# ============================================================================

print("\n[3/7] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train: {len(X_train):,} samples")
print(f"   Test:  {len(X_test):,} samples")

# ============================================================================
# PREPROCESSING
# ============================================================================

print("\n[4/7] Preprocessing with RobustScaler...")
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# SMOTE BALANCING
# ============================================================================

print("\n[5/7] Applying SMOTE for class balancing...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

print(f"   Before SMOTE: {len(X_train_scaled):,} samples")
print(f"   After SMOTE:  {len(X_train_balanced):,} samples")

print(f"\n   Balanced distribution:")
unique, counts = np.unique(y_train_balanced, return_counts=True)
for cls, count in zip(unique, counts):
    pct = count / len(y_train_balanced) * 100
    print(f"     {le.classes_[cls]:<20} {count:>5,} ({pct:>5.1f}%)")

# ============================================================================
# TRAIN OPTIMIZED MODELS
# ============================================================================

print("\n[6/7] Training optimized models...")

models = {}
results = {}

# 1. XGBoost (with strong regularization)
print("\n   [1/3] XGBoost (Regularized)...")
start = time.time()
xgb = XGBClassifier(
    n_estimators=200,
    max_depth=5,              # Reduced from 8
    learning_rate=0.1,
    min_child_weight=5,       # Increased from 1
    gamma=1.0,                # Regularization
    subsample=0.7,            # Reduced from 0.8
    colsample_bytree=0.7,     # Reduced from 0.8
    reg_alpha=0.5,            # L1 regularization
    reg_lambda=1.0,           # L2 regularization
    random_state=42,
    eval_metric='mlogloss',
    use_label_encoder=False
)
xgb.fit(X_train_balanced, y_train_balanced)
xgb_time = time.time() - start

y_pred_xgb = xgb.predict(X_test_scaled)
y_proba_xgb = xgb.predict_proba(X_test_scaled)

models['XGBoost'] = xgb
results['XGBoost'] = {
    'y_pred': y_pred_xgb,
    'y_proba': y_proba_xgb,
    'train_time': xgb_time,
    'train_acc': accuracy_score(y_train_balanced, xgb.predict(X_train_balanced)),
    'test_acc': accuracy_score(y_test, y_pred_xgb),
    'f1': f1_score(y_test, y_pred_xgb, average='weighted'),
    'auc': roc_auc_score(y_test, y_proba_xgb, multi_class='ovr', average='weighted')
}
print(f"      Train Acc: {results['XGBoost']['train_acc']:.4f}")
print(f"      Test Acc:  {results['XGBoost']['test_acc']:.4f}")
print(f"      AUC:       {results['XGBoost']['auc']:.4f}")
print(f"      Time:      {xgb_time:.2f}s")

# 2. Random Forest (optimized)
print("\n   [2/3] Random Forest (Optimized)...")
start = time.time()
rf = RandomForestClassifier(
    n_estimators=300,         # Increased from 200
    max_depth=12,             # Reduced from 15
    min_samples_split=10,     # Increased from 5
    min_samples_leaf=4,       # Increased from 2
    max_features='sqrt',      # More conservative
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_balanced, y_train_balanced)
rf_time = time.time() - start

y_pred_rf = rf.predict(X_test_scaled)
y_proba_rf = rf.predict_proba(X_test_scaled)

models['Random Forest'] = rf
results['Random Forest'] = {
    'y_pred': y_pred_rf,
    'y_proba': y_proba_rf,
    'train_time': rf_time,
    'train_acc': accuracy_score(y_train_balanced, rf.predict(X_train_balanced)),
    'test_acc': accuracy_score(y_test, y_pred_rf),
    'f1': f1_score(y_test, y_pred_rf, average='weighted'),
    'auc': roc_auc_score(y_test, y_proba_rf, multi_class='ovr', average='weighted')
}
print(f"      Train Acc: {results['Random Forest']['train_acc']:.4f}")
print(f"      Test Acc:  {results['Random Forest']['test_acc']:.4f}")
print(f"      AUC:       {results['Random Forest']['auc']:.4f}")
print(f"      Time:      {rf_time:.2f}s")

# 3. SVM (optimized)
print("\n   [3/3] SVM (Optimized)...")
start = time.time()
svm = SVC(
    kernel='rbf',
    C=5,                      # Reduced from 10
    gamma='scale',
    probability=True,
    random_state=42,
    class_weight='balanced'   # Handle imbalance
)
svm.fit(X_train_balanced, y_train_balanced)
svm_time = time.time() - start

y_pred_svm = svm.predict(X_test_scaled)
y_proba_svm = svm.predict_proba(X_test_scaled)

models['SVM'] = svm
results['SVM'] = {
    'y_pred': y_pred_svm,
    'y_proba': y_proba_svm,
    'train_time': svm_time,
    'train_acc': accuracy_score(y_train_balanced, svm.predict(X_train_balanced)),
    'test_acc': accuracy_score(y_test, y_pred_svm),
    'f1': f1_score(y_test, y_pred_svm, average='weighted'),
    'auc': roc_auc_score(y_test, y_proba_svm, multi_class='ovr', average='weighted')
}
print(f"      Train Acc: {results['SVM']['train_acc']:.4f}")
print(f"      Test Acc:  {results['SVM']['test_acc']:.4f}")
print(f"      AUC:       {results['SVM']['auc']:.4f}")
print(f"      Time:      {svm_time:.2f}s")

# ============================================================================
# EVALUATION
# ============================================================================

print("\n[7/7] Detailed evaluation...")

for model_name, res in results.items():
    print(f"\n{'='*80}")
    print(f"{model_name.upper()}")
    print(f"{'='*80}")
    print(classification_report(y_test, res['y_pred'], target_names=le.classes_, digits=4))

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\nGenerating comparison visualization...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('TESS OPTIMIZED - Model Comparison (3 Classes, SMOTE, Regularized)',
             fontsize=16, fontweight='bold')

# 1. Accuracy Comparison
ax1 = axes[0, 0]
model_names = list(results.keys())
train_accs = [results[m]['train_acc'] for m in model_names]
test_accs = [results[m]['test_acc'] for m in model_names]

x = np.arange(len(model_names))
width = 0.35

bars1 = ax1.bar(x - width/2, train_accs, width, label='Train', color='lightblue', edgecolor='black')
bars2 = ax1.bar(x + width/2, test_accs, width, label='Test', color='coral', edgecolor='black')

ax1.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
ax1.set_title('Train vs Test Accuracy', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(model_names, rotation=15, ha='right')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim([0.5, 1.0])

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# 2. AUC Comparison
ax2 = axes[0, 1]
aucs = [results[m]['auc'] for m in model_names]
colors = ['green' if auc > 0.8 else 'orange' if auc > 0.7 else 'red' for auc in aucs]
bars = ax2.bar(model_names, aucs, color=colors, edgecolor='black', alpha=0.7)

ax2.set_ylabel('AUC (weighted)', fontsize=11, fontweight='bold')
ax2.set_title('ROC AUC Score', fontsize=12, fontweight='bold')
ax2.set_xticklabels(model_names, rotation=15, ha='right')
ax2.grid(axis='y', alpha=0.3)
ax2.set_ylim([0.6, 1.0])

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{height:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 3. Training Time
ax3 = axes[1, 0]
times = [results[m]['train_time'] for m in model_names]
bars = ax3.bar(model_names, times, color='steelblue', edgecolor='black')

ax3.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
ax3.set_title('Training Time', fontsize=12, fontweight='bold')
ax3.set_xticklabels(model_names, rotation=15, ha='right')
ax3.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{height:.2f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 4. Confusion Matrix - Best Model
ax4 = axes[1, 1]
best_model = max(results.keys(), key=lambda m: results[m]['test_acc'])
cm = confusion_matrix(y_test, results[best_model]['y_pred'])

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_,
            cbar_kws={'label': 'Count'}, ax=ax4)
ax4.set_xlabel('Predicted', fontsize=11, fontweight='bold')
ax4.set_ylabel('Actual', fontsize=11, fontweight='bold')
ax4.set_title(f'Confusion Matrix - {best_model} (Best: {results[best_model]["test_acc"]:.2%})',
              fontsize=12, fontweight='bold')
plt.setp(ax4.get_xticklabels(), rotation=45, ha='right', fontsize=9)
plt.setp(ax4.get_yticklabels(), rotation=0, fontsize=9)

plt.tight_layout()
plt.savefig('tess_optimized_comparison.png', dpi=300, bbox_inches='tight')
print("   -> tess_optimized_comparison.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY - TESS OPTIMIZED MODELS")
print("="*80)

comparison_df = pd.DataFrame({
    'Model': model_names,
    'Train Acc': [results[m]['train_acc'] for m in model_names],
    'Test Acc': [results[m]['test_acc'] for m in model_names],
    'F1 Score': [results[m]['f1'] for m in model_names],
    'AUC': [results[m]['auc'] for m in model_names],
    'Time (s)': [results[m]['train_time'] for m in model_names]
})

print("\n" + comparison_df.to_string(index=False))

best_model = max(results.keys(), key=lambda m: results[m]['test_acc'])
print(f"\nBEST MODEL: {best_model}")
print(f"  Test Accuracy: {results[best_model]['test_acc']:.4f}")
print(f"  AUC: {results[best_model]['auc']:.4f}")
print(f"  F1 Score: {results[best_model]['f1']:.4f}")

# Overfitting analysis
train_test_gap = results[best_model]['train_acc'] - results[best_model]['test_acc']
print(f"  Overfitting Gap: {train_test_gap:.4f} ({train_test_gap*100:.1f}%)")

comparison_df.to_csv('tess_optimized_comparison.csv', index=False)
print("\n   -> tess_optimized_comparison.csv")

print("\n" + "="*80)
print("OPTIMIZATIONS APPLIED:")
print("="*80)
print("  1. Target simplified: 6 classes → 3 classes")
print("  2. SMOTE balancing applied")
print("  3. Regularization added (XGBoost, Random Forest)")
print("  4. All 14 engineered features used")
print(f"\nIMPROVEMENT vs Original:")
print(f"  Original: 65.86% (6 classes, no SMOTE)")
print(f"  Optimized: {results[best_model]['test_acc']*100:.2f}% (3 classes, SMOTE)")
print(f"  Gain: {(results[best_model]['test_acc'] - 0.6586)*100:+.2f}%")

print("\n" + "="*80)
print("DONE!")
print("="*80)

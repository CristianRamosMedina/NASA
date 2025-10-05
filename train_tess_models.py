"""
TESS - TRAIN 3 CLASSIFIERS
============================
Trains and compares:
1. XGBoost Classifier
2. Random Forest Classifier
3. SVM (Support Vector Machine)

Uses tess_processed.csv (8 features + target)

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
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("TESS - TRAINING 3 CLASSIFIERS")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[1/6] Loading tess_processed.csv...")
df = pd.read_csv('tess_processed.csv')

print(f"   Shape: {df.shape}")
print(f"   Target: tfopwg_disp")
print(f"   Classes: {df['tfopwg_disp'].unique()}")

# Encode target
le = LabelEncoder()
df['target'] = le.fit_transform(df['tfopwg_disp'])

print(f"\n   Target distribution:")
for cls, encoded in zip(le.classes_, range(len(le.classes_))):
    count = sum(df['target'] == encoded)
    pct = count / len(df) * 100
    print(f"     {cls}: {count:,} ({pct:.1f}%)")

# Features
feature_cols = [col for col in df.columns if col not in ['tfopwg_disp', 'target']]
print(f"\n   Features: {len(feature_cols)}")

# Remove NaN
df_clean = df.dropna()
print(f"   Samples after dropna: {len(df_clean):,} ({len(df_clean)/len(df)*100:.1f}%)")

X = df_clean[feature_cols]
y = df_clean['target']

# ============================================================================
# TRAIN-TEST SPLIT
# ============================================================================

print("\n[2/6] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train: {len(X_train):,} samples")
print(f"   Test:  {len(X_test):,} samples")

# ============================================================================
# PREPROCESSING
# ============================================================================

print("\n[3/6] Preprocessing with RobustScaler...")
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# TRAIN MODELS
# ============================================================================

print("\n[4/6] Training models...")

models = {}
results = {}

# 1. XGBoost
print("\n   [1/3] XGBoost Classifier...")
start = time.time()
xgb = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='mlogloss',
    use_label_encoder=False
)
xgb.fit(X_train_scaled, y_train)
xgb_time = time.time() - start

y_pred_xgb = xgb.predict(X_test_scaled)
y_proba_xgb = xgb.predict_proba(X_test_scaled)

models['XGBoost'] = xgb
results['XGBoost'] = {
    'y_pred': y_pred_xgb,
    'y_proba': y_proba_xgb,
    'train_time': xgb_time,
    'train_acc': accuracy_score(y_train, xgb.predict(X_train_scaled)),
    'test_acc': accuracy_score(y_test, y_pred_xgb),
    'f1': f1_score(y_test, y_pred_xgb, average='weighted'),
    'auc': roc_auc_score(y_test, y_proba_xgb, multi_class='ovr', average='weighted')
}
print(f"      Train Acc: {results['XGBoost']['train_acc']:.4f}")
print(f"      Test Acc:  {results['XGBoost']['test_acc']:.4f}")
print(f"      AUC:       {results['XGBoost']['auc']:.4f}")
print(f"      Time:      {xgb_time:.2f}s")

# 2. Random Forest
print("\n   [2/3] Random Forest Classifier...")
start = time.time()
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_scaled, y_train)
rf_time = time.time() - start

y_pred_rf = rf.predict(X_test_scaled)
y_proba_rf = rf.predict_proba(X_test_scaled)

models['Random Forest'] = rf
results['Random Forest'] = {
    'y_pred': y_pred_rf,
    'y_proba': y_proba_rf,
    'train_time': rf_time,
    'train_acc': accuracy_score(y_train, rf.predict(X_train_scaled)),
    'test_acc': accuracy_score(y_test, y_pred_rf),
    'f1': f1_score(y_test, y_pred_rf, average='weighted'),
    'auc': roc_auc_score(y_test, y_proba_rf, multi_class='ovr', average='weighted')
}
print(f"      Train Acc: {results['Random Forest']['train_acc']:.4f}")
print(f"      Test Acc:  {results['Random Forest']['test_acc']:.4f}")
print(f"      AUC:       {results['Random Forest']['auc']:.4f}")
print(f"      Time:      {rf_time:.2f}s")

# 3. SVM
print("\n   [3/3] SVM Classifier...")
start = time.time()
svm = SVC(
    kernel='rbf',
    C=10,
    gamma='scale',
    probability=True,
    random_state=42
)
svm.fit(X_train_scaled, y_train)
svm_time = time.time() - start

y_pred_svm = svm.predict(X_test_scaled)
y_proba_svm = svm.predict_proba(X_test_scaled)

models['SVM'] = svm
results['SVM'] = {
    'y_pred': y_pred_svm,
    'y_proba': y_proba_svm,
    'train_time': svm_time,
    'train_acc': accuracy_score(y_train, svm.predict(X_train_scaled)),
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

print("\n[5/6] Detailed evaluation...")

for model_name, res in results.items():
    print(f"\n{'='*80}")
    print(f"{model_name.upper()}")
    print(f"{'='*80}")
    print(classification_report(y_test, res['y_pred'], target_names=le.classes_, digits=4))

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\n[6/6] Generating comparison visualization...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('TESS - Model Comparison (XGBoost, Random Forest, SVM)',
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
ax1.set_ylim([0.3, 1.0])

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

sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges',
            xticklabels=le.classes_, yticklabels=le.classes_,
            cbar_kws={'label': 'Count'}, ax=ax4)
ax4.set_xlabel('Predicted', fontsize=11, fontweight='bold')
ax4.set_ylabel('Actual', fontsize=11, fontweight='bold')
ax4.set_title(f'Confusion Matrix - {best_model} (Best: {results[best_model]["test_acc"]:.2%})',
              fontsize=12, fontweight='bold')
plt.setp(ax4.get_xticklabels(), rotation=45, ha='right', fontsize=7)
plt.setp(ax4.get_yticklabels(), rotation=0, fontsize=7)

plt.tight_layout()
plt.savefig('tess_model_comparison.png', dpi=300, bbox_inches='tight')
print("   -> tess_model_comparison.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY - TESS MODELS")
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

comparison_df.to_csv('tess_models_comparison.csv', index=False)
print("\n   -> tess_models_comparison.csv")

print("\n" + "="*80)
print("DONE!")
print("="*80)

"""
EXOPLANET CLASSIFIER - VALIDATION WITH RANDOM FOREST
=====================================================
Uses scientifically selected features (from 1_feature_selection_scientific.py)
to train Random Forest and generate visualizations.

Outputs:
- Spearman correlation plot
- Chi-Square correlation plot
- Random Forest feature importance
- Model accuracy comparison

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("VALIDATION WITH RANDOM FOREST")
print("="*80)

# ============================================================================
# LOAD SELECTED FEATURES
# ============================================================================

print("\n[1/5] Loading selected features...")
kepler_selected = pd.read_csv('kepler_selected_features.csv')
tess_selected = pd.read_csv('tess_selected_features.csv')

print(f"   Kepler: {len(kepler_selected)} features selected")
print(f"   TESS: {len(tess_selected)} features selected")

# ============================================================================
# KEPLER - PREPARE DATA
# ============================================================================

print("\n[2/5] Preparing KEPLER data...")
kepler = pd.read_csv('Datasets/cumulative_2025.10.04_08.50.10.csv', comment='#')

# Encode target
df_kepler = kepler[kepler['koi_disposition'].notna()].copy()
le = LabelEncoder()
df_kepler['target'] = le.fit_transform(df_kepler['koi_disposition'])

# Get selected features
selected_features = kepler_selected['feature'].tolist()
df_kepler_clean = df_kepler[selected_features + ['target']].dropna()

X_kepler = df_kepler_clean[selected_features]
y_kepler = df_kepler_clean['target']

print(f"   Samples after removing NaN: {len(X_kepler):,}")
print(f"   Features used: {len(selected_features)}")
print(f"   Target distribution: {dict(zip(le.classes_, [sum(y_kepler == i) for i in range(len(le.classes_))]))}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_kepler, y_kepler, test_size=0.2, random_state=42, stratify=y_kepler
)

print(f"   Train size: {len(X_train):,} | Test size: {len(X_test):,}")

# ============================================================================
# KEPLER - TRAIN RANDOM FOREST
# ============================================================================

print("\n[3/5] Training Random Forest on KEPLER...")
rf_kepler = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_kepler.fit(X_train, y_train)

# Predictions
y_pred_train = rf_kepler.predict(X_train)
y_pred_test = rf_kepler.predict(X_test)

train_acc = rf_kepler.score(X_train, y_train)
test_acc = rf_kepler.score(X_test, y_test)

print(f"   Train Accuracy: {train_acc:.3f}")
print(f"   Test Accuracy: {test_acc:.3f}")

# Feature importance
rf_importance = pd.DataFrame({
    'feature': selected_features,
    'rf_importance': rf_kepler.feature_importances_
}).sort_values('rf_importance', ascending=False)

print("\n   Top 10 Features by Random Forest Importance:")
print(rf_importance.head(10).to_string(index=False))

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\n[4/5] Generating plots...")

# Merge RF importance with correlation metrics
kepler_selected_merged = kepler_selected.merge(rf_importance, on='feature')

# Separate features by type for plotting
spearman_features = kepler_selected_merged[kepler_selected_merged['spearman_corr'].notna()].copy()
chisquare_features = kepler_selected_merged[kepler_selected_merged['chisquare_cramers_v'].notna()].copy()

# Sort
spearman_features = spearman_features.sort_values('spearman_corr', ascending=False)
chisquare_features = chisquare_features.sort_values('chisquare_cramers_v', ascending=False)

# PLOT
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('KEPLER - Feature Analysis: Correlation vs Random Forest Importance',
             fontsize=16, fontweight='bold')

# 1. Spearman Correlation
ax1 = axes[0, 0]
if len(spearman_features) > 0:
    bars1 = ax1.barh(range(len(spearman_features)), spearman_features['spearman_corr'],
                     color='steelblue', edgecolor='black')
    ax1.set_yticks(range(len(spearman_features)))
    ax1.set_yticklabels(spearman_features['feature'], fontsize=9)
    ax1.set_xlabel('Spearman Correlation (absolute)', fontsize=11, fontweight='bold')
    ax1.set_title(f'Spearman Correlation ({len(spearman_features)} features)',
                  fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()
    for i, val in enumerate(spearman_features['spearman_corr']):
        ax1.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=8)

# 2. Chi-Square (Cramér's V)
ax2 = axes[0, 1]
if len(chisquare_features) > 0:
    bars2 = ax2.barh(range(len(chisquare_features)), chisquare_features['chisquare_cramers_v'],
                     color='coral', edgecolor='black')
    ax2.set_yticks(range(len(chisquare_features)))
    ax2.set_yticklabels(chisquare_features['feature'], fontsize=9)
    ax2.set_xlabel("Chi-Square (Cramér's V)", fontsize=11, fontweight='bold')
    ax2.set_title(f"Chi-Square Correlation ({len(chisquare_features)} features)",
                  fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()
    for i, val in enumerate(chisquare_features['chisquare_cramers_v']):
        ax2.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=8)

# 3. Random Forest Importance
ax3 = axes[1, 0]
rf_top15 = rf_importance.head(15)
bars3 = ax3.barh(range(len(rf_top15)), rf_top15['rf_importance'],
                 color='mediumseagreen', edgecolor='black')
ax3.set_yticks(range(len(rf_top15)))
ax3.set_yticklabels(rf_top15['feature'], fontsize=9)
ax3.set_xlabel('Random Forest Feature Importance', fontsize=11, fontweight='bold')
ax3.set_title(f'Random Forest Importance (Test Acc: {test_acc:.1%})',
              fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)
ax3.invert_yaxis()
for i, val in enumerate(rf_top15['rf_importance']):
    ax3.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=8)

# 4. Comparison: Max Correlation vs RF Importance
ax4 = axes[1, 1]
scatter_data = kepler_selected_merged.head(15)
colors = ['steelblue' if t == 'continuous' else 'coral' if t == 'binary' else 'orchid'
          for t in scatter_data['type']]

ax4.scatter(scatter_data['max_metric'], scatter_data['rf_importance'],
           s=200, c=colors, alpha=0.7, edgecolors='black', linewidth=1.5)

for idx, row in scatter_data.iterrows():
    ax4.annotate(row['feature'],
                (row['max_metric'], row['rf_importance']),
                fontsize=7, ha='right', va='bottom',
                xytext=(-3, 3), textcoords='offset points')

ax4.set_xlabel('Max Statistical Correlation', fontsize=11, fontweight='bold')
ax4.set_ylabel('Random Forest Importance', fontsize=11, fontweight='bold')
ax4.set_title('Correlation vs RF Importance (Top 15)', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.plot([0, 1], [0, 1], 'k--', alpha=0.2, linewidth=2)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='steelblue', label='Continuous'),
    Patch(facecolor='coral', label='Binary'),
    Patch(facecolor='orchid', label='Categorical')
]
ax4.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig('kepler_validation_analysis.png', dpi=300, bbox_inches='tight')
print("   -> kepler_validation_analysis.png")

# ============================================================================
# CLASSIFICATION REPORT
# ============================================================================

print("\n[5/5] Classification Report (Test Set):")
print("\n" + classification_report(y_test, y_pred_test, target_names=le.classes_))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_test)
print(cm)

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n[5/5] Saving results...")

# Merge all metrics
final_results = kepler_selected_merged[['feature', 'type', 'n_samples',
                                        'spearman_corr', 'chisquare_cramers_v',
                                        'mutual_info', 'max_metric', 'rf_importance']]
final_results = final_results.sort_values('rf_importance', ascending=False)
final_results.to_csv('kepler_final_features_validated.csv', index=False)

print("   -> kepler_final_features_validated.csv")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nKEPLER:")
print(f"  Features selected: {len(selected_features)}")
print(f"  Samples used: {len(X_kepler):,}")
print(f"  Train/Test split: {len(X_train):,} / {len(X_test):,}")
print(f"  Train Accuracy: {train_acc:.3f}")
print(f"  Test Accuracy: {test_acc:.3f}")
print(f"  Top feature (RF): {rf_importance.iloc[0]['feature']} ({rf_importance.iloc[0]['rf_importance']:.3f})")

print("\n" + "="*80)
print("DONE!")
print("="*80)

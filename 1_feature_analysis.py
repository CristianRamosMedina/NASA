"""
EXOPLANET CLASSIFIER - FEATURE ANALYSIS
========================================
Analyzes features using ML (Random Forest) and statistics (Spearman Correlation)
to determine the best columns for classifying exoplanets.

Datasets: KEPLER and TESS
Target: CONFIRMED vs CANDIDATE vs FALSE POSITIVE

Output:
- feature_analysis_kepler_tess.png (4 subplots: correlation + importance)
- feature_analysis_combined.png (comparative bars)
- Console report with top features

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("EXOPLANET FEATURE ANALYSIS - KEPLER & TESS")
print("="*80)

# ============================================================================
# KEPLER DATASET
# ============================================================================

print("\n[1/4] Loading KEPLER dataset...")
kepler = pd.read_csv('Datasets/cumulative_2025.10.04_08.50.10.csv', comment='#')

kepler_features = [
    # Orbital parameters
    'koi_period', 'koi_period_err1', 'koi_period_err2',
    'koi_sma', 'koi_eccen', 'koi_incl',
    # Transit parameters
    'koi_duration', 'koi_depth', 'koi_ingress',
    'koi_ror', 'koi_impact',
    # Planet parameters
    'koi_prad', 'koi_teq', 'koi_insol',
    # Stellar parameters
    'koi_steff', 'koi_slogg', 'koi_smet', 'koi_srad', 'koi_smass',
    # Fitted parameters
    'koi_srho', 'koi_dor',
    # Quality scores and flags
    'koi_score', 'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec',
    'koi_model_snr', 'koi_num_transits'
]

# Prepare data
df_kepler = kepler[['koi_disposition'] + kepler_features].copy()
df_kepler = df_kepler[df_kepler['koi_disposition'].notna()]
le = LabelEncoder()
df_kepler['target'] = le.fit_transform(df_kepler['koi_disposition'])

print(f"   Samples: {len(df_kepler):,}")
print(f"   Classes: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Calculate correlations
print("\n[2/4] Calculating correlations (Spearman)...")
kepler_corr = []
for col in kepler_features:
    if col in df_kepler.columns:
        valid = df_kepler[[col, 'target']].dropna()
        if len(valid) > 100:
            corr, pval = spearmanr(valid[col], valid['target'])
            kepler_corr.append({'feature': col, 'correlation': abs(corr), 'p_value': pval})

kepler_corr_df = pd.DataFrame(kepler_corr).sort_values('correlation', ascending=False).head(15)

# Calculate feature importance (Random Forest)
print("\n[3/4] Calculating feature importance (Random Forest)...")
features_rf = [col for col in kepler_features if df_kepler[col].notna().sum() / len(df_kepler) > 0.5]
df_rf = df_kepler[features_rf + ['target']].dropna()
X = df_rf[features_rf]
y = df_rf['target']

rf_kepler = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf_kepler.fit(X, y)

kepler_imp = pd.DataFrame({
    'feature': features_rf,
    'importance': rf_kepler.feature_importances_
}).sort_values('importance', ascending=False).head(15)

kepler_accuracy = rf_kepler.score(X, y)

# ============================================================================
# TESS DATASET
# ============================================================================

print("\n[1/4] Loading TESS dataset...")
tess = pd.read_csv('Datasets/TOI_2025.10.04_08.50.19.csv', comment='#')

tess_features = [
    # Orbital parameters
    'pl_orbper', 'pl_orbpererr1', 'pl_orbpererr2',
    # Transit parameters
    'pl_trandurh', 'pl_trandep', 'pl_trandeperr1',
    # Planet parameters
    'pl_rade', 'pl_radeerr1', 'pl_eqt', 'pl_insol',
    # Stellar parameters
    'st_teff', 'st_tefferr1', 'st_logg', 'st_rad', 'st_raderr1',
    'st_dist',
    # Proper motion
    'st_pmra', 'st_pmdec'
]

# Prepare data
df_tess = tess[['tfopwg_disp'] + tess_features].copy()
df_tess = df_tess[df_tess['tfopwg_disp'].notna()]
le_tess = LabelEncoder()
df_tess['target'] = le_tess.fit_transform(df_tess['tfopwg_disp'])

print(f"   Samples: {len(df_tess):,}")
print(f"   Classes: {dict(zip(le_tess.classes_, le_tess.transform(le_tess.classes_)))}")

# Calculate correlations
print("\n[2/4] Calculating correlations (Spearman)...")
tess_corr = []
for col in tess_features:
    if col in df_tess.columns:
        valid = df_tess[[col, 'target']].dropna()
        if len(valid) > 100:
            corr, pval = spearmanr(valid[col], valid['target'])
            tess_corr.append({'feature': col, 'correlation': abs(corr), 'p_value': pval})

tess_corr_df = pd.DataFrame(tess_corr).sort_values('correlation', ascending=False).head(15)

# Calculate feature importance (Random Forest)
print("\n[3/4] Calculating feature importance (Random Forest)...")
features_rf_tess = [col for col in tess_features if df_tess[col].notna().sum() / len(df_tess) > 0.5]
df_rf_tess = df_tess[features_rf_tess + ['target']].dropna()
X_tess = df_rf_tess[features_rf_tess]
y_tess = df_rf_tess['target']

rf_tess = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf_tess.fit(X_tess, y_tess)

tess_imp = pd.DataFrame({
    'feature': features_rf_tess,
    'importance': rf_tess.feature_importances_
}).sort_values('importance', ascending=False).head(15)

tess_accuracy = rf_tess.score(X_tess, y_tess)

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\n[4/4] Generating plots...")

plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

# PLOT 1: 4 subplots (correlation + importance)
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Feature Analysis: Correlation vs Importance (Top 15)', fontsize=16, fontweight='bold')

# KEPLER - Correlation
ax1 = axes[0, 0]
bars1 = ax1.barh(range(len(kepler_corr_df)), kepler_corr_df['correlation'], color='steelblue', edgecolor='black')
ax1.set_yticks(range(len(kepler_corr_df)))
ax1.set_yticklabels(kepler_corr_df['feature'], fontsize=9)
ax1.set_xlabel('Absolute Spearman Correlation', fontsize=11, fontweight='bold')
ax1.set_title(f'KEPLER - Correlation with Target', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)
ax1.invert_yaxis()
for i, val in enumerate(kepler_corr_df['correlation']):
    ax1.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=8)

# KEPLER - Importance
ax2 = axes[0, 1]
bars2 = ax2.barh(range(len(kepler_imp)), kepler_imp['importance'], color='coral', edgecolor='black')
ax2.set_yticks(range(len(kepler_imp)))
ax2.set_yticklabels(kepler_imp['feature'], fontsize=9)
ax2.set_xlabel('Random Forest Feature Importance', fontsize=11, fontweight='bold')
ax2.set_title(f'KEPLER - Feature Importance (Accuracy: {kepler_accuracy:.1%})', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()
for i, val in enumerate(kepler_imp['importance']):
    ax2.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=8)

# TESS - Correlation
ax3 = axes[1, 0]
bars3 = ax3.barh(range(len(tess_corr_df)), tess_corr_df['correlation'], color='mediumseagreen', edgecolor='black')
ax3.set_yticks(range(len(tess_corr_df)))
ax3.set_yticklabels(tess_corr_df['feature'], fontsize=9)
ax3.set_xlabel('Absolute Spearman Correlation', fontsize=11, fontweight='bold')
ax3.set_title(f'TESS - Correlation with Target', fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)
ax3.invert_yaxis()
for i, val in enumerate(tess_corr_df['correlation']):
    ax3.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=8)

# TESS - Importance
ax4 = axes[1, 1]
bars4 = ax4.barh(range(len(tess_imp)), tess_imp['importance'], color='orchid', edgecolor='black')
ax4.set_yticks(range(len(tess_imp)))
ax4.set_yticklabels(tess_imp['feature'], fontsize=9)
ax4.set_xlabel('Random Forest Feature Importance', fontsize=11, fontweight='bold')
ax4.set_title(f'TESS - Feature Importance (Accuracy: {tess_accuracy:.1%})', fontsize=12, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)
ax4.invert_yaxis()
for i, val in enumerate(tess_imp['importance']):
    ax4.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('feature_analysis_kepler_tess.png', dpi=300, bbox_inches='tight')
print("   -> feature_analysis_kepler_tess.png")

# PLOT 2: Combined bar chart
fig2, axes2 = plt.subplots(1, 2, figsize=(18, 10))
fig2.suptitle('Feature Analysis: Correlation AND Importance Combined', fontsize=16, fontweight='bold')

# KEPLER COMBINED
ax_k = axes2[0]
top_features_k = kepler_imp.head(10)['feature'].tolist()
corr_vals_k = []
imp_vals_k = []

for feat in top_features_k:
    corr_row = kepler_corr_df[kepler_corr_df['feature'] == feat]
    corr_vals_k.append(corr_row['correlation'].values[0] if len(corr_row) > 0 else 0)
    imp_row = kepler_imp[kepler_imp['feature'] == feat]
    imp_vals_k.append(imp_row['importance'].values[0] if len(imp_row) > 0 else 0)

x_k = np.arange(len(top_features_k))
width = 0.35

ax_k.bar(x_k - width/2, corr_vals_k, width, label='Correlation', color='steelblue', edgecolor='black')
ax_k.bar(x_k + width/2, imp_vals_k, width, label='Importance', color='coral', edgecolor='black')
ax_k.set_xlabel('Features', fontsize=12, fontweight='bold')
ax_k.set_ylabel('Value', fontsize=12, fontweight='bold')
ax_k.set_title(f'KEPLER - Top 10 Features (Accuracy: {kepler_accuracy:.1%})', fontsize=13, fontweight='bold')
ax_k.set_xticks(x_k)
ax_k.set_xticklabels(top_features_k, rotation=45, ha='right', fontsize=9)
ax_k.legend(fontsize=11)
ax_k.grid(axis='y', alpha=0.3)

# TESS COMBINED
ax_t = axes2[1]
top_features_t = tess_imp.head(10)['feature'].tolist()
corr_vals_t = []
imp_vals_t = []

for feat in top_features_t:
    corr_row = tess_corr_df[tess_corr_df['feature'] == feat]
    corr_vals_t.append(corr_row['correlation'].values[0] if len(corr_row) > 0 else 0)
    imp_row = tess_imp[tess_imp['feature'] == feat]
    imp_vals_t.append(imp_row['importance'].values[0] if len(imp_row) > 0 else 0)

x_t = np.arange(len(top_features_t))

ax_t.bar(x_t - width/2, corr_vals_t, width, label='Correlation', color='mediumseagreen', edgecolor='black')
ax_t.bar(x_t + width/2, imp_vals_t, width, label='Importance', color='orchid', edgecolor='black')
ax_t.set_xlabel('Features', fontsize=12, fontweight='bold')
ax_t.set_ylabel('Value', fontsize=12, fontweight='bold')
ax_t.set_title(f'TESS - Top 10 Features (Accuracy: {tess_accuracy:.1%})', fontsize=13, fontweight='bold')
ax_t.set_xticks(x_t)
ax_t.set_xticklabels(top_features_t, rotation=45, ha='right', fontsize=9)
ax_t.legend(fontsize=11)
ax_t.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('feature_analysis_combined.png', dpi=300, bbox_inches='tight')
print("   -> feature_analysis_combined.png")

# ============================================================================
# FINAL REPORT
# ============================================================================

print("\n" + "="*80)
print("FINAL RESULTS")
print("="*80)

print("\n--- KEPLER ---")
print(f"Accuracy: {kepler_accuracy:.1%}")
print(f"Samples: {len(X):,}")
print("\nTop 10 Features:")
print(kepler_imp.head(10).to_string(index=False))

print("\n--- TESS ---")
print(f"Accuracy: {tess_accuracy:.1%}")
print(f"Samples: {len(X_tess):,}")
print("\nTop 10 Features:")
print(tess_imp.head(10).to_string(index=False))

print("\n" + "="*80)
print("DONE!")
print("="*80)

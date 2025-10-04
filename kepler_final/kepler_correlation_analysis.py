"""
KEPLER - CORRELATION ANALYSIS
===============================
Generates correlation heatmaps and visualizations for selected features.

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("KEPLER - CORRELATION ANALYSIS")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[1/4] Loading kepler_processed.csv...")
df = pd.read_csv('kepler_processed.csv')

# Remove target and get features
feature_cols = [col for col in df.columns if col != 'koi_disposition']
df_features = df[feature_cols].copy()

# Remove NaN
df_clean = df_features.dropna()

print(f"   Shape: {df_clean.shape}")
print(f"   Features: {len(feature_cols)}")

# ============================================================================
# CORRELATION MATRIX (PEARSON)
# ============================================================================

print("\n[2/4] Calculating Pearson correlation...")
corr_pearson = df_clean.corr(method='pearson')

print(f"   Correlation matrix shape: {corr_pearson.shape}")

# ============================================================================
# CORRELATION MATRIX (SPEARMAN)
# ============================================================================

print("\n[3/4] Calculating Spearman correlation...")
corr_spearman = df_clean.corr(method='spearman')

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\n[4/4] Generating visualizations...")

# Create figure with 2 heatmaps
fig, axes = plt.subplots(1, 2, figsize=(28, 12))
fig.suptitle('KEPLER - Feature Correlation Analysis (20 Selected Features)',
             fontsize=18, fontweight='bold')

# 1. Pearson Correlation Heatmap
ax1 = axes[0]
mask = np.triu(np.ones_like(corr_pearson, dtype=bool), k=1)
sns.heatmap(corr_pearson, mask=mask, annot=False, cmap='coolwarm',
            center=0, vmin=-1, vmax=1, square=True,
            cbar_kws={'label': 'Pearson Correlation', 'shrink': 0.8},
            ax=ax1, linewidths=0.5)
ax1.set_title('Pearson Correlation Heatmap (Linear)', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=8)
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=8)

# 2. Spearman Correlation Heatmap
ax2 = axes[1]
mask = np.triu(np.ones_like(corr_spearman, dtype=bool), k=1)
sns.heatmap(corr_spearman, mask=mask, annot=False, cmap='coolwarm',
            center=0, vmin=-1, vmax=1, square=True,
            cbar_kws={'label': 'Spearman Correlation', 'shrink': 0.8},
            ax=ax2, linewidths=0.5)
ax2.set_title('Spearman Correlation Heatmap (Non-linear)', fontsize=14, fontweight='bold', pad=20)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=8)
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=8)

plt.tight_layout()
plt.savefig('kepler_correlation_heatmaps.png', dpi=300, bbox_inches='tight')
print("   -> kepler_correlation_heatmaps.png")

# ============================================================================
# DETAILED HEATMAP (with annotations for high correlations)
# ============================================================================

fig, ax = plt.subplots(figsize=(20, 18))
fig.suptitle('KEPLER - Spearman Correlation Matrix (Detailed)',
             fontsize=16, fontweight='bold')

# Create mask for upper triangle
mask = np.triu(np.ones_like(corr_spearman, dtype=bool), k=1)

# Create annotation matrix (only show values >= 0.7 or <= -0.7)
annot_matrix = corr_spearman.copy()
annot_matrix = annot_matrix.applymap(lambda x: f'{x:.2f}' if abs(x) >= 0.7 else '')

sns.heatmap(corr_spearman, mask=mask, annot=annot_matrix, fmt='',
            cmap='coolwarm', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5,
            cbar_kws={'label': 'Spearman Correlation', 'shrink': 0.8},
            ax=ax, annot_kws={'fontsize': 7})

ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)
ax.set_title('High correlations (|r| >= 0.7) annotated', fontsize=12, pad=20)

plt.tight_layout()
plt.savefig('kepler_correlation_detailed.png', dpi=300, bbox_inches='tight')
print("   -> kepler_correlation_detailed.png")

# ============================================================================
# TOP CORRELATIONS
# ============================================================================

print("\n" + "="*80)
print("TOP POSITIVE CORRELATIONS (Spearman)")
print("="*80)

# Get upper triangle indices
upper_triangle = np.triu_indices_from(corr_spearman, k=1)
corr_pairs = []

for i, j in zip(*upper_triangle):
    corr_pairs.append({
        'Feature 1': corr_spearman.index[i],
        'Feature 2': corr_spearman.columns[j],
        'Correlation': corr_spearman.iloc[i, j]
    })

df_corr_pairs = pd.DataFrame(corr_pairs)
df_corr_pairs = df_corr_pairs.sort_values('Correlation', ascending=False)

print("\nTop 20 Positive Correlations:")
print(df_corr_pairs.head(20).to_string(index=False))

print("\n" + "="*80)
print("TOP NEGATIVE CORRELATIONS (Spearman)")
print("="*80)

print("\nTop 10 Negative Correlations:")
print(df_corr_pairs.tail(10).to_string(index=False))

# Save correlation pairs
df_corr_pairs.to_csv('kepler_correlation_pairs.csv', index=False)
print("\n   -> kepler_correlation_pairs.csv")

# ============================================================================
# DISTRIBUTION PLOTS (Top 6 features by importance)
# ============================================================================

print("\n[BONUS] Distribution plots for top features...")

# Get top features from previous analysis
top_features = [
    'koi_score', 'koi_prad', 'koi_model_snr',
    'koi_max_sngle_ev', 'koi_fwm_stat_sig', 'koi_incl'
]

# Add target
df_with_target = df[top_features + ['koi_disposition']].dropna()

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('KEPLER - Distribution of Top 6 Features by Class',
             fontsize=16, fontweight='bold')

axes = axes.flatten()

for idx, feature in enumerate(top_features):
    ax = axes[idx]

    for target_class in df_with_target['koi_disposition'].unique():
        data = df_with_target[df_with_target['koi_disposition'] == target_class][feature]
        ax.hist(data, bins=30, alpha=0.5, label=target_class, edgecolor='black')

    ax.set_xlabel(feature, fontsize=10, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('kepler_feature_distributions.png', dpi=300, bbox_inches='tight')
print("   -> kepler_feature_distributions.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

high_corr = df_corr_pairs[abs(df_corr_pairs['Correlation']) >= 0.8]
print(f"\nFeature pairs with |correlation| >= 0.8: {len(high_corr)}")
print(f"Max positive correlation: {df_corr_pairs['Correlation'].max():.4f}")
print(f"Max negative correlation: {df_corr_pairs['Correlation'].min():.4f}")

if len(high_corr) > 0:
    print(f"\nHighly correlated pairs (|r| >= 0.8):")
    print(high_corr.to_string(index=False))

print("\nGenerated files:")
print("  - kepler_correlation_heatmaps.png (2 heatmaps: Pearson + Spearman)")
print("  - kepler_correlation_detailed.png (Detailed with annotations)")
print("  - kepler_correlation_pairs.csv (All pairwise correlations)")
print("  - kepler_feature_distributions.png (Top 6 features by class)")

print("\n" + "="*80)
print("DONE!")
print("="*80)

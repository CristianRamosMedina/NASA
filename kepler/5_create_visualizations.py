"""
Script 5: Create Correlation Visualizations
Creates correlation matrix and heatmap for documentation
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

print("=" * 80)
print("CREATING CORRELATION VISUALIZATIONS")
print("=" * 80)

# Load engineered data
df = pd.read_csv('kepler/kepler_engineered.csv')

print(f"\nDataset: {df.shape}")

# Separate features and target
X = df.drop(['is_exoplanet'], axis=1)
y = df['is_exoplanet']

# Calculate correlation with target
print(f"\nCalculating correlations with target...")
correlations = {}

for col in X.columns:
    # Spearman correlation (handles non-linear relationships)
    corr, _ = spearmanr(X[col], y)
    correlations[col] = corr

# Sort by absolute correlation
sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

# ============================================================================
# VISUALIZATION 1: Top 20 Features Correlation Bar Chart
# ============================================================================

print(f"\nCreating correlation bar chart...")

top_20 = sorted_corr[:20]
features = [x[0] for x in top_20]
corr_values = [x[1] for x in top_20]

plt.figure(figsize=(12, 8))
colors = ['#d73027' if x < 0 else '#1a9850' for x in corr_values]
bars = plt.barh(range(len(features)), corr_values, color=colors)

plt.yticks(range(len(features)), features)
plt.xlabel('Spearman Correlation with Exoplanet Classification', fontsize=12, fontweight='bold')
plt.title('Top 20 Features by Correlation\n(Positive = More likely Exoplanet, Negative = Less likely)',
          fontsize=14, fontweight='bold', pad=20)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, corr_values)):
    plt.text(val + 0.01 if val > 0 else val - 0.01, i, f'{val:.3f}',
             va='center', ha='left' if val > 0 else 'right', fontsize=9)

plt.tight_layout()
plt.savefig('kepler/correlation_bar_chart.png', dpi=150, bbox_inches='tight')
print(f"[+] Saved: kepler/correlation_bar_chart.png")

# ============================================================================
# VISUALIZATION 2: Correlation Heatmap (Top Features)
# ============================================================================

print(f"\nCreating correlation heatmap...")

# Select top 25 features for readability
top_25_features = [x[0] for x in sorted_corr[:25]]
df_top = X[top_25_features].copy()
df_top['is_exoplanet'] = y

# Calculate correlation matrix
corr_matrix = df_top.corr()

# Create heatmap
plt.figure(figsize=(16, 14))
sns.heatmap(corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            annot_kws={'size': 8})

plt.title('Correlation Heatmap - Top 25 Features + Target\n(Green = Positive Correlation, Red = Negative Correlation)',
          fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig('kepler/correlation_heatmap.png', dpi=150, bbox_inches='tight')
print(f"[+] Saved: kepler/correlation_heatmap.png")

# ============================================================================
# VISUALIZATION 3: Feature Category Correlation Summary
# ============================================================================

print(f"\nCreating category summary...")

# Categorize features
categories = {
    'Base - Orbital': ['koi_period', 'koi_sma', 'koi_eccen', 'koi_incl', 'koi_prad'],
    'Base - Transit': ['koi_duration', 'koi_depth', 'koi_ror', 'koi_impact'],
    'Base - Stellar': ['koi_steff', 'koi_slogg', 'koi_srad', 'koi_smass', 'koi_smet'],
    'Base - Detection': ['koi_count', 'koi_num_transits', 'koi_model_snr'],
    'Base - FP Flags': ['koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec'],
    'Engineered - Planet/Star': ['planet_star_radius_ratio', 'planet_density_proxy', 'insol_teq_ratio'],
    'Engineered - Orbital': ['orbital_velocity', 'hill_sphere_approx', 'periapsis_distance', 'apoapsis_distance'],
    'Engineered - Transit': ['depth_consistency', 'duration_impact_relation', 'transit_snr'],
    'Engineered - Stellar': ['stellar_density', 'main_sequence_deviation', 'metallicity_temp'],
    'Engineered - Colors': ['g_r_color', 'r_i_color', 'j_k_color'],
    'Engineered - Detection': ['is_multiplanet_system', 'total_fp_flags', 'snr_per_transit']
}

# Calculate average correlation per category
category_corr = {}
for cat, feats in categories.items():
    valid_feats = [f for f in feats if f in correlations]
    if valid_feats:
        avg_corr = np.mean([abs(correlations[f]) for f in valid_feats])
        category_corr[cat] = avg_corr

# Sort categories
sorted_cats = sorted(category_corr.items(), key=lambda x: x[1], reverse=True)

plt.figure(figsize=(12, 8))
cats = [x[0] for x in sorted_cats]
vals = [x[1] for x in sorted_cats]

colors_cat = ['#2166ac' if 'Base' in cat else '#b2182b' for cat in cats]
plt.barh(range(len(cats)), vals, color=colors_cat)
plt.yticks(range(len(cats)), cats, fontsize=10)
plt.xlabel('Average Absolute Correlation', fontsize=12, fontweight='bold')
plt.title('Feature Categories by Average Correlation Strength\n(Blue = Base Features, Red = Engineered Features)',
          fontsize=14, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

for i, val in enumerate(vals):
    plt.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('kepler/correlation_by_category.png', dpi=150, bbox_inches='tight')
print(f"[+] Saved: kepler/correlation_by_category.png")

# ============================================================================
# Save correlation summary
# ============================================================================

print(f"\nSaving correlation summary...")

corr_summary = {
    'top_20_correlations': [
        {'feature': feat, 'correlation': corr}
        for feat, corr in sorted_corr[:20]
    ],
    'category_averages': [
        {'category': cat, 'avg_correlation': corr}
        for cat, corr in sorted_cats
    ]
}

import json
with open('kepler/correlation_summary.json', 'w') as f:
    json.dump(corr_summary, f, indent=2)

print(f"[+] Saved: kepler/correlation_summary.json")

print(f"\n" + "=" * 80)
print("VISUALIZATIONS COMPLETE")
print("=" * 80)
print(f"\nGenerated files:")
print(f"  - kepler/correlation_bar_chart.png")
print(f"  - kepler/correlation_heatmap.png")
print(f"  - kepler/correlation_by_category.png")
print(f"  - kepler/correlation_summary.json")
print("=" * 80)

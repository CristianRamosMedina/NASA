"""
Script 2: Intelligent Feature Analysis for Kepler
Analyzes all columns and identifies which are useful for classification

RULES:
1. NO error columns (ra_err, dec_err, etc.) - don't contribute to classification
2. NO score columns if they directly indicate the answer (>75 = confirmed)
3. Focus on physical properties of the planetary system
4. Identify correlation types (linear, non-linear, categorical)
"""
import pandas as pd
import numpy as np
from scipy import stats
import json

print("=" * 80)
print("INTELLIGENT FEATURE ANALYSIS")
print("=" * 80)

# Load data
df = pd.read_csv('kepler/kepler_raw.csv')

# Create binary target for analysis
df['is_exoplanet'] = (df['koi_disposition'] == 'CONFIRMED').astype(int)

print(f"\nDataset: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Target distribution:")
print(df['koi_disposition'].value_counts())

# Categorize all columns
print(f"\n" + "=" * 80)
print("CATEGORIZING ALL COLUMNS")
print("=" * 80)

excluded_features = {
    'error_columns': [],
    'score_columns': [],
    'identifier_columns': [],
    'target_columns': [],
    'high_nulls': []
}

potential_features = {
    'orbital_properties': [],
    'transit_properties': [],
    'stellar_properties': [],
    'photometric_properties': [],
    'ratios_and_derived': []
}

# Analyze each column
for col in df.columns:
    # Skip target
    if col in ['koi_disposition', 'is_exoplanet']:
        excluded_features['target_columns'].append(col)
        continue

    # Identifiers
    if col in ['kepid', 'kepoi_name', 'kepler_name', 'ra_str', 'dec_str']:
        excluded_features['identifier_columns'].append(col)
        continue

    # Error columns - EXCLUDED
    if '_err' in col or 'err_' in col:
        excluded_features['error_columns'].append(col)
        continue

    # Score columns - need to check if they leak information
    if 'score' in col.lower() or 'disposition' in col.lower():
        excluded_features['score_columns'].append(col)
        continue

    # High nulls (>50%)
    null_pct = df[col].isnull().sum() / len(df) * 100
    if null_pct > 50:
        excluded_features['high_nulls'].append((col, f"{null_pct:.1f}%"))
        continue

    # Categorize by feature type
    if col.startswith('koi_period') or col.startswith('koi_time0') or col in ['koi_eccen', 'koi_longp', 'koi_prad', 'koi_sma', 'koi_incl']:
        potential_features['orbital_properties'].append(col)
    elif col.startswith('koi_duration') or col.startswith('koi_depth') or col.startswith('koi_ror') or col.startswith('koi_impact'):
        potential_features['transit_properties'].append(col)
    elif col.startswith('koi_steff') or col.startswith('koi_srad') or col.startswith('koi_smass') or col.startswith('koi_slogg'):
        potential_features['stellar_properties'].append(col)
    elif 'mag' in col and '_err' not in col:
        potential_features['photometric_properties'].append(col)
    else:
        potential_features['ratios_and_derived'].append(col)

# Print results
print(f"\n>>> EXCLUDED FEATURES <<<")
print(f"\n1. ERROR COLUMNS ({len(excluded_features['error_columns'])}):")
print(f"   Reason: Measurement uncertainty doesn't help classify planets")
print(f"   Examples: {excluded_features['error_columns'][:5]}")

print(f"\n2. SCORE/DISPOSITION COLUMNS ({len(excluded_features['score_columns'])}):")
print(f"   Reason: May leak information about the answer")
for col in excluded_features['score_columns']:
    print(f"   - {col}")

print(f"\n3. IDENTIFIER COLUMNS ({len(excluded_features['identifier_columns'])}):")
print(f"   Reason: Not physical properties")
for col in excluded_features['identifier_columns']:
    print(f"   - {col}")

print(f"\n4. HIGH NULL COLUMNS ({len(excluded_features['high_nulls'])}):")
print(f"   Reason: >50% missing data")
for col, pct in excluded_features['high_nulls'][:10]:
    print(f"   - {col}: {pct} nulls")

print(f"\n\n>>> POTENTIAL FEATURES <<<")

for category, features in potential_features.items():
    if features:
        print(f"\n{category.upper().replace('_', ' ')} ({len(features)}):")
        for feat in features:
            null_pct = df[feat].isnull().sum() / len(df) * 100
            print(f"   - {feat} (nulls: {null_pct:.1f}%)")

# Analyze correlations for potential features
print(f"\n" + "=" * 80)
print("CORRELATION ANALYSIS")
print("=" * 80)

all_potential = []
for feats in potential_features.values():
    all_potential.extend(feats)

# Filter to numeric columns with <30% nulls
numeric_features = []
for col in all_potential:
    if pd.api.types.is_numeric_dtype(df[col]):
        null_pct = df[col].isnull().sum() / len(df) * 100
        if null_pct < 30:
            numeric_features.append(col)

print(f"\nAnalyzing {len(numeric_features)} numeric features with <30% nulls")

# Calculate different correlation types
correlations = {}

for feat in numeric_features:
    # Remove nulls for correlation
    valid_data = df[[feat, 'is_exoplanet']].dropna()

    if len(valid_data) < 100:
        continue

    X = valid_data[feat].values
    y = valid_data['is_exoplanet'].values

    # Pearson (linear)
    pearson_r, pearson_p = stats.pearsonr(X, y)

    # Spearman (monotonic, non-linear)
    spearman_r, spearman_p = stats.spearmanr(X, y)

    # Point-biserial (for binary target)
    pointbiserial_r, pointbiserial_p = stats.pointbiserialr(y, X)

    correlations[feat] = {
        'pearson': abs(pearson_r),
        'spearman': abs(spearman_r),
        'pointbiserial': abs(pointbiserial_r),
        'null_pct': df[feat].isnull().sum() / len(df) * 100,
        'mean_exoplanet': valid_data[valid_data['is_exoplanet'] == 1][feat].mean(),
        'mean_not_exoplanet': valid_data[valid_data['is_exoplanet'] == 0][feat].mean()
    }

# Sort by best correlation (using max of all methods)
sorted_correlations = sorted(
    correlations.items(),
    key=lambda x: max(x[1]['pearson'], x[1]['spearman'], x[1]['pointbiserial']),
    reverse=True
)

print(f"\nTop 30 features by correlation:")
print(f"{'Feature':<30} {'Pearson':<10} {'Spearman':<10} {'PtBiserial':<12} {'Nulls%':<8}")
print("-" * 80)

for feat, corr in sorted_correlations[:30]:
    print(f"{feat:<30} {corr['pearson']:>8.4f}   {corr['spearman']:>8.4f}   {corr['pointbiserial']:>10.4f}   {corr['null_pct']:>6.1f}%")

# Save analysis
analysis_results = {
    'excluded_features': excluded_features,
    'potential_features': potential_features,
    'correlations': {k: v for k, v in sorted_correlations[:30]},
    'total_features_analyzed': len(df.columns),
    'features_kept': len(all_potential),
    'features_excluded': len(df.columns) - len(all_potential)
}

with open('kepler/feature_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2, default=str)

print(f"\n\nAnalysis saved to: kepler/feature_analysis.json")
print("=" * 80)

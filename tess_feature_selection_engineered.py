"""
TESS - Feature Selection on Engineered Dataset
================================================
Re-applies statistical feature selection on the engineered TESS dataset.

Uses tess_engineered.csv (74 features) instead of raw TESS data.
Removes ID columns (toi, toipfx, tid, etc.)
Threshold: 0.20 (between Kepler's 0.3 and previous TESS 0.15)

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("TESS - Feature Selection on Engineered Dataset (Threshold >= 0.20)")
print("="*80)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def detect_feature_type(series, threshold_categorical=10):
    n_unique = series.nunique()
    if n_unique <= 2:
        return 'binary'
    elif n_unique <= threshold_categorical:
        return 'categorical'
    else:
        return 'continuous'

def is_flag_feature(name):
    flag_keywords = ['flag', 'lim', 'symerr']
    return any(kw in name.lower() for kw in flag_keywords)

def calculate_metric(df, feature_col, target_col, feature_type, is_flag):
    mask = df[feature_col].notna() & df[target_col].notna()
    X_clean = df.loc[mask, feature_col]
    y_clean = df.loc[mask, target_col]

    if len(X_clean) < 100:
        return None, None, None, 'insufficient_data'

    metric_value = None
    p_value = None
    metric_name = None

    try:
        if is_flag:
            X_reshaped = X_clean.values.reshape(-1, 1)
            mi_score = mutual_info_classif(X_reshaped, y_clean,
                                          discrete_features=True,
                                          random_state=42)[0]
            metric_value = mi_score
            p_value = None
            metric_name = 'mutual_info'

        elif feature_type in ['binary', 'categorical']:
            contingency_table = pd.crosstab(X_clean, y_clean)
            chi2, pval, dof, expected = chi2_contingency(contingency_table)
            n = contingency_table.sum().sum()
            min_dim = min(contingency_table.shape) - 1
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
            metric_value = cramers_v
            p_value = pval
            metric_name = 'chi_square'

        else:
            corr, pval = spearmanr(X_clean, y_clean)
            metric_value = abs(corr)
            p_value = pval
            metric_name = 'spearman'

    except Exception as e:
        return None, None, None, f'error: {str(e)}'

    return metric_value, p_value, metric_name, 'success'

# ============================================================================
# LOAD ENGINEERED TESS DATA
# ============================================================================

print("\n[1/4] Loading TESS engineered dataset...")
tess = pd.read_csv('tess_engineered.csv')

print(f"   Shape: {tess.shape}")
print(f"   Total columns: {len(tess.columns)}")

# Filter by disposition
tess_clean = tess[tess['tfopwg_disp'].notna()].copy()
le = LabelEncoder()
tess_clean['target_encoded'] = le.fit_transform(tess_clean['tfopwg_disp'])

print(f"   Samples with disposition: {len(tess_clean):,}")
print(f"   Target classes: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# ============================================================================
# FILTER FEATURES
# ============================================================================

print("\n[2/4] Filtering features...")

# Exclude ID columns, flags, and target
exclude_patterns = ['rowid', 'toi', 'toipfx', 'tid', 'ctoi', 'pnum',
                   'rastr', 'decstr', 'tfopwg_disp', 'target',
                   'lim', 'symerr', 'created', 'update', 'str', 'alias']

numeric_cols = tess_clean.select_dtypes(include=[np.number]).columns.tolist()
feature_cols = [col for col in numeric_cols
               if not any(pattern in col.lower() for pattern in exclude_patterns)]

print(f"   Features to analyze: {len(feature_cols)}")

# ============================================================================
# CALCULATE CORRELATIONS
# ============================================================================

print(f"\n[3/4] Analyzing features...")

results = []

for i, col in enumerate(feature_cols):
    if (i + 1) % 20 == 0:
        print(f"   Progress: {i+1}/{len(feature_cols)}")

    feature_type = detect_feature_type(tess_clean[col])
    is_flag = is_flag_feature(col)

    metric_value, p_value, metric_name, status = calculate_metric(
        tess_clean, col, 'target_encoded', feature_type, is_flag
    )

    if status == 'success' and metric_value is not None:
        is_significant = (p_value is None) or (p_value < 0.05)
        is_selected = (metric_value >= 0.20) and is_significant

        results.append({
            'feature': col,
            'type': feature_type,
            'is_flag': is_flag,
            'metric_name': metric_name,
            'metric_value': metric_value,
            'p_value': p_value,
            'is_significant': is_significant,
            'is_selected': is_selected,
            'n_samples': tess_clean[col].notna().sum()
        })

df_results = pd.DataFrame(results).sort_values('metric_value', ascending=False)

selected = df_results[df_results['is_selected'] == True]
excluded = df_results[df_results['is_selected'] == False]

print(f"\n   SELECTED features (>= 0.20, p < 0.05): {len(selected)}")
print(f"   EXCLUDED features (< 0.20 or p >= 0.05): {len(excluded)}")

if len(selected) > 0:
    print(f"\n--- SELECTED FEATURES ---")
    print(selected[['feature', 'type', 'metric_name', 'metric_value', 'p_value']].to_string(index=False))

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n[4/4] Saving results...")

selected.to_csv('tess_selected_engineered.csv', index=False)
df_results.to_csv('tess_all_engineered.csv', index=False)

print("   -> tess_selected_engineered.csv")
print("   -> tess_all_engineered.csv")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nTESS ENGINEERED (threshold >= 0.20):")
print(f"  Total features analyzed: {len(df_results)}")
print(f"  SELECTED: {len(selected)}")
print(f"  EXCLUDED: {len(excluded)}")

if len(selected) > 0:
    print(f"\n  Metric breakdown:")
    print(f"    - Spearman: {len(selected[selected['metric_name'] == 'spearman'])}")
    print(f"    - Chi-Square: {len(selected[selected['metric_name'] == 'chi_square'])}")
    print(f"    - Mutual Info: {len(selected[selected['metric_name'] == 'mutual_info'])}")

    print(f"\n  Top 10 features:")
    top10 = selected.head(10)[['feature', 'metric_value', 'metric_name']]
    for idx, row in top10.iterrows():
        print(f"    {row['feature']:<35} {row['metric_value']:.3f} ({row['metric_name']})")

print("\n" + "="*80)
print("DONE! Now create tess_final/ folder with complete pipeline")
print("="*80)

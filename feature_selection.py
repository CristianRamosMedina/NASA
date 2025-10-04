"""
FINAL FEATURE SELECTION - KEPLER & TESS
=========================================
Re-applies scientific feature selection with adjusted thresholds:
- KEPLER: >= 0.3 correlation (moderate)
- TESS: >= 0.2 correlation (weak-moderate, due to low feature quality)

Uses optimized metric calculation (only correct metric per type).

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("FINAL FEATURE SELECTION - KEPLER (0.3) & TESS (0.15)")
print("="*80)

# ============================================================================
# HELPER FUNCTIONS (same as optimized version)
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

def analyze_dataset(df, target_col, dataset_name, threshold=0.3):
    print(f"\n{'='*80}")
    print(f"{dataset_name.upper()} DATASET (Threshold >= {threshold})")
    print(f"{'='*80}")

    df = df[df[target_col].notna()].copy()
    le = LabelEncoder()
    df['target_encoded'] = le.fit_transform(df[target_col])

    print(f"   Total samples: {len(df):,}")
    print(f"   Target classes: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    exclude_patterns = ['rowid', 'id', 'name', 'date', 'disposition', 'comment',
                       'quarters', 'delivname', 'datalink', 'limbdark', 'trans_mod',
                       'fittype', 'parm_prov', 'sparprov', 'target', 'str', 'disp_prov',
                       'rastr', 'decstr', 'vet_stat', 'alias', 'pnum', 'refname']

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [col for col in numeric_cols
                   if not any(pattern in col.lower() for pattern in exclude_patterns)]

    print(f"   Features to analyze: {len(feature_cols)}")

    results = []

    print(f"\n   Analyzing features...")
    for i, col in enumerate(feature_cols):
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i+1}/{len(feature_cols)}")

        feature_type = detect_feature_type(df[col])
        is_flag = is_flag_feature(col)

        metric_value, p_value, metric_name, status = calculate_metric(
            df, col, 'target_encoded', feature_type, is_flag
        )

        if status == 'success' and metric_value is not None:
            is_significant = (p_value is None) or (p_value < 0.05)
            is_selected = (metric_value >= threshold) and is_significant

            results.append({
                'feature': col,
                'type': feature_type,
                'is_flag': is_flag,
                'metric_name': metric_name,
                'metric_value': metric_value,
                'p_value': p_value,
                'is_significant': is_significant,
                'is_selected': is_selected,
                'n_samples': df[col].notna().sum()
            })

    df_results = pd.DataFrame(results).sort_values('metric_value', ascending=False)

    selected = df_results[df_results['is_selected'] == True]
    excluded = df_results[df_results['is_selected'] == False]

    print(f"\n   SELECTED features (>= {threshold}, p < 0.05): {len(selected)}")
    print(f"   EXCLUDED features (< {threshold} or p >= 0.05): {len(excluded)}")

    if len(selected) > 0:
        print(f"\n--- SELECTED FEATURES ---")
        print(selected[['feature', 'type', 'metric_name', 'metric_value', 'p_value']].head(30).to_string(index=False))

    return df_results, selected, excluded, le

# ============================================================================
# KEPLER (threshold 0.3)
# ============================================================================

print("\n[1/2] Loading KEPLER...")
kepler = pd.read_csv('Datasets/cumulative_2025.10.04_08.50.10.csv', comment='#')

kepler_all, kepler_selected, kepler_excluded, kepler_le = analyze_dataset(
    kepler, 'koi_disposition', 'KEPLER', threshold=0.3
)

# ============================================================================
# TESS (threshold 0.2 - lowered due to low feature quality)
# ============================================================================

print("\n[2/2] Loading TESS...")
tess = pd.read_csv('Datasets/TOI_2025.10.04_08.50.19.csv', comment='#')

tess_all, tess_selected, tess_excluded, tess_le = analyze_dataset(
    tess, 'tfopwg_disp', 'TESS', threshold=0.15
)

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n[SAVE] Saving results...")

kepler_selected.to_csv('kepler_selected_final.csv', index=False)
kepler_all.to_csv('kepler_all_final.csv', index=False)
print("   -> kepler_selected_final.csv")
print("   -> kepler_all_final.csv")

tess_selected.to_csv('tess_selected_final.csv', index=False)
tess_all.to_csv('tess_all_final.csv', index=False)
print("   -> tess_selected_final.csv")
print("   -> tess_all_final.csv")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

print(f"\nKEPLER (threshold >= 0.3):")
print(f"  Total features analyzed: {len(kepler_all)}")
print(f"  SELECTED: {len(kepler_selected)}")
print(f"  EXCLUDED: {len(kepler_excluded)}")
if len(kepler_selected) > 0:
    print(f"  Metric breakdown:")
    print(f"    - Spearman: {len(kepler_selected[kepler_selected['metric_name'] == 'spearman'])}")
    print(f"    - Chi-Square: {len(kepler_selected[kepler_selected['metric_name'] == 'chi_square'])}")
    print(f"    - Mutual Info: {len(kepler_selected[kepler_selected['metric_name'] == 'mutual_info'])}")

print(f"\nTESS (threshold >= 0.15, lowered due to weak features):")
print(f"  Total features analyzed: {len(tess_all)}")
print(f"  SELECTED: {len(tess_selected)}")
print(f"  EXCLUDED: {len(tess_excluded)}")
if len(tess_selected) > 0:
    print(f"  Metric breakdown:")
    print(f"    - Spearman: {len(tess_selected[tess_selected['metric_name'] == 'spearman'])}")
    print(f"    - Chi-Square: {len(tess_selected[tess_selected['metric_name'] == 'chi_square'])}")
    print(f"    - Mutual Info: {len(tess_selected[tess_selected['metric_name'] == 'mutual_info'])}")

print("\n" + "="*80)
print("DONE!")
print("="*80)

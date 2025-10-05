"""
TESS - Prepare Final Dataset
==============================
Extracts 14 selected engineered features for model training.

Author: NASA Exoplanet Team
"""

import pandas as pd
import json

print("="*80)
print("TESS - Prepare Final Dataset (14 Features)")
print("="*80)

# Load selected features
print("\n[1/3] Loading selected features...")
selected = pd.read_csv('../tess_selected_engineered_015.csv')
feature_list = selected['feature'].tolist()

print(f"   Selected features: {len(feature_list)}")

# Load engineered dataset
print("\n[2/3] Loading engineered dataset...")
tess_eng = pd.read_csv('../tess_engineered.csv')

print(f"   Total samples: {len(tess_eng):,}")
print(f"   Total columns: {len(tess_eng.columns)}")

# Extract selected features + target
output_cols = feature_list + ['tfopwg_disp']
tess_processed = tess_eng[output_cols].copy()

# Remove rows with ALL NaN in features
tess_clean = tess_processed.dropna(subset=feature_list, how='all')

print(f"   Samples after dropna: {len(tess_clean):,} ({len(tess_clean)/len(tess_eng)*100:.1f}%)")

# Save
print("\n[3/3] Saving...")
tess_clean.to_csv('tess_processed.csv', index=False)
print("   -> tess_processed.csv")

# Save feature list as JSON
with open('tess_features.json', 'w') as f:
    json.dump(feature_list, f, indent=2)
print("   -> tess_features.json")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nDataset: tess_processed.csv")
print(f"  Samples: {len(tess_clean):,}")
print(f"  Features: {len(feature_list)}")
print(f"  Target: tfopwg_disp")

print(f"\nSelected Features:")
for i, feat in enumerate(feature_list, 1):
    corr = selected[selected['feature'] == feat]['metric_value'].values[0]
    print(f"  {i:2d}. {feat:<35} (corr: {corr:.3f})")

print("\n" + "="*80)
print("DONE!")
print("="*80)

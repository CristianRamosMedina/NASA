"""
GENERATE PROCESSED DATASETS
============================
Creates processed CSVs with only selected features + target.

Output:
- kepler_processed.csv (20 features + koi_disposition)
- tess_processed.csv (4 features + tfopwg_disp)

Author: NASA Exoplanet Team
"""

import pandas as pd

print("="*80)
print("GENERATING PROCESSED DATASETS")
print("="*80)

# ============================================================================
# KEPLER
# ============================================================================

print("\n[1/2] Processing KEPLER...")

# Load selected features
kepler_selected = pd.read_csv('kepler_selected_final.csv')
selected_features = kepler_selected['feature'].tolist()

print(f"   Selected features: {len(selected_features)}")

# Load full dataset
kepler = pd.read_csv('Datasets/cumulative_2025.10.04_08.50.10.csv', comment='#')

# Select features + target
kepler_processed = kepler[selected_features + ['koi_disposition']].copy()

# Remove rows with NaN in target
kepler_processed = kepler_processed[kepler_processed['koi_disposition'].notna()]

print(f"   Original samples: {len(kepler):,}")
print(f"   After removing NaN target: {len(kepler_processed):,}")

# Save
kepler_processed.to_csv('kepler_processed.csv', index=False)
print(f"   Saved: kepler_processed.csv ({len(kepler_processed):,} rows × {len(kepler_processed.columns)} cols)")

# ============================================================================
# TESS
# ============================================================================

print("\n[2/2] Processing TESS...")

# Load selected features
tess_selected = pd.read_csv('tess_selected_final.csv')
selected_features_tess = tess_selected['feature'].tolist()

print(f"   Selected features: {len(selected_features_tess)}")

# Load full dataset
tess = pd.read_csv('Datasets/TOI_2025.10.04_08.50.19.csv', comment='#')

# Select features + target
tess_processed = tess[selected_features_tess + ['tfopwg_disp']].copy()

# Remove rows with NaN in target
tess_processed = tess_processed[tess_processed['tfopwg_disp'].notna()]

print(f"   Original samples: {len(tess):,}")
print(f"   After removing NaN target: {len(tess_processed):,}")

# Save
tess_processed.to_csv('tess_processed.csv', index=False)
print(f"   Saved: tess_processed.csv ({len(tess_processed):,} rows × {len(tess_processed.columns)} cols)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nKEPLER:")
print(f"  File: kepler_processed.csv")
print(f"  Samples: {len(kepler_processed):,}")
print(f"  Features: {len(selected_features)} + 1 target (koi_disposition)")
print(f"  Columns: {', '.join(selected_features[:5])}...")

print(f"\nTESS:")
print(f"  File: tess_processed.csv")
print(f"  Samples: {len(tess_processed):,}")
print(f"  Features: {len(selected_features_tess)} + 1 target (tfopwg_disp)")
print(f"  Columns: {', '.join(selected_features_tess)}")

print("\n" + "="*80)
print("DONE!")
print("="*80)

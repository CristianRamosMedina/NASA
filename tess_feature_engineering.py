"""
TESS - Feature Engineering to Match Kepler Quality
===================================================
Creates engineered features from TESS raw data to improve model performance.

Strategy:
1. Remove ID features (toi, toipfx)
2. Create ratios and derived metrics from planet parameters
3. Add quality indicators from measurement uncertainties
4. Normalize stellar properties
5. Create interaction features

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("TESS - FEATURE ENGINEERING")
print("="*80)

# Load TESS data
print("\n[1/5] Loading TESS dataset...")
tess = pd.read_csv('Datasets/TOI_2025.10.04_08.50.19.csv', comment='#')
print(f"   Shape: {tess.shape}")
print(f"   Total columns: {len(tess.columns)}")

# Filter by disposition
tess_clean = tess[tess['tfopwg_disp'].notna()].copy()
print(f"   Samples with disposition: {len(tess_clean):,}")

# Encode target
le = LabelEncoder()
tess_clean['target'] = le.fit_transform(tess_clean['tfopwg_disp'])
print(f"   Classes: {list(le.classes_)}")

# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

print("\n[2/5] Engineering features...")

# --- 1. PLANET QUALITY INDICATORS ---
print("   [A] Planet quality indicators...")

# Transit depth / error ratio (higher = better quality signal)
tess_clean['pl_trandep_snr'] = np.where(
    (tess_clean['pl_trandep'].notna()) & (tess_clean['pl_trandeperr1'].notna()) & (tess_clean['pl_trandeperr1'] > 0),
    tess_clean['pl_trandep'] / tess_clean['pl_trandeperr1'],
    np.nan
)

# Orbital period / error ratio
tess_clean['pl_orbper_snr'] = np.where(
    (tess_clean['pl_orbper'].notna()) & (tess_clean['pl_orbpererr1'].notna()) & (tess_clean['pl_orbpererr1'] > 0),
    tess_clean['pl_orbper'] / tess_clean['pl_orbpererr1'],
    np.nan
)

# Planet radius / error ratio
tess_clean['pl_rade_snr'] = np.where(
    (tess_clean['pl_rade'].notna()) & (tess_clean['pl_radeerr1'].notna()) & (tess_clean['pl_radeerr1'] > 0),
    tess_clean['pl_rade'] / tess_clean['pl_radeerr1'],
    np.nan
)

# Transit duration / error ratio
tess_clean['pl_trandurh_snr'] = np.where(
    (tess_clean['pl_trandurh'].notna()) & (tess_clean['pl_trandurherr1'].notna()) & (tess_clean['pl_trandurherr1'] > 0),
    tess_clean['pl_trandurh'] / tess_clean['pl_trandurherr1'],
    np.nan
)

# --- 2. PLANET PHYSICAL FEATURES ---
print("   [B] Planet physical features...")

# Transit depth (direct measurement)
tess_clean['pl_trandep_value'] = tess_clean['pl_trandep']

# Planetary radius (Earth radii)
tess_clean['pl_rade_value'] = tess_clean['pl_rade']

# Orbital period (days)
tess_clean['pl_orbper_value'] = tess_clean['pl_orbper']

# Equilibrium temperature
tess_clean['pl_eqt_value'] = tess_clean['pl_eqt']

# Insolation flux
tess_clean['pl_insol_value'] = tess_clean['pl_insol']

# Transit duration
tess_clean['pl_trandurh_value'] = tess_clean['pl_trandurh']

# --- 3. STELLAR QUALITY INDICATORS ---
print("   [C] Stellar quality indicators...")

# TESS magnitude (brightness) - already selected
tess_clean['st_tmag_value'] = tess_clean['st_tmag']

# Distance (parsecs) - already selected
tess_clean['st_dist_value'] = tess_clean['st_dist']

# Distance measurement quality (relative error)
tess_clean['st_dist_quality'] = np.where(
    (tess_clean['st_dist'].notna()) & (tess_clean['st_disterr1'].notna()) & (tess_clean['st_dist'] > 0),
    tess_clean['st_disterr1'] / tess_clean['st_dist'],
    np.nan
)

# Stellar radius
tess_clean['st_rad_value'] = tess_clean['st_rad']

# Stellar radius quality
tess_clean['st_rad_quality'] = np.where(
    (tess_clean['st_rad'].notna()) & (tess_clean['st_raderr1'].notna()) & (tess_clean['st_rad'] > 0),
    tess_clean['st_raderr1'] / tess_clean['st_rad'],
    np.nan
)

# Stellar effective temperature
tess_clean['st_teff_value'] = tess_clean['st_teff']

# Stellar log(g)
tess_clean['st_logg_value'] = tess_clean['st_logg']

# --- 4. DERIVED ORBITAL FEATURES ---
print("   [D] Derived orbital features...")

# Planet-to-star radius ratio (proxy for transit depth)
tess_clean['pl_rad_ratio'] = np.where(
    (tess_clean['pl_rade'].notna()) & (tess_clean['st_rad'].notna()) & (tess_clean['st_rad'] > 0),
    tess_clean['pl_rade'] / (tess_clean['st_rad'] * 109.2),  # Convert solar radii to Earth radii
    np.nan
)

# Semi-major axis estimate (Kepler's 3rd law)
# a^3 / P^2 = constant * M_star
# a (AU) ≈ (P^2 * M_star)^(1/3)
# Using st_rad as proxy for mass (larger stars tend to be more massive)
tess_clean['pl_semimajor_proxy'] = np.where(
    (tess_clean['pl_orbper'].notna()) & (tess_clean['st_rad'].notna()) & (tess_clean['st_rad'] > 0),
    (tess_clean['pl_orbper']**2 * tess_clean['st_rad'])**(1/3),
    np.nan
)

# Expected transit duration based on period and stellar radius
# T_dur ≈ (P/π) * (R_star/a)
tess_clean['pl_trandur_expected'] = np.where(
    (tess_clean['pl_semimajor_proxy'].notna()) & (tess_clean['st_rad'].notna()) & (tess_clean['pl_semimajor_proxy'] > 0),
    (tess_clean['pl_orbper'] / np.pi) * (tess_clean['st_rad'] / tess_clean['pl_semimajor_proxy']) * 24,  # hours
    np.nan
)

# Transit duration ratio (observed / expected)
tess_clean['pl_trandur_ratio'] = np.where(
    (tess_clean['pl_trandurh'].notna()) & (tess_clean['pl_trandur_expected'].notna()) & (tess_clean['pl_trandur_expected'] > 0),
    tess_clean['pl_trandurh'] / tess_clean['pl_trandur_expected'],
    np.nan
)

# --- 5. BRIGHTNESS & DISTANCE RATIOS ---
print("   [E] Brightness-distance features...")

# Brightness rank (normalized TESS magnitude)
tess_clean['st_brightness_norm'] = np.where(
    tess_clean['st_tmag'].notna(),
    (tess_clean['st_tmag'] - tess_clean['st_tmag'].min()) / (tess_clean['st_tmag'].max() - tess_clean['st_tmag'].min()),
    np.nan
)

# Distance rank (normalized)
tess_clean['st_distance_norm'] = np.where(
    tess_clean['st_dist'].notna(),
    (tess_clean['st_dist'] - tess_clean['st_dist'].min()) / (tess_clean['st_dist'].max() - tess_clean['st_dist'].min()),
    np.nan
)

# Brightness-distance product (closer + brighter = better)
tess_clean['st_brightness_dist_product'] = np.where(
    (tess_clean['st_brightness_norm'].notna()) & (tess_clean['st_distance_norm'].notna()),
    tess_clean['st_brightness_norm'] * (1 - tess_clean['st_distance_norm']),  # Invert distance
    np.nan
)

# --- 6. COMPOSITE QUALITY SCORE ---
print("   [F] Composite quality score...")

# Count non-null planet measurements
planet_cols = ['pl_trandep', 'pl_orbper', 'pl_rade', 'pl_trandurh', 'pl_insol', 'pl_eqt']
tess_clean['measurement_completeness'] = tess_clean[planet_cols].notna().sum(axis=1) / len(planet_cols)

# Average SNR (signal-to-noise ratio) across measurements
snr_cols = ['pl_trandep_snr', 'pl_orbper_snr', 'pl_rade_snr', 'pl_trandurh_snr']
tess_clean['avg_measurement_snr'] = tess_clean[snr_cols].mean(axis=1)

# ============================================================================
# SELECT ENGINEERED FEATURES
# ============================================================================

print("\n[3/5] Selecting engineered features...")

# Remove ID features
exclude_patterns = ['rowid', 'toi', 'toipfx', 'tid', 'ctoi_alias', 'pl_pnum',
                   'rastr', 'decstr', 'tfopwg_disp', 'target',
                   'lim', 'symerr', 'toi_created', 'rowupdate']

# Get all numeric columns
numeric_cols = tess_clean.select_dtypes(include=[np.number]).columns.tolist()

# Filter out excluded patterns
engineered_features = [col for col in numeric_cols
                      if not any(pattern in col.lower() for pattern in exclude_patterns)]

print(f"   Total engineered features: {len(engineered_features)}")

# Identify which are newly created
original_cols = set(tess.columns)
new_features = [f for f in engineered_features if f not in original_cols]
print(f"   Newly created features: {len(new_features)}")
print(f"   Examples: {new_features[:10]}")

# ============================================================================
# SAVE ENGINEERED DATASET
# ============================================================================

print("\n[4/5] Saving engineered dataset...")

# Prepare final dataset
output_cols = engineered_features + ['tfopwg_disp', 'target']
tess_engineered = tess_clean[output_cols].copy()

# Remove samples with ALL NaN features
tess_engineered_clean = tess_engineered.dropna(subset=engineered_features, how='all')

print(f"   Samples before dropna: {len(tess_engineered):,}")
print(f"   Samples after dropna: {len(tess_engineered_clean):,}")
print(f"   Features: {len(engineered_features)}")

tess_engineered_clean.to_csv('tess_engineered.csv', index=False)
print("   -> tess_engineered.csv")

# ============================================================================
# FEATURE STATISTICS
# ============================================================================

print("\n[5/5] Feature statistics...")

# Calculate correlation with target for new features
from scipy.stats import spearmanr

new_feature_corr = []
for feature in new_features:
    mask = tess_clean[feature].notna() & tess_clean['target'].notna()
    if mask.sum() >= 100:
        try:
            corr, pval = spearmanr(tess_clean.loc[mask, feature], tess_clean.loc[mask, 'target'])
            new_feature_corr.append({
                'feature': feature,
                'correlation': abs(corr),
                'p_value': pval,
                'n_samples': mask.sum()
            })
        except:
            pass

if new_feature_corr:
    df_corr = pd.DataFrame(new_feature_corr).sort_values('correlation', ascending=False)
    print(f"\n   Top 15 Newly Engineered Features (by correlation):")
    print(df_corr.head(15).to_string(index=False))

    # Save
    df_corr.to_csv('tess_engineered_features_correlation.csv', index=False)
    print("\n   -> tess_engineered_features_correlation.csv")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nOriginal TESS features: {len(original_cols)}")
print(f"Engineered features: {len(engineered_features)}")
print(f"   - Newly created: {len(new_features)}")
print(f"   - From original dataset: {len(engineered_features) - len(new_features)}")
print(f"\nSamples: {len(tess_engineered_clean):,}")
print(f"Target classes: {len(le.classes_)}")

print("\n" + "="*80)
print("DONE! Now run feature selection on tess_engineered.csv")
print("="*80)

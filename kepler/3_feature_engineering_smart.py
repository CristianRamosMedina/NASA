"""
Script 3: Intelligent Feature Engineering for Kepler
Creates only MEANINGFUL features with clear physical/astronomical reasoning

PHILOSOPHY:
- Each feature must have a clear reason WHY it helps classify exoplanets
- No features "just because" - every one is justified
- Focus on physical relationships, not random combinations
"""
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("INTELLIGENT FEATURE ENGINEERING")
print("=" * 80)

# Load data
df = pd.read_csv('kepler/kepler_raw.csv')
df['is_exoplanet'] = (df['koi_disposition'] == 'CONFIRMED').astype(int)

print(f"\nOriginal dataset: {df.shape}")

# ============================================================================
# STEP 1: Select base features (no errors, no scores)
# ============================================================================

base_features = [
    # Orbital properties
    'koi_period', 'koi_sma', 'koi_eccen', 'koi_incl', 'koi_prad',

    # Transit properties
    'koi_duration', 'koi_depth', 'koi_ror', 'koi_impact',

    # Stellar properties
    'koi_steff', 'koi_slogg', 'koi_srad', 'koi_smass', 'koi_smet',

    # Photometry (brightness in different bands)
    'koi_kepmag', 'koi_gmag', 'koi_rmag', 'koi_imag', 'koi_jmag', 'koi_hmag', 'koi_kmag',

    # Derived/calculated
    'koi_teq', 'koi_insol', 'koi_dor', 'koi_model_snr',

    # Count features
    'koi_count', 'koi_num_transits',

    # False positive flags (important!)
    'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec',

    # Sky coordinates
    'ra', 'dec'
]

# Create working dataframe
df_work = df[base_features + ['is_exoplanet']].copy()

print(f"\nBase features selected: {len(base_features)}")
print(f"Missing data summary:")
print(df_work.isnull().sum()[df_work.isnull().sum() > 0])

# ============================================================================
# STEP 2: Engineer INTELLIGENT features
# ============================================================================

print(f"\n" + "=" * 80)
print("CREATING ENGINEERED FEATURES")
print("=" * 80)

engineered_features = {}

# ---------------------------------------------------------------------------
# A. Planet-Star Relationship Features
# ---------------------------------------------------------------------------
print(f"\n>>> A. PLANET-STAR RELATIONSHIP FEATURES")

# A1: Planet-to-star radius ratio (alternative calculation)
if 'koi_prad' in df_work.columns and 'koi_srad' in df_work.columns:
    df_work['planet_star_radius_ratio'] = df_work['koi_prad'] / (df_work['koi_srad'] * 109.1)  # Convert solar radii to Earth radii
    engineered_features['planet_star_radius_ratio'] = {
        'formula': 'koi_prad / (koi_srad * 109.1)',
        'reasoning': 'Ratio of planet to star size. True planets have specific size ratios; large ratios may indicate stellar companion'
    }
    print(f"[+] planet_star_radius_ratio: Planet/star size ratio")

# A2: Planet density proxy (mass/radius^3)
if 'koi_prad' in df_work.columns and 'koi_smass' in df_work.columns:
    # Assuming planet mass correlates with star mass for estimation
    df_work['planet_density_proxy'] = df_work['koi_smass'] / (df_work['koi_prad'] ** 3)
    engineered_features['planet_density_proxy'] = {
        'formula': 'koi_smass / (koi_prad^3)',
        'reasoning': 'Density proxy. Rocky planets have higher density than gas giants; helps distinguish planet types'
    }
    print(f"[+] planet_density_proxy: Helps distinguish rocky vs gas planets")

# A3: Insolation to equilibrium temperature ratio
if 'koi_insol' in df_work.columns and 'koi_teq' in df_work.columns:
    df_work['insol_teq_ratio'] = df_work['koi_insol'] / (df_work['koi_teq'] ** 4)
    engineered_features['insol_teq_ratio'] = {
        'formula': 'koi_insol / (koi_teq^4)',
        'reasoning': 'Stefan-Boltzmann relationship. Inconsistencies may indicate false positives'
    }
    print(f"[+] insol_teq_ratio: Stefan-Boltzmann consistency check")

# ---------------------------------------------------------------------------
# B. Orbital Dynamics Features
# ---------------------------------------------------------------------------
print(f"\n>>> B. ORBITAL DYNAMICS FEATURES")

# B1: Orbital velocity (2pi * semi-major axis / period)
if 'koi_sma' in df_work.columns and 'koi_period' in df_work.columns:
    df_work['orbital_velocity'] = (2 * np.pi * df_work['koi_sma']) / df_work['koi_period']
    engineered_features['orbital_velocity'] = {
        'formula': '(2pi * koi_sma) / koi_period',
        'reasoning': 'Orbital velocity. Unusually high values may indicate unstable orbits or measurement errors'
    }
    print(f"[+] orbital_velocity: v = 2pir/T")

# B2: Hill sphere radius (orbital stability)
if 'koi_sma' in df_work.columns and 'koi_smass' in df_work.columns:
    # Simplified: r_hill ≈ a * (m_planet / (3 * m_star))^(1/3)
    # Using stellar mass as proxy
    df_work['hill_sphere_approx'] = df_work['koi_sma'] * (1 / (3 * df_work['koi_smass'])) ** (1/3)
    engineered_features['hill_sphere_approx'] = {
        'formula': 'koi_sma * (1 / (3 * koi_smass))^(1/3)',
        'reasoning': 'Hill sphere approximation. Indicates orbital stability region'
    }
    print(f"[+] hill_sphere_approx: Orbital stability indicator")

# B3: Eccentricity-based features
if 'koi_eccen' in df_work.columns and 'koi_sma' in df_work.columns:
    # Periapsis and apoapsis distances
    df_work['periapsis_distance'] = df_work['koi_sma'] * (1 - df_work['koi_eccen'])
    df_work['apoapsis_distance'] = df_work['koi_sma'] * (1 + df_work['koi_eccen'])
    engineered_features['periapsis_distance'] = {
        'formula': 'koi_sma * (1 - koi_eccen)',
        'reasoning': 'Closest approach to star. Affects temperature and tidal forces'
    }
    engineered_features['apoapsis_distance'] = {
        'formula': 'koi_sma * (1 + koi_eccen)',
        'reasoning': 'Farthest distance from star. Extreme orbits may indicate false positives'
    }
    print(f"[+] periapsis_distance & apoapsis_distance: Orbital extremes")

# ---------------------------------------------------------------------------
# C. Transit Geometry Features
# ---------------------------------------------------------------------------
print(f"\n>>> C. TRANSIT GEOMETRY FEATURES")

# C1: Transit depth consistency (should match (R_planet/R_star)^2)
if 'koi_depth' in df_work.columns and 'koi_ror' in df_work.columns:
    expected_depth = (df_work['koi_ror'] ** 2) * 1e6  # Convert to ppm
    df_work['depth_consistency'] = np.abs(df_work['koi_depth'] - expected_depth) / expected_depth
    engineered_features['depth_consistency'] = {
        'formula': 'abs(koi_depth - (koi_ror^2 * 1e6)) / (koi_ror^2 * 1e6)',
        'reasoning': 'Transit depth should equal (Rp/Rs)^2. Large deviations indicate problems'
    }
    print(f"[+] depth_consistency: Geometric consistency check")

# C2: Impact parameter effect on duration
if 'koi_impact' in df_work.columns and 'koi_duration' in df_work.columns and 'koi_period' in df_work.columns:
    # For central transits (b=0), duration is longer
    df_work['duration_impact_relation'] = df_work['koi_duration'] * (1 + df_work['koi_impact'] ** 2)
    engineered_features['duration_impact_relation'] = {
        'formula': 'koi_duration * (1 + koi_impact^2)',
        'reasoning': 'Duration depends on impact parameter. Helps identify grazing transits'
    }
    print(f"[+] duration_impact_relation: Grazing transit detector")

# C3: Transit signal-to-noise ratio
if 'koi_depth' in df_work.columns and 'koi_num_transits' in df_work.columns:
    df_work['transit_snr'] = df_work['koi_depth'] * np.sqrt(df_work['koi_num_transits'])
    engineered_features['transit_snr'] = {
        'formula': 'koi_depth * sqrt(koi_num_transits)',
        'reasoning': 'SNR improves with sqrt(N) transits. Higher SNR = more confident detection'
    }
    print(f"[+] transit_snr: Detection confidence metric")

# ---------------------------------------------------------------------------
# D. Stellar Properties Features
# ---------------------------------------------------------------------------
print(f"\n>>> D. STELLAR PROPERTIES FEATURES")

# D1: Stellar density (from log(g) and radius)
if 'koi_slogg' in df_work.columns and 'koi_srad' in df_work.columns:
    # ρ = g / (G * R^2), log(g) = log(ρ) + log(G*R^2)
    df_work['stellar_density'] = 10**df_work['koi_slogg'] / (df_work['koi_srad'] ** 2)
    engineered_features['stellar_density'] = {
        'formula': '10^koi_slogg / (koi_srad^2)',
        'reasoning': 'Stellar density from surface gravity. Helps identify stellar type'
    }
    print(f"[+] stellar_density: Star type indicator")

# D2: Main sequence position (Teff vs Mass relationship)
if 'koi_steff' in df_work.columns and 'koi_smass' in df_work.columns:
    # Roughly: Teff ∝ M^0.5 for main sequence stars
    expected_teff = 5778 * (df_work['koi_smass'] ** 0.5)  # Solar Teff = 5778K
    df_work['main_sequence_deviation'] = np.abs(df_work['koi_steff'] - expected_teff) / expected_teff
    engineered_features['main_sequence_deviation'] = {
        'formula': 'abs(koi_steff - (5778 * koi_smass^0.5)) / (5778 * koi_smass^0.5)',
        'reasoning': 'Deviation from main sequence. Large deviations may indicate evolved stars'
    }
    print(f"[+] main_sequence_deviation: Star evolution indicator")

# D3: Metallicity-temperature correlation
if 'koi_smet' in df_work.columns and 'koi_steff' in df_work.columns:
    df_work['metallicity_temp'] = df_work['koi_smet'] * (df_work['koi_steff'] / 5778)
    engineered_features['metallicity_temp'] = {
        'formula': 'koi_smet * (koi_steff / 5778)',
        'reasoning': 'Metal-rich stars (high metallicity) more likely to have planets'
    }
    print(f"[+] metallicity_temp: Planet formation indicator")

# ---------------------------------------------------------------------------
# E. Color and Photometry Features
# ---------------------------------------------------------------------------
print(f"\n>>> E. COLOR AND PHOTOMETRY FEATURES")

# E1: Optical color indices
if 'koi_gmag' in df_work.columns and 'koi_rmag' in df_work.columns:
    df_work['g_r_color'] = df_work['koi_gmag'] - df_work['koi_rmag']
    engineered_features['g_r_color'] = {
        'formula': 'koi_gmag - koi_rmag',
        'reasoning': 'g-r color index. Indicates star temperature/type'
    }
    print(f"[+] g_r_color: Optical color index")

if 'koi_rmag' in df_work.columns and 'koi_imag' in df_work.columns:
    df_work['r_i_color'] = df_work['koi_rmag'] - df_work['koi_imag']
    engineered_features['r_i_color'] = {
        'formula': 'koi_rmag - koi_imag',
        'reasoning': 'r-i color index. Another temperature indicator'
    }
    print(f"[+] r_i_color: Another color index")

# E2: Near-infrared color
if 'koi_jmag' in df_work.columns and 'koi_kmag' in df_work.columns:
    df_work['j_k_color'] = df_work['koi_jmag'] - df_work['koi_kmag']
    engineered_features['j_k_color'] = {
        'formula': 'koi_jmag - koi_kmag',
        'reasoning': 'J-K color. Less affected by extinction than optical colors'
    }
    print(f"[+] j_k_color: Infrared color index")

# ---------------------------------------------------------------------------
# F. Statistical/Detection Features
# ---------------------------------------------------------------------------
print(f"\n>>> F. STATISTICAL/DETECTION FEATURES")

# F1: Multi-planet system indicator
if 'koi_count' in df_work.columns:
    df_work['is_multiplanet_system'] = (df_work['koi_count'] > 1).astype(int)
    engineered_features['is_multiplanet_system'] = {
        'formula': 'koi_count > 1',
        'reasoning': 'Multi-planet systems more likely to be real (planets rarely come alone)'
    }
    print(f"[+] is_multiplanet_system: Multiple planets = higher confidence")

# F2: False positive flag combination
if all(col in df_work.columns for col in ['koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec']):
    df_work['total_fp_flags'] = df_work['koi_fpflag_nt'] + df_work['koi_fpflag_ss'] + df_work['koi_fpflag_co'] + df_work['koi_fpflag_ec']
    engineered_features['total_fp_flags'] = {
        'formula': 'sum of all false positive flags',
        'reasoning': 'More FP flags = higher chance of being false positive'
    }
    print(f"[+] total_fp_flags: Combined false positive indicator")

# F3: Signal quality metrics
if 'koi_model_snr' in df_work.columns and 'koi_num_transits' in df_work.columns:
    df_work['snr_per_transit'] = df_work['koi_model_snr'] / np.sqrt(df_work['koi_num_transits'])
    engineered_features['snr_per_transit'] = {
        'formula': 'koi_model_snr / sqrt(koi_num_transits)',
        'reasoning': 'SNR normalized by number of transits. Indicates signal strength'
    }
    print(f"[+] snr_per_transit: Per-transit signal strength")

# ============================================================================
# STEP 3: Save engineered dataset
# ============================================================================

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nOriginal features: {len(base_features)}")
print(f"Engineered features: {len(engineered_features)}")
print(f"Total features: {len(base_features) + len(engineered_features)}")
print(f"\nFinal dataset shape: {df_work.shape}")

# Handle missing values - simple imputation with median
print(f"\nHandling missing values...")
numeric_cols = df_work.select_dtypes(include=[np.number]).columns
df_work[numeric_cols] = df_work[numeric_cols].fillna(df_work[numeric_cols].median())

print(f"Missing values after imputation:")
print(df_work.isnull().sum().sum())

# Save
df_work.to_csv('kepler/kepler_engineered.csv', index=False)
print(f"\n[+] Saved: kepler/kepler_engineered.csv")

# Save feature documentation
feature_docs = {
    'base_features': base_features,
    'engineered_features': engineered_features,
    'total_features': len(base_features) + len(engineered_features),
    'dataset_shape': list(df_work.shape)
}

with open('kepler/feature_documentation.json', 'w') as f:
    json.dump(feature_docs, f, indent=2)

print(f"[+] Saved: kepler/feature_documentation.json")
print("=" * 80)

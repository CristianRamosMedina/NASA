# NASA Exoplanet Archive - Data Dictionary
**Complete Column Reference for Kepler & TESS Datasets**

---

## Table of Contents
1. [Kepler Selected Features (20)](#kepler-selected-features)
2. [TESS Selected Features (8 → 6 after cleanup)](#tess-selected-features)
3. [Comparison: Kepler vs TESS](#comparison-kepler-vs-tess)
4. [Target Variables](#target-variables)
5. [Data Quality Metrics](#data-quality-metrics)

---

## Kepler Selected Features

### Dataset: `cumulative_2025.10.04_08.50.10.csv`
**API**: [Kepler Objects of Interest](https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html)

| # | Column | Type | Unit | Corr | P-value | Description |
|---|--------|------|------|------|---------|-------------|
| 1 | `koi_score` | float | N/A | 0.750 | 0.0 | **Robovetter disposition score** (0-1, higher = planet) |
| 2 | `koi_fwm_stat_sig` | float | N/A | 0.451 | 0.0 | Flux-weighted centroid motion significance |
| 3 | `koi_srho_err2` | float | g/cm³ | 0.377 | 0.0 | Stellar density uncertainty (negative) |
| 4 | `koi_dor_err2` | float | N/A | 0.365 | 2.4e-285 | Planet-star distance ratio error (negative) |
| 5 | `koi_dor_err1` | float | N/A | 0.365 | 2.4e-285 | Planet-star distance ratio error (positive) |
| 6 | `koi_incl` | float | deg | 0.362 | 1.8e-283 | Orbital inclination (90° = edge-on) |
| 7 | `koi_prad_err1` | float | R⊕ | 0.351 | 8.8e-266 | Planetary radius uncertainty (positive) |
| 8 | `koi_count` | int | N/A | 0.343† | 0.0 | Number of planet candidates in system |
| 9 | `koi_dor` | float | N/A | 0.330 | 6.0e-232 | Semi-major axis / stellar radius (a/R★) |
| 10 | `koi_dikco_mdec_err` | float | arcsec | 0.328 | 4.6e-225 | KIC-centroid offset Dec error (diff image) |
| 11 | `koi_period_err1` | float | days | 0.327 | 1.3e-226 | Orbital period uncertainty (positive) |
| 12 | `koi_period_err2` | float | days | 0.327 | 1.3e-226 | Orbital period uncertainty (negative) |
| 13 | `koi_dikco_mra_err` | float | arcsec | 0.319 | 2.6e-212 | KIC-centroid offset RA error (diff image) |
| 14 | `koi_prad_err2` | float | R⊕ | 0.316 | 1.5e-212 | Planetary radius uncertainty (negative) |
| 15 | `koi_dikco_msky_err` | float | arcsec | 0.315 | 5.5e-206 | KIC-centroid offset sky error (diff image) |
| 16 | `koi_max_sngle_ev` | float | N/A | 0.314 | 8.3e-192 | Maximum single-event statistic |
| 17 | `koi_prad` | float | R⊕ | 0.312 | 6.2e-207 | **Planetary radius** |
| 18 | `koi_dicco_mdec_err` | float | arcsec | 0.311 | 8.7e-201 | Centroid offset Dec error (diff image) |
| 19 | `koi_model_snr` | float | N/A | 0.309 | 3.9e-202 | Transit model signal-to-noise ratio |
| 20 | `koi_dicco_mra_err` | float | arcsec | 0.301 | 1.3e-186 | Centroid offset RA error (diff image) |

**† Chi-Square (Cramér's V) for categorical variable**

---

## TESS Selected Features

### Dataset: `TOI_2025.10.04_08.50.19.csv`
**API**: [TESS Objects of Interest](https://exoplanetarchive.ipac.caltech.edu/docs/API_toi_columns.html)

| # | Column | Type | Unit | Corr | P-value | Description | Status |
|---|--------|------|------|------|---------|-------------|--------|
| ~~1~~ | ~~`toi`~~ | identifier | N/A | 0.405 | 6.6e-302 | TOI catalog number | ❌ **REMOVE** |
| ~~2~~ | ~~`toipfx`~~ | integer | N/A | 0.405 | 6.7e-302 | TOI integer prefix | ❌ **REMOVE** |
| 3 | `st_tmag` | float | mag | 0.299 | 1.7e-158 | **TESS-band magnitude** (brightness) | ✓ Valid |
| 4 | `st_dist` | float | pc | 0.238 | 8.0e-97 | Distance to system | ✓ Valid |
| 5 | `st_disterr1` | float | pc | 0.184 | 4.7e-54 | Distance uncertainty (positive) | ✓ Valid |
| 6 | `st_disterr2` | float | pc | 0.184 | 4.7e-54 | Distance uncertainty (negative) | ✓ Valid |
| 7 | `st_pmdecerr1` | float | mas/yr | 0.170 | 2.3e-50 | Proper motion Dec error (positive) | ✓ Valid |
| 8 | `st_pmdecerr2` | float | mas/yr | 0.170 | 2.3e-50 | Proper motion Dec error (negative) | ✓ Valid |

**Valid Features**: 6 (after removing identifiers)
**Correlation Range**: 0.170 - 0.299 (weak to moderate)

---

## Comparison: Kepler vs TESS

| Metric | Kepler | TESS | Notes |
|--------|--------|------|-------|
| **Selected Features** | 20 | 6 (valid) | TESS lacks quality metrics |
| **Best Correlation** | 0.750 (koi_score) | 0.299 (st_tmag) | 2.5x stronger |
| **Threshold** | >= 0.3 | >= 0.15 | TESS lowered due to weak features |
| **Samples** | 9,564 | 7,703 | Similar dataset sizes |
| **Target Classes** | 3 | 6 | TESS more complex, imbalanced |
| **Test Accuracy** | 89.25% | 69.76% | 20% gap |
| **Overfitting Gap** | 8.6% (RF) | 28.7% (XGBoost) | TESS struggles to generalize |

---

## Target Variables

### Kepler: `koi_disposition`
**Type**: Categorical (3 classes)

| Class | Code | Count | % | Description |
|-------|------|-------|---|-------------|
| CANDIDATE | 0 | ~2,300 | 25% | Awaiting confirmation |
| CONFIRMED | 1 | ~3,200 | 35% | Validated planet |
| FALSE POSITIVE | 2 | ~3,700 | 40% | Not a planet |

**Balance**: Well-balanced, no severe class imbalance

---

### TESS: `tfopwg_disp`
**Type**: Categorical (6 classes)

| Class | Code | Count | % | Description |
|-------|------|-------|---|-------------|
| APC | 0 | ~350 | 5% | Ambiguous Planet Candidate |
| CP | 1 | ~450 | 6.5% | Confirmed Planet |
| FA | 2 | ~120 | 1.7% | False Alarm |
| FP | 3 | ~1,950 | 28% | False Positive |
| KP | 4 | ~40 | 0.6% | Known Planet |
| PC | 5 | ~4,200 | 60.7% | **Planet Candidate (dominant)** |

**Balance**: SEVERE imbalance, PC dominates at 60.7%

---

## Data Quality Metrics

### Feature Selection Statistics

| Dataset | Total Cols | Analyzed | Selected | Selection Rate | Avg Correlation |
|---------|-----------|----------|----------|----------------|-----------------|
| Kepler | 141 | 103 | 20 | 19.4% | 0.355 |
| TESS | 94 | 67 | 6 (valid) | 9.0% | 0.207 |

### Missing Data

**Kepler**:
- Samples before dropna: 9,564
- Samples after dropna: 7,070 (26% loss)
- Features with >30% missing: 15

**TESS**:
- Samples before dropna: 7,703
- Samples after dropna: 6,995 (9% loss)
- Features with >30% missing: 8

---

## Feature Categories

### Kepler Breakdown

| Category | Count | Example Features | Purpose |
|----------|-------|------------------|---------|
| Centroid Tests | 8 | `koi_dikco_mdec_err`, `koi_dicco_mra_err` | Validate transit origin |
| Orbital Geometry | 5 | `koi_incl`, `koi_dor` | Planet-star configuration |
| Planet Size | 4 | `koi_prad`, `koi_prad_err1` | Radius measurements |
| Detection Quality | 2 | `koi_model_snr`, `koi_max_sngle_ev` | Signal strength |
| Score/Quality | 1 | **`koi_score`** | Pre-computed disposition |
| Period | 2 | `koi_period_err1/2` | Orbital period errors |

---

### TESS Breakdown

| Category | Count | Example Features | Purpose |
|----------|-------|------------------|---------|
| Stellar Properties | 4 | `st_tmag`, `st_dist` | Brightness/distance |
| Astrometry | 2 | `st_pmdecerr1/2` | Catalog quality |
| ~~Identifiers~~ | ~~2~~ | ~~`toi`, `toipfx`~~ | ~~Removed~~ |

---

## Key Insights

### Why Kepler Outperforms TESS?

1. **Robovetter Score** (`koi_score`):
   - Kepler's most powerful feature (0.750 correlation)
   - Pre-computed by NASA using multi-test pipeline
   - TESS has NO equivalent

2. **Centroid Validation**:
   - Kepler: 8 centroid features (0.301-0.328)
   - TESS: 0 centroid features
   - Critical for detecting background eclipsing binaries

3. **Mission Maturity**:
   - Kepler: 8+ years, fully vetted
   - TESS: Ongoing mission, early-stage candidates

4. **Dataset Simplicity**:
   - Kepler: 3 balanced classes
   - TESS: 6 imbalanced classes (PC = 60.7%)

---

## Recommended Actions

### TESS Improvements

1. ✅ **Remove identifiers**: `toi`, `toipfx`
2. ⚠️ **Lower threshold**: 0.15 → 0.10 to capture more physical features
3. ⚠️ **Simplify target**: 6 classes → 3 (CONFIRMED, FALSE POSITIVE, CANDIDATE)
4. ⚠️ **Feature engineering**: Add brightness/distance ratios
5. ⚠️ **Class balancing**: Use SMOTE or class weights

### Kepler Production Readiness

1. ✅ Features validated and documented
2. ✅ No identifier leakage
3. ⚠️ Save trained models as `.pkl` files
4. ⚠️ Add cross-validation for robustness
5. ⚠️ Fix feature selection leakage (calculate correlations on train set only)

---

## References

- [Kepler API Columns](https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html)
- [TESS API Columns](https://exoplanetarchive.ipac.caltech.edu/docs/API_toi_columns.html)
- [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

---

**Generated**: 2025-10-05
**Author**: NASA Exoplanet Classification Pipeline
**Version**: 1.0

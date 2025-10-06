# NASA Exoplanet Classification Project

Intelligent machine learning pipeline for classifying Kepler exoplanet candidates using **smart feature engineering** and rigorous validation.

## 🎯 Project Philosophy

This project follows a **quality over quantity** approach:
- ✅ **No error columns** (measurement uncertainty doesn't help classification)
- ✅ **No score/disposition leakage** (would give away the answer)
- ✅ **Every feature has a physical/astronomical reason**
- ✅ **Rigorous validation** (no 100% accuracy = no data leakage)

## 📊 Results Summary

### Best Model: Gradient Boosting
- **Test Accuracy**: 94.56%
- **Precision (Exoplanet)**: 90%
- **Recall (Exoplanet)**: 91%
- **Overfitting Gap**: 1.63% ✅ (well controlled)

### Model Comparison

| Model | Train Acc | Test Acc | CV Acc | Overfit Gap |
|-------|-----------|----------|--------|-------------|
| **Gradient Boosting** | 96.20% | **94.56%** | 93.40% | 1.63% |
| Random Forest | 96.58% | 94.04% | 93.23% | 2.53% |
| Logistic Regression | 88.79% | 90.02% | 88.35% | -1.23% |

## 🔬 Feature Engineering Strategy

**Total: 52 features (33 base + 19 engineered)**

All 52 features were used together to train the models and achieve 94.56% accuracy.

### Base Features (33)

Selected from 153 original columns, excluding:
- **68 error columns** (ra_err, dec_err, etc.) - Don't contribute to classification
- **2 score columns** (koi_score, koi_pdisposition) - Would leak information
- **5 high-null columns** (>50% missing data)
- **5 identifier columns** (kepid, names, etc.) - Not physical properties

#### Orbital Properties (7)
1. **koi_period** - Orbital period in days
2. **koi_time0bk** - Transit time (BJD - 2,454,833.0)
3. **koi_time0** - Transit epoch (BJD - 2,454,833.0)
4. **koi_eccen** - Orbital eccentricity
5. **koi_prad** - Planetary radius (Earth radii)
6. **koi_sma** - Semi-major axis (AU)
7. **koi_incl** - Orbital inclination (degrees)

#### Transit Properties (4)
8. **koi_duration** - Transit duration (hours)
9. **koi_depth** - Transit depth (ppm)
10. **koi_ror** - Planet-star radius ratio
11. **koi_impact** - Impact parameter

#### Stellar Properties (4)
12. **koi_steff** - Stellar effective temperature (K)
13. **koi_slogg** - Stellar surface gravity (log10(cm/s²))
14. **koi_srad** - Stellar radius (Solar radii)
15. **koi_smass** - Stellar mass (Solar masses)

#### Photometric Properties (8)
16. **koi_kepmag** - Kepler magnitude
17. **koi_gmag** - g-band magnitude
18. **koi_rmag** - r-band magnitude
19. **koi_imag** - i-band magnitude
20. **koi_zmag** - z-band magnitude
21. **koi_jmag** - J-band magnitude (2MASS)
22. **koi_hmag** - H-band magnitude (2MASS)
23. **koi_kmag** - K-band magnitude (2MASS)

#### Derived/Calculated Properties (6)
24. **koi_teq** - Equilibrium temperature (K)
25. **koi_insol** - Insolation flux (Earth flux)
26. **koi_dor** - Planet-star distance over stellar radius
27. **koi_model_snr** - Transit signal-to-noise ratio
28. **koi_smet** - Stellar metallicity [Fe/H]

#### Detection/Count Features (2)
29. **koi_count** - Number of planet candidates in system
30. **koi_num_transits** - Number of transits observed

#### False Positive Flags (4)
31. **koi_fpflag_nt** - Not transit-like flag
32. **koi_fpflag_ss** - Stellar eclipse flag
33. **koi_fpflag_co** - Centroid offset flag
34. **koi_fpflag_ec** - Ephemeris match flag

#### Sky Coordinates (2)
35. **ra** - Right Ascension (degrees)
36. **dec** - Declination (degrees)

---

### Engineered Features (19)

Created from base features using physical/astronomical principles:

#### A. Planet-Star Relationship (3 features)
1. **planet_star_radius_ratio**: `koi_prad / (koi_srad * 109.1)`
   - *Why*: True planets have specific size ratios; large ratios may indicate stellar companion

2. **planet_density_proxy**: `koi_smass / (koi_prad^3)`
   - *Why*: Rocky planets have higher density than gas giants

3. **insol_teq_ratio**: `koi_insol / (koi_teq^4)`
   - *Why*: Stefan-Boltzmann consistency check; inconsistencies indicate false positives

#### B. Orbital Dynamics (4 features)
4. **orbital_velocity**: `(2π * koi_sma) / koi_period`
   - *Why*: Unusually high values indicate unstable orbits

5. **hill_sphere_approx**: `koi_sma * (1 / (3 * koi_smass))^(1/3)`
   - *Why*: Orbital stability indicator

6. **periapsis_distance**: `koi_sma * (1 - koi_eccen)`
   - *Why*: Closest approach affects temperature and tidal forces

7. **apoapsis_distance**: `koi_sma * (1 + koi_eccen)`
   - *Why*: Extreme orbits may indicate false positives

#### C. Transit Geometry (3 features)
8. **depth_consistency**: `abs(koi_depth - (koi_ror^2 * 1e6)) / (koi_ror^2 * 1e6)`
   - *Why*: Transit depth should equal (Rp/Rs)²; large deviations indicate problems

9. **duration_impact_relation**: `koi_duration * (1 + koi_impact^2)`
   - *Why*: Helps identify grazing transits

10. **transit_snr**: `koi_depth * sqrt(koi_num_transits)`
    - *Why*: SNR improves with √N transits; higher SNR = more confident detection

#### D. Stellar Properties (3 features)
11. **stellar_density**: `10^koi_slogg / (koi_srad^2)`
    - *Why*: Helps identify stellar type

12. **main_sequence_deviation**: `abs(koi_steff - (5778 * koi_smass^0.5)) / (5778 * koi_smass^0.5)`
    - *Why*: Large deviations may indicate evolved stars

13. **metallicity_temp**: `koi_smet * (koi_steff / 5778)`
    - *Why*: Metal-rich stars more likely to have planets

#### E. Color & Photometry (3 features)
14. **g_r_color**: `koi_gmag - koi_rmag`
    - *Why*: Indicates star temperature/type

15. **r_i_color**: `koi_rmag - koi_imag`
    - *Why*: Another temperature indicator

16. **j_k_color**: `koi_jmag - koi_kmag`
    - *Why*: Less affected by extinction than optical colors

#### F. Statistical/Detection (3 features)
17. **is_multiplanet_system**: `koi_count > 1`
    - *Why*: Multi-planet systems more likely to be real

18. **total_fp_flags**: Sum of all false positive flags
    - *Why*: More FP flags = higher chance of being false positive

19. **snr_per_transit**: `koi_model_snr / sqrt(koi_num_transits)`
    - *Why*: Indicates per-transit signal strength

### Top 10 Most Important Features

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | total_fp_flags | 46.12% | Detection |
| 2 | koi_model_snr | 31.07% | Base |
| 3 | metallicity_temp | 2.83% | Stellar |
| 4 | koi_period | 2.65% | Orbital |
| 5 | planet_density_proxy | 2.41% | Planet-Star |
| 6 | depth_consistency | 1.52% | Transit |
| 7 | is_multiplanet_system | 1.41% | Detection |
| 8 | snr_per_transit | 1.25% | Detection |
| 9 | koi_count | 1.22% | Base |
| 10 | koi_impact | 0.91% | Transit |

## 📁 Project Structure

```
NASA/
├── kepler/                              # Kepler pipeline
│   ├── 1_download_data.py              # Download dataset from NASA
│   ├── 2_analyze_features.py           # Intelligent feature analysis
│   ├── 3_feature_engineering_smart.py  # Smart feature engineering
│   ├── 4_train_and_validate.py         # Model training & validation
│   ├── kepler_raw.csv                  # Raw dataset (9,564 samples)
│   ├── kepler_engineered.csv           # Engineered dataset (52 features)
│   ├── feature_analysis.json           # Feature analysis results
│   ├── feature_documentation.json      # Feature reasoning docs
│   ├── model_comparison.csv            # Model performance comparison
│   ├── training_results.json           # Detailed training results
│   └── feature_importance.png          # Feature importance plot
│
├── projectonasa/                        # Frontend application
│   ├── app.js                          # Express server
│   ├── views/                          # EJS templates
│   ├── public/                         # Static files
│   └── package.json                    # Dependencies
│
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 🚀 Quick Start

### 1. Frontend Setup

```bash
cd projectonasa
npm install
npm start
```

Frontend will be available at `http://localhost:3000`

### 2. Run Kepler Pipeline

```bash
# Download data
python kepler/1_download_data.py

# Analyze features
python kepler/2_analyze_features.py

# Engineer features
python kepler/3_feature_engineering_smart.py

# Train and validate
python kepler/4_train_and_validate.py
```

## 🔍 Validation & Quality Checks

### ✅ No Data Leakage
- Train accuracy: 96.20% (NOT 100%)
- Test accuracy: 94.56%
- If train = 100%, something is wrong!

### ✅ Controlled Overfitting
- Overfit gap: 1.63% (< 15% threshold)
- Cross-validation confirms: 93.40% ± 0.30%

### ✅ Appropriate Correlations
- Used Pearson (linear), Spearman (monotonic), and Point-Biserial (binary target)
- Different features require different correlation methods

### ✅ No "Baboso" Features
- Every feature has clear physical/astronomical reasoning
- No random combinations or "kitchen sink" approach

## 📈 Performance Metrics

### Confusion Matrix
```
                Predicted
              Not  Exoplanet
Actual Not    1309   55
Actual Exo    49     500
```

- **True Positives**: 500 exoplanets correctly identified
- **False Positives**: 55 non-exoplanets misclassified
- **False Negatives**: 49 exoplanets missed
- **True Negatives**: 1309 non-exoplanets correctly identified

## 🛠 Technologies

- **Python 3.10+**
  - pandas, numpy - Data manipulation
  - scikit-learn - Machine learning
  - scipy - Statistical analysis
  - matplotlib, seaborn - Visualization

- **Node.js / Express**
  - Frontend web application
  - EJS templates
  - Tailwind CSS

## 📝 Key Insights

1. **False Positive Flags** are the most important features (46%)
2. **SNR-based features** are crucial for detection confidence
3. **Metallicity** correlates with planet presence (metal-rich stars)
4. **Multi-planet systems** are more likely to be real
5. **Consistency checks** (depth, geometry) help filter false positives

## 🎓 Lessons Learned

### ❌ What NOT to Do
- Don't include error columns - they add noise
- Don't use score/disposition columns - data leakage
- Don't create features "just because" - each needs reasoning
- Don't trust 100% accuracy - check for leakage
- Don't use only linear correlations - data isn't always linear

### ✅ What TO Do
- Remove error columns systematically
- Validate for leakage and overfitting
- Document reasoning for each feature
- Use multiple correlation methods
- Check train/test gap rigorously

## 🤖 Generated with Claude Code

This project was developed using intelligent feature engineering principles and rigorous machine learning practices.

**Branch**: `feature_kepler_intelligent`
**Date**: 2025-10-05

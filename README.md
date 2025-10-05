# Exoplanet Classifier - Machine Learning Pipeline

Complete machine learning pipeline for exoplanet classification using Kepler and TESS mission data.

**Goal:** Classify exoplanets as **CONFIRMED**, **CANDIDATE**, or **FALSE POSITIVE** using scientifically selected features and ensemble models.

---

## 📁 Project Structure

```
NASA/
├── Datasets/
│   ├── cumulative_2025.10.04_08.50.10.csv    # Kepler (9,564 exoplanets, 141 features)
│   └── TOI_2025.10.04_08.50.19.csv           # TESS (7,703 exoplanets, 87 features)
│
├── kepler_final/                              # Kepler complete pipeline
│   ├── train_kepler_models.py                # Train XGBoost, Random Forest, SVM
│   ├── predict_new_candidate.py              # Predict new Kepler candidates
│   ├── kepler_processed.csv                  # Clean dataset (7,070 samples × 21 cols)
│   ├── kepler_features.json                  # 20 selected features list
│   └── README_KEPLER.md                      # Detailed Kepler documentation
│
├── feature_selection.py                       # Statistical feature selection
├── prepare_datasets.py                        # Generate processed CSVs
├── tess_feature_engineering.py                # TESS feature engineering (NEW!)
├── train_tess_models.py                       # Train TESS models
│
├── kepler_selected_final.csv                  # Kepler: 20 features selected
├── tess_engineered.csv                        # TESS: 74 engineered features (NEW!)
├── tess_selected_final.csv                    # TESS: 8 features selected (old)
│
├── DATA_DICTIONARY.md                         # Complete column documentation
└── README.md                                  # This file
```

---

## 🚀 Quick Start

### **Workflow 1: KEPLER (Production Ready)**

```bash
# 1. Feature selection (statistical)
python feature_selection.py

# 2. Prepare clean dataset
python prepare_datasets.py

# 3. Train models
cd kepler_final
python train_kepler_models.py

# 4. Predict new candidates
python predict_new_candidate.py --demo
```

---

### **Workflow 2: TESS (With Feature Engineering)**

```bash
# 1. Feature engineering (create quality metrics)
python tess_feature_engineering.py

# 2. Feature selection on engineered features
# (Edit feature_selection.py to use tess_engineered.csv)

# 3. Train models
python train_tess_models.py
```

---

## 📊 Results Summary

### **KEPLER** 🏆

| Model | Test Accuracy | AUC | F1 Score | Training Time |
|-------|---------------|-----|----------|---------------|
| **Random Forest** | **89.25%** | **97.24%** | **89.04%** | **0.49s** |
| XGBoost | 88.61% | 97.18% | 88.49% | 0.90s |
| SVM | 80.27% | 93.57% | 78.66% | 3.84s |

**Dataset:**
- Total: 9,564 samples
- Clean: 7,070 samples (73.9% after removing NaN)
- Features: 20 (from 122 analyzed)
- Classes: CONFIRMED (28.7%), CANDIDATE (20.7%), FALSE POSITIVE (50.6%)

**Top 5 Features:**
1. `koi_score` (0.750 Spearman) - Disposition confidence
2. `koi_fwm_stat_sig` (0.451) - Centroid shift statistic
3. `koi_srho_err2` (0.377) - Stellar density error
4. `koi_dor_err2` (0.365) - Orbital distance error
5. `koi_incl` (0.362) - Orbital inclination

---

### **TESS** ⚠️ (Before Feature Engineering)

| Model | Test Accuracy | AUC | F1 Score | Training Time |
|-------|---------------|-----|----------|---------------|
| **XGBoost** | **69.76%** | **81.28%** | **66.70%** | **1.36s** |
| Random Forest | 69.48% | 81.49% | 65.27% | 0.50s |
| SVM | 60.26% | 73.31% | 45.97% | 5.21s |

**Dataset:**
- Total: 7,703 samples
- Features: 8 (from 73 analyzed, threshold lowered to 0.15)
- Classes: 6 (PC 60.7%, FP 15.5%, CP 8.9%, KP 7.6%, APC 6.0%, FA 1.3%)

**Issues:**
- Weak feature correlations (max 0.405 from `toi` identifier)
- ❌ **ID leakage**: `toi` and `toipfx` are identifiers, not physical features
- No pre-calculated disposition score like Kepler
- Highly imbalanced classes

---

### **TESS (After Feature Engineering)** ✅ NEW!

**Created 26 new features:**
- **SNR metrics**: `pl_trandep_snr`, `pl_orbper_snr`, `pl_rade_snr`, `pl_trandurh_snr`
- **Physical values**: `pl_trandep_value`, `pl_rade_value`, `pl_orbper_value`, `pl_eqt_value`
- **Derived features**: `pl_rad_ratio`, `pl_semimajor_proxy`, `pl_trandur_ratio`
- **Quality indicators**: `measurement_completeness`, `avg_measurement_snr`
- **Stellar ratios**: `st_brightness_norm`, `st_distance_norm`, `st_brightness_dist_product`

**Top 15 Engineered Features (by Spearman correlation):**
1. `st_tmag_value` (0.299)
2. `st_brightness_norm` (0.299)
3. `st_brightness_dist_product` (0.297)
4. `st_dist_value` (0.238)
5. `st_distance_norm` (0.238)
6. `st_dist_quality` (0.126)
7. `pl_trandurh_value` (0.115)
8. `pl_semimajor_proxy` (0.109)
9. `pl_orbper_value` (0.102)
10. `pl_trandur_expected` (0.094)

**Next Steps:**
- Re-run `feature_selection.py` on `tess_engineered.csv`
- Remove `toi` and `toipfx` identifiers
- Expected improvement: More stable 60-65% accuracy without ID leakage

---

## 🔬 Methodology

### **Feature Engineering (TESS Only)**

**Problem:** TESS lacks pre-calculated quality scores like Kepler's `koi_score`

**Solution:** Create derived metrics from raw measurements:

1. **Signal-to-Noise Ratios**
   ```python
   pl_trandep_snr = pl_trandep / pl_trandeperr1
   ```
   - Higher SNR → Better measurement quality → Higher confidence

2. **Orbital Physics**
   ```python
   pl_semimajor_proxy = (P² × M_star)^(1/3)  # Kepler's 3rd law
   pl_trandur_expected = (P/π) × (R_star/a) × 24
   pl_trandur_ratio = observed / expected
   ```
   - Consistency checks for transit physics

3. **Stellar Quality Indicators**
   ```python
   st_dist_quality = st_disterr1 / st_dist  # Relative error
   st_brightness_dist_product = brightness × (1/distance)
   ```
   - Better measurements → More reliable

4. **Completeness Metrics**
   ```python
   measurement_completeness = count(non-null) / total_measurements
   avg_measurement_snr = mean(all_snr_metrics)
   ```
   - More complete data → Higher quality candidate

---

### **Feature Selection**

1. Load raw NASA data (CSVs from Exoplanet Archive)
2. **[TESS ONLY]** Run feature engineering first
3. Detect feature types (continuous, binary, categorical)
4. Calculate appropriate correlation metrics:
   - **Spearman** for continuous features (non-linear, outlier-resistant)
   - **Chi-Square (Cramér's V)** for categorical features
   - **Mutual Information** for combinatorial flags
5. Filter by correlation threshold and p-value < 0.05
6. **Remove identifier columns** (toi, toipfx, rowid, etc.)

---

### **Model Training**

1. Load processed datasets (selected features only)
2. Train-test split (80/20, stratified)
3. Preprocessing with RobustScaler
4. Train 3 models: XGBoost, Random Forest, SVM
5. Evaluate with accuracy, AUC, F1, confusion matrix
6. Compare and select best model

---

## 📈 Key Findings

### **Why TESS Needs Feature Engineering:**

| Aspect | Kepler | TESS (Raw) | TESS (Engineered) |
|--------|--------|------------|-------------------|
| **Best Feature** | koi_score (0.750) | toi (0.405) ❌ ID | st_tmag (0.299) ✓ |
| **Quality Metrics** | Pre-calculated | ❌ None | ✓ Created 26 |
| **Feature Count** | 20 (>= 0.3) | 8 (>= 0.15) | 74 total |
| **ID Leakage** | None | toi, toipfx | ✓ Removed |
| **Expected Accuracy** | 89.25% | 69.76% (inflated) | ~60-65% (valid) |

---

### **Kepler vs TESS Comparison:**

**Kepler Advantages:**
- ✅ Mature mission (8+ years of analysis)
- ✅ Pre-calculated `koi_score` from Robovetter pipeline
- ✅ Comprehensive centroid tests (8 features)
- ✅ Balanced 3-class problem
- ✅ Strong correlations (max 0.75)

**TESS Challenges:**
- ⚠️ Ongoing mission (early-stage candidates)
- ⚠️ No disposition score equivalent
- ⚠️ No centroid offset measurements in dataset
- ⚠️ 6 highly imbalanced classes (PC dominates at 60.7%)
- ⚠️ Weak correlations (max 0.299 after removing IDs)

---

## 📝 Essential Scripts

| File | Purpose | Input | Output |
|------|---------|-------|--------|
| `feature_selection.py` | Statistical feature selection | Raw CSVs | `*_selected_final.csv` |
| `tess_feature_engineering.py` | Create TESS quality metrics | `TOI_*.csv` | `tess_engineered.csv` |
| `prepare_datasets.py` | Extract selected features | Selected CSVs | `*_processed.csv` |
| `train_tess_models.py` | Train TESS models | `tess_processed.csv` | Models + plots |
| `kepler_final/train_kepler_models.py` | Train Kepler models | `kepler_processed.csv` | Models + plots |
| `kepler_final/predict_new_candidate.py` | Predict new data | Raw 141-col CSV | Predictions |

**Total:** 6 essential scripts (down from 9)

---

## 📚 Documentation

- **DATA_DICTIONARY.md**: Complete column reference for Kepler & TESS
  - Official NASA API column names
  - Units, types, descriptions
  - Physical interpretation
  - Feature selection justification

- **kepler_final/README_KEPLER.md**: Detailed Kepler pipeline documentation

---

## 🎯 Next Steps

1. ✅ **TESS Feature Engineering** - COMPLETED
2. ⏳ **Re-run feature selection** on `tess_engineered.csv` with threshold 0.20-0.25
3. ⏳ **Remove ID features** (toi, toipfx) from selection
4. ⏳ **Re-train TESS models** with engineered features
5. ⏳ **Save trained models** as `.pkl` files for deployment
6. ⏳ **Add cross-validation** for robust metrics
7. ⏳ **K2 dataset** analysis (if needed)

---

## 👥 Contributors

NASA Space Apps Challenge Team

---

## 📄 License

NASA Space Apps Challenge 2025

Data Source: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

# TESS Exoplanet Classification Pipeline
**Machine Learning Pipeline with Feature Engineering**

---

## 📊 Results Summary

### Model Performance (14 Engineered Features)

| Model | Train Acc | Test Acc | AUC | F1 Score | Time |
|-------|-----------|----------|-----|----------|------|
| **XGBoost** | **99.96%** | **65.86%** | **77.25%** | **61.66%** | 1.65s |
| Random Forest | 88.33% | 65.35% | 77.62% | 60.27% | 0.56s |
| SVM | 60.77% | 60.20% | 68.50% | 45.71% | 6.60s |

**Winner**: XGBoost (65.86% test accuracy)

**⚠️ Critical Issue**: XGBoost shows **severe overfitting** (99.96% train vs 65.86% test = 34% gap)

---

## 📈 Comparison: Raw vs Engineered Features

| Metric | Raw TESS | Engineered TESS | Change |
|--------|----------|-----------------|--------|
| **Features** | 8 | 14 | +6 |
| **Best Feature** | toi (0.405) ❌ ID | st_tmag (0.299) ✓ | Valid |
| **Test Accuracy** | 69.76% | 65.86% | -3.9% |
| **Overfitting** | 28.7% gap | 34% gap | Worse |
| **F1 Score** | 66.70% | 61.66% | -5% |
| **ID Leakage** | Yes (toi, toipfx) | No | ✓ Fixed |

**Analysis**:
- Lower accuracy BUT scientifically valid (no ID leakage)
- Still severe overfitting due to class imbalance (PC = 60.7%)
- Engineered features are weaker than raw ID features

---

## 🔬 Feature Engineering Process

### Created 26 New Features:

**1. Signal-to-Noise Ratios (4)**
- `pl_trandep_snr`: Transit depth / error
- `pl_orbper_snr`: Orbital period / error
- `pl_rade_snr`: Planet radius / error
- `pl_trandurh_snr`: Transit duration / error

**2. Physical Measurements (6)**
- `pl_trandep_value`, `pl_rade_value`, `pl_orbper_value`
- `pl_eqt_value`, `pl_insol_value`, `pl_trandurh_value`

**3. Derived Orbital Features (3)**
- `pl_rad_ratio`: Planet/star radius ratio
- `pl_semimajor_proxy`: Semi-major axis (Kepler's 3rd law)
- `pl_trandur_ratio`: Observed/expected duration

**4. Quality Indicators (2)**
- `measurement_completeness`: Non-null count / total
- `avg_measurement_snr`: Mean SNR across measurements

**5. Stellar Features (3)**
- `st_brightness_norm`: Normalized TESS magnitude
- `st_distance_norm`: Normalized distance
- `st_brightness_dist_product`: Brightness × (1/distance)

---

## 📋 Selected Features (14 total, threshold >= 0.15)

| # | Feature | Correlation | Type | Category |
|---|---------|-------------|------|----------|
| 1 | `st_brightness_norm` | 0.299 | Engineered | Stellar brightness (normalized) |
| 2 | `st_tmag` | 0.299 | Raw | TESS-band magnitude |
| 3 | `st_tmag_value` | 0.299 | Engineered | TESS magnitude (duplicate) |
| 4 | `st_brightness_dist_product` | 0.297 | Engineered | Brightness × (1/distance) |
| 5 | `st_distance_norm` | 0.238 | Engineered | Distance (normalized) |
| 6 | `st_dist` | 0.238 | Raw | Distance (parsecs) |
| 7 | `st_dist_value` | 0.238 | Engineered | Distance (duplicate) |
| 8 | `st_disterr1` | 0.184 | Raw | Distance error (+) |
| 9 | `st_disterr2` | 0.184 | Raw | Distance error (-) |
| 10 | `pl_tranmiderr1` | 0.179 | Raw | Transit midpoint error (+) |
| 11 | `pl_tranmiderr2` | 0.179 | Raw | Transit midpoint error (-) |
| 12 | `st_pmdecerr2` | 0.170 | Raw | Proper motion Dec error (-) |
| 13 | `st_pmdecerr1` | 0.170 | Raw | Proper motion Dec error (+) |
| 14 | `pl_tranmid` | 0.162 | Raw | Transit midpoint time (BJD) |

**Note**: Several duplicates (st_tmag/st_tmag_value, st_dist/st_dist_value) can be removed.

---

## 🎯 Key Insights

### Why TESS Accuracy is Lower Than Kepler?

**1. No Disposition Score**
- Kepler has `koi_score` (0.750 correlation) - pre-calculated by NASA
- TESS has NO equivalent quality metric
- Best TESS feature: `st_tmag` (0.299) - stellar brightness

**2. Class Imbalance**
```
PC (Planet Candidate):  60.7%  ← Dominant class
FP (False Positive):    15.5%
CP (Confirmed Planet):   8.9%
KP (Known Planet):       7.6%
APC:                     6.0%
FA (False Alarm):        1.3%
```
- Model learns to predict PC for everything
- Poor performance on minority classes (FA: 0% recall)

**3. Weak Feature Correlations**
- Max correlation: 0.299 (vs Kepler's 0.750)
- Most features are stellar properties (indirect indicators)
- No centroid tests (like Kepler has)

**4. Severe Overfitting**
- XGBoost: 99.96% train → 65.86% test (34% gap)
- Model memorizes training data
- Doesn't generalize to new candidates

---

## 🔧 Dataset Information

**Raw TESS**: `TOI_2025.10.04_08.50.19.csv`
- 7,703 samples
- 87 columns

**Engineered**: `tess_engineered.csv`
- 7,703 samples
- 74 features (26 new + 48 original)

**Processed**: `tess_processed.csv`
- 6,984 samples (90.7% after dropna)
- 14 selected features + target
- Target: `tfopwg_disp` (6 classes)

---

## 📁 Files in tess_final/

| File | Description |
|------|-------------|
| `prepare_tess_dataset.py` | Extract 14 selected features from engineered dataset |
| `train_tess_models.py` | Train XGBoost, Random Forest, SVM |
| `tess_processed.csv` | Clean dataset (6,984 × 15) |
| `tess_features.json` | List of 14 selected features |
| `tess_model_comparison.png` | Model comparison visualization |
| `tess_models_comparison.csv` | Metrics comparison table |
| `README_TESS.md` | This file |

---

## 🚀 Usage

### 1. Prepare Dataset
```bash
cd tess_final
python prepare_tess_dataset.py
```

### 2. Train Models
```bash
python train_tess_models.py
```

### 3. View Results
- Visualization: `tess_model_comparison.png`
- Metrics: `tess_models_comparison.csv`

---

## ⚠️ Recommendations for Improvement

### 1. **Address Class Imbalance**
```python
# Option A: SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Option B: Class weights
xgb = XGBClassifier(scale_pos_weight=class_weights, ...)
```

### 2. **Simplify Target (6 → 3 classes)**
```python
# Merge classes
tess['target_simple'] = tess['tfopwg_disp'].map({
    'CP': 'CONFIRMED',
    'KP': 'CONFIRMED',
    'PC': 'CANDIDATE',
    'APC': 'CANDIDATE',
    'FP': 'FALSE_POSITIVE',
    'FA': 'FALSE_POSITIVE'
})
```

### 3. **Reduce Overfitting**
```python
# XGBoost with regularization
xgb = XGBClassifier(
    max_depth=5,           # Reduce from 8
    min_child_weight=5,    # Increase from 1
    gamma=1.0,             # Add regularization
    subsample=0.7,         # Reduce from 0.8
    colsample_bytree=0.7   # Reduce from 0.8
)
```

### 4. **Remove Duplicate Features**
- Keep: `st_tmag`, `st_dist`
- Remove: `st_tmag_value`, `st_dist_value`, `st_brightness_norm`, `st_distance_norm`
- Reduces multicollinearity

### 5. **Add Cross-Validation**
```python
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5)
scores = cross_val_score(xgb, X, y, cv=cv)
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## 📊 Confusion Matrix Analysis (XGBoost)

**Strong Performance:**
- PC (Planet Candidate): 89.5% recall (752/840 correct)
- CP (Confirmed Planet): 46.3% recall

**Weak Performance:**
- APC: 1.3% recall (1/75 correct)
- FA (False Alarm): 0% recall (0/15 correct)
- KP (Known Planet): 30.7% recall

**Problem**: Model predicts PC for most samples (PC has 60.7% of data)

---

## 🔬 Comparison with Kepler

| Aspect | Kepler | TESS |
|--------|--------|------|
| **Accuracy** | 89.25% | 65.86% |
| **Features** | 20 | 14 |
| **Best Feature** | koi_score (0.750) | st_tmag (0.299) |
| **Classes** | 3 (balanced) | 6 (imbalanced) |
| **Overfitting** | 8.6% gap | 34% gap |
| **Quality Metrics** | ✓ Pre-calculated | ❌ None |
| **Centroid Tests** | ✓ 8 features | ❌ None |

**Conclusion**: TESS pipeline works but is fundamentally limited by dataset quality.

---

## 📄 Next Steps

1. ✅ Feature engineering - DONE
2. ✅ Feature selection (14 features) - DONE
3. ✅ Model training - DONE
4. ⏳ Implement class balancing (SMOTE or weights)
5. ⏳ Simplify to 3-class problem
6. ⏳ Add regularization to reduce overfitting
7. ⏳ Remove duplicate features
8. ⏳ Save models as `.pkl` for deployment

---

Generated: 2025-10-05
NASA Space Apps Challenge Team
Data: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

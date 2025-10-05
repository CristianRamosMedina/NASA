# KEPLER - Exoplanet Classification Pipeline

Complete pipeline for Kepler exoplanet classification using machine learning.

---

## 📊 Dataset

**Source**: NASA Exoplanet Archive - Kepler Candidates
- **Total samples**: 9,564 KOIs (Kepler Objects of Interest)
- **Clean samples**: 7,070 (after removing NaN)
- **Features selected**: 20 (from 122 analyzed)
- **Target classes**: 3
  - CONFIRMED: 2,746 (28.7%)
  - CANDIDATE: 1,979 (20.7%)
  - FALSE POSITIVE: 4,839 (50.6%)

---

## 🔬 Feature Selection

**Method**: Statistical correlation analysis
- **Threshold**: Correlation >= 0.3, p-value < 0.05
- **Metrics used**:
  - Spearman correlation (19 features - continuous)
  - Chi-Square / Cramér's V (1 feature - categorical: koi_count)

**Top 5 Features**:
1. `koi_score` (0.750) - Disposition confidence
2. `koi_fwm_stat_sig` (0.451) - Centroid shift statistic
3. `koi_srho_err2` (0.377) - Stellar density error
4. `koi_dor_err2/err1` (0.365) - Orbital distance errors
5. `koi_incl` (0.362) - Orbital inclination

See **KEPLER_FEATURES_DICTIONARY.md** for complete feature descriptions.

---

## 🤖 Models Trained

### **1. Random Forest (WINNER)** 🏆
- **Test Accuracy**: 89.25%
- **AUC**: 97.24%
- **F1 Score**: 89.04%
- **Training time**: 0.49s

### **2. XGBoost**
- **Test Accuracy**: 88.61%
- **AUC**: 97.18%
- **F1 Score**: 88.49%
- **Training time**: 0.90s

### **3. SVM**
- **Test Accuracy**: 80.27%
- **AUC**: 93.57%
- **F1 Score**: 78.66%
- **Training time**: 3.84s

---

## 📈 Performance Metrics (Random Forest)

### Per-Class Performance:
| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| CANDIDATE | 0.77 | 0.68 | 0.72 | 261 |
| CONFIRMED | 0.88 | 0.91 | 0.89 | 520 |
| FALSE POSITIVE | 0.95 | 0.97 | 0.96 | 633 |

**Overall Accuracy**: 89.25%

---

## 📁 Files

### **Scripts**
- `3_train_kepler_models.py` - Train XGBoost, Random Forest, SVM
- `4_kepler_correlation_analysis.py` - Correlation analysis and visualizations

### **Data**
- `kepler_processed.csv` - Clean dataset (7,070 rows × 21 columns)
- `kepler_selected_final.csv` - 20 selected features with metrics
- `kepler_all_final.csv` - All 103 analyzed features

### **Results**
- `kepler_models_comparison.csv` - Model performance comparison
- `kepler_correlation_pairs.csv` - All pairwise feature correlations

### **Visualizations**
- `kepler_model_comparison.png` - 3 models performance comparison
- `kepler_correlation_heatmaps.png` - Pearson + Spearman heatmaps
- `kepler_correlation_detailed.png` - Detailed correlation with annotations
- `kepler_feature_distributions.png` - Top 6 features by class
- `kepler_validation_analysis.png` - Random Forest validation

### **Documentation**
- `KEPLER_FEATURES_DICTIONARY.md` - Complete feature descriptions
- `README_KEPLER.md` - This file

---

## 🔑 Key Findings

### **High Feature Correlations** (|r| >= 0.8)
- Centroid offset features highly correlated (0.91-0.96)
- `koi_prad_err1` ↔ `koi_prad_err2` = -0.91
- `koi_dor_err1` ↔ `koi_dor_err2` = -1.0 (perfect anticorrelation)
- `koi_period_err1` ↔ `koi_period_err2` = -1.0

### **Best Discriminators**
- `koi_score`: Strong separation (CONFIRMED ~1.0, FALSE POSITIVE ~0.0)
- `koi_model_snr`: FALSE POSITIVES have low SNR
- `koi_fwm_stat_sig`: Detects centroid shifts (false positives)

---

## 🚀 Usage

### Load Processed Data
```python
import pandas as pd
df = pd.read_csv('kepler_processed.csv')
X = df.drop('koi_disposition', axis=1)
y = df['koi_disposition']
```

### Train Models
```bash
python 3_train_kepler_models.py
```

### Correlation Analysis
```bash
python 4_kepler_correlation_analysis.py
```

---

## 📊 Preprocessing Pipeline

1. **Load raw data** (9,564 samples)
2. **Select 20 features** (correlation >= 0.3)
3. **Remove NaN** (7,070 samples remain)
4. **Train-test split** (80/20 stratified)
5. **RobustScaler** normalization
6. **Train models** (XGBoost, Random Forest, SVM)
7. **Evaluate** (Accuracy, AUC, F1, Confusion Matrix)

---

## ✅ Conclusion

**Random Forest** achieves **89.25% accuracy** with excellent generalization:
- **Strong performance** on all 3 classes
- **Fast training** (0.49s)
- **High AUC** (97.24%) indicates excellent ranking ability
- **Ready for deployment**

---

Generated: 2025-10-04
Author: NASA Exoplanet Team
Source: NASA Exoplanet Archive

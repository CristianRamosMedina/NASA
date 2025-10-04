# Exoplanet Classifier - Machine Learning Pipeline

Complete machine learning pipeline for exoplanet classification using Kepler and TESS mission data.

**Goal:** Classify exoplanets as **CONFIRMED**, **CANDIDATE**, or **FALSE POSITIVE** using scientifically selected features and ensemble models.

---

## 📁 Project Structure

```
NASA/
├── Datasets/
│   ├── cumulative_2025.10.04_08.50.10.csv    # Kepler (9,564 exoplanets, 141 features)
│   ├── TOI_2025.10.04_08.50.19.csv           # TESS (7,703 exoplanets, 87 features)
│   └── k2pandc_2025.10.04_08.51.50.csv       # K2 (4,004 exoplanets, 295 features)
│
├── kepler_final/                              # Kepler complete pipeline
│   ├── train_kepler_models.py                # Train XGBoost, Random Forest, SVM
│   ├── kepler_correlation_analysis.py        # Correlation heatmaps and analysis
│   ├── kepler_accuracy_comparison.py         # Model comparison visualizations
│   ├── predict_new_candidate.py              # Predict new Kepler candidates
│   ├── kepler_processed.csv                  # Clean dataset (7,070 samples × 21 cols)
│   ├── kepler_features.json                  # 20 selected features list
│   ├── KEPLER_FEATURES_DICTIONARY.md         # Feature descriptions
│   └── README_KEPLER.md                      # Detailed Kepler documentation
│
├── lightgbm_models/                           # LightGBM experiments (archived)
│
├── feature_selection.py                       # Statistical feature selection
├── validate_features_rf.py                    # Random Forest validation
├── prepare_datasets.py                        # Generate processed CSVs
├── train_tess_models.py                       # Train TESS models
│
├── kepler_selected_final.csv                  # Kepler: 20 features selected
├── tess_selected_final.csv                    # TESS: 8 features selected
├── tess_processed.csv                         # TESS clean dataset (6,995 × 9 cols)
│
├── .gitignore
└── README.md                                  # This file
```

---

## 🚀 Quick Start

### **1. Feature Selection** (Scientific Method)

Select features based on statistical correlation with target:

```bash
python feature_selection.py
```

**Method:**
- **Kepler**: Threshold >= 0.3 correlation
- **TESS**: Threshold >= 0.15 correlation (lowered due to weak features)
- **Metrics**: Spearman (continuous), Chi-Square (categorical), Mutual Information (flags)

**Output:**
- `kepler_selected_final.csv` (20 features)
- `tess_selected_final.csv` (8 features)

---

### **2. Prepare Datasets**

Extract selected features from raw data:

```bash
python prepare_datasets.py
```

**Output:**
- `kepler_processed.csv` (7,070 samples × 21 columns)
- `tess_processed.csv` (6,995 samples × 9 columns)

---

### **3. Train Models**

#### **Kepler (BEST RESULTS)**

```bash
cd kepler_final
python train_kepler_models.py
```

**Models trained:**
- XGBoost
- Random Forest 🏆 (Winner: 89.25% accuracy)
- SVM

**Output:**
- `kepler_model_comparison.png`
- `kepler_models_comparison.csv`

#### **TESS**

```bash
python train_tess_models.py
```

**Models trained:**
- XGBoost 🏆 (Winner: 69.76% accuracy)
- Random Forest
- SVM

---

### **4. Predict New Candidates** (Kepler)

```bash
cd kepler_final
python predict_new_candidate.py --input new_data.csv
```

Or demo with sample data:

```bash
python predict_new_candidate.py --demo
```

**Process:**
1. Loads raw Kepler data (141 columns)
2. Extracts ONLY the 20 selected features
3. Preprocesses (handles NaN, scales)
4. Predicts with Random Forest

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

**Visualizations:**
- [kepler_final/kepler_model_comparison.png](kepler_final/kepler_model_comparison.png)
- [kepler_final/kepler_correlation_heatmaps.png](kepler_final/kepler_correlation_heatmaps.png)
- [kepler_final/kepler_accuracy_detailed_comparison.png](kepler_final/kepler_accuracy_detailed_comparison.png)

---

### **TESS** ⚠️

| Model | Test Accuracy | AUC | F1 Score | Training Time |
|-------|---------------|-----|----------|---------------|
| **XGBoost** | **69.76%** | **81.28%** | **66.70%** | **1.36s** |
| Random Forest | 69.48% | 81.49% | 65.27% | 0.50s |
| SVM | 60.26% | 73.31% | 45.97% | 5.21s |

**Dataset:**
- Total: 7,703 samples
- Clean: 6,995 samples (90.8%)
- Features: 8 (from 73 analyzed, threshold lowered to 0.15)
- Classes: 6 (PC 60.7%, FP 15.5%, CP 8.9%, KP 7.6%, APC 6.0%, FA 1.3%)

**Issues:**
- Weak feature correlations (max 0.405)
- Highly imbalanced classes
- No pre-calculated score like Kepler
- XGBoost overfitting (98.5% train, 69.8% test)

**Selected Features:**
1. `toi` (0.405) - TOI identifier
2. `toipfx` (0.405) - TOI prefix
3. `st_tmag` (0.299) - TESS magnitude
4. `st_dist` (0.238) - Stellar distance
5-8. Stellar proper motion and distance errors

---

## 🔬 Methodology

### **Feature Selection**
1. Load raw NASA data (CSVs from Exoplanet Archive)
2. Detect feature types (continuous, binary, categorical)
3. Calculate appropriate correlation metrics:
   - **Spearman** for continuous features (non-linear, outlier-resistant)
   - **Chi-Square (Cramér's V)** for categorical features
   - **Mutual Information** for combinatorial flags
4. Filter by correlation threshold and p-value < 0.05
5. Save selected features

### **Model Training**
1. Load processed datasets (selected features only)
2. Train-test split (80/20, stratified)
3. Preprocessing with RobustScaler
4. Train 3 models: XGBoost, Random Forest, SVM
5. Evaluate with accuracy, AUC, F1, confusion matrix
6. Compare and select best model

### **Prediction Pipeline**
1. Load new candidate data (141 Kepler columns)
2. Feature selector extracts 20 selected features
3. Preprocess (handle NaN, scale)
4. Predict with trained Random Forest
5. Return disposition: CONFIRMED / CANDIDATE / FALSE POSITIVE

---

## 📈 Key Findings

### **Kepler Success Factors:**
✅ High-quality features (koi_score, SNR, false positive flags)
✅ Balanced 3-class problem
✅ Strong correlations (max 0.75)
✅ 89.25% accuracy with Random Forest

### **TESS Challenges:**
⚠️ No pre-calculated disposition score
⚠️ 6 highly imbalanced classes
⚠️ Weak feature correlations (max 0.40)
⚠️ Limited to 8 features at threshold 0.15

### **Feature Correlations:**
- **High multicollinearity** in centroid offset features (r > 0.9)
- **Perfect anticorrelation** in error pairs (err1 ↔ err2 = -1.0)
- **Best discriminator**: `koi_score` (Kepler only)

---

## 📝 Files Description

### **Scripts**

| File | Description |
|------|-------------|
| `feature_selection.py` | Statistical feature selection (Spearman, Chi-Square, MI) |
| `prepare_datasets.py` | Generate processed CSVs with selected features |
| `validate_features_rf.py` | Random Forest validation of selected features |
| `train_tess_models.py` | Train and compare TESS models |
| `kepler_final/train_kepler_models.py` | Train and compare Kepler models |
| `kepler_final/kepler_correlation_analysis.py` | Correlation heatmaps and analysis |
| `kepler_final/kepler_accuracy_comparison.py` | Detailed model comparison plots |
| `kepler_final/predict_new_candidate.py` | Prediction pipeline for new data |

### **Data Files**

| File | Rows | Cols | Description |
|------|------|------|-------------|
| `kepler_processed.csv` | 7,070 | 21 | Kepler clean dataset (20 features + target) |
| `tess_processed.csv` | 6,995 | 9 | TESS clean dataset (8 features + target) |
| `kepler_selected_final.csv` | 20 | 9 | Kepler selected features with metrics |
| `tess_selected_final.csv` | 8 | 9 | TESS selected features with metrics |
| `kepler_features.json` | - | - | List of 20 Kepler features for prediction |

---

## 🎯 Next Steps

1. **Save trained models**: Export Random Forest as `.pkl` for deployment
2. **TESS improvement**: Feature engineering, class balancing, lower threshold
3. **K2 dataset**: Apply same pipeline to K2 data
4. **Ensemble methods**: Combine Kepler models for better accuracy
5. **API deployment**: Flask/FastAPI endpoint for predictions

---

## 👥 Contributors

NASA Space Apps Challenge Team

---

## 📄 License

NASA Space Apps Challenge 2025

Data Source: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

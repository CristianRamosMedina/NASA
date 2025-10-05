"""
KEPLER - TRAIN AND SAVE RANDOM FOREST MODEL
============================================
Trains the Random Forest model and saves it as .pkl for production use

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("="*80)
print("KEPLER - TRAINING AND SAVING RANDOM FOREST MODEL")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[1/5] Loading kepler_processed.csv...")
df = pd.read_csv('kepler_processed.csv')

print(f"   Shape: {df.shape}")
print(f"   Target: koi_disposition")
print(f"   Classes: {df['koi_disposition'].unique()}")

# Encode target
le = LabelEncoder()
df['target'] = le.fit_transform(df['koi_disposition'])

print(f"\n   Target distribution:")
for cls, encoded in zip(le.classes_, range(len(le.classes_))):
    count = sum(df['target'] == encoded)
    pct = count / len(df) * 100
    print(f"     {cls}: {count:,} ({pct:.1f}%) -> Label {encoded}")

# Features
feature_cols = [col for col in df.columns if col not in ['koi_disposition', 'target']]
print(f"\n   Features: {len(feature_cols)}")

# Remove NaN
df_clean = df.dropna()
print(f"   Samples after dropna: {len(df_clean):,}")

X = df_clean[feature_cols]
y = df_clean['target']

# ============================================================================
# TRAIN-TEST SPLIT
# ============================================================================

print("\n[2/5] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train: {len(X_train):,} samples")
print(f"   Test:  {len(X_test):,} samples")

# ============================================================================
# PREPROCESSING
# ============================================================================

print("\n[3/5] Preprocessing with RobustScaler...")
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# TRAIN RANDOM FOREST
# ============================================================================

print("\n[4/5] Training Random Forest Classifier...")
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train_scaled, y_train)

# Evaluate
y_pred = rf.predict(X_test_scaled)
train_acc = accuracy_score(y_train, rf.predict(X_train_scaled))
test_acc = accuracy_score(y_test, y_pred)

print(f"\n   Train Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
print(f"   Test Accuracy:  {test_acc:.4f} ({test_acc*100:.2f}%)")

print("\n   Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_, digits=4))

# ============================================================================
# SAVE MODEL ARTIFACTS
# ============================================================================

print("\n[5/5] Saving model artifacts...")

# 1. Save Random Forest model
with open('kepler_rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)
print("   -> kepler_rf_model.pkl")

# 2. Save scaler
with open('kepler_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("   -> kepler_scaler.pkl")

# 3. Save label encoder
with open('kepler_label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
print("   -> kepler_label_encoder.pkl")

# 4. Save feature list (already exists as kepler_features.json)
with open('kepler_features.json', 'w') as f:
    json.dump(list(feature_cols), f, indent=2)
print("   -> kepler_features.json")

# 5. Save model metadata
metadata = {
    "model_type": "Random Forest Classifier",
    "n_features": len(feature_cols),
    "features": list(feature_cols),
    "n_classes": len(le.classes_),
    "classes": list(le.classes_),
    "train_accuracy": float(train_acc),
    "test_accuracy": float(test_acc),
    "n_train_samples": len(X_train),
    "n_test_samples": len(X_test)
}

with open('kepler_model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("   -> kepler_model_metadata.json")

print("\n" + "="*80)
print("MODEL SAVED SUCCESSFULLY")
print("="*80)
print(f"\nModel: Random Forest")
print(f"Accuracy: {test_acc*100:.2f}%")
print(f"Classes: {', '.join(le.classes_)}")
print(f"Features: {len(feature_cols)}")
print("\nReady for production use!")
print("="*80)

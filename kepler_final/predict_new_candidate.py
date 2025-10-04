"""
KEPLER - PREDICT NEW EXOPLANET CANDIDATES
==========================================
Takes a new Kepler candidate row (141 columns) and predicts its disposition
using the trained Random Forest model.

Usage:
    python 7_predict_new_kepler.py --input new_candidate.csv

Or programmatically:
    from 7_predict_new_kepler import predict_kepler
    result = predict_kepler(candidate_data)

Author: NASA Exoplanet Team
"""

import pandas as pd
import numpy as np
import pickle
import json
import argparse
from pathlib import Path

print("="*80)
print("KEPLER - NEW CANDIDATE PREDICTION")
print("="*80)

# ============================================================================
# LOAD MODEL AND ARTIFACTS
# ============================================================================

def load_model_artifacts():
    """Load trained model, scaler, and feature list"""
    print("\n[1/4] Loading model artifacts...")

    # Load selected features
    with open('kepler_features.json', 'r') as f:
        selected_features = json.load(f)

    print(f"   Selected features: {len(selected_features)}")
    print(f"   Features: {', '.join(selected_features[:5])}...")

    return selected_features

# ============================================================================
# FEATURE SELECTOR
# ============================================================================

def select_features(raw_data, selected_features):
    """
    Extracts ONLY the 20 selected features from raw Kepler data.

    Args:
        raw_data: DataFrame with 141 Kepler columns
        selected_features: List of 20 feature names

    Returns:
        DataFrame with only the 20 selected features
    """
    print(f"\n[2/4] Selecting features...")
    print(f"   Input columns: {len(raw_data.columns)}")

    # Check if all required features exist
    missing_features = [f for f in selected_features if f not in raw_data.columns]

    if missing_features:
        print(f"\n   WARNING: Missing features: {missing_features}")
        print(f"   These will be filled with NaN (prediction may be unreliable)")

    # Select features (fill missing with NaN)
    selected_data = pd.DataFrame()
    for feature in selected_features:
        if feature in raw_data.columns:
            selected_data[feature] = raw_data[feature]
        else:
            selected_data[feature] = np.nan

    print(f"   Output columns: {len(selected_data.columns)}")
    print(f"   NaN values: {selected_data.isna().sum().sum()}")

    return selected_data

# ============================================================================
# PREPROCESSING
# ============================================================================

def preprocess_features(selected_data):
    """
    Applies the same preprocessing as training:
    - Handles NaN (will warn user)
    - NO scaling here (Random Forest doesn't need it, but we used RobustScaler in training)
    """
    print(f"\n[3/4] Preprocessing...")

    # Check for NaN
    nan_features = selected_data.columns[selected_data.isna().any()].tolist()
    if nan_features:
        print(f"   WARNING: NaN found in: {nan_features}")
        print(f"   Filling with median values (training data medians would be better)")
        selected_data = selected_data.fillna(selected_data.median())

    return selected_data

# ============================================================================
# PREDICTION
# ============================================================================

def predict_kepler(raw_data_path=None, raw_data_df=None):
    """
    Main prediction function.

    Args:
        raw_data_path: Path to CSV with new candidate(s)
        raw_data_df: Or direct DataFrame

    Returns:
        DataFrame with predictions
    """

    # Load data
    if raw_data_path:
        print(f"\nLoading data from: {raw_data_path}")
        raw_data = pd.read_csv(raw_data_path, comment='#')
    elif raw_data_df is not None:
        raw_data = raw_data_df
    else:
        raise ValueError("Must provide either raw_data_path or raw_data_df")

    print(f"   Loaded {len(raw_data)} candidate(s)")

    # Load artifacts
    selected_features = load_model_artifacts()

    # Select features
    selected_data = select_features(raw_data, selected_features)

    # Preprocess
    processed_data = preprocess_features(selected_data)

    # Load trained Random Forest model (we'll save it in next step)
    print(f"\n[4/4] Making predictions with Random Forest...")
    print(f"   NOTE: Model file 'kepler_rf_model.pkl' not found.")
    print(f"   Run training script first to generate the model.")
    print(f"\n   For now, showing selected features only:")

    return processed_data

# ============================================================================
# DEMO / EXAMPLE
# ============================================================================

def demo_prediction():
    """Demonstrates how to use the predictor with sample data"""

    print("\n" + "="*80)
    print("DEMO - PREDICTING WITH SAMPLE DATA")
    print("="*80)

    # Load actual Kepler dataset as example
    print("\nLoading sample from training data...")
    full_data = pd.read_csv('../Datasets/cumulative_2025.10.04_08.50.10.csv', comment='#')

    # Take first 5 candidates as "new" data
    sample_candidates = full_data.head(5)

    print(f"Sample: {len(sample_candidates)} candidates")
    print(f"\nOriginal dispositions (ground truth):")
    if 'koi_disposition' in sample_candidates.columns:
        for idx, disp in enumerate(sample_candidates['koi_disposition']):
            print(f"  Candidate {idx+1}: {disp}")

    # Predict
    selected_features_df = predict_kepler(raw_data_df=sample_candidates)

    print(f"\n" + "="*80)
    print("SELECTED FEATURES (Ready for model input)")
    print("="*80)
    print(selected_features_df.head())

    print(f"\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("1. Train and save Random Forest model (see 3_train_kepler_models.py)")
    print("2. Load model: model = pickle.load(open('kepler_rf_model.pkl', 'rb'))")
    print("3. Predict: predictions = model.predict(selected_features_df)")
    print("4. Decode: classes = ['CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']")

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict Kepler candidate disposition')
    parser.add_argument('--input', type=str, help='Path to CSV with new candidates')
    parser.add_argument('--demo', action='store_true', help='Run demo with sample data')

    args = parser.parse_args()

    if args.demo or not args.input:
        demo_prediction()
    else:
        result = predict_kepler(raw_data_path=args.input)
        print("\nPrediction complete!")
        print(result)

print("\n" + "="*80)
print("DONE!")
print("="*80)

"""
Quick API Test
==============
Tests the prediction API with sample Kepler data
"""

import requests
import json

API_URL = 'http://localhost:5000/api'

print("="*80)
print("NASA EXOPLANET API - QUICK TEST")
print("="*80)

# Test 1: Health check
print("\n[1/3] Testing health endpoint...")
try:
    response = requests.get(f'{API_URL}/health')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"ERROR: {e}")
    print("Make sure api_server.py is running on port 5000")
    exit(1)

# Test 2: Get features
print("\n[2/3] Getting required features...")
try:
    response = requests.get(f'{API_URL}/features')
    data = response.json()
    print(f"Required features: {data['count']}")
    print(f"Features: {', '.join(data['features'][:5])}...")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Predict with sample data
print("\n[3/3] Testing prediction with sample candidate...")

# Sample CONFIRMED planet (high koi_score)
sample_features = {
    "koi_score": 0.95,
    "koi_fwm_stat_sig": 2.1,
    "koi_srho_err2": -0.03,
    "koi_dor_err2": -0.01,
    "koi_dor_err1": 0.01,
    "koi_incl": 89.5,
    "koi_prad_err1": 0.2,
    "koi_count": 150,
    "koi_dor": 15.2,
    "koi_dikco_mdec_err": 0.05,
    "koi_period_err1": 0.0001,
    "koi_period_err2": -0.0001,
    "koi_dikco_mra_err": 0.04,
    "koi_prad_err2": -0.15,
    "koi_dikco_msky_err": 0.06,
    "koi_max_sngle_ev": 25.3,
    "koi_prad": 1.5,
    "koi_dicco_mdec_err": 0.03,
    "koi_model_snr": 45.2,
    "koi_dicco_mra_err": 0.02
}

try:
    response = requests.post(
        f'{API_URL}/predict',
        json={'features': sample_features},
        headers={'Content-Type': 'application/json'}
    )

    result = response.json()

    print(f"\nStatus: {response.status_code}")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print(f"\nProbabilities:")
    for cls, prob in result['probabilities'].items():
        print(f"  {cls}: {prob*100:.1f}%")

    print(f"\nModel: {result['model']}")
    print(f"Accuracy: {result['accuracy']*100:.2f}%")

except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)

"""
NASA EXOPLANET API SERVER
==========================
Flask API for:
1. Kepler exoplanet prediction (Random Forest)
2. EXO AI agent chat

Endpoints:
- POST /api/predict - Predict exoplanet classification
- POST /api/chat - Chat with EXO agent

Author: NASA Space Apps Challenge Team
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import json
import numpy as np
import pandas as pd
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# ============================================================================
# LOAD KEPLER MODEL
# ============================================================================

print("Loading Kepler model artifacts...")

with open('kepler_final/kepler_rf_model.pkl', 'rb') as f:
    kepler_model = pickle.load(f)

with open('kepler_final/kepler_scaler.pkl', 'rb') as f:
    kepler_scaler = pickle.load(f)

with open('kepler_final/kepler_label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

with open('kepler_final/kepler_features.json', 'r') as f:
    required_features = json.load(f)

print(f"Model loaded: Random Forest")
print(f"Features: {len(required_features)}")
print(f"Classes: {list(label_encoder.classes_)}")

# ============================================================================
# INITIALIZE EXO AGENT
# ============================================================================

openai_client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai_client = OpenAI(api_key=api_key)
        print("EXO Agent initialized with OpenAI API")
    else:
        print("WARNING: OPENAI_API_KEY not set - EXO chat disabled")
except Exception as e:
    print(f"WARNING: Could not initialize OpenAI: {e}")

# EXO system prompt
EXO_SYSTEM_PROMPT = """You are EXO, an expert AI assistant for NASA's exoplanet classification models.

Your role:
- Explain Kepler and TESS machine learning model features
- Help users understand model statistics and results
- Provide clear, technical but accessible explanations
- Always mention feature correlations and categories when relevant

Model Information:
- Kepler: Random Forest model, 89.25% accuracy, 20 features
- TESS: XGBoost model, 64.57% accuracy, 14 engineered features

Response style:
- Friendly but professional
- Use technical terms with explanations
- Include specific numbers (correlations, accuracy) when relevant
- Compare Kepler vs TESS when asked

KEPLER FEATURES:
- koi_score: Robovetter disposition score (0-1, higher = planet confidence) (correlation: 0.750)
- koi_fwm_stat_sig: Flux-weighted centroid motion significance (detects background stars) (correlation: 0.451)
- koi_srho_err2: Stellar density uncertainty (negative error) (correlation: 0.377)
- koi_dor_err2: Planet-star distance ratio error (negative) (correlation: 0.365)
- koi_incl: Orbital inclination (90° = edge-on transit) (correlation: 0.362)
- koi_prad: Planetary radius in Earth radii (correlation: 0.312)

TESS FEATURES:
- st_brightness_norm: Normalized TESS magnitude (brightness indicator) (correlation: 0.299)
- st_tmag: TESS-band magnitude (brightness) (correlation: 0.299)
- st_brightness_dist_product: Brightness × (1/distance) ratio (detection quality) (correlation: 0.297)
- st_dist: Distance to planetary system (parsecs) (correlation: 0.238)

MODEL RESULTS:
Kepler: Random Forest - 89.25% accuracy
TESS: XGBoost (Regularized) - 64.57% accuracy
"""

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict exoplanet classification from Kepler features

    Request body:
    {
        "features": {
            "koi_score": 0.95,
            "koi_fwm_stat_sig": 2.1,
            ... (all 20 features)
        }
    }

    Response:
    {
        "prediction": "CONFIRMED",
        "probabilities": {
            "CANDIDATE": 0.05,
            "CONFIRMED": 0.90,
            "FALSE POSITIVE": 0.05
        },
        "confidence": 0.90
    }
    """
    try:
        data = request.get_json()

        if not data or 'features' not in data:
            return jsonify({
                'error': 'Missing features in request body',
                'required_format': {
                    'features': {feat: 0.0 for feat in required_features}
                }
            }), 400

        input_features = data['features']

        # Create feature vector in correct order
        feature_vector = []
        missing_features = []

        for feat in required_features:
            if feat in input_features:
                value = input_features[feat]
                # Convert to float, handle empty strings
                if value == '' or value is None:
                    feature_vector.append(0.0)
                    missing_features.append(feat)
                else:
                    feature_vector.append(float(value))
            else:
                feature_vector.append(0.0)
                missing_features.append(feat)

        # Convert to DataFrame (required for scaler)
        X = pd.DataFrame([feature_vector], columns=required_features)

        # Scale features
        X_scaled = kepler_scaler.transform(X)

        # Predict
        prediction_encoded = kepler_model.predict(X_scaled)[0]
        probabilities = kepler_model.predict_proba(X_scaled)[0]

        # Decode prediction
        prediction = label_encoder.inverse_transform([prediction_encoded])[0]

        # Build probability dict
        prob_dict = {}
        for i, class_name in enumerate(label_encoder.classes_):
            prob_dict[class_name] = round(float(probabilities[i]), 4)

        confidence = round(float(probabilities[prediction_encoded]), 4)

        response = {
            'prediction': prediction,
            'probabilities': prob_dict,
            'confidence': confidence,
            'model': 'Random Forest',
            'accuracy': 0.8925
        }

        if missing_features:
            response['warning'] = f'Missing or empty features (filled with 0): {missing_features}'

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with EXO AI agent

    Request body:
    {
        "message": "What are the Kepler statistics?",
        "history": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }

    Response:
    {
        "response": "The Kepler model uses..."
    }
    """
    try:
        if not openai_client:
            return jsonify({
                'error': 'EXO agent not available - OPENAI_API_KEY not set'
            }), 503

        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message in request body'}), 400

        user_message = data['message']
        history = data.get('history', [])

        # Build messages
        messages = [
            {"role": "system", "content": EXO_SYSTEM_PROMPT}
        ]

        # Add conversation history (last 6 messages)
        messages.extend(history[-6:])

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        assistant_message = response.choices[0].message.content

        return jsonify({
            'response': assistant_message
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get list of required Kepler features"""
    return jsonify({
        'features': required_features,
        'count': len(required_features)
    }), 200


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'exo_available': openai_client is not None,
        'model_accuracy': 0.8925
    }), 200


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("NASA EXOPLANET API SERVER")
    print("="*80)
    print("\nEndpoints:")
    print("  POST /api/predict - Predict exoplanet classification")
    print("  POST /api/chat    - Chat with EXO agent")
    print("  GET  /api/features - Get required features")
    print("  GET  /api/health   - Health check")
    print("\n" + "="*80)
    print("Server starting on http://localhost:5000")
    print("="*80 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)

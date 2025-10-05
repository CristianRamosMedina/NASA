# NASA Exoplanet Classifier - Setup Instructions

## Overview

This project includes:
- **Kepler Random Forest Model** (89.25% accuracy) for exoplanet classification
- **Flask API Server** for predictions and EXO AI chat
- **Express.js Frontend** with dynamic workspace
- **EXO AI Assistant** - Chat widget powered by OpenAI GPT-3.5

---

## Prerequisites

### Python Requirements
```bash
pip install flask flask-cors scikit-learn pandas numpy xgboost openai
```

### Node.js Requirements
```bash
cd projectonasa
npm install
```

---

## Setup Steps

### 1. Set OpenAI API Key

The EXO chat assistant requires an OpenAI API key.

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

> Get your API key from: https://platform.openai.com/api-keys

---

### 2. Start the Backend API Server

Open **Terminal 1**:

```bash
python api_server.py
```

This will start the Flask API server on **http://localhost:5000**

**Endpoints:**
- `POST /api/predict` - Kepler model predictions
- `POST /api/chat` - EXO AI assistant
- `GET /api/health` - Health check
- `GET /api/features` - Get required features

---

### 3. Start the Frontend Server

Open **Terminal 2**:

```bash
cd projectonasa
node app.js
```

This will start the Express frontend on **http://localhost:3000**

---

### 4. Open the Application

Navigate to: **http://localhost:3000**

---

## Using the Application

### New Candidate Prediction

1. Click **"Add Candidate"** → **"New Candidate"** in the sidebar
2. Fill in Kepler features (20 total):
   - Left column: `koi_score`, `koi_fwm_stat_sig`, `koi_srho_err2`, etc.
   - Right column: `koi_period_err1`, `koi_period_err2`, etc.
3. Click **"Submit"**
4. View prediction results:
   - **CONFIRMED** (green) - High confidence planet
   - **CANDIDATE** (yellow) - Possible planet
   - **FALSE POSITIVE** (red) - Not a planet

### EXO AI Assistant

1. Click the **chat button** (bottom-right corner)
2. Ask questions like:
   - "What are the Kepler statistics?"
   - "Explain koi_score"
   - "Why is TESS accuracy lower?"
   - "List the top TESS features"
   - "Compare Kepler vs TESS performance"

---

## Kepler Model Features (20 Features)

| Feature | Description | Correlation |
|---------|-------------|-------------|
| `koi_score` | Robovetter disposition score (0-1) | 0.750 |
| `koi_fwm_stat_sig` | Flux-weighted centroid motion significance | 0.451 |
| `koi_srho_err2` | Stellar density uncertainty (negative) | 0.377 |
| `koi_dor_err2` | Planet-star distance ratio error (negative) | 0.365 |
| `koi_dor_err1` | Planet-star distance ratio error (positive) | - |
| `koi_incl` | Orbital inclination (90° = edge-on) | 0.362 |
| `koi_prad_err1` | Planetary radius error (positive) | - |
| `koi_count` | Number of transits detected | - |
| `koi_dor` | Planet-star distance ratio | - |
| `koi_dikco_mdec_err` | Differential centroid offset (Dec) | - |
| `koi_period_err1` | Orbital period uncertainty (positive) | - |
| `koi_period_err2` | Orbital period uncertainty (negative) | - |
| `koi_dikco_mra_err` | Differential centroid offset (RA) | - |
| `koi_prad_err2` | Planetary radius error (negative) | - |
| `koi_dikco_msky_err` | Differential centroid offset (sky) | - |
| `koi_max_sngle_ev` | Maximum single event statistic | - |
| `koi_prad` | Planetary radius (Earth radii) | 0.312 |
| `koi_dicco_mdec_err` | Difference centroid offset (Dec) | - |
| `koi_model_snr` | Model signal-to-noise ratio | - |
| `koi_dicco_mra_err` | Difference centroid offset (RA) | - |

---

## Model Performance

### Kepler Random Forest
- **Accuracy:** 89.25%
- **AUC:** 97.24%
- **Classes:** CANDIDATE, CONFIRMED, FALSE POSITIVE
- **Training samples:** 5,656
- **Test samples:** 1,414

### Classification Report
```
                precision    recall  f1-score   support

     CANDIDATE     0.7672    0.6820    0.7221       261
     CONFIRMED     0.8820    0.9058    0.8937       520
FALSE POSITIVE     0.9460    0.9684    0.9571       633

      accuracy                         0.8925      1414
```

---

## Troubleshooting

### API Server Won't Start
```bash
# Check if port 5000 is available
netstat -ano | findstr :5000

# Make sure all packages are installed
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
# Check if port 3000 is available
netstat -ano | findstr :3000

# Install dependencies
cd projectonasa
npm install
```

### EXO Chat Not Working
```bash
# Verify OpenAI API key is set
echo %OPENAI_API_KEY%  # Windows CMD
echo $env:OPENAI_API_KEY  # PowerShell
echo $OPENAI_API_KEY  # Linux/Mac

# Check API server logs for errors
```

### Prediction Fails
- Make sure both servers are running
- Check browser console (F12) for errors
- Verify API server is accessible at http://localhost:5000
- Test API directly: `curl http://localhost:5000/api/health`

---

## File Structure

```
NASA/
├── api_server.py              # Flask API server
├── exo_agent.py               # EXO console agent (standalone)
├── test_exo_agent.py          # EXO test script
├── kepler_final/              # Kepler model files
│   ├── kepler_rf_model.pkl    # Trained Random Forest model
│   ├── kepler_scaler.pkl      # Feature scaler
│   ├── kepler_label_encoder.pkl
│   ├── kepler_features.json   # 20 feature names
│   └── kepler_model_metadata.json
├── projectonasa/              # Frontend application
│   ├── app.js                 # Express server
│   ├── views/
│   │   ├── dashboard.ejs      # Main page
│   │   └── partials/
│   │       └── sidebar.ejs    # Navigation menu
│   └── public/
│       ├── js/
│       │   ├── dashboard.js   # Dynamic workspace + prediction
│       │   └── exo-chat.js    # EXO chat widget
│       ├── css/
│       │   └── styles.css     # Space theme styles
│       └── img/exoplanet/     # Planet images (e1-e4.png)
└── Datasets/                  # Original NASA data
```

---

## API Examples

### Predict Exoplanet

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
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
  }'
```

### Chat with EXO

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the Kepler statistics?"
  }'
```

---

## Notes

- **TESS data is preserved** but not implemented in frontend (future work)
- Only **Kepler model** is used for predictions
- Model files are in `kepler_final/` directory
- EXO can answer questions about both Kepler and TESS

---

**Created:** 2025-10-05
**Team:** NASA Space Apps Challenge
**Model:** Random Forest (89.25% accuracy)
**Assistant:** EXO (GPT-3.5-turbo)

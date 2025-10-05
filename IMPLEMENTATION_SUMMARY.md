# NASA Exoplanet Classifier - Implementation Summary

## What Was Built

### 1. Backend API Server (`api_server.py`)

**Flask REST API** running on port 5000

#### Endpoints:
- `POST /api/predict` - Kepler exoplanet classification
  - Input: 20 Kepler features
  - Output: Prediction (CONFIRMED/CANDIDATE/FALSE POSITIVE) + probabilities
  - Model: Random Forest (89.25% accuracy)

- `POST /api/chat` - EXO AI assistant
  - Input: User message + conversation history
  - Output: AI response about exoplanet features/statistics
  - Model: GPT-3.5-turbo

- `GET /api/health` - Health check
- `GET /api/features` - List of required features

#### Technologies:
- Flask + Flask-CORS
- scikit-learn (Random Forest model)
- OpenAI API (GPT-3.5-turbo)
- pickle (model persistence)

---

### 2. Frontend Application (`projectonasa/`)

**Express.js + EJS** running on port 3000

#### Features:

**A. Dynamic Workspace**
- Sidebar navigation
- Collapsible menus
- Single-page application feel

**B. New Candidate Section**
- 20 Kepler feature inputs (2 columns)
- Real-time prediction via API
- Visual results display:
  - Exoplanet image (random)
  - Prediction result (color-coded)
  - Confidence percentage
  - Probability bars for all 3 classes
  - Model information

**C. EXO Chat Widget**
- Floating chat button (bottom-right)
- Collapsible chat panel
- Real-time AI responses
- Conversation history
- Typing indicator

#### Technologies:
- Express.js (server)
- EJS (templates)
- Tailwind CSS (styling)
- Vanilla JavaScript (no frameworks)
- Fetch API (HTTP requests)

---

### 3. Machine Learning Model

**Kepler Random Forest Classifier**

#### Performance:
- **Accuracy:** 89.25%
- **AUC:** 97.24%
- **Classes:** 3 (CANDIDATE, CONFIRMED, FALSE POSITIVE)

#### Features (20):
1. `koi_score` (0.750 correlation) - Most important
2. `koi_fwm_stat_sig` (0.451)
3. `koi_srho_err2` (0.377)
4. `koi_dor_err2` (0.365)
5. `koi_incl` (0.362)
6. `koi_prad` (0.312)
7-20. Additional orbital and centroid features

#### Files:
- `kepler_rf_model.pkl` - Trained model
- `kepler_scaler.pkl` - Feature scaler (RobustScaler)
- `kepler_label_encoder.pkl` - Target encoder
- `kepler_features.json` - Feature names
- `kepler_model_metadata.json` - Model info

---

### 4. EXO AI Assistant

**GPT-3.5-turbo powered chatbot**

#### Capabilities:
- Explain Kepler/TESS features
- Compare model performance
- Provide statistical analysis
- Answer technical questions
- User-friendly explanations

#### Knowledge Base:
- Kepler: 20 features + correlations
- TESS: 14 features + correlations
- Model accuracies and results
- Feature engineering insights

---

## File Structure

```
NASA/
├── api_server.py              # Flask API (port 5000)
├── exo_agent.py               # Standalone console EXO
├── test_api.py                # API test script
├── test_exo_agent.py          # EXO console test
├── SETUP_INSTRUCTIONS.md      # Full setup guide
├── START_SERVERS.md           # Quick start
├── IMPLEMENTATION_SUMMARY.md  # This file
│
├── kepler_final/              # Model files
│   ├── kepler_rf_model.pkl    # Trained model (89.25%)
│   ├── kepler_scaler.pkl      # RobustScaler
│   ├── kepler_label_encoder.pkl
│   ├── kepler_features.json   # 20 features
│   ├── kepler_model_metadata.json
│   ├── save_kepler_model.py   # Training script
│   └── kepler_processed.csv   # Processed data
│
└── projectonasa/              # Frontend app
    ├── app.js                 # Express server (port 3000)
    ├── views/
    │   ├── dashboard.ejs      # Main page
    │   └── partials/
    │       └── sidebar.ejs    # Navigation
    └── public/
        ├── js/
        │   ├── dashboard.js   # Workspace + API calls
        │   └── exo-chat.js    # Chat widget
        ├── css/
        │   └── styles.css     # Space theme
        └── img/exoplanet/
            ├── e1.png
            ├── e2.png
            ├── e3.png
            └── e4.png
```

---

## How to Use

### 1. Start Backend
```bash
python api_server.py
```

### 2. Start Frontend
```bash
cd projectonasa
node app.js
```

### 3. Open Browser
```
http://localhost:3000
```

### 4. Predict Exoplanet
1. Sidebar → Add Candidate → New Candidate
2. Fill features (at least 1 required, 20 recommended)
3. Click "Submit"
4. View prediction result

### 5. Chat with EXO
1. Click chat button (bottom-right)
2. Ask questions:
   - "What are the Kepler statistics?"
   - "Explain koi_score"
   - "Why is TESS accuracy lower?"

---

## API Examples

### Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"koi_score": 0.95, ...}}'
```

### Chat
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is koi_score?"}'
```

---

## Key Design Decisions

### 1. Only Kepler Model in Frontend
- TESS data preserved in backend
- Kepler has higher accuracy (89.25% vs 64.57%)
- Frontend focuses on best model
- EXO can still explain TESS features

### 2. Flask + Express Architecture
- Flask: Python ML model serving
- Express: Node.js frontend
- Separation of concerns
- Easy to scale independently

### 3. Chat Widget Integration
- Non-intrusive floating button
- Available on all pages
- Persistent conversation history
- Real-time AI responses

### 4. Feature Input Design
- 2-column layout (10+10 features)
- All 20 Kepler features accessible
- Empty fields handled gracefully
- Clear labels with tooltips (can add)

### 5. Result Display
- Color-coded predictions:
  - Green: CONFIRMED
  - Yellow: CANDIDATE
  - Red: FALSE POSITIVE
- Probability bars (visual)
- Confidence percentage
- Model transparency (accuracy shown)

---

## Technologies Used

### Backend
- Python 3.10
- Flask 3.1.2
- Flask-CORS 6.0.1
- scikit-learn 1.5.2
- pandas 2.2.3
- numpy 2.1.3
- OpenAI 1.57.4
- pickle (stdlib)

### Frontend
- Node.js
- Express.js 4.x
- EJS (templating)
- Tailwind CSS 3.x
- Vanilla JavaScript ES6+

### ML Model
- Random Forest Classifier
- RobustScaler (preprocessing)
- LabelEncoder (target encoding)
- 200 estimators
- max_depth=15

---

## Performance Metrics

### Kepler Model
```
                precision    recall  f1-score   support

     CANDIDATE     0.7672    0.6820    0.7221       261
     CONFIRMED     0.8820    0.9058    0.8937       520
FALSE POSITIVE     0.9460    0.9684    0.9571       633

      accuracy                         0.8925      1414
```

### Response Times
- Prediction API: ~50-100ms
- EXO Chat: ~2-5s (GPT-3.5 latency)
- Frontend load: <1s

---

## Future Enhancements

1. **TESS Integration**
   - Add TESS model predictions
   - Compare Kepler vs TESS side-by-side

2. **Database Integration**
   - Save user predictions
   - Historical analysis

3. **Batch Predictions**
   - Upload CSV files
   - Bulk classification

4. **Model Explainability**
   - SHAP values
   - Feature importance visualization
   - Decision tree visualization

5. **User Authentication**
   - Login system
   - API key management
   - Usage tracking

6. **Enhanced UI**
   - 3D planet visualization
   - Interactive charts
   - Feature tooltips

---

## Credits

**Team:** NASA Space Apps Challenge
**Date:** October 5, 2025
**Model:** Random Forest (89.25% accuracy)
**AI Assistant:** EXO (GPT-3.5-turbo)
**Dataset:** NASA Exoplanet Archive (Kepler KOI)

---

## License

MIT License - NASA Space Apps Challenge 2025

# Testing Guide - NASA Exoplanet Classifier

## Quick Test (5 minutes)

### Step 1: Start Servers

**Terminal 1 - Backend API:**
```bash
python api_server.py
```

Expected output:
```
Loading Kepler model artifacts...
Model loaded: Random Forest
Features: 20
Classes: ['CANDIDATE', 'CONFIRMED', 'FALSE POSITIVE']
EXO Agent initialized with OpenAI API

================================================================================
NASA EXOPLANET API SERVER
================================================================================

Endpoints:
  POST /api/predict - Predict exoplanet classification
  POST /api/chat    - Chat with EXO agent
  GET  /api/features - Get required features
  GET  /api/health   - Health check

================================================================================
Server starting on http://localhost:5000
================================================================================
```

**Terminal 2 - Frontend:**
```bash
cd projectonasa
node app.js
```

Expected output:
```
🚀 Servidor corriendo en http://localhost:3000
```

---

### Step 2: Test API (Optional)

Run the test script:
```bash
python test_api.py
```

Expected output:
```
================================================================================
NASA EXOPLANET API - QUICK TEST
================================================================================

[1/3] Testing health endpoint...
Status: 200
{
  "status": "healthy",
  "model_loaded": true,
  "exo_available": true,
  "model_accuracy": 0.8925
}

[2/3] Getting required features...
Required features: 20
Features: koi_score, koi_fwm_stat_sig, koi_srho_err2, koi_dor_err2, koi_dor_err1...

[3/3] Testing prediction with sample candidate...

Status: 200
Prediction: CONFIRMED
Confidence: 90.5%

Probabilities:
  CANDIDATE: 5.2%
  CONFIRMED: 90.5%
  FALSE POSITIVE: 4.3%

Model: Random Forest
Accuracy: 89.25%
```

---

### Step 3: Test Frontend

1. Open browser: **http://localhost:3000**

2. You should see:
   - Welcome screen with "Welcome to ExoFinder"
   - Sidebar with NASA logo
   - Animated planets in background
   - Chat button (bottom-right)

---

### Step 4: Test Prediction

1. Click **"Add Candidate"** in sidebar
2. Click **"New Candidate"**
3. Fill in sample values:

**Left Column:**
```
koi_score: 0.95
koi_fwm_stat_sig: 2.1
koi_srho_err2: -0.03
koi_dor_err2: -0.01
koi_dor_err1: 0.01
koi_incl: 89.5
koi_prad_err1: 0.2
koi_count: 150
koi_dor: 15.2
koi_dikco_mdec_err: 0.05
```

**Right Column:**
```
koi_period_err1: 0.0001
koi_period_err2: -0.0001
koi_dikco_mra_err: 0.04
koi_prad_err2: -0.15
koi_dikco_msky_err: 0.06
koi_max_sngle_ev: 25.3
koi_prad: 1.5
koi_dicco_mdec_err: 0.03
koi_model_snr: 45.2
koi_dicco_mra_err: 0.02
```

4. Click **"Submit"**

Expected result:
- Loading message: "Analyzing candidate..."
- Exoplanet image appears (spinning)
- Prediction: **CONFIRMED** (green)
- Confidence: ~90%
- Probability bars showing distribution
- Model info: Random Forest, 89.25% accuracy

---

### Step 5: Test EXO Chat

1. Click **chat button** (bottom-right corner)
2. Chat panel opens
3. Type: `What are the Kepler statistics?`
4. Press Enter or click "Send"

Expected response (within 2-5 seconds):
```
The Kepler model is a Random Forest model with an accuracy
of 89.25%. It uses 20 features to classify exoplanets.
Some key features include koi_score, koi_fwm_stat_sig,
koi_srho_err2, koi_dor_err2, koi_incl, and koi_prad...
```

5. Try more questions:
   - `Explain koi_score`
   - `Why is TESS accuracy lower?`
   - `List the top TESS features`
   - `Compare Kepler vs TESS`

---

## Test Cases

### Test Case 1: CONFIRMED Planet (High Confidence)

**Input:**
- koi_score: **0.95** (very high)
- koi_incl: **89.5** (edge-on transit)
- koi_prad: **1.5** (Earth-sized)

**Expected:**
- Prediction: CONFIRMED
- Confidence: >85%

---

### Test Case 2: FALSE POSITIVE (Low koi_score)

**Input:**
- koi_score: **0.1** (very low)
- koi_fwm_stat_sig: **10.5** (high centroid offset)

**Expected:**
- Prediction: FALSE POSITIVE
- Confidence: >70%

---

### Test Case 3: CANDIDATE (Uncertain)

**Input:**
- koi_score: **0.5** (medium)
- Mixed features

**Expected:**
- Prediction: CANDIDATE or CONFIRMED
- Confidence: 50-70%

---

### Test Case 4: Minimal Input

**Input:**
- Only koi_score: **0.8**
- All other fields empty

**Expected:**
- Warning: "Missing or empty features"
- Prediction still works (fills with 0)
- Lower confidence

---

## Error Testing

### Error 1: API Server Not Running

**Action:** Stop api_server.py, try prediction

**Expected:**
```
Error: Could not connect to EXO API
Make sure the server is running on port 5000
```

---

### Error 2: Missing OpenAI API Key

**Action:** Unset OPENAI_API_KEY, try chat

**Expected:**
```
Error: EXO agent not available - OPENAI_API_KEY not set
```

---

### Error 3: Invalid Input

**Action:** Enter text in number field

**Expected:**
- Browser validation prevents submit
- Or API returns error

---

## Performance Testing

### Prediction Speed
- Expected: 50-200ms per prediction
- Test: Submit 10 candidates sequentially

### Chat Response Time
- Expected: 2-5 seconds (OpenAI latency)
- Test: Send 5 messages in a row

### Frontend Load Time
- Expected: <1 second
- Test: Refresh page multiple times

---

## Browser Compatibility

Tested on:
- Chrome 120+ ✓
- Firefox 115+ ✓
- Edge 120+ ✓
- Safari 17+ (should work)

---

## Troubleshooting

### Issue: "Port already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

---

### Issue: "Module not found"

**Backend:**
```bash
pip install flask flask-cors scikit-learn pandas numpy openai
```

**Frontend:**
```bash
cd projectonasa
npm install
```

---

### Issue: Prediction always returns same result

**Check:**
1. Are you filling different values?
2. Is model file corrupted? (re-run save_kepler_model.py)
3. Check browser console for errors (F12)

---

### Issue: Chat doesn't respond

**Check:**
1. Is OPENAI_API_KEY set? `echo %OPENAI_API_KEY%`
2. Is API key valid? (check OpenAI dashboard)
3. Is api_server.py showing "EXO Agent initialized"?
4. Browser console for fetch errors

---

## Success Criteria

✅ Backend starts without errors
✅ Frontend starts on port 3000
✅ Health check returns 200
✅ Prediction works with sample data
✅ Chat responds within 5 seconds
✅ UI displays results correctly
✅ No console errors
✅ Probabilities sum to ~100%

---

## Next Steps After Testing

1. ✅ Verify all features work
2. ✅ Test with real Kepler data (from Datasets/)
3. ✅ Deploy to production server (optional)
4. ✅ Share with team
5. ✅ Collect feedback

---

**Last Updated:** 2025-10-05
**Status:** Ready for Testing
**Model Accuracy:** 89.25%

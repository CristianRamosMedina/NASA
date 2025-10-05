# EXO Agent Setup Guide

## 🤖 What is EXO?

EXO is an AI-powered assistant that explains Kepler and TESS exoplanet model features and statistics.

---

## 🔧 Setup (Step by Step)

### 1. Install OpenAI Python Package

```bash
pip install openai
```

### 2. Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### 3. Set Environment Variable

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

**Or create `.env` file:**
```bash
# Copy example
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-key-here
```

### 4. Run EXO Agent

```bash
python exo_agent.py
```

---

## 💬 Example Usage

### Welcome Screen:
```
╔══════════════════════════════════════════════════════════╗
║  👋 Hello! I'm EXO, your Exoplanet Expert Assistant     ║
╚══════════════════════════════════════════════════════════╝

I can help you explore and understand our NASA exoplanet
classification models (Kepler & TESS).

🌟 What I can do:
  • Explain model features and their importance
  • Show you statistics and accuracy metrics
  • Compare Kepler vs TESS performance
  • Answer questions about planetary classification

📊 Quick Stats:
  • Kepler: 89.25% accuracy (Random Forest, 20 features)
  • TESS: 64.57% accuracy (XGBoost, 14 features)
```

### Sample Conversation:

```
🌍 You: What are the Kepler statistics?

🤖 EXO: The Kepler model uses a Random Forest classifier with impressive
performance:

- **Accuracy**: 89.25%
- **AUC**: 97.24%
- **Features**: 20 selected from 141 original columns
- **Classes**: 3 (CONFIRMED, CANDIDATE, FALSE POSITIVE)

The best feature is koi_score (0.750 correlation) - a pre-calculated
disposition score by NASA's Robovetter pipeline. This score combines
multiple quality tests and is the strongest predictor.

Other top features include centroid tests (koi_fwm_stat_sig) and orbital
geometry measurements (koi_incl, koi_dor).
```

```
🌍 You: Why is TESS accuracy lower?

🤖 EXO: TESS has 64.57% accuracy (24.68% lower than Kepler) for 3 main reasons:

1. **No Pre-calculated Score**: Kepler has koi_score (0.750 correlation),
   TESS doesn't have an equivalent quality metric

2. **Weaker Features**: TESS best feature is st_tmag (0.299 correlation) -
   60% weaker than Kepler's best feature

3. **Missing Centroid Tests**: Kepler has 8 centroid features to detect
   false positives, TESS dataset doesn't include these

Despite being lower, 64.57% is still much better than random guessing
(33%) and useful for screening candidates.
```

```
🌍 You: Explain koi_score

🤖 EXO: koi_score is the most important feature in the Kepler model
(correlation: 0.750).

**What it is:**
- A disposition confidence score from 0 to 1
- Pre-calculated by NASA's Robovetter algorithm
- Combines results from multiple validation tests

**How it works:**
- Higher values (closer to 1) = higher confidence it's a real planet
- Lower values = likely a false positive
- Incorporates centroid tests, transit shape analysis, and statistical checks

**Why it's powerful:**
NASA engineers already did the hard work of combining 10+ different tests
into this single score, making it the strongest predictor in our model.

TESS doesn't have an equivalent, which is why TESS accuracy is lower.
```

---

## 🎯 Available Questions

### General:
- "What can you do?"
- "Compare Kepler and TESS"
- "What models did you use?"

### Kepler Specific:
- "What are the Kepler statistics?"
- "List Kepler features"
- "Explain koi_score"
- "Why is Kepler so accurate?"

### TESS Specific:
- "What are the TESS statistics?"
- "List TESS features"
- "Explain st_tmag"
- "Why is TESS accuracy lower?"

### Technical:
- "What is correlation?"
- "How does Random Forest work?"
- "What is AUC?"
- "Explain overfitting"

---

## 🔒 Security Notes

1. **Never commit `.env` file** - it contains your API key
2. `.env` is already in `.gitignore`
3. Use `.env.example` as template
4. API key format: `sk-...` (starts with sk-)
5. Keep your key secret!

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not set"
```bash
# Set environment variable (see step 3 above)
```

### Error: "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### Error: "Authentication failed"
```bash
# Check your API key is correct
# Make sure it starts with 'sk-'
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY% # Windows
```

### Response is slow
- Normal: OpenAI API can take 2-5 seconds
- Using gpt-3.5-turbo (fast model)
- First response is slower (initializing)

---

## 📝 Technical Details

**Model**: GPT-3.5-Turbo
**Temperature**: 0.7 (balanced creativity)
**Max Tokens**: 500 (concise responses)
**Context**: Includes feature data + conversation history

**Features Loaded**:
- Kepler: Top 6 features with correlations
- TESS: Top 4 features with correlations
- Model results: Accuracy, AUC, winner

---

## 🚀 Next Steps (Frontend Integration)

After testing in console:
1. Create FastAPI backend endpoint
2. Expose `/chat` route
3. Connect to React frontend
4. Add streaming responses (optional)

See `exo_agent.py` for implementation details.

---

**Created**: 2025-10-05
**Author**: NASA Space Apps Challenge Team

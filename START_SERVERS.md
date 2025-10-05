# Quick Start Guide

## Start Both Servers

### Terminal 1 - Backend API (Port 5000)
```bash
python api_server.py
```

### Terminal 2 - Frontend (Port 3000)
```bash
cd projectonasa
node app.js
```

### Open Browser
```
http://localhost:3000
```

## Features

1. **New Candidate Prediction**
   - Sidebar → Add Candidate → New Candidate
   - Fill Kepler features (20 inputs)
   - Click Submit
   - View: CONFIRMED / CANDIDATE / FALSE POSITIVE

2. **EXO AI Chat**
   - Click chat button (bottom-right)
   - Ask about Kepler/TESS features
   - Get model explanations

## Requirements

- OpenAI API key set: `set OPENAI_API_KEY=your-key`
- Python packages: `flask flask-cors scikit-learn pandas numpy openai`
- Node.js installed

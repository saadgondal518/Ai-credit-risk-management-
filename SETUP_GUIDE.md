# AI Credit Risk Management System - Complete Setup Guide

## 📋 Project Overview
This is a full-stack AI application that predicts credit risk using machine learning. It includes a Python backend with a trained ML model and a web-based frontend.

## 🏗️ Project Structure
```
ai-credit-risk-management/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── model_training.py      # Script to train the ML model
│   ├── data_preprocessing.py  # Data cleaning and preparation
│   ├── models/
│   │   └── credit_risk_model.pkl    # Trained model (generated after training)
│   └── requirements.txt
│
├── frontend/
│   ├── index.html            # Main web interface
│   ├── style.css             # Styling
│   └── script.js             # Frontend logic
│
├── README.md
├── .gitignore
└── requirements.txt          # All dependencies


## 🚀 Step-by-Step Installation

### Step 1: Create Project Folder
```bash
# Open VS Code Terminal (Ctrl + `)
mkdir ai-credit-risk-management
cd ai-credit-risk-management
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 3: Create Folder Structure
```bash
mkdir backend
mkdir backend/models
mkdir frontend
```

### Step 4: Install Dependencies
```bash
# Copy the requirements.txt file content and create the file
pip install -r requirements.txt
```

### Step 5: Prepare the Dataset
```bash
# Run this Python command to download the dataset
python backend/data_preprocessing.py --download
```

### Step 6: Train the Model
```bash
# This creates the ML model
python backend/model_training.py
```

### Step 7: Run the Backend Server
```bash
# In your terminal (with venv activated)
python backend/app.py
```
You should see: "Running on http://127.0.0.1:5000"

### Step 8: Run the Frontend
Open a new terminal:
```bash
# Navigate to frontend folder
cd frontend

# Start a simple Python server (or use Live Server in VS Code)
python -m http.server 8000
```
Then open: http://localhost:8000

---

## 🔧 VS Code Setup Tips

1. **Install Extensions:**
   - Python (by Microsoft)
   - Pylance
   - Thunder Client (for API testing)
   - Live Server (for frontend)

2. **Set Python Interpreter:**
   - Press Ctrl+Shift+P
   - Type "Python: Select Interpreter"
   - Choose the one in your `venv` folder

3. **Debug Configuration:**
   - Create `.vscode/launch.json`
   - Add debug configuration for Flask

---

## 📝 How to Use the Application

1. Open the web interface at http://localhost:8000
2. Fill in the credit applicant details
3. Click "Predict Risk"
4. View the risk score (0-1) and recommendation
5. Higher score = Higher credit risk

---

## 🐙 GitHub Setup

### First Time Only:
```bash
git init
git add .
git commit -m "Initial commit: AI Credit Risk Management System"
git remote add origin https://github.com/saadgondal518/ai-credit-risk-management.git
git branch -M main
git push -u origin main
```

### After Making Changes:
```bash
git add .
git commit -m "Describe your changes"
git push
```

---

## ✅ Verification Checklist
- [ ] Virtual environment created and activated
- [ ] All packages installed (pip list shows flask, scikit-learn, pandas, etc.)
- [ ] Dataset downloaded successfully
- [ ] Model trained (check backend/models/credit_risk_model.pkl exists)
- [ ] Backend running on localhost:5000
- [ ] Frontend accessible on localhost:8000
- [ ] Can submit credit data and get predictions
- [ ] Ready to push to GitHub


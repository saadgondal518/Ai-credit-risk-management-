# 🏦 AI Credit Risk Management System

A full-stack machine learning application that predicts credit risk using Random Forest classification. Built with Python (Flask) backend and HTML/CSS/JavaScript frontend.

## 🎯 Features

- **ML-Powered Predictions**: Random Forest classifier trained on real credit data
- **Real-time Risk Assessment**: Instant credit risk scoring (0-1 scale)
- **User-Friendly Interface**: Modern, responsive web interface
- **REST API**: Complete API for predictions and batch operations
- **Risk Categories**: Low, Medium, and High risk classifications
- **Visual Dashboard**: Color-coded risk indicators and detailed metrics
- **Production-Ready**: Fully documented and ready to deploy

## 📊 Project Structure

```
ai-credit-risk-management/
│
├── backend/
│   ├── app.py                      # Flask REST API server
│   ├── model_training.py           # ML model training script
│   ├── data_preprocessing.py       # Data preparation script
│   ├── models/
│   │   ├── credit_risk_model.pkl   # Trained Random Forest model
│   │   └── scaler.pkl              # Feature scaler
│   ├── data/
│   │   ├── X_processed.csv         # Processed features
│   │   └── y_processed.csv         # Target variable
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                  # Main web interface
│   ├── style.css                   # Styling
│   └── script.js                   # JavaScript logic
│
├── README.md                        # This file
├── SETUP_GUIDE.md                  # Detailed setup instructions
└── requirements.txt                # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/saadgondal518/ai-credit-risk-management.git
cd ai-credit-risk-management
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Prepare dataset**
Download the [Give Me Some Credit dataset](https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset) or use:
```bash
python backend/data_preprocessing.py --download
```

5. **Train the model**
```bash
python backend/model_training.py
```

6. **Start the backend**
```bash
python backend/app.py
```
Backend will run on: `http://127.0.0.1:5000`

7. **Start the frontend** (new terminal)
```bash
cd frontend
python -m http.server 8000
```
Frontend will run on: `http://localhost:8000`

## 📝 How to Use

1. Open the web interface at `http://localhost:8000`
2. Fill in the applicant's credit information:
   - Age
   - Monthly Income
   - Credit Limit
   - Debt-to-Income Ratio
   - Monthly Debt
   - Number of Open Accounts
   - Credit History (late payments)
   - Age of Credit Line
   - Number of Dependents

3. Click **"Predict Risk"** to get the assessment
4. Review the results:
   - **Risk Score** (0-1): Numerical probability
   - **Risk Level**: Low/Medium/High classification
   - **Recommendation**: Approve/Review/Reject decision

## 🔌 API Endpoints

### Get API Status
```bash
GET /
```
Returns API status and version

### Get Required Features
```bash
GET /api/features
```
Returns list of features the model expects

### Single Prediction
```bash
POST /api/predict
Content-Type: application/json

{
  "age": 35,
  "income": 50000,
  "credit_limit": 10000,
  "debt_ratio": 0.3,
  "monthly_debt": 1500,
  "number_of_open_accounts": 5,
  "number_of_times_90_days_late": 0,
  "age_of_credit_line": 120,
  "number_of_times_60_days_late": 0,
  "number_of_dependents": 2
}
```

Response:
```json
{
  "status": "success",
  "risk_score": 0.2847,
  "risk_level": "Low Risk",
  "recommendation": "✅ Approve - Applicant has low credit risk",
  "color": "green",
  "prediction": 0,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Batch Prediction
```bash
POST /api/batch-predict
Content-Type: application/json

{
  "applicants": [
    {"age": 35, "income": 50000, ...},
    {"age": 45, "income": 60000, ...}
  ]
}
```

### Model Information
```bash
GET /api/model-info
```
Returns details about the trained model

## 🤖 Machine Learning Details

### Model Type
- **Algorithm**: Random Forest Classifier
- **Number of Trees**: 100
- **Max Depth**: 20
- **Train/Test Split**: 80/20

### Features Used (10)
1. Age
2. Monthly Income
3. Credit Limit
4. Debt-to-Income Ratio
5. Monthly Debt
6. Number of Open Accounts
7. Times 90+ Days Late
8. Age of Credit Line (months)
9. Times 60+ Days Late
10. Number of Dependents

### Performance Metrics
The model achieves:
- **Accuracy**: High precision on test data
- **AUC-ROC**: Excellent discrimination ability
- **Recall**: Good coverage of high-risk cases

## 🛠️ Troubleshooting

### Backend not starting
```bash
# Check if port 5000 is in use
# Kill the process using port 5000 and try again

# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000
```

### Model not found
```bash
# Train the model first
python backend/model_training.py

# Verify files exist
ls backend/models/
```

### CORS errors in browser
- Frontend and backend must have different ports
- Backend runs on 5000, frontend on 8000
- Check that CORS is enabled in Flask app

### Dataset download fails
- Download manually from [Kaggle](https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset)
- Place CSV in `data/` folder
- Run preprocessing: `python backend/data_preprocessing.py`

## 📦 Dependencies

### Backend
- Flask 2.3.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin support
- scikit-learn 1.3.0 - ML algorithms
- pandas 2.0.0 - Data processing
- numpy 1.24.0 - Numerical computing
- joblib 1.3.0 - Model serialization

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript (No frameworks required)

## 🚀 Deployment

### Deploy to Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# Set environment variables
heroku config:set FLASK_ENV=production
```

### Deploy to AWS/Google Cloud
See the documentation for their specific deployment processes.

## 📚 Learning Resources

### Understand the Code
- Start with `SETUP_GUIDE.md` for step-by-step instructions
- Read the comments in each Python file
- Check the console (F12) for debug messages

### Modify the Model
1. Edit hyperparameters in `model_training.py`
2. Add new features in `data_preprocessing.py`
3. Retrain: `python backend/model_training.py`

### Improve Predictions
- Collect more training data
- Feature engineering and selection
- Ensemble with other algorithms
- Hyperparameter tuning

## 📈 Project Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Historical prediction logging
- [ ] Mobile app version
- [ ] Advanced visualization dashboard
- [ ] Real-time model monitoring
- [ ] A/B testing framework
- [ ] Docker containerization

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created as an educational AI/ML project demonstrating:
- Full-stack development
- Machine learning pipeline
- REST API design
- Frontend-backend integration
- Production-ready code practices

## 🙏 Acknowledgments

- Dataset: [Give Me Some Credit Dataset](https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset)
- Icons: Emoji Unicode
- Framework: Flask, scikit-learn, pandas

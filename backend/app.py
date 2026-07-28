
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for frontend

# Global variables for model and scaler
model = None
scaler = None
feature_names = None


def load_model_and_scaler():
    """Load the trained model and scaler"""
    global model, scaler, feature_names
    
    model_path = 'backend/models/credit_risk_model.pkl'
    scaler_path = 'backend/models/scaler.pkl'
    
    try:
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            print("✅ Model and scaler loaded successfully!")
            return True
        else:
            print("❌ Model or scaler not found!")
            print("   Please run: python backend/model_training.py")
            return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False


def get_feature_names():
    """Get feature names from preprocessed data"""
    try:
        X = pd.read_csv('backend/data/X_processed.csv')
        return X.columns.tolist()
    except:
        return None


@app.route('/', methods=['GET'])
def home():
    """Home route - API status"""
    return jsonify({
        'status': 'running',
        'service': 'AI Credit Risk Management API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get list of required features"""
    global feature_names
    
    if feature_names is None:
        feature_names = get_feature_names()
    
    if feature_names:
        return jsonify({
            'status': 'success',
            'features': feature_names,
            'count': len(feature_names)
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Features not available'
        }), 500


@app.route('/api/predict', methods=['POST'])
def predict_risk():
    """
    Predict credit risk for a given applicant
    
    Expected JSON format:
    {
        "age": 35,
        "income": 50000,
        "credit_limit": 10000,
        ... (other features)
    }
    """
    
    try:
        # Check if model is loaded
        if model is None or scaler is None:
            return jsonify({
                'status': 'error',
                'message': 'Model not loaded. Please train the model first.'
            }), 500
        
        # Get JSON data
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        # Get feature names
        global feature_names
        if feature_names is None:
            feature_names = get_feature_names()
        
        if feature_names is None:
            return jsonify({
                'status': 'error',
                'message': 'Feature configuration not found'
            }), 500
        
        # Prepare features in correct order
        feature_values = []
        for feature in feature_names:
            if feature in data:
                value = data[feature]
                # Handle missing values
                if value is None or value == '':
                    value = 0
                feature_values.append(float(value))
            else:
                # Missing feature - use default value
                feature_values.append(0)
        
        # Convert to numpy array
        X_new = np.array([feature_values])
        
        # Scale features
        X_new_scaled = scaler.transform(X_new)
        
        # Make prediction
        risk_probability = model.predict_proba(X_new_scaled)[0][1]
        risk_prediction = model.predict(X_new_scaled)[0]
        
        # Determine risk level and recommendation
        if risk_probability < 0.3:
            risk_level = "Low Risk"
            recommendation = "✅ Approve - Applicant has low credit risk"
            color = "green"
        elif risk_probability < 0.6:
            risk_level = "Medium Risk"
            recommendation = "⚠️  Review - Applicant has moderate credit risk"
            color = "orange"
        else:
            risk_level = "High Risk"
            recommendation = "❌ Reject - Applicant has high credit risk"
            color = "red"
        
        # Return results
        return jsonify({
            'status': 'success',
            'risk_score': round(float(risk_probability), 4),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'color': color,
            'prediction': int(risk_prediction),
            'timestamp': datetime.now().isoformat()
        })
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid data format: {str(e)}'
        }), 400
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f'Prediction error: {str(e)}'
        }), 500


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction for multiple applicants
    
    Expected JSON format:
    {
        "applicants": [
            {"age": 35, "income": 50000, ...},
            {"age": 45, "income": 60000, ...}
        ]
    }
    """
    
    try:
        if model is None or scaler is None:
            return jsonify({
                'status': 'error',
                'message': 'Model not loaded'
            }), 500
        
        data = request.get_json()
        applicants = data.get('applicants', [])
        
        if not applicants:
            return jsonify({
                'status': 'error',
                'message': 'No applicants provided'
            }), 400
        
        global feature_names
        if feature_names is None:
            feature_names = get_feature_names()
        
        results = []
        
        for idx, applicant in enumerate(applicants):
            # Prepare features
            feature_values = []
            for feature in feature_names:
                value = applicant.get(feature, 0)
                if value is None or value == '':
                    value = 0
                feature_values.append(float(value))
            
            # Make prediction
            X_new = np.array([feature_values])
            X_new_scaled = scaler.transform(X_new)
            risk_probability = model.predict_proba(X_new_scaled)[0][1]
            
            results.append({
                'applicant_id': idx,
                'risk_score': round(float(risk_probability), 4),
                'risk_level': 'High' if risk_probability > 0.6 else 'Medium' if risk_probability > 0.3 else 'Low'
            })
        
        return jsonify({
            'status': 'success',
            'total_applicants': len(applicants),
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    
    if model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 500
    
    return jsonify({
        'status': 'success',
        'model_type': str(type(model).__name__),
        'model_params': model.get_params() if hasattr(model, 'get_params') else {},
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("   AI CREDIT RISK - FLASK BACKEND")
    print("=" * 50)
    
    # Load model
    if load_model_and_scaler():
        print("\n✅ Ready to serve predictions!")
        print("\n📌 API Endpoints:")
        print("   GET  /                          - API status")
        print("   GET  /api/features              - Get required features")
        print("   POST /api/predict               - Single prediction")
        print("   POST /api/batch-predict         - Multiple predictions")
        print("   GET  /api/model-info            - Model information")
        print("\n🌐 Starting server...")
        print("   Open: http://127.0.0.1:5000")
        print("=" * 50 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("\n❌ Cannot start server without a trained model!")
        print("   Please run: python backend/model_training.py")

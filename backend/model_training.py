
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


def load_preprocessed_data(data_dir='backend/data'):
    """Load the preprocessed data"""
    print("📂 Loading preprocessed data...")
    
    try:
        X = pd.read_csv(os.path.join(data_dir, 'X_processed.csv'))
        y = pd.read_csv(os.path.join(data_dir, 'y_processed.csv')).iloc[:, 0]
        
        print(f"✅ Data loaded successfully!")
        print(f"   Features shape: {X.shape}")
        print(f"   Target shape: {y.shape}")
        
        return X, y
    except FileNotFoundError:
        print("❌ Preprocessed data not found!")
        print("   Please run: python backend/data_preprocessing.py")
        return None, None


def prepare_data_for_training(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets"""
    print("\n📊 Splitting data into train/test sets...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y
    )
    
    print(f"✅ Data split completed!")
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Testing set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    """Normalize the features"""
    print("\n📈 Scaling features...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✅ Features scaled successfully!")
    
    return X_train_scaled, X_test_scaled, scaler


def train_model(X_train, y_train):
    """Train the Random Forest model"""
    print("\n🤖 Training Random Forest model...")
    print("   This may take a few minutes...")
    
    model = RandomForestClassifier(
        n_estimators=100,      # Number of trees
        max_depth=20,          # Maximum depth of trees
        min_samples_split=10,  # Minimum samples to split
        min_samples_leaf=5,    # Minimum samples in leaf
        random_state=42,
        n_jobs=-1,             # Use all CPU cores
        verbose=1
    )
    
    model.fit(X_train, y_train)
    
    print("✅ Model training completed!")
    
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("\n📊 Evaluating model performance...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    print("\n" + "="*50)
    print("📈 MODEL PERFORMANCE METRICS")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC-ROC Score: {auc_score:.4f}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    print("\n🔲 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("="*50)
    
    return accuracy, auc_score


def save_model(model, scaler, output_dir='backend/models'):
    """Save the trained model and scaler"""
    print(f"\n💾 Saving model and scaler...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'credit_risk_model.pkl')
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"✅ Model saved to: {model_path}")
    print(f"✅ Scaler saved to: {scaler_path}")


def main():
    """Main training workflow"""
    print("=" * 50)
    print("   AI CREDIT RISK - MODEL TRAINING")
    print("=" * 50)
    
    # Load data
    X, y = load_preprocessed_data()
    if X is None:
        print("\n❌ Cannot proceed without data. Exiting.")
        return
    
    # Split data
    X_train, X_test, y_train, y_test = prepare_data_for_training(X, y)
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    
    # Train model
    model = train_model(X_train_scaled, y_train)
    
    # Evaluate
    accuracy, auc_score = evaluate_model(model, X_test_scaled, y_test)
    
    # Save
    save_model(model, scaler)
    
    print("\n" + "=" * 50)
    print("✅ Model training completed successfully!")
    print("=" * 50)
    print("\n📌 Next step: Run 'python backend/app.py' to start the server")


if __name__ == "__main__":
    main()

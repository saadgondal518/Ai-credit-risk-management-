import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Try to import kagglehub for downloading dataset
try:
    import kagglehub
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    print("Note: kagglehub not installed. Install with: pip install kagglehub")


def download_dataset():
    """Download the Give Me Some Credit dataset from Kaggle"""
    print("📥 Downloading Give Me Some Credit dataset...")
    
    try:
        # Download dataset
        path = kagglehub.dataset_download("brycecf/give-me-some-credit-dataset")
        print(f"✅ Dataset downloaded to: {path}")
        
        # Find the CSV file
        csv_file = None
        for file in os.listdir(path):
            if file.endswith('.csv'):
                csv_file = os.path.join(path, file)
                break
        
        if csv_file:
            return pd.read_csv(csv_file)
        else:
            print("❌ No CSV file found in downloaded dataset")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\n📌 Alternative: Download manually from:")
        print("   https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset")
        print("   Then place the CSV in the 'data' folder")
        return None


def load_local_dataset(filepath):
    """Load dataset from local file"""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded dataset from {filepath}")
        return df
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None


def preprocess_data(df):
    """Clean and prepare the data"""
    print("\n🔧 Preprocessing data...")
    
    # Make a copy
    df = df.copy()
    
    # Drop rows with too many missing values
    df = df.dropna(thresh=len(df.columns) * 0.8)
    
    # Fill missing values with median for numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Remove any remaining NaN values
    df = df.dropna()
    
    print(f"✅ Data shape after preprocessing: {df.shape}")
    print(f"   - Rows: {df.shape[0]}")
    print(f"   - Columns: {df.shape[1]}")
    
    return df


def prepare_features_and_target(df):
    """Separate features and target variable"""
    print("\n📊 Preparing features and target...")
    
    # The target is usually the first column (SeriousDlqin2yrs)
    # Adjust based on your dataset's actual target column
    
    # Common target column names
    target_col = None
    for col in df.columns:
        if 'serious' in col.lower() or 'delinquent' in col.lower() or 'default' in col.lower():
            target_col = col
            break
    
    if target_col is None:
        # If no obvious target, use the first column
        target_col = df.columns[0]
    
    print(f"✅ Target variable: {target_col}")
    
    # Separate features and target
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    # Remove ID columns if present
    X = X.loc[:, ~X.columns.str.contains('ID', case=False, na=False)]
    
    print(f"✅ Features shape: {X.shape}")
    print(f"✅ Target shape: {y.shape}")
    print(f"✅ Target class distribution:\n{y.value_counts()}")
    
    return X, y


def save_preprocessed_data(X, y, output_dir='backend/data'):
    """Save preprocessed data"""
    os.makedirs(output_dir, exist_ok=True)
    
    X.to_csv(os.path.join(output_dir, 'X_processed.csv'), index=False)
    y.to_csv(os.path.join(output_dir, 'y_processed.csv'), index=False)
    
    print(f"\n💾 Preprocessed data saved to {output_dir}/")


def main():
    """Main preprocessing workflow"""
    print("=" * 50)
    print("   AI CREDIT RISK - DATA PREPROCESSING")
    print("=" * 50)
    
    # Check for local dataset
    dataset_path = 'data/cs-training.csv'  # Adjust if your file has different name
    
    if os.path.exists(dataset_path):
        print(f"\n📂 Found local dataset at {dataset_path}")
        df = load_local_dataset(dataset_path)
    elif KAGGLE_AVAILABLE:
        df = download_dataset()
    else:
        print("\n❌ Dataset not found. Please:")
        print("   1. Install kagglehub: pip install kagglehub")
        print("   2. Or download manually and place in 'data' folder")
        return
    
    if df is None:
        print("\n❌ Failed to load dataset. Exiting.")
        return
    
    # Preprocess
    df = preprocess_data(df)
    
    # Prepare features and target
    X, y = prepare_features_and_target(df)
    
    # Save preprocessed data
    save_preprocessed_data(X, y)
    
    print("\n" + "=" * 50)
    print("✅ Data preprocessing completed successfully!")
    print("=" * 50)
    print("\n📌 Next step: Run 'python backend/model_training.py'")


if __name__ == "__main__":
    main()

# pipeline.py
import sys
from data_ingestion import DataIngestion
from data_cleaning import DataCleaning
from feature_engineering import FeatureEngineering
from feature_scaling import FeatureScaler
from data_splitter import DataSplitter
from train import evaluate_models
from model_evaluate import ModelEvaluator
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier 
import pandas as pd
import os

# Add project root to Python path (optional, for imports)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

def run_pipeline():
    try:
        # Step 1: Data Ingestion
        print("🚀 Starting pipeline: Loading data...")
        ingestion = DataIngestion("project_data.csv")
        raw_data = ingestion.load_data()

        # Step 2: Data Cleaning
        print("\n🚀 Cleaning data...")
        cleaner = DataCleaning(raw_data)
        cleaned_data = cleaner.clean_data()
        cleaned_data.to_csv("data/pre_proceesed_data/cleaned_data.csv", index=False)
        print("✅ Cleaned data saved.")

        # Step 3: Feature Engineering
        print("\n🚀 Engineering features...")
        fe = FeatureEngineering(cleaned_data)
        engineered_data = fe.engineer_features(save_path="data/pre_proceesed_data/processed_data.csv")
        print("✅ Engineered data saved.")

        # Step 4: Feature Scaling
        print("\n🚀 Scaling features...")
        scaler = FeatureScaler(engineered_data, scaler_type="standard")
        scaled_data = scaler.scale_features(save_path="data/pre_proceesed_data/scaled_data.csv")
        print("✅ Scaled data saved.")

        # Step 5: Data Splitting and Resampling
        print("\n🚀 Splitting and resampling data...")
        X = scaled_data.drop(columns=["is_safe"])
        y = scaled_data["is_safe"]
        splitter = DataSplitter(X, y)
        X_train_res, X_test, y_train_res, y_test = splitter.split_and_resample()

        # Step 6: Model Training
        print("\n🚀 Training models...")
        models = {
            "Random Forest": RandomForestClassifier(random_state=42, n_jobs=-1),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
            "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
            "K-Neighbors Classifier": KNeighborsClassifier(n_jobs=-1),
            "XGBClassifier": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
            "Support Vector Classifier": SVC(probability=True, random_state=42),
        }
        results = evaluate_models(X, y, models)
        os.makedirs("models", exist_ok=True)
        results.to_csv("models/model_results.csv", index=False)
        print("✅ Model results saved to models/model_results.csv")

        # Step 7: Evaluate a specific model (e.g., Random Forest)
        print("\n🚀 Evaluating Random Forest model...")
        rf_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        rf_model.fit(X_train_res, y_train_res)
        evaluator = ModelEvaluator(rf_model, X_test, y_test)
        metrics = evaluator.evaluate()
        evaluator.plot_confusion_matrix(save_path="models/confusion_matrix_rf.png")
        print("✅ Pipeline completed successfully!")

    except MLProjectException as e:
        print(f"Pipeline error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    run_pipeline()
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score
)
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

def evaluate_clf(true, predicted, predicted_prob=None):
    """Calculate key metrics for classifier."""
    acc = accuracy_score(true, predicted)
    f1 = f1_score(true, predicted)
    precision = precision_score(true, predicted)
    recall = recall_score(true, predicted)
    roc_auc = roc_auc_score(true, predicted_prob) if predicted_prob is not None else None
    return acc, f1, precision, recall, roc_auc

def evaluate_models(X, y, models):
    """
    Splits data, trains models, evaluates performance, and returns a report DataFrame.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        smt = SMOTEENN(smote=SMOTE(k_neighbors=1, random_state=42), random_state=42)
        X_train_res, y_train_res = smt.fit_resample(X_train, y_train)

        print("✅ Resampling complete.")
        print("Class distribution after resampling:", dict(pd.Series(y_train_res).value_counts()))

        models_list, accuracy_list, auc_list = [], [], []

        for model_name, model in models.items():
            print(f"\n🚀 Training {model_name}...")
            model.fit(X_train_res, y_train_res)

            y_train_pred = model.predict(X_train_res)
            y_test_pred = model.predict(X_test)
            y_train_prob = model.predict_proba(X_train_res)[:, 1] if hasattr(model, "predict_proba") else None
            y_test_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

            train_acc, train_f1, train_prec, train_recall, train_auc = evaluate_clf(y_train_res, y_train_pred, y_train_prob)
            test_acc, test_f1, test_prec, test_recall, test_auc = evaluate_clf(y_test, y_test_pred, y_test_prob)

            print(f"\n📊 {model_name} Performance")
            print("Training Set:")
            print(f"- Accuracy: {train_acc:.4f}, F1: {train_f1:.4f}, Precision: {train_prec:.4f}, Recall: {train_recall:.4f}")
            print(f"- ROC-AUC: {train_auc:.4f}" if train_auc else "- ROC-AUC: N/A")
            print("Test Set:")
            print(f"- Accuracy: {test_acc:.4f}, F1: {test_f1:.4f}, Precision: {test_prec:.4f}, Recall: {test_recall:.4f}")
            print(f"- ROC-AUC: {test_auc:.4f}" if test_auc else "- ROC-AUC: N/A")
            print("=" * 40)

            models_list.append(model_name)
            accuracy_list.append(test_acc)
            auc_list.append(test_auc if test_auc else np.nan)

        report = pd.DataFrame({
            "Model Name": models_list,
            "Test Accuracy": accuracy_list,
            "Test ROC-AUC": auc_list
        }).sort_values(by="Test Accuracy", ascending=False)

        return report

    except Exception as e:
        raise MLProjectException(
            error_message="Error during model evaluation",
            error_detail=e
        )

if __name__ == "__main__":
    try:
        file_path = "data/pre_proceesed_data/processed_data.csv"
        df = pd.read_csv(file_path)
        X = df.drop(columns=["is_safe"])
        y = df["is_safe"]

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
        print("\n📌 Final Model Comparison:")
        print(results)

        os.makedirs("models", exist_ok=True)
        results.to_csv("models/model_results.csv", index=False)
        print("\n✅ Model results saved to models/model_results.csv")

    except MLProjectException as e:
        print(f"Error: {e}")
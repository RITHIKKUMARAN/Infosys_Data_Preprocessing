import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score, classification_report, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to Python path (optional, retained for flexibility)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

class ModelEvaluator:
    """
    Class for evaluating trained models with enhanced metrics and visualizations.
    """

    def __init__(self, model, X_test: pd.DataFrame, y_test: pd.Series):
        if not isinstance(X_test, pd.DataFrame) or not isinstance(y_test, pd.Series):
            raise ValueError("X_test must be a DataFrame and y_test a Series.")
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def evaluate(self):
        """
        Evaluate the model and return key metrics.
        """
        try:
            y_pred = self.model.predict(self.X_test)
            y_prob = self.model.predict_proba(self.X_test)[:, 1] if hasattr(self.model, "predict_proba") else None

            metrics = {
                "accuracy": accuracy_score(self.y_test, y_pred),
                "f1_score": f1_score(self.y_test, y_pred),
                "precision": precision_score(self.y_test, y_pred),
                "recall": recall_score(self.y_test, y_pred),
                "roc_auc": roc_auc_score(self.y_test, y_prob) if y_prob is not None else None
            }

            print("\n📊 Model Evaluation Metrics:")
            for metric, value in metrics.items():
                if value is not None:
                    print(f"{metric.replace('_', ' ').title()}: {value:.4f}")
                else:
                    print(f"{metric.replace('_', ' ').title()}: N/A")

            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred))

            return metrics

        except Exception as e:
            raise MLProjectException(
                error_message="Error during model evaluation",
                error_detail=e
            )

    def plot_confusion_matrix(self, save_path=None):
        """
        Plot and optionally save the confusion matrix.
        """
        try:
            y_pred = self.model.predict(self.X_test)
            cm = confusion_matrix(self.y_test, y_pred)
            plt.figure(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            plt.title("Confusion Matrix")
            if save_path:
                plt.savefig(save_path)
                print(f"✅ Confusion matrix saved to {save_path}")
            else:
                plt.show()
            plt.close()
        except Exception as e:
            raise MLProjectException(
                error_message="Error plotting confusion matrix",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        file_path = "processed_data.csv"
        df = pd.read_csv(file_path)
        X = df.drop(columns=["is_safe"])
        y = df["is_safe"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_test, y_test)
        metrics = evaluator.evaluate()
        evaluator.plot_confusion_matrix(save_path="models/confusion_matrix.png")

    except MLProjectException as e:
        print(f"Error: {e}")
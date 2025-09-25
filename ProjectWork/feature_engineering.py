import os
import sys
import numpy as np
import pandas as pd

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

class FeatureEngineering:
    """
    Class for creating engineered features with improved robustness.
    """

    def __init__(self, data: pd.DataFrame, target_col="is_safe"):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        self.data = data
        self.target_col = target_col
        self.thresholds = {
            "aluminium": 2.8,
            "ammonia": 32.5,
            "arsenic": 0.01,
            "barium": 2,
            "cadmium": 0.005,
            "chloramine": 4,
            "chromium": 0.1,
            "copper": 1.3,
            "fluoride": 1.5,
            "bacteria": 0,
            "viruses": 0,
            "lead": 0.015,
            "nitrates": 10,
            "nitrites": 1,
            "mercury": 0.002,
            "perchlorate": 56,
            "radium": 5,
            "selenium": 0.5,
            "silver": 0.1,
            "uranium": 0.3,
        }

    def danger_flags(self):
        """Create binary flags for threshold exceedance."""
        try:
            for col, th in self.thresholds.items():
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors="coerce")
                    self.data[f"{col}_high"] = (self.data[col] > th).astype(int)
            return self.data
        except Exception as e:
            raise MLProjectException("Error in danger_flags", e)

    def danger_count(self):
        """Count number of chemicals exceeding safe thresholds."""
        try:
            danger_flags = [f"{col}_high" for col in self.thresholds.keys() if f"{col}_high" in self.data.columns]
            if danger_flags:
                self.data["danger_count"] = self.data[danger_flags].sum(axis=1)
            return self.data
        except Exception as e:
            raise MLProjectException("Error in danger_count", e)

    def ratio_features(self):
        """Create ratio-based features with safe division."""
        try:
            if "nitrates" in self.data.columns and "nitrites" in self.data.columns:
                self.data["nitrate_nitrite_ratio"] = np.where(
                    self.data["nitrites"] > 0,
                    self.data["nitrates"] / self.data["nitrites"],
                    0,
                )
            if "copper" in self.data.columns and "lead" in self.data.columns:
                self.data["copper_lead_ratio"] = np.where(
                    self.data["lead"] > 0,
                    self.data["copper"] / self.data["lead"],
                    0,
                )
            return self.data
        except Exception as e:
            raise MLProjectException("Error in ratio_features", e)

    def interaction_features(self):
        """Create interaction-based features."""
        try:
            if "bacteria" in self.data.columns and "viruses" in self.data.columns:
                self.data["bacteria_viruses"] = self.data["bacteria"] * self.data["viruses"]
            if "arsenic" in self.data.columns and "mercury" in self.data.columns:
                self.data["arsenic_mercury"] = self.data["arsenic"] * self.data["mercury"]
            return self.data
        except Exception as e:
            raise MLProjectException("Error in interaction_features", e)

    def engineer_features(self, save_path=None):
        """
        Run full feature engineering pipeline.
        """
        try:
            self.data = self.danger_flags()
            self.data = self.danger_count()
            self.data = self.ratio_features()
            self.data = self.interaction_features()

            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                self.data.to_csv(save_path, index=False)
                print(f"✅ Processed data saved to: {save_path}")

            print(f"✅ Feature engineering complete. Final shape: {self.data.shape}")
            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error in feature engineering pipeline",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        file_path = "project_data.csv"
        df = pd.read_csv(file_path)
        fe = FeatureEngineering(df)
        final_data = fe.engineer_features(save_path="data/pre_proceesed_data/processed_data.csv")
        print("\n🔹 Engineered Data Sample:")
        print(final_data.head())
    except MLProjectException as e:
        print(f"Error: {e}")
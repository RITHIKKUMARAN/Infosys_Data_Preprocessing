import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

class FeatureScaler:
    """
    Class for scaling numerical features using StandardScaler or MinMaxScaler.
    """

    def __init__(self, data: pd.DataFrame, target_col="is_safe", scaler_type="standard"):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        self.data = data
        self.target_col = target_col
        self.scaler_type = scaler_type
        self.scaler = None

    def scale_features(self, save_path=None):
        """
        Scale numerical features excluding the target.
        """
        try:
            if self.target_col in self.data.columns:
                X = self.data.drop(columns=[self.target_col])
                y = self.data[self.target_col]
            else:
                X = self.data
                y = None

            numeric_cols = X.select_dtypes(include=["float64", "int64"]).columns
            if not numeric_cols.empty:
                if self.scaler_type == "standard":
                    self.scaler = StandardScaler()
                elif self.scaler_type == "minmax":
                    self.scaler = MinMaxScaler()
                else:
                    raise ValueError("Invalid scaler_type. Choose 'standard' or 'minmax'.")

                X[numeric_cols] = self.scaler.fit_transform(X[numeric_cols])
            else:
                print("⚠️ No numerical columns to scale.")

            scaled_data = pd.concat([X, y], axis=1) if y is not None else X

            if save_path:
                scaled_data.to_csv(save_path, index=False)
                print(f"✅ Scaled data saved to {save_path}")

            return scaled_data

        except Exception as e:
            raise MLProjectException(
                error_message="Error during feature scaling",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        file_path = "data/pre_proceesed_data/processed_data.csv"
        df = pd.read_csv(file_path)
        scaler = FeatureScaler(df, scaler_type="standard")
        scaled_df = scaler.scale_features(save_path="data/pre_proceesed_data/scaled_data.csv")
        print("\n✅ Scaled Data Sample:")
        print(scaled_df.head())
    except MLProjectException as e:
        print(f"Error: {e}")
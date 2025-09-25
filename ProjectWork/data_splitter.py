import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import SMOTE

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

class DataSplitter:
    """
    Handles splitting dataset into train/test sets and balancing classes.
    Improved with input validation and configurable resampling.
    """

    def __init__(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
        if not isinstance(X, pd.DataFrame) or not isinstance(y, pd.Series):
            raise ValueError("X must be a DataFrame and y a Series.")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of rows.")
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state

    def split_and_resample(self, use_smoteenn=True, k_neighbors=1):
        """
        Split into train/test and apply resampling.
        - use_smoteenn=True → use SMOTEENN (resample + clean).
        - use_smoteenn=False → use SMOTE.
        """
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y,
                test_size=self.test_size,
                random_state=self.random_state,
                stratify=self.y
            )

            # Resample training set
            if use_smoteenn:
                smt = SMOTEENN(smote=SMOTE(k_neighbors=k_neighbors, random_state=self.random_state),
                               random_state=self.random_state)
            else:
                smt = SMOTE(k_neighbors=k_neighbors, random_state=self.random_state)

            X_train_res, y_train_res = smt.fit_resample(X_train, y_train)

            print("✅ Data splitting and resampling complete.")
            print("🔹 Original Train Class Distribution:", dict(y_train.value_counts()))
            print("🔹 Resampled Train Class Distribution:", dict(pd.Series(y_train_res).value_counts()))
            print(f"🔹 Shapes: X_train_res: {X_train_res.shape}, X_test: {X_test.shape}")

            return X_train_res, X_test, y_train_res, y_test

        except Exception as e:
            raise MLProjectException(
                error_message="Error during data splitting and resampling",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        file_path = "data/pre_proceesed_data/processed_data.csv"
        df = pd.read_csv(file_path)
        X = df.drop(columns=["is_safe"])
        y = df["is_safe"]
        splitter = DataSplitter(X, y)
        X_train_res, X_test, y_train_res, y_test = splitter.split_and_resample()
    except MLProjectException as e:
        print(f"Error: {e}")
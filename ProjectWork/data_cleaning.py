import os
import sys
import pandas as pd

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException
from data_ingestion import DataIngestion

class DataCleaning:
    """
    Class to clean and preprocess raw data with improved missing value handling and logging.
    """

    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        self.data = data

    def convert_to_numeric(self):
        """
        Convert specific columns to numeric types.
        """
        try:
            numeric_cols = ["ammonia", "is_safe"]
            for col in numeric_cols:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors="coerce")
            self.data = self.data.dropna(subset=["is_safe"])
            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error converting columns to numeric",
                error_detail=e
            )

    def handle_missing_values(self):
        """
        Handle missing values with mean for numeric and mode for categorical.
        """
        try:
            features_with_na = [f for f in self.data.columns if self.data[f].isnull().sum() > 0]
            for feature in features_with_na:
                missing_pct = round(self.data[feature].isnull().mean() * 100, 2)
                print(f"⚠️ {feature}: {missing_pct}% missing values")
                if missing_pct > 50:
                    print(f"Warning: High missing values in {feature}. Consider dropping.")

            for col in self.data.columns:
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    self.data[col].fillna(self.data[col].mean(), inplace=True)
                elif pd.api.types.is_object_dtype(self.data[col]):
                    self.data[col].fillna(self.data[col].mode()[0], inplace=True)

            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error while handling missing values",
                error_detail=e
            )

    def encode_categorical(self):
        """
        Convert categorical variables to dummy variables.
        """
        try:
            self.data = pd.get_dummies(self.data, drop_first=True, dummy_na=False)
            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error encoding categorical variables",
                error_detail=e
            )

    def clean_target(self):
        """
        Ensure target column 'is_safe' contains only binary values (0,1).
        """
        try:
            if "is_safe" in self.data.columns:
                self.data["is_safe"] = pd.to_numeric(self.data["is_safe"], errors="coerce")
                self.data = self.data[self.data["is_safe"].isin([0, 1])]
                print(f"✅ Target cleaned. Rows after cleaning: {self.data.shape[0]}")
            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error cleaning target column",
                error_detail=e
            )

    def clean_data(self):
        """
        Full cleaning pipeline.
        """
        try:
            print("Starting data cleaning...")
            self.data = self.data.drop_duplicates()
            self.data = self.convert_to_numeric()
            self.data = self.clean_target()
            self.data = self.handle_missing_values()
            self.data = self.encode_categorical()
            print(f"✅ Data cleaning complete. Final shape: {self.data.shape}")
            return self.data
        except Exception as e:
            raise MLProjectException(
                error_message="Error in clean_data pipeline",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        file_path = "project_data.csv"
        data = DataIngestion(file_path).load_data()
        print("🔹 Raw Data Sample:")
        print(data.head())

        cleaner = DataCleaning(data)
        cleaned_data = cleaner.clean_data()
        print("\n✅ Cleaned Data Sample:")
        print(cleaned_data.head())
        cleaned_data.to_csv("data/pre_proceesed_data/cleaned_data.csv", index=False)
        print("✅ Cleaned data saved to data/pre_proceesed_data/cleaned_data.csv")

    except MLProjectException as e:
        print(f"Error: {e}")
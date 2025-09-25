import sys
import pandas as pd
import os

# Add project root (optional)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from exception.execptions import MLProjectException

class DataIngestion:
    """
    Class to handle data ingestion for ML project.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self):
        """
        Load dataset from CSV file.
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")
            data = pd.read_csv(self.file_path)
            print(f"✅ Data loaded from {self.file_path}. Shape: {data.shape}")
            return data
        except Exception as e:
            raise MLProjectException(
                error_message="Error while loading data in DataIngestion",
                error_detail=e
            )

if __name__ == "__main__":
    try:
        file_path = "project_data.csv"
        ingestion = DataIngestion(file_path)
        df = ingestion.load_data()
        print("🔹 Data Sample:")
        print(df.head())
    except MLProjectException as e:
        print(f"Error: {e}")
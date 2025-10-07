import requests
from typing import Literal

class ExtractiveSummarizer:
    """
    Extractive summarization using Hugging Face API with BART model.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def summarize(self, text: str, length: Literal['short', 'medium', 'long']='medium') -> str:
        """
        Summarize text extractively using BART.

        Args:
            text (str): Input text.
            length (str): 'short', 'medium', 'long' controlling summary length.

        Returns:
            str: Summary of the input text.
        """
        length_map = {
            'short': {"max_length": 60, "min_length": 30},
            'medium': {"max_length": 130, "min_length": 60},
            'long': {"max_length": 200, "min_length": 130}
        }
        params = length_map.get(length, length_map['medium'])
        payload = {
            "inputs": text,
            "parameters": {**params, "do_sample": False, "num_beams": 4}
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', 'No summary generated')
                return str(result)
            else:
                return f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

import requests
from typing import Literal

class AbstractiveSummarizer:
    """
    Abstractive summarization and paraphrasing using Hugging Face API.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.summarize_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.paraphrase_url = "https://api-inference.huggingface.co/models/Vamsi/T5_Paraphrase_Paws"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def summarize(self, text: str, length: Literal['short', 'medium', 'long']='medium') -> str:
        """
        Abstractive summarization using BART.

        Args:
            text (str): Input text.
            length (str): 'short', 'medium', or 'long'.

        Returns:
            str: Summarized text.
        """
        length_map = {
            'short': {"max_length": 60, "min_length": 30},
            'medium': {"max_length": 130, "min_length": 60},
            'long': {"max_length": 200, "min_length": 130}
        }
        params = length_map.get(length, length_map['medium'])
        payload = {"inputs": text, "parameters": {**params, "do_sample": False, "early_stopping": True}}

        try:
            response = requests.post(self.summarize_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', 'No summary generated')
                return str(result)
            else:
                return f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def paraphrase(self, text: str) -> str:
        """
        Paraphrase text using T5 model.

        Args:
            text (str): Input text.

        Returns:
            str: Paraphrased text.
        """
        payload = {
            "inputs": f"paraphrase: {text}",
            "parameters": {"max_length": 256, "num_beams": 5, "num_return_sequences": 1, "temperature": 1.5}
        }
        try:
            response = requests.post(self.paraphrase_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', 'No paraphrase generated')
                return str(result)
            else:
                return f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def _build_session(retries=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(['GET', 'POST'])
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session


class ExtractiveSummarizer:
    def __init__(self, api_key, timeout=20):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.session = _build_session()
        self.timeout = timeout

    def summarize(self, text, length='medium'):
        """
        Extractive-style summarization using Hugging Face API
        """
        length_map = {
            'short': {"max_length": 60, "min_length": 30},
            'medium': {"max_length": 130, "min_length": 60},
            'long': {"max_length": 200, "min_length": 130}
        }

        params = length_map.get(length, length_map['medium'])

        payload = {
            "inputs": text,
            "parameters": {
                **params,
                "do_sample": False,
                "num_beams": 4
            }
        }

        try:
            response = self.session.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', 'No summary generated')
                return str(result)
            else:
                return f"API Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error: {str(e)}"

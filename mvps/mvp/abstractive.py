import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def _build_session(retries=5, backoff_factor=1.0, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class AbstractiveSummarizer:
    def __init__(self, api_key, timeout=45):
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.session = _build_session()

        self.summarize_primary = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        self.summarize_fallback = "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
        self.paraphrase_primary = "https://api-inference.huggingface.co/models/tuner007/pegasus_paraphrase"
        self.paraphrase_fallback = "https://api-inference.huggingface.co/models/Vamsi/T5_Paraphrase_Paws"


    def _wait_for_model_ready(self, model_url, max_wait=180):
        start = time.time()
        while time.time() - start < max_wait:
            try:
                r = self.session.post(model_url, headers=self.headers, json={"inputs": "ping"}, timeout=10)
                if r.status_code == 200:
                    return True
                data = r.json()
                if isinstance(data, dict) and "loading" in str(data).lower():
                    print(f"[INFO] Model is loading... waiting 10 s more.")
                    time.sleep(10)
                else:
                    return True
            except Exception:
                time.sleep(10)
        return False

    def summarize(self, text, length="medium"):
        length_map = {
            "short": {"max_length": 60, "min_length": 30},
            "medium": {"max_length": 130, "min_length": 60},
            "long": {"max_length": 200, "min_length": 130},
        }
        params = length_map.get(length, length_map["medium"])
        payload = {"inputs": text, "parameters": {**params, "do_sample": False, "early_stopping": True}}

        for model_url in [self.summarize_primary, self.summarize_fallback]:
            print(f"[INFO] Trying summarization model → {model_url}")
            ready = self._wait_for_model_ready(model_url)
            if not ready:
                print(f"[WARN] Model {model_url} never became ready.")
                continue
            try:
                r = self.session.post(model_url, headers=self.headers, json=payload, timeout=self.timeout)
                if r.status_code == 200:
                    res = r.json()
                    if isinstance(res, list) and res:
                        return res[0].get("summary_text", "No summary generated.")
                    return str(res)
                print(f"[WARN] Status {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ReadTimeout:
                print("[WARN] Read timeout, switching to fallback model.")
                continue
        return "Timeout: Both summarization models failed."

    def paraphrase(self, text):
        payload = {
            "inputs": f"paraphrase: {text}",
            "parameters": {"max_length": 256, "num_beams": 5, "num_return_sequences": 1, "temperature": 1.5},
        }

        for model_url in [self.paraphrase_primary, self.paraphrase_fallback]:
            print(f"[INFO] Trying paraphrase model → {model_url}")
            ready = self._wait_for_model_ready(model_url)
            if not ready:
                continue
            try:
                r = self.session.post(model_url, headers=self.headers, json=payload, timeout=self.timeout)
                if r.status_code == 200:
                    res = r.json()
                    if isinstance(res, list) and res:
                        return res[0].get("generated_text", "No paraphrase generated.")
                    return str(res)
                print(f"[WARN] Status {r.status_code}: {r.text[:200]}")
            except requests.exceptions.ReadTimeout:
                print("[WARN] Read timeout; trying fallback.")
                continue
        return "Timeout: Both paraphraser models failed."

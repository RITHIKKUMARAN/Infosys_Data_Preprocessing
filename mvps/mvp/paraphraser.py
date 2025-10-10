import time
import requests


class Paraphraser:
    """Paraphrasing using T5 model. Generates multiple reworded versions of input text.

    Model: ramsrigouthamg/t5_paraphraser
    """

    def __init__(self, api_key, timeout=30):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/tuner007/pegasus_paraphrase"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.timeout = timeout

    def _generate_paraphrases(self, text, num_return_sequences):
        """Internal helper to call Hugging Face API."""
        payload = {
            "inputs": f"paraphrase: {text}",
            "parameters": {
                "max_length": 256,
                "num_return_sequences": num_return_sequences,
                "num_beams": max(5, num_return_sequences),
                "temperature": 0.9,
                "top_p": 0.95,
                "do_sample": True
            }
        }

        # Retry logic for model loading
        for attempt in range(3):
            try:
                response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=self.timeout)
            except requests.exceptions.Timeout:
                # Let caller handle timeout messaging
                raise
            except Exception as e:
                return [f"❌ Error calling paraphrase API: {str(e)}"]

            if response.status_code == 503:
                # Model is loading on the HF side; wait and retry
                if attempt < 2:
                    time.sleep(20)
                    continue
                else:
                    return ["⚠️ Model still loading. Please try again later."]

            if response.status_code == 200:
                try:
                    results = response.json()
                except Exception:
                    return ["⚠️ Received invalid JSON from API."]

                if isinstance(results, list) and len(results) > 0:
                    paraphrases = []
                    for r in results:
                        # Common fields: 'generated_text', 'summary_text', or plain string
                        if isinstance(r, dict):
                            val = r.get('generated_text') or r.get('summary_text') or ''
                        else:
                            val = str(r)
                        val = val.strip()
                        if val:
                            paraphrases.append(val)

                    return paraphrases if paraphrases else ["⚠️ No paraphrase generated."]

                # Unexpected response shape
                return ["⚠️ No paraphrase generated."]

            # Non-200 and non-503 responses
            return [f"❌ API Error: {response.status_code} - {response.text}"]

        return ["⚠️ Model still loading. Please try again later."]

    def paraphrase(self, text, num_return_sequences=3):
        """
        Generate multiple paraphrased versions of input text.
        Returns a list of strings or a single-element list containing an error message.
        """
        if not isinstance(text, str) or not text.strip():
            return ["⚠️ Input text is empty! Please provide valid content."]

        num_return_sequences = min(max(1, int(num_return_sequences)), 5)

        try:
            return self._generate_paraphrases(text, num_return_sequences)
        except requests.exceptions.Timeout:
            return ["❌ Request timeout. Please try again."]
        except Exception as e:
            return [f"❌ Error: {str(e)}"]


if __name__ == "__main__":
    # Quick local test (requires HF_API_KEY in env)
    import os
    from dotenv import load_dotenv

    load_dotenv()
    HF_API_KEY = os.getenv("HF_API_KEY")
    if not HF_API_KEY:
        print("⚠️ Please set HF_API_KEY in your .env file")
    else:
        p = Paraphraser(HF_API_KEY)
        text = "Machine learning is changing the world rapidly."
        print("\n✨ Input:", text)
        print("\n🔁 Paraphrased Versions:\n")
        results = p.paraphrase(text, num_return_sequences=3)
        for idx, r in enumerate(results, 1):
            print(f"{idx}. {r}")

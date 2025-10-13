import os
import requests
from dotenv import load_dotenv


class Paraphraser:
    """
    Paraphrasing using Groq Cloud's LLaMA 3.1 models.
    Models:
      - llama-3.1-8b-instant  (fast, good quality)
      - llama-3.1-70b-versatile (higher quality, slower)
    """

    def __init__(self, api_key=None, model_name="llama-3.1-8b-instant"):
        load_dotenv()

        # ✅ Support both manual and env-based API key
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env")

        # ✅ Correct REST endpoint (no '/openai/')
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model_name = model_name

    def paraphrase(self, text, num_return_sequences=3):
        """
        Generate paraphrased versions of input text using Groq Cloud API.
        """
        if not text.strip():
            return ["⚠️ Please provide valid text."]

        prompt = (
            f"Paraphrase the following text into {num_return_sequences} distinct, natural, "
            f"and fluent English variations:\n\n{text}"
        )

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI that paraphrases text clearly and naturally."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 400
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                text_response = data["choices"][0]["message"]["content"]
                # Split into distinct paraphrases
                lines = [line.strip() for line in text_response.split("\n") if line.strip()]
                return lines[:num_return_sequences]
            else:
                return [f"❌ API Error {response.status_code}: {response.text}"]

        except Exception as e:
            return [f"❌ Error: {str(e)}"]


if __name__ == "__main__":
    paraphraser = Paraphraser(model_name="llama-3.1-8b-instant")
    text = "Machine learning is changing the world rapidly."

    print(f"\n✨ Input: {text}")
    print(f"🤖 Using Model: {paraphraser.model_name}\n")

    results = paraphraser.paraphrase(text, num_return_sequences=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")

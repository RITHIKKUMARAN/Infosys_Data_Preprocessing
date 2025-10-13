from mvp.extractive import ExtractiveSummarizer
from mvp.abstractive import AbstractiveSummarizer
from mvp.paraphraser import Paraphraser
import os
from dotenv import load_dotenv

class SummarizationPipeline:
    """ Combined pipeline for Summarization (Hugging Face) + Paraphrasing (GROQ LLaMA 3.1). """

    def __init__(self):
        print("🔧 Initializing Summarization + Paraphrasing Pipeline...")
        load_dotenv()

        hf_api_key = os.getenv("HF_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")

        try:
            self.extractive = ExtractiveSummarizer(hf_api_key)
            print("✅ Extractive Summarizer loaded")
        except Exception as e:
            print(f"⚠️ Warning: Extractive Summarizer failed: {e}")
            self.extractive = None

       
        try:
            self.abstractive = AbstractiveSummarizer(hf_api_key)
            print("✅ Abstractive Summarizer loaded")
        except Exception as e:
            print(f"⚠️ Warning: Abstractive Summarizer failed: {e}")
            self.abstractive = None

        # --- GROQ Paraphraser ---
        try:
            self.paraphraser = Paraphraser(groq_api_key)
            print("✅ GROQ Paraphraser loaded")
        except Exception as e:
            print(f"⚠️ Warning: GROQ Paraphraser failed: {e}")
            self.paraphraser = None

        print("✨ SummarizationPipeline initialized successfully!\n")


    def summarize(self, text, method="abstractive", length="medium"):
        if not text or not text.strip():
            return "⚠️ No text provided."
        try:
            if method == "extractive":
                if self.extractive is None:
                    return "❌ Extractive Summarizer unavailable."
                return self.extractive.summarize(text, length)
            else:
                if self.abstractive is None:
                    return "❌ Abstractive Summarizer unavailable."
                return self.abstractive.summarize(text, length)
        except Exception as e:
            return f"❌ Error during summarization: {e}"

    # -------- Paraphrasing (GROQ) --------
    def paraphrase(self, text, num_return_sequences=3):
        if not text or not text.strip():
            return "⚠️ Please provide valid text."
        if self.paraphraser is None:
            return "❌ Paraphraser unavailable (GROQ not configured)."
        try:
            results = self.paraphraser.paraphrase(text, num_return_sequences)
            return "\n\n".join(results)
        except Exception as e:
            return f"❌ Error in paraphrasing: {e}"

  
    def get_status(self):
        return {
            "extractive": self.extractive is not None,
            "abstractive": self.abstractive is not None,
            "groq_paraphraser": self.paraphraser is not None,
        }

if __name__ == "__main__":
    print("🚀 Running Summarization + GROQ Paraphrasing Test...\n")
    pipeline = SummarizationPipeline()

    text = """
    Artificial Intelligence (AI) is transforming industries by automating repetitive tasks,
    improving efficiency, and enabling better decision-making across sectors such as healthcare,
    finance, and transportation.
    """

    # Abstractive Summary
    print("\n🧠 Abstractive Summary:\n", pipeline.summarize(text, method="abstractive"))

    # Extractive Summary
    print("\n📄 Extractive Summary:\n", pipeline.summarize(text, method="extractive"))

    # GROQ Paraphrasing
    print("\n✨ GROQ Paraphrasing Results:\n",
          pipeline.paraphrase("AI is transforming the world rapidly.", 3))

    # Status
    print("\n🔍 Module Status:\n", pipeline.get_status())

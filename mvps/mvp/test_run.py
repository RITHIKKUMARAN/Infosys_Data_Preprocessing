import os
import sys
from dotenv import load_dotenv

# Make sure project root (parent of this folder) is on sys.path so
# `mvps` can be imported as a package and its relative imports work.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the pipeline from the local `mvps` package
from mvps.mvp_pipeline import SummarizationPipeline

# Load environment variables
load_dotenv()

api_key = os.getenv("HF_API_KEY")

if not api_key:
    print("⚠️ Please set your HF_API_KEY in .env file")
else:
    summarizer = SummarizationPipeline(api_key)

    text = """Machine learning is a subset of artificial intelligence that enables systems 
    to learn and improve from experience without being explicitly programmed."""

    print("=== Abstractive Summary ===")
    print(summarizer.summarize(text, method='abstractive', length='short'))

    print("\n=== Extractive Summary ===")
    print(summarizer.summarize(text, method='extractive', length='short'))

    print("\n=== Paraphrase ===")
    print(summarizer.paraphrase(text))

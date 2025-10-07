from pipeline import SummarizationPipeline

api_key = "YOUR_HUGGINGFACE_API_KEY"
pipeline = SummarizationPipeline(api_key)

text = "Artificial Intelligence is transforming industries by enabling automation and decision-making."

# Extractive summary
extractive_summary = pipeline.summarize(text, method='extractive')
print("Extractive Summary:", extractive_summary)

# Abstractive summary
abstractive_summary = pipeline.summarize(text, method='abstractive')
print("Abstractive Summary:", abstractive_summary)

# Paraphrased text
paraphrased_text = pipeline.paraphrase(text)
print("Paraphrase:", paraphrased_text)

from .extractive import ExtractiveSummarizer
from .abstractive import AbstractiveSummarizer
from .paraphraser import Paraphraser

class SummarizationPipeline:
    def __init__(self, api_key):
        self.extractive = ExtractiveSummarizer(api_key)
        self.abstractive = AbstractiveSummarizer(api_key)
        self.paraphraser = Paraphraser(api_key)

    def summarize(self, text, method='abstractive', length='medium'):
        """
        Summarize text using specified method

        Args:
            text (str): Input text to summarize
            method (str): 'extractive' or 'abstractive'
            length (str): 'short', 'medium', or 'long'

        Returns:
            str: Summarized text
        """
        if method == 'extractive':
            return self.extractive.summarize(text, length)
        else:
            return self.abstractive.summarize(text, length)

    def paraphrase(self, text):
        """Paraphrase the given text"""
        return self.abstractive.paraphrase(text)

    def paraphrase_many(self, text, num_return_sequences=3):
        """Return multiple paraphrased versions as a list of strings."""
        return self.paraphraser.paraphrase(text, num_return_sequences=num_return_sequences)

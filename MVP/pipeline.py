from .extractive import ExtractiveSummarizer
from .abstractive import AbstractiveSummarizer

class SummarizationPipeline:
    """
    Unified pipeline for extractive and abstractive summarization, and paraphrasing.
    """
    def __init__(self, api_key: str):
        self.extractive = ExtractiveSummarizer(api_key)
        self.abstractive = AbstractiveSummarizer(api_key)

    def summarize(self, text: str, method: str='abstractive', length: str='medium') -> str:
        """
        Summarize text using specified method.

        Args:
            text (str): Input text.
            method (str): 'extractive' or 'abstractive'.
            length (str): 'short', 'medium', or 'long'.

        Returns:
            str: Summarized text.
        """
        if method == 'extractive':
            return self.extractive.summarize(text, length)
        else:
            return self.abstractive.summarize(text, length)

    def paraphrase(self, text: str) -> str:
        """
        Paraphrase the input text.

        Args:
            text (str): Input text.

        Returns:
            str: Paraphrased text.
        """
        return self.abstractive.paraphrase(text)

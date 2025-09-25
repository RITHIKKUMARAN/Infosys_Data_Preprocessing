class MLProjectException(Exception):
    """
    Custom exception class for ML project errors.
    """
    def __init__(self, error_message: str, error_detail: Exception):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        return f"{self.error_message}: {self.error_detail}"
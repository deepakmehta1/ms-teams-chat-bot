class KeyManager:
    """
    A class to manage the OpenAI API key, loading it from the environment or a config file.
    """

    def __init__(self, config):
        self.api_key = self._load_api_key(config)

    def _load_api_key(self, config):
        api_key = config.OPENAI_API_KEY
        if not api_key:
            raise ValueError(
                "API key not found. Please set OPENAI_API_KEY the environment variable."
            )
        return api_key

    def get_api_key(self):
        """
        Return the OpenAI API key.
        """
        return self.api_key

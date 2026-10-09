from .base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self, model: str, temperature: float = 0.0):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        """
        TODO: connect to the approved Gemini interface.
        Return the raw response unchanged.
        Never repair, retry, or post-process silently here.
        """
        raise NotImplementedError("Implement after model/API settings are frozen.")

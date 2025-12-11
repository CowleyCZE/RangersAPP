"""Vlastní výjimky aplikace"""


class GDForgeException(Exception):
    """Základní výjimka aplikace"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMException(GDForgeException):
    """Výjimka související s LLM komunikací"""
    def __init__(self, message: str, provider: str = "unknown"):
        super().__init__(f"LLM Error ({provider}): {message}", 503)
        self.provider = provider


class GenerationException(GDForgeException):
    """Výjimka při generování kódu"""
    def __init__(self, message: str):
        super().__init__(f"Generation Error: {message}", 500)


class ValidationException(GDForgeException):
    """Výjimka při validaci vstupu"""
    def __init__(self, message: str):
        super().__init__(f"Validation Error: {message}", 400)

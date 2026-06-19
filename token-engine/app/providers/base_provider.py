"""
Abstract interface for LLM providers.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    """
    Generate a response using a specific provider.
    """

    @abstractmethod
    def generate_response(
        self,
        task: str,
        context: str,
        strategy: str
    ) -> str:
        pass
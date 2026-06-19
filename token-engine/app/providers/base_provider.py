from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        task: str,
        context: str,
        strategy: str
    ) -> str:
        pass
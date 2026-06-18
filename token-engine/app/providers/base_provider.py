from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        task,
        context
    ):
        pass
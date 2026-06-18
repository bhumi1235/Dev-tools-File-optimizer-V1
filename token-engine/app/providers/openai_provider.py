from app.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def generate_response(
        self,
        task,
        context
    ):

        raise NotImplementedError(
            "OpenAI provider not implemented yet."
        )
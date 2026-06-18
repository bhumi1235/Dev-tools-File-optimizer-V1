from app.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def generate_response(
        self,
        task,
        context
    ):

        raise NotImplementedError(
            "Gemini provider not implemented yet."
        )
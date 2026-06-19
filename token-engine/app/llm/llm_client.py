from app.providers.groq_provider import GroqProvider


provider = GroqProvider()


def generate_response(
    task: str,
    context: str,
    strategy: str
) -> str:

    return provider.generate_response(
        task,
        context,
        strategy
    )
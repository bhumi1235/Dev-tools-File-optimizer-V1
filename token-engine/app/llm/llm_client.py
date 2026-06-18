from app.providers.groq_provider import GroqProvider


provider = GroqProvider()


def generate_response(
    task,
    context,
    strategy
):

    return provider.generate_response(
        task,
        context,
        strategy
    )
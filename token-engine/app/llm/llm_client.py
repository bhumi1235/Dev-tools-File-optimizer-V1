from app.providers.groq_provider import GroqProvider

def generate_response(
    task: str,
    context: str,
    strategy: str
) -> str:
    
    provider = GroqProvider()

    return provider.generate_response(
        task,
        context,
        strategy
    )
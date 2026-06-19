from app.providers.groq_provider import GroqProvider


def test_provider_initializes():

    provider = GroqProvider()

    assert provider is not None
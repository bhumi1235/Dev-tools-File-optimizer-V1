from app.chunking.chunker import chunk_text


def test_chunk_text_returns_chunks():

    sample = """
Authentication Flow

The login service validates user credentials.
JWT tokens are generated after successful verification.
"""

    chunks = chunk_text(
        sample
    )

    assert isinstance(
        chunks,
        list
    )

    assert len(
        chunks
    ) > 0
from app.chunking.markdown_chunker import chunk_markdown


def test_markdown_chunker_returns_chunks():

    sample = """
# Authentication

JWT tokens are used for stateless authentication.

## Passwords

Passwords are hashed using bcrypt.
"""

    chunks = chunk_markdown(
        sample
    )

    assert isinstance(
        chunks,
        list
    )

    assert len(
        chunks
    ) > 0
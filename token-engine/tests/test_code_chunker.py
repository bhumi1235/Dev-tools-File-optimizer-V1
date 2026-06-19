from app.chunking.code_chunker import chunk_python_code


def test_code_chunker_returns_chunks():

    sample = """
def authenticate():

    return True


class User:

    pass
"""

    chunks = chunk_python_code(
        sample
    )

    assert isinstance(
        chunks,
        list
    )

    assert len(
        chunks
    ) > 0
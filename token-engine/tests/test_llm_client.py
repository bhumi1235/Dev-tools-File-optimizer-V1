from app.llm.llm_client import generate_response


def test_generate_response_exists():

    assert callable(
        generate_response
    )
from app.llm.llm_client import generate_response


context = """
JWT tokens are used to maintain stateless authentication.

Passwords should be hashed using bcrypt before storage.
"""

instruction = "How should passwords be stored?"


response = generate_response(
    instruction,
    context
)

print(response)
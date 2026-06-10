from app.chunking.chunker import chunk_text


sample = """
Authentication Flow

The login service validates user credentials using email and password. After successful verification, a JWT token is generated and attached to the response. Middleware checks token validity on every protected route. Session expiration is handled through token expiry timestamps. Passwords are hashed using bcrypt before being stored in the database. Authentication failures return unauthorized responses and prevent access to protected resources.
"""


chunks = chunk_text(sample)

for i, chunk in enumerate(chunks):

    print()
    print("Chunk", i + 1)
    print(chunk)
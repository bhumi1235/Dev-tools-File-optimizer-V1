from app.chunking.markdown_chunker import chunk_markdown


sample = """
# Authentication Notes

## JWT

JWT tokens are used to maintain stateless authentication.

## Password Security

Passwords should be hashed using bcrypt before storage.

## Sessions

Middleware validates tokens on protected routes.

# Machine Learning

Neural networks learn through backpropagation.
"""


chunks = chunk_markdown(sample)

for i, chunk in enumerate(chunks):

    print()
    print(f"Chunk {i+1}")
    print(chunk)
from app.chunking.code_chunker import chunk_python_code


sample = """
class User:

    def __init__(self):
        pass


def authenticate():

    token = "abc"

    return token


def logout():

    return True
"""


chunks = chunk_python_code(
    sample
)

for i, chunk in enumerate(chunks):

    print()
    print("Chunk", i + 1)
    print(chunk)
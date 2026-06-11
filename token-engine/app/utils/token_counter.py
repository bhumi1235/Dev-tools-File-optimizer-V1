import re
import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):

    # Remove source tags
    text = re.sub(
        r'\[Source:.*?\]',
        '',
        text
    )

    # Normalize whitespace
    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return len(
        encoder.encode(text)
    )
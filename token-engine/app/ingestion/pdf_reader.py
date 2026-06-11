import fitz
import re


def read_pdf(file_path):

    text = ""

    doc = fitz.open(file_path)

    for page in doc:

        text += page.get_text()

    doc.close()

    # remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # normalize line breaks
    text = re.sub(r"\n{2,}", "\n\n", text)

    # repair words split across lines
    text = text.replace("-\n", "")

    # replace single line breaks inside sentences with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    return text.strip()
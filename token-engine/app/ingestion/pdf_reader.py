import fitz


def read_pdf(file_path):

    text = ""

    doc = fitz.open(file_path)

    for page in doc:

        text += page.get_text()

    return text
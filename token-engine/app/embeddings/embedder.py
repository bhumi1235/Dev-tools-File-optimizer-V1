from sentence_transformers import SentenceTransformer

from app.config import MODEL_NAME


model = None


def get_model():

    global model

    if model is None:

        model = SentenceTransformer(
            MODEL_NAME
        )

    return model


def embed_text(
    text: str
):

    model = get_model()

    return model.encode(
        text
    )
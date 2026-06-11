from dotenv import load_dotenv
import os

load_dotenv()

MAX_CHUNK_WORDS = int(
    os.getenv(
        "MAX_CHUNK_WORDS",
        35
    )
)

OVERLAP_SENTENCES = int(
    os.getenv(
        "OVERLAP_SENTENCES",
        1
    )
)

SIMILARITY_THRESHOLD = float(
    os.getenv(
        "SIMILARITY_THRESHOLD",
        0.9
    )
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "sentence-transformers/all-MiniLM-L6-v2"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)
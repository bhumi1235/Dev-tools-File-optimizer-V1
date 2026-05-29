# tests/test_embeddings.py

from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity

query = "authentication bug"

chunk1 = "login authentication routing middleware"
chunk2 = "machine learning lecture notes"

q = embed_text(query)

c1 = embed_text(chunk1)
c2 = embed_text(chunk2)

print("Auth:", cosine_similarity(q, c1))
print("ML:", cosine_similarity(q, c2))
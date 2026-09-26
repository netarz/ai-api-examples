"""Embeddings + a tiny semantic search, no vector database and no numpy.

Use one embedding model for both documents and queries; vectors from
different models cannot be compared.

Docs: https://netarz.ir/docs/ai/embeddings
"""
import math
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)
EMBEDDING_MODEL = "text-embedding-3-small"  # or text-embedding-3-large, gemini-embedding-001

DOCS = [
    "برای تحویل سفارش، یک بار احراز هویت لازم است.",
    "کش‌بک بعد از تکمیل سفارش حساب می‌شود.",
    "کلید API را فقط روی سرور نگه دارید.",
]


def embed(texts: list[str]) -> list[list[float]]:
    res = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [row.embedding for row in res.data]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


doc_vectors = embed(DOCS)  # embed documents once and store them in real code
question = "کلیدم را کجا بگذارم؟"
[query_vector] = embed([question])

ranked = sorted(zip(DOCS, doc_vectors), key=lambda pair: cosine(query_vector, pair[1]), reverse=True)
print("best match:", ranked[0][0])

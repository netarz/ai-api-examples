"""A small Persian RAG (retrieval-augmented generation) in plain Python.

1. Embed a handful of Persian passages once.
2. Embed the question and rank the passages by cosine similarity.
3. Send the best passages to a chat model and ask it to answer only from them.

No vector database and no numpy: fine for a few hundred passages. For more,
store the vectors in a real index (pgvector, Qdrant, ...) and keep the rest.

Run:
    pip install -r requirements.txt
    export NETARZ_API_KEY="sk-ntz-v1-..."
    python rag_persian.py "کلید را کجا نگه دارم؟"

Docs: https://netarz.ir/docs/ai/embeddings
"""
import math
import os
import sys

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)

# For Persian, text-embedding-3-large and the Gemini embedding models do better
# than text-embedding-ada-002. Use the same model for passages and questions.
EMBEDDING_MODEL = os.getenv("NETARZ_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("NETARZ_MODEL", "gpt-4o-mini")
TOP_K = 2

PASSAGES = [
    "کلید دسترسی (API Key) را فقط روی سرور نگه دارید، نه در کد مرورگر یا اپ موبایل.",
    "پیش از هر درخواست، درگاه مبلغ بلندترین جواب ممکن را از اعتبار کنار می‌گذارد. با max_tokens این مبلغ کوچک می‌شود.",
    "درخواستی که پیش از تولید جواب با خطا تمام شود هزینه ندارد.",
    "مدل‌های Claude فقط با پیشوند openrouter/anthropic/ در دسترس‌اند.",
    "برای هر کلید می‌توانید سقف هزینه و برای هر پروژه بودجهٔ ماهانه بگذارید.",
    "فهرست مدل‌ها را بدون کلید از GET /models بگیرید.",
]


def embed(texts: list[str]) -> list[list[float]]:
    res = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [row.embedding for row in sorted(res.data, key=lambda row: row.index)]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def retrieve(question: str, passages: list[str], vectors: list[list[float]], k: int) -> list[tuple[float, str]]:
    [q] = embed([question])
    scored = [(cosine(q, v), p) for p, v in zip(passages, vectors)]
    return sorted(scored, reverse=True)[:k]


question = sys.argv[1] if len(sys.argv) > 1 else "چطور جلوی خرج شدن کل اعتبار را بگیرم؟"

passage_vectors = embed(PASSAGES)  # in real code, embed once and store the vectors
hits = retrieve(question, PASSAGES, passage_vectors, TOP_K)

print("retrieved:")
for score, passage in hits:
    print(f"  {score:.3f}  {passage}")

context = "\n".join(f"- {passage}" for _, passage in hits)
answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "فقط با تکیه بر متن‌های زیر به فارسی جواب بدهید. "
                "اگر جواب در متن‌ها نیست، بگویید نمی‌دانید.\n\n" + context
            ),
        },
        {"role": "user", "content": question},
    ],
    max_tokens=300,
)

print("\nanswer:")
print(answer.choices[0].message.content)

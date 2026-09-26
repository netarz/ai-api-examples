"""LangChain (Python) on the NetArz gateway: chat, a model swap, and a tiny RAG.

pip install -r requirements.txt
export NETARZ_API_KEY="sk-ntz-v1-..."
python chat_and_rag.py

Docs: https://netarz.ir/docs/ai/sdks
"""
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

BASE_URL = os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")
KEY = os.environ["NETARZ_API_KEY"]

llm = ChatOpenAI(base_url=BASE_URL, api_key=KEY, model="gpt-4o-mini", max_tokens=400, timeout=120)

# Swapping providers is just a different id (Claude needs the openrouter/ prefix).
claude = ChatOpenAI(base_url=BASE_URL, api_key=KEY, model="openrouter/anthropic/claude-haiku-4.5", max_tokens=400)

print(llm.invoke("در یک جمله بگویید LangChain به چه کاری می‌آید.").content)

# check_embedding_ctx_length=False sends raw text instead of OpenAI tiktoken ids,
# which keeps non-OpenAI embedding models (e.g. gemini-embedding-001) working too.
embeddings = OpenAIEmbeddings(
    base_url=BASE_URL,
    api_key=KEY,
    model="text-embedding-3-small",
    check_embedding_ctx_length=False,
)

store = InMemoryVectorStore.from_texts(
    [
        "برای تحویل سفارش، یک بار احراز هویت لازم است.",
        "کش‌بک بعد از تکمیل سفارش حساب می‌شود و پس از دورهٔ انتظار به کیف پول می‌آید.",
        "کلید API را فقط روی سرور نگه دارید، نه در اپ موبایل.",
    ],
    embedding=embeddings,
)
retriever = store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_messages([
    ("system", "فقط بر اساس این متن جواب بدهید و اگر جواب در متن نیست، بگویید نمی‌دانید:\n{context}"),
    ("human", "{question}"),
])

question = "کش‌بک کی به کیف پولم می‌آید؟"
context = "\n".join(doc.page_content for doc in retriever.invoke(question))
answer = (prompt | claude).invoke({"context": context, "question": question})
print(answer.content)

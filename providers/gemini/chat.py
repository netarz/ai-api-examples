"""Google Gemini through NetArz, with the OpenAI SDK.

Direct Gemini ids have no prefix (gemini-3.5-flash, gemini-3.1-flash-lite, ...).
The same models also exist on OpenRouter as openrouter/google/<id>.
Google's image models (Imagen) are not on the gateway; for images use an
OpenAI GPT Image model (../../python/images.py).

Page: https://netarz.ir/ai-api/gemini
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://netarz.ir/api/ai/v1",
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=120,
)

r = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[{"role": "user", "content": "یک توضیح دوخطی دربارهٔ فرق امبدینگ و مدل گفت‌وگو بنویسید."}],
    max_tokens=800,  # Gemini "thinking" tokens count toward the output
)
print(r.choices[0].message.content)

# Gemini embeddings on the same key.
emb = client.embeddings.create(model="gemini-embedding-001", input=["نرخ دلار", "قیمت یورو"])
print(len(emb.data), "vectors of", len(emb.data[0].embedding), "dimensions")

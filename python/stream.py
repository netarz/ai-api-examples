"""Streaming (Server-Sent Events) through the NetArz AI gateway.

The last chunk before [DONE] carries `usage`; you do not need to send
stream_options.include_usage, the gateway adds it for every provider.

Docs: https://netarz.ir/docs/ai/streaming
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=120,
)

stream = client.chat.completions.create(
    model=os.getenv("NETARZ_MODEL", "gpt-4o-mini"),
    messages=[{"role": "user", "content": "یک شعر کوتاه دربارهٔ پاییز بنویسید."}],
    stream=True,
    max_tokens=200,
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.usage:  # final event
        print(f"\n\ntokens: {chunk.usage.total_tokens}")

"""Basic chat completion through the NetArz AI gateway (OpenAI-compatible).

Run:
    pip install -r requirements.txt
    export NETARZ_API_KEY="sk-ntz-v1-..."
    python chat.py

Docs: https://netarz.ir/docs/ai/chat-completions
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)

# Any id from https://netarz.ir/ai-api/models works here, e.g.
# "openrouter/anthropic/claude-sonnet-4.5", "gemini-3.5-flash", "deepseek-flash".
MODEL = os.getenv("NETARZ_MODEL", "gpt-4o-mini")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید."},
        {"role": "user", "content": "برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید."},
    ],
    # Always send max_tokens: the gateway reserves credit for the largest
    # possible answer before the call, so a cap keeps that reservation small.
    max_tokens=200,
)

print(response.choices[0].message.content)
# response.id is the NetArz request id (same as the X-Request-Id header).
print(f"\nrequest id: {response.id} | tokens: {response.usage.total_tokens}")

"""Function calling (tools) through the NetArz AI gateway.

The same OpenAI-style `tools` array works for GPT, Gemini, DeepSeek and
Claude (via OpenRouter ids): the gateway translates it to each provider.

Docs: https://netarz.ir/docs/ai/chat-completions
"""
import json
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)
MODEL = os.getenv("NETARZ_MODEL", "gpt-4.1-mini")

# Your own function. Here it is a stub; in a real app it would query your DB.
def get_order_status(order_number: str) -> dict:
    return {"order_number": order_number, "status": "delivered", "delivered_at": "2026-08-29"}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "وضعیت یک سفارش را با شمارهٔ سفارش برمی‌گرداند.",
        "parameters": {
            "type": "object",
            "properties": {"order_number": {"type": "string"}},
            "required": ["order_number"],
        },
    },
}]

messages = [{"role": "user", "content": "سفارش NZ-10422 در چه وضعیتی است؟"}]

first = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, max_tokens=300)
reply = first.choices[0].message

if not reply.tool_calls:
    print(reply.content)
    raise SystemExit

messages.append(reply)
for call in reply.tool_calls:
    args = json.loads(call.function.arguments or "{}")
    result = get_order_status(**args) if call.function.name == "get_order_status" else {"error": "unknown tool"}
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps(result, ensure_ascii=False),
    })

final = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, max_tokens=300)
print(final.choices[0].message.content)

"""JSON output: `json_object` (any model with the json capability) and a strict
`json_schema` (use an OpenAI model for the schema form).

Docs: https://netarz.ir/docs/ai/chat-completions
"""
import json
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)

# 1) Free-form JSON object.
loose = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "فقط یک شیء JSON معتبر برگردانید."},
        {"role": "user", "content": "برای محصول «کفش دویدن» سه ویژگی کوتاه با کلید features بنویسید."},
    ],
    max_tokens=200,
)
print(json.loads(loose.choices[0].message.content))

# 2) Strict schema: the answer must match this shape exactly.
schema = {
    "name": "product_card",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "category": {"type": "string", "enum": ["gift_card", "subscription", "software", "other"]},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title", "category", "tags"],
        "additionalProperties": False,
    },
}

strict = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_schema", "json_schema": schema},
    messages=[
        {"role": "user", "content": "از این متن یک کارت محصول بسازید: «گیفت کارت ۵۰ دلاری اپل برای ریجن آمریکا»"},
    ],
    max_tokens=200,
)
card = json.loads(strict.choices[0].message.content)
print(card["title"], card["category"], card["tags"])

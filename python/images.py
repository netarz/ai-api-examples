"""Image generation with an OpenAI GPT Image model.

Every image model on the gateway is an OpenAI GPT Image model; they always
return base64 (`b64_json`), never a URL. Sizes and qualities per model are in
`capabilities` of GET /models?type=image.

Docs: https://netarz.ir/docs/ai/images
"""
import base64
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=180,
)

img = client.images.generate(
    model="gpt-image-1-mini",
    prompt="لوگوی مینیمال یک کافه با رنگ طلایی روی پس‌زمینهٔ ساده",
    size="1024x1024",   # 1024x1024 | 1024x1536 | 1536x1024
    quality="low",      # low | medium | high; higher quality = more output tokens = higher cost
    n=1,
)

with open("logo.png", "wb") as f:
    f.write(base64.b64decode(img.data[0].b64_json))
print("saved logo.png")

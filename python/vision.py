"""Ask a model about an image (vision input) through the NetArz AI gateway.

The image goes in the user message as an `image_url` part: either a public
https URL or a local file sent as a base64 data URL. Only models whose
`capabilities.vision` is true in GET /models accept images, and every image
costs input tokens, reported by the provider in `usage`.

Run:
    pip install -r requirements.txt
    export NETARZ_API_KEY="sk-ntz-v1-..."
    python vision.py                      # sample image from Wikimedia Commons
    python vision.py receipt.jpg          # a local file
    python vision.py https://example.com/photo.png

Docs: https://netarz.ir/docs/ai/chat-completions
"""
import base64
import mimetypes
import os
import sys

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
)

# Check capabilities.vision in https://netarz.ir/api/ai/v1/models?type=chat
MODEL = os.getenv("NETARZ_MODEL", "gpt-4o-mini")
SAMPLE = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"


def image_part(source: str) -> dict:
    """Build an image_url content part from a URL or a local file path."""
    if source.startswith(("http://", "https://", "data:")):
        url = source
    else:
        mime = mimetypes.guess_type(source)[0] or "image/jpeg"
        with open(source, "rb") as fh:
            url = f"data:{mime};base64,{base64.b64encode(fh.read()).decode('ascii')}"
    return {"type": "image_url", "image_url": {"url": url}}


source = sys.argv[1] if len(sys.argv) > 1 else SAMPLE

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "در این تصویر چه می‌بینید؟ در دو جمله بگویید."},
                image_part(source),
            ],
        }
    ],
    max_tokens=200,
)

print(response.choices[0].message.content)
print(f"\ninput tokens (text + image): {response.usage.prompt_tokens}")

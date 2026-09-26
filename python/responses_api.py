"""OpenAI Responses API through the gateway.

/responses is a pass-through for OpenAI models only. For Claude, Gemini,
DeepSeek and other OpenRouter ids use /chat/completions instead.
Pro and Codex models (for example gpt-5.4-pro, gpt-5.3-codex) answer only here.

The gateway drops `store`, so `previous_response_id` cannot be used:
send the whole conversation in `input` on every turn.

Docs: https://netarz.ir/docs/ai/responses-api
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=180,
)

response = client.responses.create(
    model=os.getenv("NETARZ_MODEL", "gpt-4.1-mini"),
    instructions="کوتاه و روشن جواب بدهید.",
    input="سه نکته برای نگه‌داری امن کلید API بنویسید.",
    max_output_tokens=300,  # keeps the credit reservation small, like max_tokens
)
print(response.output_text)

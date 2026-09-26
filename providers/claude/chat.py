"""Claude (Anthropic) through NetArz.

Claude is reachable only via OpenRouter: every id starts with
`openrouter/anthropic/` (for example openrouter/anthropic/claude-sonnet-4.5).
Without that prefix the gateway answers 404 model_not_found.

Use the OpenAI SDK and /chat/completions. The Anthropic SDK and the
/v1/messages route do not work on the gateway.

Page: https://netarz.ir/ai-api/claude
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://netarz.ir/api/ai/v1",
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=180,
)

# 1) A fast, lower-cost Claude.
quick = client.chat.completions.create(
    model="openrouter/anthropic/claude-haiku-4.5",
    messages=[
        {"role": "system", "content": "کوتاه و دقیق جواب بدهید."},  # becomes Claude's `system` field
        {"role": "user", "content": "فرق API و اپلیکیشن را در دو جمله بگویید."},
    ],
    max_tokens=200,
)
print(quick.choices[0].message.content)

# 2) Extended thinking: reasoning_effort is translated to a thinking budget.
#    max_tokens must be larger than that budget.
deep = client.chat.completions.create(
    model="openrouter/anthropic/claude-sonnet-4.5",
    reasoning_effort="medium",  # low | medium | high
    max_tokens=4000,
    messages=[{"role": "user", "content": "سه عدد صحیح متوالی که مجموعشان ۹۹ است کدام‌اند؟"}],
)
print(deep.choices[0].message.content)
print(deep.usage.completion_tokens_details)  # reasoning_tokens are billed as output

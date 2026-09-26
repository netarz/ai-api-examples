"""DeepSeek through NetArz.

Direct ids: deepseek-flash, deepseek-v4-pro.
Other DeepSeek models, R1 included, come via OpenRouter with the
openrouter/deepseek/ prefix. R1 returns its chain of thought in an extra
field on the message (`reasoning_content`).

Page: https://netarz.ir/ai-api/deepseek
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://netarz.ir/api/ai/v1",
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=180,
)

r = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "یک تابع پایتون بنویسید که عدد را با جداکنندهٔ هزارگان فارسی برگرداند."}],
    max_tokens=500,
)
print(r.choices[0].message.content)

r1 = client.chat.completions.create(
    model="openrouter/deepseek/deepseek-r1",
    messages=[{"role": "user", "content": "۱۷ عدد اول است؟ کوتاه توضیح بدهید."}],
    max_tokens=1500,
)
message = r1.choices[0].message
print("answer:", message.content)
# The chain of thought is an extra field outside the OpenAI schema; read it defensively.
extra = message.model_extra or {}
reasoning = extra.get("reasoning_content") or extra.get("reasoning") or ""
print("reasoning:", reasoning[:300])

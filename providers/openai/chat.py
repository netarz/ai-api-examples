"""OpenAI models (GPT) through NetArz: same SDK, same code, a NetArz key.

Chat models answer on /chat/completions. Pro and Codex models
(gpt-5.4-pro, gpt-5.3-codex, ...) answer only on /responses; see
../../python/responses_api.py.

Page: https://netarz.ir/ai-api/openai
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://netarz.ir/api/ai/v1",
    api_key=os.environ["NETARZ_API_KEY"],
)

for model in ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]:
    kwargs = {"max_completion_tokens": 400} if model.startswith("gpt-5") else {"max_tokens": 100}
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "در یک جمله بگویید API چیست."}],
        **kwargs,
    )
    print(f"{model}: {r.choices[0].message.content}")

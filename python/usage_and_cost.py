"""Read token usage and what a request cost.

Three sources, from quickest to most exact:

1. `usage` in the response: prompt, completion, cached and reasoning tokens.
2. An estimate: those tokens times the model's prices from GET /models
   (public, no key). Useful for a live cost display in your own app.
3. GET /requests/{id}: the amount actually taken from your credit for that
   request, in USD. GET /usage adds it up per day or per model.

Run:
    pip install -r requirements.txt
    export NETARZ_API_KEY="sk-ntz-v1-..."
    python usage_and_cost.py

Docs: https://netarz.ir/docs/ai/account-and-usage
      https://netarz.ir/docs/ai/billing
"""
import os
import time
from decimal import Decimal

import requests
from openai import OpenAI

BASE = os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")
KEY = os.environ["NETARZ_API_KEY"]
MODEL = os.getenv("NETARZ_MODEL", "gpt-4o-mini")
HEADERS = {"Authorization": f"Bearer {KEY}"}
MILLION = Decimal(1_000_000)

client = OpenAI(base_url=BASE, api_key=KEY)


def model_prices(model_id: str) -> dict:
    models = requests.get(f"{BASE}/models", params={"type": "chat"}, timeout=30).json()["data"]
    for m in models:
        if m["id"] == model_id:
            return m["pricing"]
    raise SystemExit(f"{model_id} is not in the chat model list")


def estimate_usd(usage, prices: dict) -> Decimal:
    """Token-based estimate. Cached input is billed at its own price."""
    details = getattr(usage, "prompt_tokens_details", None)
    cached = (getattr(details, "cached_tokens", 0) or 0) if details else 0
    fresh_input = usage.prompt_tokens - cached
    cost = Decimal(fresh_input) * Decimal(prices["input_per_million"]) / MILLION
    cost += Decimal(usage.completion_tokens) * Decimal(prices["output_per_million"]) / MILLION
    if cached:
        cached_price = prices.get("cached_input_per_million") or prices["input_per_million"]
        cost += Decimal(cached) * Decimal(cached_price) / MILLION
    return cost


response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "سه نکته برای نوشتن یک ایمیل کاری کوتاه بگویید."}],
    max_tokens=200,
)
usage = response.usage

print(response.choices[0].message.content)
print("\n-- usage (from the response) --")
print(f"prompt: {usage.prompt_tokens} | completion: {usage.completion_tokens} | total: {usage.total_tokens}")
reasoning = getattr(getattr(usage, "completion_tokens_details", None), "reasoning_tokens", None)
if reasoning:
    print(f"reasoning tokens (billed as output): {reasoning}")

print("\n-- estimate (usage x prices from GET /models) --")
print(f"about ${estimate_usd(usage, model_prices(MODEL)):.6f}")

print("\n-- charged (GET /requests/{id}) --")
# Settlement happens right after the answer; retry briefly if it is still pending.
for _ in range(5):
    r = requests.get(f"{BASE}/requests/{response.id}", headers=HEADERS, timeout=30)
    body = r.json()
    if not r.ok:
        print("error:", body["error"]["code"], "-", body["error"]["message"])
        break
    if body["status"] != "pending":
        print(f"status: {body['status']} | usd: {body['usd']} | latency: {body['latency_ms']} ms")
        break
    time.sleep(1)

print("\n-- this project, last 30 days, per model (GET /usage) --")
report = requests.get(f"{BASE}/usage", params={"group": "model"}, headers=HEADERS, timeout=30).json()
for row in report.get("data", []):
    print(f"{row['key']}: {row['requests']} requests, ${row['usd']}")
print(f"total: ${report.get('total_usd')}")

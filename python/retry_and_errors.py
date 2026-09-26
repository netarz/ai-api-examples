"""Error handling that matches the gateway's error codes.

- 429: wait for Retry-After, then retry with backoff.
- 502/503: the provider failed; nothing was charged, retry once or twice.
- 402: out of credit or over a spend limit; retrying will not help.
- 400/404: fix the request (404 model_not_found often means a missing
  `openrouter/` prefix on a Claude id).

Docs: https://netarz.ir/docs/ai/errors
"""
import os
import random
import time

from openai import APIStatusError, OpenAI, RateLimitError

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    max_retries=0,  # we retry ourselves below
)


def ask(messages: list[dict], model: str = "gpt-4o-mini", attempts: int = 5):
    for i in range(attempts):
        try:
            return client.chat.completions.create(model=model, messages=messages, max_tokens=300)
        except RateLimitError as e:
            wait = float(e.response.headers.get("Retry-After", 2 ** i)) + random.random()
            time.sleep(wait)
        except APIStatusError as e:
            code = (e.body or {}).get("error", {}).get("code") if isinstance(e.body, dict) else None
            if e.status_code == 402:
                raise RuntimeError(f"top up or raise the limit ({code})") from e
            if e.status_code >= 500:
                time.sleep(2 ** i)
                continue
            raise
    raise RuntimeError("giving up after retries")


if __name__ == "__main__":
    r = ask([{"role": "user", "content": "سلام"}])
    print(r.choices[0].message.content)

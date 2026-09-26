"""Check a key and list models.

GET /models needs no key (filter with ?type=chat|embedding|image|audio|video).
GET /me shows the balance, the key's effective RPM and spend limit.

Docs: https://netarz.ir/docs/ai/authentication
"""
import os

import requests

BASE = os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")

models = requests.get(f"{BASE}/models", params={"type": "chat"}, timeout=30).json()["data"]
print(f"{len(models)} chat models, for example:")
for m in models[:5]:
    print(" ", m["id"], "| tools:", m["capabilities"].get("tools"), "| context:", m.get("context_length"))

key = os.getenv("NETARZ_API_KEY")
if key:
    me = requests.get(f"{BASE}/me", headers={"Authorization": f"Bearer {key}"}, timeout=30)
    body = me.json()
    if me.ok:
        print("\nbalance (USD):", body["balance"]["usd"])
        print("key rpm limit:", body["key"]["rpm_limit"])
    else:
        print("\nerror:", body["error"]["code"], "-", body["error"]["message"])

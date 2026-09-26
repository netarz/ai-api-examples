"""A small Telegram bot that answers with a model on the NetArz AI gateway.

- Long polling (getUpdates), no web server, no extra framework.
- Keeps the last few turns per chat in memory.
- Run it on a server that can reach api.telegram.org.

pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="123456:ABC..."     # from @BotFather
export NETARZ_API_KEY="sk-ntz-v1-..."
python bot.py

Guide (Persian): https://netarz.ir/wiki/ai-telegram-bot-webservice
"""
import os
import time
from collections import defaultdict, deque

import requests
from openai import APIStatusError, OpenAI

TELEGRAM = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}"
MODEL = os.getenv("NETARZ_MODEL", "gpt-4o-mini")
SYSTEM = "شما دستیار فارسی‌زبان یک کسب‌وکار هستید. کوتاه، دقیق و مؤدب جواب بدهید و همیشه «شما» خطاب کنید."
HISTORY_TURNS = 6

ai = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=90,
)
history: dict[int, deque] = defaultdict(lambda: deque(maxlen=HISTORY_TURNS * 2))


def send(chat_id: int, text: str) -> None:
    requests.post(f"{TELEGRAM}/sendMessage", json={"chat_id": chat_id, "text": text[:4096]}, timeout=30)


def answer(chat_id: int, text: str) -> str:
    turns = history[chat_id]
    turns.append({"role": "user", "content": text[:4000]})
    try:
        r = ai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}, *turns],
            max_tokens=600,
        )
    except APIStatusError as e:
        turns.pop()
        # Log the stable error code for yourself; show the user a plain sentence.
        print("gateway error:", e.status_code, getattr(e, "body", None))
        return "الان نمی‌توانم جواب بدهم. چند دقیقهٔ دیگر دوباره بپرسید."
    reply = r.choices[0].message.content or ""
    turns.append({"role": "assistant", "content": reply})
    return reply


def main() -> None:
    offset = 0
    print("bot is running, model:", MODEL)
    while True:
        try:
            updates = requests.get(
                f"{TELEGRAM}/getUpdates", params={"offset": offset, "timeout": 50}, timeout=60
            ).json().get("result", [])
        except requests.RequestException as e:
            print("telegram error:", e)
            time.sleep(5)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message") or {}
            text = message.get("text")
            if not text:
                continue
            chat_id = message["chat"]["id"]
            if text.startswith("/start"):
                history.pop(chat_id, None)
                send(chat_id, "سلام. سؤالتان را بنویسید.")
                continue
            send(chat_id, answer(chat_id, text))


if __name__ == "__main__":
    main()

"""Text to speech, then speech to text, on the same key.

TTS input is capped at 4,096 characters; audio uploads at 25 MB.
Docs: https://netarz.ir/docs/ai/audio
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1"),
    api_key=os.environ["NETARZ_API_KEY"],
    timeout=120,
)

# 1) Text to speech (voices: alloy, echo, fable, onyx, nova, shimmer).
speech = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="nova",
    input="سفارش شما ثبت شد. جزئیات را در «سفارش‌های من» می‌بینید.",
    instructions="آرام و گرم صحبت کنید.",  # only gpt-4o-mini-tts reads this
    response_format="mp3",
)
speech.write_to_file("message.mp3")
print("saved message.mp3")

# 2) Speech to text. language="fa" improves Persian accuracy.
with open("message.mp3", "rb") as audio_file:
    text = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="fa",
        response_format="text",  # json | text | srt | vtt | verbose_json
    )
print("transcript:", text)

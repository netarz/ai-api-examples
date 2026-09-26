#!/usr/bin/env bash
# Embeddings, image generation and text-to-speech with cURL.
# Docs: https://netarz.ir/docs/ai/embeddings , /docs/ai/images , /docs/ai/audio
set -euo pipefail
: "${NETARZ_API_KEY:?Set NETARZ_API_KEY first}"
API=https://netarz.ir/api/ai/v1

echo "== embeddings"
curl -sS "$API/embeddings" \
  -H "Authorization: Bearer $NETARZ_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": ["گیفت کارت اپل", "اشتراک اسپاتیفای"]}' | head -c 300
echo -e "\n"

echo "== image (base64 in data[0].b64_json)"
curl -sS "$API/images/generations" \
  -H "Authorization: Bearer $NETARZ_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gpt-image-1-mini", "prompt": "یک فنجان قهوه روی میز چوبی، نور صبح", "size": "1024x1024", "quality": "low"}' \
  | python3 -c 'import sys, json, base64; open("image.png", "wb").write(base64.b64decode(json.load(sys.stdin)["data"][0]["b64_json"])); print("saved image.png")'

echo "== text to speech"
curl -sS "$API/audio/speech" \
  -H "Authorization: Bearer $NETARZ_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "voice": "alloy", "input": "سفارش شما ثبت شد."}' \
  --output speech.mp3 && echo "saved speech.mp3"

echo "== speech to text"
curl -sS "$API/audio/transcriptions" \
  -H "Authorization: Bearer $NETARZ_API_KEY" \
  -F file=@speech.mp3 -F model=whisper-1 -F language=fa -F response_format=text

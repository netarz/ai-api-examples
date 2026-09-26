#!/usr/bin/env bash
# Streaming with cURL (-N disables buffering). Each line is "data: {...}", ending with "data: [DONE]".
# Docs: https://netarz.ir/docs/ai/streaming
set -euo pipefail
: "${NETARZ_API_KEY:?Set NETARZ_API_KEY first}"

curl -sS -N https://netarz.ir/api/ai/v1/chat/completions \
  -H "Authorization: Bearer $NETARZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "یک شعر کوتاه دربارهٔ پاییز بنویسید."}],
    "stream": true,
    "max_tokens": 200
  }'

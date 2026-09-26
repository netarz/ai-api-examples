#!/usr/bin/env bash
# Chat completion with cURL.  Usage: NETARZ_API_KEY=sk-ntz-v1-... ./chat.sh [model]
# Docs: https://netarz.ir/docs/ai/chat-completions
set -euo pipefail
: "${NETARZ_API_KEY:?Set NETARZ_API_KEY first}"
MODEL="${1:-gpt-4o-mini}"

curl -sS https://netarz.ir/api/ai/v1/chat/completions \
  -H "Authorization: Bearer $NETARZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"در یک جمله خودتان را معرفی کنید.\"}],
    \"max_tokens\": 150
  }"
echo

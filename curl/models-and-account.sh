#!/usr/bin/env bash
# List models (no key needed) and check your key (balance, RPM, spend limit).
# Docs: https://netarz.ir/docs/ai/models-and-pricing , https://netarz.ir/docs/ai/authentication
set -euo pipefail

# type = chat | embedding | image | audio | video
curl -sS "https://netarz.ir/api/ai/v1/models?type=chat" | head -c 800
echo -e "\n..."

if [ -n "${NETARZ_API_KEY:-}" ]; then
  curl -sS https://netarz.ir/api/ai/v1/me -H "Authorization: Bearer $NETARZ_API_KEY"
  echo
fi

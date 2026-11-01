#!/usr/bin/env bash
# Latest exchange rates with curl + jq. No API key.
# Usage: ./rates.sh USD EUR 100
set -euo pipefail
FROM="${1:-USD}"; TO="${2:-EUR}"; AMOUNT="${3:-1}"

curl -s "https://allratestoday.com/api/open/latest/${FROM}" \
  | jq --arg to "$TO" --argjson amt "$AMOUNT" \
      '{date, from: .base_code, to: $to, rate: .rates[$to], result: (.rates[$to] * $amt)}'

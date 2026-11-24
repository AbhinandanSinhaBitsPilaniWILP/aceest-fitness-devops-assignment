#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/evidence/raw" "$ROOT/evidence/screenshots"

if curl --fail --silent http://127.0.0.1:8000/health > "$ROOT/evidence/raw/health.json"; then
  echo "Health evidence written to evidence/raw/health.json"
else
  echo "Local application is not running; start it before capturing screenshots." >&2
fi

echo "Save browser screenshots under evidence/screenshots using evidence/README.md."
echo "Do not include credentials, access tokens, or one-time codes in evidence."


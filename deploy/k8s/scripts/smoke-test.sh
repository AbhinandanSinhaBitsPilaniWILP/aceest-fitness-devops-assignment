#!/usr/bin/env bash
set -euo pipefail

STRATEGY="${1:-rolling}"

case "$STRATEGY" in
  rolling|shadow|ab)
    DEPLOYMENT="aceest-fitness"
    ;;
  blue-green)
    DEPLOYMENT="aceest-fitness-green"
    ;;
  canary)
    DEPLOYMENT="aceest-fitness-canary"
    ;;
  *)
    echo "Unsupported deployment strategy: $STRATEGY" >&2
    exit 2
    ;;
esac

kubectl --namespace aceest get "deployment/$DEPLOYMENT"
kubectl --namespace aceest wait --for=condition=Available "deployment/$DEPLOYMENT" --timeout=120s
kubectl --namespace aceest exec "deployment/$DEPLOYMENT" -- python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"


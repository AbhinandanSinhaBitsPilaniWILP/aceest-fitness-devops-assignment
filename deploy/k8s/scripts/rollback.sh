#!/usr/bin/env bash
set -euo pipefail

STRATEGY="${1:-rolling}"

case "$STRATEGY" in
  rolling)
    kubectl rollout undo deployment/aceest-fitness --namespace aceest
    kubectl rollout status deployment/aceest-fitness --namespace aceest --timeout=120s
    ;;
  blue-green)
    kubectl --namespace aceest patch service aceest-fitness-active --type merge --patch '{"spec":{"selector":{"app":"aceest-fitness","track":"blue"}}}'
    kubectl rollout undo deployment/aceest-fitness-green --namespace aceest --ignore-not-found=true
    ;;
  canary)
    kubectl rollout undo deployment/aceest-fitness-canary --namespace aceest --ignore-not-found=true
    ;;
  shadow)
    kubectl rollout undo deployment/aceest-fitness-shadow --namespace aceest --ignore-not-found=true
    kubectl rollout undo deployment/aceest-fitness --namespace aceest
    ;;
  ab)
    kubectl rollout undo deployment/aceest-fitness-b --namespace aceest --ignore-not-found=true
    kubectl rollout undo deployment/aceest-fitness --namespace aceest
    ;;
  *)
    echo "Unsupported deployment strategy: $STRATEGY" >&2
    exit 2
    ;;
esac


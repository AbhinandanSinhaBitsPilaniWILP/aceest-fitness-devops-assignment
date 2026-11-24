#!/usr/bin/env bash
set -euo pipefail

STRATEGY="${1:-rolling}"
IMAGE="${2:-aceest-fitness:latest}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

kubectl apply -f "$K8S_ROOT/base/namespace.yaml"
kubectl apply -f "$K8S_ROOT/base/service.yaml" -f "$K8S_ROOT/base/deployment.yaml"

case "$STRATEGY" in
  rolling)
    kubectl --namespace aceest set image deployment/aceest-fitness aceest-fitness="$IMAGE"
    kubectl --namespace aceest rollout status deployment/aceest-fitness --timeout=120s
    ;;
  blue-green)
    kubectl apply -f "$K8S_ROOT/strategies/blue-green.yaml"
    kubectl --namespace aceest set image deployment/aceest-fitness-green aceest-fitness="$IMAGE"
    kubectl --namespace aceest rollout status deployment/aceest-fitness-green --timeout=120s
    ;;
  canary)
    kubectl apply -f "$K8S_ROOT/strategies/canary.yaml"
    kubectl --namespace aceest set image deployment/aceest-fitness-canary aceest-fitness="$IMAGE"
    kubectl --namespace aceest rollout status deployment/aceest-fitness-canary --timeout=120s
    ;;
  shadow)
    kubectl apply -f "$K8S_ROOT/strategies/shadow-istio.yaml"
    kubectl --namespace aceest set image deployment/aceest-fitness-shadow aceest-fitness="$IMAGE"
    kubectl --namespace aceest rollout status deployment/aceest-fitness-shadow --timeout=120s
    ;;
  ab)
    kubectl apply -f "$K8S_ROOT/strategies/ab-ingress.yaml"
    kubectl --namespace aceest set image deployment/aceest-fitness-b aceest-fitness="$IMAGE"
    kubectl --namespace aceest rollout status deployment/aceest-fitness-b --timeout=120s
    ;;
  *)
    echo "Unsupported deployment strategy: $STRATEGY" >&2
    exit 2
    ;;
esac


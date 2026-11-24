$ErrorActionPreference = "Stop"

kubectl --namespace aceest get deployment/aceest-fitness
kubectl --namespace aceest get service/aceest-fitness
kubectl --namespace aceest wait --for=condition=Available deployment/aceest-fitness --timeout=120s


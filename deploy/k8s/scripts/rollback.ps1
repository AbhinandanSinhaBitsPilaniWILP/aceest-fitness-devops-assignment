$ErrorActionPreference = "Stop"

kubectl rollout undo deployment/aceest-fitness --namespace aceest
kubectl rollout undo deployment/aceest-fitness-green --namespace aceest --ignore-not-found=true
kubectl rollout undo deployment/aceest-fitness-canary --namespace aceest --ignore-not-found=true
kubectl rollout undo deployment/aceest-fitness-shadow --namespace aceest --ignore-not-found=true
kubectl rollout undo deployment/aceest-fitness-b --namespace aceest --ignore-not-found=true


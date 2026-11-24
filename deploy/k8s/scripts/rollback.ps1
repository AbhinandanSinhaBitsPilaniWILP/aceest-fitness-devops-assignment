param(
    [ValidateSet("rolling", "blue-green", "canary", "shadow", "ab")]
    [string]$Strategy = "rolling"
)
$ErrorActionPreference = "Stop"

switch ($Strategy) {
    "rolling" { kubectl rollout undo deployment/aceest-fitness --namespace aceest }
    "blue-green" {
        kubectl -n aceest patch service aceest-fitness-active --type merge --patch '{"spec":{"selector":{"app":"aceest-fitness","track":"blue"}}}'
        kubectl rollout undo deployment/aceest-fitness-green --namespace aceest --ignore-not-found=true
    }
    "canary" { kubectl rollout undo deployment/aceest-fitness-canary --namespace aceest --ignore-not-found=true }
    "shadow" {
        kubectl rollout undo deployment/aceest-fitness-shadow --namespace aceest --ignore-not-found=true
        kubectl rollout undo deployment/aceest-fitness --namespace aceest
    }
    "ab" {
        kubectl rollout undo deployment/aceest-fitness-b --namespace aceest --ignore-not-found=true
        kubectl rollout undo deployment/aceest-fitness --namespace aceest
    }
}


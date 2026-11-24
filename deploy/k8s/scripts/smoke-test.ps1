param(
    [ValidateSet("rolling", "blue-green", "canary", "shadow", "ab")]
    [string]$Strategy = "rolling"
)
$ErrorActionPreference = "Stop"

$deployment = switch ($Strategy) {
    "rolling" { "aceest-fitness" }
    "shadow" { "aceest-fitness-shadow" }
    "ab" { "aceest-fitness-b" }
    "blue-green" { "aceest-fitness-green" }
    "canary" { "aceest-fitness-canary" }
}

kubectl --namespace aceest get "deployment/$deployment"
kubectl --namespace aceest wait --for=condition=Available "deployment/$deployment" --timeout=120s
kubectl --namespace aceest exec "deployment/$deployment" -- python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"


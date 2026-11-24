param(
    [ValidateSet("rolling", "blue-green", "canary", "shadow", "ab")]
    [string]$Strategy = "rolling",
    [Parameter(Mandatory = $true)]
    [string]$Image
)

$ErrorActionPreference = "Stop"
$k8sRoot = Split-Path -Parent $PSScriptRoot

kubectl apply -f "$k8sRoot\base\namespace.yaml"

switch ($Strategy) {
    "rolling" {
        kubectl apply -f "$k8sRoot\base\pvc.yaml"
        kubectl apply -f "$k8sRoot\base\service.yaml"
        kubectl apply -f "$k8sRoot\base\deployment.yaml"
        kubectl -n aceest set image deployment/aceest-fitness aceest-fitness=$Image
    }
    "blue-green" {
        kubectl apply -f "$k8sRoot\strategies\blue-green.yaml"
        kubectl -n aceest set image deployment/aceest-fitness-green aceest-fitness=$Image
    }
    "canary" {
        kubectl apply -f "$k8sRoot\strategies\canary.yaml"
        kubectl -n aceest set image deployment/aceest-fitness-canary aceest-fitness=$Image
    }
    "shadow" {
        kubectl apply -f "$k8sRoot\base\pvc.yaml"
        kubectl apply -f "$k8sRoot\base\service.yaml"
        kubectl apply -f "$k8sRoot\base\deployment.yaml"
        kubectl apply -f "$k8sRoot\strategies\shadow-istio.yaml"
        kubectl -n aceest set image deployment/aceest-fitness-shadow aceest-fitness=$Image
    }
    "ab" {
        kubectl apply -f "$k8sRoot\base\pvc.yaml"
        kubectl apply -f "$k8sRoot\base\service.yaml"
        kubectl apply -f "$k8sRoot\base\deployment.yaml"
        kubectl apply -f "$k8sRoot\strategies\ab-ingress.yaml"
        kubectl -n aceest set image deployment/aceest-fitness-b aceest-fitness=$Image
    }
}


$ErrorActionPreference = "Stop"

$evidenceRoot = Join-Path $PSScriptRoot "..\evidence"
$rawRoot = Join-Path $evidenceRoot "raw"
$screenshots = Join-Path $evidenceRoot "screenshots"
New-Item -ItemType Directory -Force -Path $rawRoot, $screenshots | Out-Null

try {
    Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -OutFile (Join-Path $rawRoot "health.json")
    Write-Host "Health evidence written to evidence/raw/health.json"
} catch {
    Write-Warning "Local application is not running; start it before capturing screenshots."
}

Write-Host "Save browser screenshots under evidence/screenshots using the names in evidence/README.md."
Write-Host "Do not include credentials, access tokens, or one-time codes in evidence."


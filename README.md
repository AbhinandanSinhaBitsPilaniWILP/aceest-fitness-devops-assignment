# ACEest Fitness DevOps Assignment

ACEest Fitness is a small Flask web application used to demonstrate Assignment 2's end-to-end CI/CD pipeline. It provides a browser page, a health check, client management, and fitness-progress recording backed by SQLite.

## Run locally

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest
$env:PYTHONPATH = "$PWD\src"
python -m flask --app "aceest:create_app()" run --debug --port 8000
```

Open <http://127.0.0.1:8000>. The health endpoint is <http://127.0.0.1:8000/health>.

On a POSIX shell, use `export PYTHONPATH=src` before the Flask command.

## Repository layout

- `src/aceest/` - Flask application and SQLite persistence.
- `tests/` - Pytest application and delivery-contract tests.
- `legacy/` - supplied Assignment 1 Python versions retained for traceability.
- `Dockerfile` and `docker-compose.yml` - container build and local runtime.
- `Jenkinsfile` and `sonar-project.properties` - CI, quality gate, and delivery configuration.
- `deploy/k8s/` - baseline and progressive Kubernetes deployment examples.
- `REPORT.md` - submission report and evidence checklist.

## DevOps verification

```powershell
python -m pytest --cov=src/aceest --cov-report=term-missing
ruff check src tests scripts
docker build -t aceest-fitness:local .
kubectl apply --dry-run=client -f deploy/k8s/base
```

The Jenkins pipeline requires credentials configured in Jenkins for Docker Hub, SonarQube, and the Kubernetes context. It defaults to safe validation and only deploys when the `DEPLOY` parameter is explicitly set to `true`.


# ACEest Fitness DevOps Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Flask-based ACEest Fitness application and a submission-ready CI/CD repository covering testing, quality gates, containers, Kubernetes deployment strategies, rollback, and evidence reporting.

**Architecture:** A Flask application exposes a health endpoint, client CRUD, progress recording, and a small browser UI backed by SQLite. Jenkins runs tests and quality checks, builds tagged Docker images, and optionally deploys to Kubernetes. Kubernetes manifests demonstrate a safe baseline plus rolling, blue-green, canary, shadow, and A/B patterns.

**Tech Stack:** Python 3.12, Flask, SQLite, Pytest, pytest-cov, Ruff, SonarQube, Docker, Jenkins, Kubernetes/Minikube, Markdown/HTML report.

**Spec:** `docs/superpowers/specs/2026-11-24-aceest-devops-design.md`

## Global Constraints

- The deployable application must be Flask-based.
- Tests must run with Pytest and be runnable without external services.
- The container must run as a non-root user and expose port 8000.
- Deployment configuration must be parameterized; no credentials or tokens may be committed.
- Report claims must label local verification versus external-service evidence.
- All five named progressive deployment patterns and rollback must have repository artifacts or executable guidance.

## Review Focus

- Empty and malformed client payloads must return clear 4xx responses rather than server errors; covered in `tests/test_app.py`.
- Database state must survive application-factory calls and use parameterized SQL; covered by client/progress API tests.
- Health checks must be usable by Docker/Kubernetes; covered by the health endpoint test and manifest validation.
- Image tags and deployment strategy inputs must be explicit and safe; covered by Jenkinsfile/static configuration checks.
- Rollback must be an executable documented path; covered by strategy script syntax and report checklist.

---

### Task 1: Repository scaffold and Flask application contract

**Files:**
- Create: `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini`, `src/aceest/__init__.py`, `src/aceest/app.py`, `tests/test_app.py`
- Modify: none
- Test: `tests/test_app.py`

**Interfaces:**
- Produces `aceest.create_app(config=None)`, Flask routes `/health`, `/api/clients`, `/api/clients/<int:client_id>`, `/api/clients/<int:client_id>/progress`, and `/`.

- [ ] Write failing tests for the health response, client creation/listing, validation, progress recording, and factory isolation.
- [ ] Run `pytest -q`; confirm failure because the Flask package and application contract do not exist.
- [ ] Implement the minimal Flask application and SQLite schema needed by those tests.
- [ ] Run `pytest -q`; confirm all application tests pass.
- [ ] Commit `feat: add tested flask fitness service`.

### Task 2: Browser interface and application documentation

**Files:**
- Create: `templates/index.html`, `static/app.js`, `static/styles.css`, `README.md`
- Modify: `src/aceest/app.py`, `tests/test_app.py`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes the API contract from Task 1 and produces a usable browser page that calls the API without server-side secrets.

- [ ] Add a failing test for the rendered home page and documented API behavior.
- [ ] Run the focused test and confirm the template/static contract is missing.
- [ ] Add the page, browser JavaScript, CSS, and README usage instructions.
- [ ] Run the focused test and the full Pytest suite; confirm pass.
- [ ] Commit `feat: add fitness web interface and usage docs`.

### Task 3: Container, quality, and Jenkins automation

**Files:**
- Create: `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `sonar-project.properties`, `Jenkinsfile`, `scripts/quality-check.ps1`, `scripts/quality-check.sh`
- Modify: `README.md`
- Test: `tests/test_pipeline_contract.py`

**Interfaces:**
- Consumes the application start command `gunicorn --bind 0.0.0.0:8000 'aceest:create_app()'` and produces parameterized Jenkins stages and a health-checkable image.

- [ ] Write failing contract tests that assert required pipeline stages, image port, non-root execution, and SonarQube properties.
- [ ] Run the contract tests and confirm the configuration files are missing.
- [ ] Add the Docker/Jenkins/SonarQube files and local quality scripts.
- [ ] Run contract tests, Pytest with coverage, and the quality script; confirm pass or record tool-specific unavailable status.
- [ ] Commit `ci: add container quality gate and jenkins pipeline`.

### Task 4: Kubernetes deployments and rollback strategies

**Files:**
- Create: `deploy/k8s/base/*.yaml`, `deploy/k8s/strategies/*.yaml`, `deploy/k8s/scripts/*.ps1`, `deploy/k8s/scripts/*.sh`, `tests/test_kubernetes_contract.py`
- Modify: `README.md`, `Jenkinsfile`
- Test: `tests/test_kubernetes_contract.py`

**Interfaces:**
- Produces manifests for baseline rolling update, blue-green, canary, shadow, and A/B deployment, plus switch/rollback scripts using `kubectl`.

- [ ] Write failing manifest tests for required Kubernetes objects, probes, selectors, strategy labels, and rollback commands.
- [ ] Run the tests and confirm the manifests/scripts are missing.
- [ ] Add the manifests and cross-platform strategy scripts with image/tag parameterization.
- [ ] Run manifest tests and `kubectl apply --dry-run=client` when kubectl is available; otherwise report the exact unavailable tool.
- [ ] Commit `deploy: add kubernetes rollout strategies and rollback`.

### Task 5: Legacy source preservation and submission report

**Files:**
- Create: `legacy/*.py`, `evidence/README.md`, `REPORT.md`, `scripts/build_report.py`, `scripts/capture_evidence.ps1`, `scripts/capture_evidence.sh`
- Modify: `README.md`
- Test: `tests/test_submission_contract.py`

**Interfaces:**
- Consumes the supplied archive versions and repository artifacts; produces a report with a requirements matrix, architecture, instructions, evidence slots, risks, and external-link placeholders.

- [ ] Write failing tests for legacy-version presence, report sections, and evidence checklist completeness.
- [ ] Run the tests and confirm the submission package is incomplete.
- [ ] Copy the supplied versions into `legacy/`, add report/evidence tooling, and document the Flask migration gap honestly.
- [ ] Run submission contract tests and build the report HTML/Markdown output.
- [ ] Commit `docs: add submission report and evidence checklist`.

### Task 6: End-to-end verification and packaging

**Files:**
- Modify: `REPORT.md`, `README.md` only if verification reveals a gap
- Test: full repository verification

- [ ] Run the complete test suite with coverage.
- [ ] Run syntax compilation for all Python files.
- [ ] Build the Docker image if Docker is available and exercise `/health`.
- [ ] Validate the Kubernetes manifests and Jenkins static contract.
- [ ] Generate final report outputs and package the repository under `outputs/`.
- [ ] Commit `chore: verify and package assignment submission`.


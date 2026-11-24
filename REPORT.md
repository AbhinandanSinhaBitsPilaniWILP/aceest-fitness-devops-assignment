# ACEest Fitness DevOps Assignment Report

Student: Abhinandan Sinha  
Account: AbhinandanSinhaBitsPilaniWILP  
Assignment: Introduction to DevOps - CI/CD Pipeline Assignment 2  
Report state: Local implementation complete; external-service evidence is clearly marked below.

## Executive summary

This submission implements an end-to-end DevOps repository for ACEest Fitness and Gym. The deployable application is a Flask service with a browser interface, health endpoint, client management, and fitness-progress recording. It is backed by SQLite and packaged for a non-root Docker runtime on port 8000.

The repository includes Pytest tests, coverage reporting, Ruff quality checks, SonarQube configuration, a Jenkins pipeline, a Dockerfile, Docker Compose, Kubernetes manifests, five progressive deployment examples, rollback scripts, the supplied Assignment 1 versions, and this evidence-led report.

The supplied archive contained Tkinter desktop applications rather than Flask services. The original files are preserved under legacy/; the deployable Flask application was built separately so the repository meets the assignment's explicit Flask requirement without losing the supplied version evidence.

## Architecture

~~~text
GitHub commit / tag
        |
        v
Jenkins checkout -> install -> Pytest + coverage -> Ruff -> SonarQube quality gate
        |
        v
Docker build -> versioned image -> Docker Hub (when PUSH_IMAGE=true)
        |
        v
Kubernetes / Minikube -> rolling | blue-green | canary | shadow | A/B
        |
        v
health smoke test -> evidence capture -> rollback on failure
~~~

### Application components

- src/aceest/app.py - Flask application factory, SQLite schema, API routes, health check, and persistence.
- templates/index.html - browser UI.
- static/app.js and static/styles.css - client creation and list display.
- tests/test_app.py - API, validation, progress, rendering, and database-isolation tests.

### API surface

| Endpoint | Purpose |
|---|---|
| GET / | Browser application page |
| GET /health | Kubernetes and Docker health check |
| GET /api/clients | List clients |
| POST /api/clients | Create a client with name, email, and goal |
| GET /api/clients/<id> | Read a client and progress history |
| PUT /api/clients/<id> | Update client details |
| DELETE /api/clients/<id> | Delete a client and its progress |
| POST /api/clients/<id>/progress | Record weight and workout progress |

## Requirements traceability

| Assignment requirement | Repository implementation | Evidence status |
|---|---|---|
| Flask application | src/aceest, templates, static assets | Verified locally |
| Git and GitHub | Local Git repository, commit history, README publishing instructions | Verified locally and pushed to public GitHub repository |
| Pytest | tests/, pytest.ini, pytest-cov | Verified locally: 28 tests passed |
| Jenkins | Jenkinsfile with checkout, install, tests, quality, image, push, deploy, smoke stages | Pipeline source verified; Jenkins run requires configured server |
| SonarQube | sonar-project.properties, Jenkins quality-gate stage | Configuration verified; live gate requires SonarQube server |
| Docker / Podman | Dockerfile, .dockerignore, docker-compose.yml | Docker build requires Docker/Podman; not installed in the build environment |
| Container registry | Parameterized Docker Hub push using Jenkins credential dockerhub | Requires authenticated Docker Hub repository |
| Kubernetes / Minikube | Base namespace, Deployment, Service, probes, and resource limits | YAML parse verified; kubectl/cluster not installed in the build environment |
| Progressive deployments | deploy/k8s/strategies/ for rolling, blue-green, canary, shadow, and A/B | Manifests and scripts verified; live screenshots require cluster |
| Rollback | deploy/k8s/scripts/rollback.sh and rollback.ps1, Jenkins failure rollback | Command path verified; live rollback evidence requires cluster |
| Short report | This report plus evidence/README.md | Included |
| Hosted CI verification | .github/workflows/ci.yml | Verified remotely: GitHub Actions run 45430323848 succeeded, including Docker image build |

## CI/CD implementation

Jenkins uses a Linux agent label linux-python-docker. The pipeline defaults to a validation-only run. Pushing images requires PUSH_IMAGE=true, and deployment requires DEPLOY=true; this prevents an ordinary commit from changing an external environment unexpectedly.

The pipeline uses the following Jenkins credentials and tools, which must be created by the Jenkins administrator:

- dockerhub username/password credential.
- SonarQube server installation named sonarqube.
- sonar-scanner configured as a Jenkins tool.
- A Kubernetes-enabled agent with kubectl and the target context.

The Jenkins post-failure block attempts kubectl rollout undo after a failed deployment. The standalone rollback scripts provide the same recovery path for operators.

## Quality and testing results

Local verification performed during repository construction:

~~~text
Pytest: 28 passed
Coverage: 98% total for src/aceest
Ruff: All checks passed
Kubernetes YAML: all base and strategy YAML documents parsed successfully
Python syntax: application and preserved legacy files compile successfully
GitHub Actions: verify and container jobs succeeded
~~~

The quality gate is configured to consume coverage.xml. SonarQube will provide the authoritative gate result after the project is connected to a SonarQube server.

## Deployment strategies

### Rolling update

base/deployment.yaml and strategies/rolling.yaml use maxUnavailable: 0 and maxSurge: 1, readiness probes, and a bounded revision history. The service remains available while new pods become ready.

### Blue-green deployment

blue-green.yaml creates blue and green workloads plus active and preview Services. The preview Service is used for validation. Switching the active Service selector from track: blue to track: green promotes the candidate; reversing the selector provides a fast rollback.

### Canary release

canary.yaml creates stable and canary workloads. Both carry traffic: enabled, and the shared Service can distribute traffic according to replica weighting. The canary is scaled gradually while health, error rate, and response time are monitored.

### Shadow deployment

shadow-istio.yaml deploys a candidate shadow workload and an Istio VirtualService that mirrors requests to it while the stable workload continues serving responses. Shadow responses are not returned to users.

### A/B testing

ab-ingress.yaml defines a candidate B workload and NGINX Ingress header routing using X-ACEest-Variant: b. This makes the selected variant explicit and reproducible for a tester.

## Links

- Local application: http://127.0.0.1:8000/ - available when started with the README command.
- Local health check: http://127.0.0.1:8000/health.
- GitHub account: https://github.com/AbhinandanSinhaBitsPilaniWILP - verified through GitHub CLI authentication.
- GitHub repository: https://github.com/AbhinandanSinhaBitsPilaniWILP/aceest-fitness-devops-assignment - public repository with the verified main branch.
- GitHub Actions verification: https://github.com/AbhinandanSinhaBitsPilaniWILP/aceest-fitness-devops-assignment/actions/runs/45430323848 - successful tests, quality checks, artifacts, and Docker image build.
- Docker Hub repository: to be filled after the authenticated Docker Hub username and repository are created.
- Jenkins build URL: to be filled after the Jenkins job is created.
- SonarQube project URL: to be filled after the project is created on the configured SonarQube server.
- Kubernetes endpoint: to be filled after Minikube or a cloud cluster is provisioned.

## Screenshots

Screenshots must be stored in evidence/screenshots/ using the names in evidence/README.md. The evidence guide deliberately separates locally capturable screens from external-service proof so that generated images are not misrepresented as Jenkins, SonarQube, Docker Hub, or Kubernetes evidence.

Current capture result: the local server started successfully, but browser access to the localhost origin was declined by the desktop browser permission gate. No screenshot was fabricated. Run scripts/capture_evidence.ps1 or scripts/capture_evidence.sh from an environment that permits localhost browser access, then place the resulting images in evidence/screenshots/.

| Screenshot | What it proves | Status |
|---|---|---|
| 01-home-page.png | Flask application UI | Capture locally; blocked by current browser permission gate |
| 02-health-endpoint.png | Health response | Capture locally; blocked by current browser permission gate |
| 03-jenkins-success.png | Jenkins stages succeeded | Requires Jenkins |
| 04-sonarqube-quality-gate.png | Quality gate passed | Requires SonarQube |
| 05-dockerhub-tags.png | Versioned registry images | Requires Docker Hub |
| 06-kubernetes-rolling.png | Rolling deployment | Requires cluster |
| 07-kubernetes-blue-green.png | Active/preview promotion | Requires cluster |
| 08-kubernetes-canary.png | Canary rollout | Requires cluster |
| 09-kubernetes-shadow.png | Mirrored traffic | Requires Istio-enabled cluster |
| 10-kubernetes-ab.png | Header-based A/B routing | Requires ingress |
| 11-kubernetes-rollback.png | Rollback evidence | Requires cluster |

## Challenges and mitigation

1. Framework mismatch: the supplied code was Tkinter, while the assignment requires Flask. The original code is preserved and the deployable service is implemented in Flask.
2. External tools are environment-dependent: Docker, kubectl, Jenkins, SonarQube, Docker Hub, and GitHub credentials are not assumed. Configuration is committed, while live claims remain pending until the tool result is captured.
3. Deployment safety: Jenkins deployment is opt-in, image tags are explicit, health probes are required, and rollback commands are included in both shell and PowerShell forms.
4. Version traceability: all ten supplied files are kept under legacy/, while the deployable application has a clear package boundary and test suite.

## Submission checklist

- [x] Flask application source and browser UI.
- [x] Pytest tests and local coverage evidence.
- [x] Jenkinsfile with automated test, quality, build, push, deploy, smoke, and rollback path.
- [x] Dockerfile and Docker Compose file.
- [x] SonarQube project configuration.
- [x] Kubernetes base manifests and all five strategy examples.
- [x] Rollback scripts.
- [x] Supplied source versions preserved.
- [x] Detailed report and evidence guide.
- [x] GitHub repository created and pushed.
- [ ] Docker Hub repository created and images pushed.
- [ ] Jenkins successful run screenshot and URL.
- [ ] SonarQube quality-gate screenshot and URL.
- [ ] Kubernetes endpoint and deployment screenshots.

The unchecked items require authenticated external systems and cannot be truthfully completed from local repository construction alone.


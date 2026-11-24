# ACEest Fitness DevOps Pipeline Design

## Intent

Deliver a submission-ready repository for Assignment 2: a small, maintainable Flask fitness-management service surrounded by an automated CI/CD workflow. The repository must make the required pipeline stages reproducible locally and provide Kubernetes manifests and evidence templates for Jenkins, SonarQube, Docker, deployment strategies, and rollback.

## Goals

- Provide a Flask web application with useful fitness-client and progress functionality.
- Preserve the supplied Assignment 1 Python versions under `legacy/` for traceability.
- Add Pytest coverage, containerization, Jenkins automation, SonarQube configuration, registry tagging, and Kubernetes deployment manifests.
- Demonstrate rolling, blue-green, canary, shadow, and A/B deployment patterns with rollback instructions.
- Produce a detailed final report that distinguishes verified local evidence from evidence requiring authenticated external services.

## Non-goals

- Reproducing every Tkinter screen as a web page.
- Claiming a live GitHub, Docker Hub, Jenkins, SonarQube, or Kubernetes result without fresh evidence from that service.
- Storing the user's email, passwords, access tokens, or one-time codes in the repository.

## Chosen approach

Use a hybrid migration. The supplied files remain in `legacy/` as the original version history. A fresh Flask service is the deployable application because the assignment explicitly requires Flask, while the original archive is a Tkinter desktop application. The service uses a small SQLite repository, JSON APIs, and a browser page, keeping the runtime simple enough for Docker and Minikube.

## Pipeline contract

The normal path is checkout -> install -> Pytest -> SonarQube scan and quality gate -> Docker build -> registry push -> Kubernetes deploy -> smoke test. Deployment is gated by an explicit Jenkins parameter and rollback is available through Kubernetes rollout commands and the included strategy scripts.

## External-service boundary

GitHub publishing, Docker Hub pushes, Jenkins execution, SonarQube results, and a live cluster endpoint are external side effects. They are represented by safe, parameterized configuration and can only be verified after the user completes interactive authentication or provides already-configured credentials.


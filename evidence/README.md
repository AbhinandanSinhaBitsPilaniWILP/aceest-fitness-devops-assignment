# Evidence Capture Guide

This folder is the evidence index for the submission report. Capture only the application state and tool results needed for assessment; never capture credentials, passwords, access tokens, email codes, or browser account data.

## Required screenshots

1. 01-home-page.png - Flask application home page.
2. 02-health-endpoint.png - /health response.
3. 03-jenkins-success.png - successful Jenkins run showing tests, quality gate, image build, and deployment stages.
4. 04-sonarqube-quality-gate.png - SonarQube project and passed quality gate.
5. 05-dockerhub-tags.png - Docker Hub repository showing versioned image tags.
6. 06-kubernetes-rolling.png - rolling-update deployment and healthy pods.
7. 07-kubernetes-blue-green.png - active and preview services with the selected track.
8. 08-kubernetes-canary.png - stable/canary workload and traffic evidence.
9. 09-kubernetes-shadow.png - mirror configuration and stable response.
10. 10-kubernetes-ab.png - A/B header routing result.
11. 11-kubernetes-rollback.png - rollout history and successful rollback.

## Evidence boundary

Screenshots 1 and 2 can be captured locally. Screenshots 3-11 require the relevant authenticated Jenkins, SonarQube, Docker Hub, ingress/service-mesh, or Kubernetes environment. Until those services are authenticated and run, the report must mark them as pending rather than presenting generated placeholders as proof.


from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_dockerfile_runs_as_non_root_and_exposes_health_port():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.12-slim" in dockerfile
    assert "EXPOSE 8000" in dockerfile
    assert "USER appuser" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "gunicorn" in dockerfile


def test_jenkinsfile_has_required_quality_and_delivery_stages():
    jenkinsfile = (ROOT / "Jenkinsfile").read_text(encoding="utf-8")

    for stage in ("Checkout", "Install", "Unit tests", "Quality", "Build image", "Deploy", "Smoke test"):
        assert f"stage('{stage}')" in jenkinsfile
    assert "waitForQualityGate" in jenkinsfile
    assert "withCredentials" in jenkinsfile
    assert "DEPLOYMENT_STRATEGY" in jenkinsfile
    assert "rollback" in jenkinsfile.lower()


def test_sonar_configuration_targets_source_and_tests():
    sonar = (ROOT / "sonar-project.properties").read_text(encoding="utf-8")

    assert "sonar.projectKey=aceest-fitness" in sonar
    assert "sonar.sources=src" in sonar
    assert "sonar.tests=tests" in sonar
    assert "sonar.python.coverage.reportPaths" in sonar


def test_local_quality_scripts_run_the_same_checks_as_ci():
    powershell = (ROOT / "scripts/quality-check.ps1").read_text(encoding="utf-8")
    shell = (ROOT / "scripts/quality-check.sh").read_text(encoding="utf-8")

    for script in (powershell, shell):
        assert "pytest" in script
        assert "ruff" in script
        assert "cov" in script


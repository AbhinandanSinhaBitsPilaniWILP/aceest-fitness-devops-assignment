from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
BASE = ROOT / "deploy/k8s/base"
STRATEGIES = ROOT / "deploy/k8s/strategies"
SCRIPTS = ROOT / "deploy/k8s/scripts"


def test_base_manifests_define_namespace_service_and_safe_deployment():
    namespace = (BASE / "namespace.yaml").read_text(encoding="utf-8")
    service = (BASE / "service.yaml").read_text(encoding="utf-8")
    deployment = (BASE / "deployment.yaml").read_text(encoding="utf-8")

    assert "kind: Namespace" in namespace
    assert "name: aceest" in namespace
    assert "kind: Service" in service
    assert "selector:" in service
    assert "kind: Deployment" in deployment
    assert "maxUnavailable: 0" in deployment
    assert "maxSurge: 1" in deployment
    assert "readinessProbe:" in deployment
    assert "livenessProbe:" in deployment
    assert "runAsNonRoot: true" in deployment
    assert "containerPort: 8000" in deployment


def test_all_required_progressive_strategy_manifests_exist():
    expected = {
        "blue-green.yaml": ("aceest-fitness-active", "track: blue", "track: green"),
        "canary.yaml": ("canary", "stable", "traffic: enabled"),
        "shadow-istio.yaml": ("mirror:", "aceest-fitness-shadow", "VirtualService"),
        "ab-ingress.yaml": ("canary-by-header", "X-ACEest-Variant", "aceest-fitness-b"),
        "rolling.yaml": ("RollingUpdate", "maxUnavailable: 0", "maxSurge: 1"),
    }

    for filename, fragments in expected.items():
        content = (STRATEGIES / filename).read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in content, f"{fragment!r} missing from {filename}"


def test_deployment_scripts_are_parameterized_and_can_rollback():
    deploy = (SCRIPTS / "deploy.sh").read_text(encoding="utf-8")
    rollback = (SCRIPTS / "rollback.sh").read_text(encoding="utf-8")
    powershell = (SCRIPTS / "deploy.ps1").read_text(encoding="utf-8")

    assert 'case "$STRATEGY"' in deploy
    assert 'kubectl' in deploy
    assert 'IMAGE="${2:-' in deploy
    assert 'kubectl rollout undo' in rollback
    assert 'param(' in powershell
    assert 'kubectl' in powershell


def test_smoke_and_rollback_scripts_have_failure_safe_shell_options():
    smoke = (SCRIPTS / "smoke-test.sh").read_text(encoding="utf-8")
    rollback = (SCRIPTS / "rollback.sh").read_text(encoding="utf-8")

    assert "set -euo pipefail" in smoke
    assert "set -euo pipefail" in rollback
    assert "--namespace aceest" in smoke


def test_all_kubernetes_yaml_is_parseable():
    manifests = list(BASE.glob("*.yaml")) + list(STRATEGIES.glob("*.yaml"))

    assert manifests
    for manifest in manifests:
        documents = list(yaml.safe_load_all(manifest.read_text(encoding="utf-8")))
        assert documents and all(document and "kind" in document for document in documents), manifest


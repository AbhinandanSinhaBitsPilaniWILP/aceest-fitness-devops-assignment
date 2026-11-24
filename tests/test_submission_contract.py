from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_all_supplied_application_versions_are_preserved():
    expected = {
        "Aceestver-1.0.py",
        "Aceestver-1.1.py",
        "Aceestver1.1.2.py",
        "Aceestver2.0.1.py",
        "Aceestver-2.1.2.py",
        "Aceestver-2.2.1.py",
        "Aceestver-2.2.4.py",
        "Aceestver-3.0.1.py",
        "Aceestver-3.1.2.py",
        "Aceestver-3.2.4.py",
    }

    assert {path.name for path in (ROOT / "legacy").glob("*.py")} == expected


def test_report_covers_submission_requirements_and_evidence_boundaries():
    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    evidence = (ROOT / "evidence/README.md").read_text(encoding="utf-8")

    for heading in (
        "Executive summary",
        "Architecture",
        "Requirements traceability",
        "Jenkins",
        "SonarQube",
        "Docker",
        "Kubernetes",
        "Deployment strategies",
        "Rollback",
        "Screenshots",
        "Links",
        "Submission checklist",
    ):
        assert heading in report
    assert "local verification" in report.lower()
    assert "external" in report.lower()
    assert "screenshot" in evidence.lower()
    assert "credentials" in evidence.lower()


def test_report_builder_and_capture_scripts_are_present():
    builder = (ROOT / "scripts/build_report.py").read_text(encoding="utf-8")
    capture_ps = (ROOT / "scripts/capture_evidence.ps1").read_text(encoding="utf-8")
    capture_sh = (ROOT / "scripts/capture_evidence.sh").read_text(encoding="utf-8")

    assert "REPORT.md" in builder
    assert "evidence/screenshots" in capture_ps
    assert "evidence/screenshots" in capture_sh


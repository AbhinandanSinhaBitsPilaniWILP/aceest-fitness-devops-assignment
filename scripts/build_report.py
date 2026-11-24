"""Build user-facing report copies without modifying the source report."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"
SOURCE = ROOT / "REPORT.md"


def build_report() -> tuple[Path, Path]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    markdown_path = OUTPUT / "DevOps_Assignment_Final_Report.md"
    html_path = OUTPUT / "DevOps_Assignment_Final_Report.html"
    content = SOURCE.read_text(encoding="utf-8")
    markdown_path.write_text(content, encoding="utf-8")
    html_path.write_text(
        "<!doctype html><meta charset='utf-8'><title>ACEest Fitness DevOps Assignment Report</title>"
        "<style>body{font-family:system-ui;max-width:1000px;margin:2rem auto;padding:0 1rem}"
        "pre{white-space:pre-wrap;line-height:1.5}h1{color:#0d5b6e}</style>"
        f"<h1>ACEest Fitness DevOps Assignment Report</h1><pre>{html.escape(content)}</pre>",
        encoding="utf-8",
    )
    return markdown_path, html_path


if __name__ == "__main__":
    for path in build_report():
        print(path)


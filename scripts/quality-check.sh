#!/usr/bin/env bash
set -euo pipefail

python -m pytest --cov=src/aceest --cov-report=xml --cov-report=term-missing
ruff check src tests scripts


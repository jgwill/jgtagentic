#!/bin/bash
# 🧠🌸🔮 Agentic Test Runner — Bash Ritual
# This script runs the agentic test suite and names the expected results for clarity and spiral anchoring.
. /opt/binscripts/load.sh

set -e
cd "$(dirname "$0")"
conda activate jgtagentic

EXPECTED="All tests should pass. You should see 5 passed for test_agentic_orchestrator.py and 1 passed for test_fdb_signals.py."

printf '\n🌸 Running pytest for jgtagentic...\n\n'
pytest --maxfail=1 --disable-warnings -v tests/

printf '\n🧠 Expected Results:\n%s\n' "$EXPECTED"

# FDBDataAnalyzer Capabilities

The `FDBDataAnalyzer` module parses cached CSV datasets under `data/current/cds` and exposes the last completed bar for analysis. It ships with a CLI that prints JSON summaries for quick inspection.

## Features
- **get_last_two_bars** — returns the last two rows of a dataset, ensuring the second-to-last row is the completed candle.
- **analyze_latest** — produces a dictionary of FDB metrics for the most recent completed bar.
- **CLI** — invoke with `fdb-data-analyzer -i EUR-USD -t H1` to print JSON output.

### Example

```bash
fdb-data-analyzer -i EUR-USD -t H1
```
This prints the latest completed bar's FDB metrics so other agents can react without running the full scanner.

## Tests
- `tests/test_data_analyzer.py` verifies bar retrieval and analysis results.
- `tests/test_agentic_orchestrator.py` exercises the analyzer within the orchestrator spiral.

This document is indexed at `Workspace.jgwill.jgtagentic:50.250618.files.docs.FDBDataAnalyzer_CLI_and_Tests.md`.

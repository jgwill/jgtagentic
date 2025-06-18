# Agentic Orchestrator Test Coverage

`tests/test_agentic_orchestrator.py` validates how our modular agents interact in a minimal spiral. The suite ensures every step of the workflow can be exercised without the full trading stack.

## Covered Capabilities
- **EntryScriptGen** — creates bash entry scripts embedding the signal instrument and timeframe.
- **CampaignEnv** — prepares a campaign directory with placeholder files.
- **FDBScanAgent** — runs timeframe scans in dry-run mode or executes real scans when jgtml is available.
- **AgenticDecider** — inspects the signal and returns a decision dictionary.
- **Integration Spiral** — orchestrates the above modules to mimic a real campaign setup.

Each test prints or asserts minimal output so other agents can reuse the workflow. This document is indexed at `Workspace.jgwill.jgtagentic:50.250618.files.docs.Agentic_Orchestrator_and_Tests.md`.

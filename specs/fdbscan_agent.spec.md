# FDBScanAgent Specification

## Purpose

`FDBScanAgent` performs fractal divergent bar scanning within the `jgtagentic` framework. It bridges the original Bash scanning rituals and the `jgtml` library, enabling automated signal collection that feeds into larger workflows.

## Key Behaviors

- Scan a single timeframe with optional instrument filtering.
- Execute the canonical scan sequence (H4 → H1 → m15 → m5).
- Support a `--real` flag that toggles between dry-run mode and true invocation of `jgtml.fdb_scanner_2408`.
- Provide a CLI interface for direct invocation.

## Integration Notes

- Upcoming FTS database schemas will store scan results and should be queried by `FDBScanAgent` once integrated.
- The agent is used by `agentic_entry_orchestrator` and the project CLI.
- Future reinforcement learning modules may adjust scan parameters based on feedback from the Trading Echo Lattice.


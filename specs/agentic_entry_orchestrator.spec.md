# Agentic Entry Orchestrator Specification

## Purpose

The orchestrator coordinates the full signal-to-entry workflow. It prepares the campaign environment, generates scripts, triggers scans, and records decisions, acting as the bridge between lower-level agents.

## Key Behaviors

- Load a JSON file of signals and iterate through them.
- Invoke `CampaignEnv`, `EntryScriptGen`, `FDBScanAgent`, and `AgenticDecider` in sequence.
- Optionally run external shell commands (`wtf`) for timeframe orchestration.
- Maintain a log file for each run.

## Integration Notes

- Receives signals produced by FTS processes or manual imports.
- Should be callable via `jgtagenticcli orchestrate` or as a standalone module.
- Future enhancements may include reading/writing from the Trading Echo Lattice or triggering `JupyterBookAgent` updates.


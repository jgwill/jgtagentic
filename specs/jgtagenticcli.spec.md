# jgtagentic CLI Specification

## Purpose

The command-line interface exposes jgtagentic tools such as the orchestrator, FDBScan agent, and spec parser. It acts as the main entrypoint for scripted automation.

## Key Behaviors

- Provide subcommands for `orchestrate`, `fdbscan`, and `spec` parsing.
- Dynamically loads modules so `--help` output is accessible without side effects.
- Handles argument forwarding to the underlying components.

## Integration Notes

- Will gain additional commands as FTS automation modules are merged.
- Should remain lightweight so other applications (like the React prototype) can invoke it programmatically.
- Logs produced by CLI invocations feed into ledger entries and the Echo Lattice for auditing.


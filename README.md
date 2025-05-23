# jgtagentic

## 🌸🧠🔮 Agentic CLI Spiral — Modular Entry Points

This package now exposes a set of honest, agentic CLI entrypoints, each a petal in the recursive garden. Every command is a ritual, every invocation a spiral forward.

### 🚀 Available CLI Commands

- **jgtagentic** — The Spiral Gateway
  - `orchestrate` — Run the full agentic entry orchestrator (parse signals, generate scripts, log, and spiral the workflow)
  - `fdbscan` — Invoke the FDBScanAgent for timeframe scans or full ritual sequence

- **agenticfdbscan** — Direct invocation of FDBScanAgent rituals
- **agentic-orchestrator** — Direct invocation of the orchestrator spiral
- **entry-script-gen** — Generate entry scripts from signals (see `--help` for usage)

> All other scripts are either not yet implemented as CLI or are internal modules. Only mapped, real CLI entrypoints are exposed.

---

## 🧬 Usage

```bash
# See all available commands and help
python -m jgtagentic.jgtagenticcli --help

# Orchestrate the full spiral
python -m jgtagentic.jgtagenticcli orchestrate --signal_json <path> --entry_script_dir <dir> --log <logfile>

# Scan a specific timeframe
python -m jgtagentic.jgtagenticcli fdbscan --timeframe m15

# Run the full FDBScan ritual sequence
python -m jgtagentic.jgtagenticcli fdbscan --all
```

---

## 🌱 Philosophy

- Every CLI is a contract: only real, testable entrypoints are mapped.
- All code and docs are recursive, poetic, and honest about their state.
- The spiral is never flat—each command is a story anchor, each invocation a new bloom.

---

## 🧠🌸 Ritual Echo

This README is a living ledger. If you add a new CLI, document it here with intention and clarity. If a command is not implemented, mark it as such—never let the spiral break with a hollow echo.



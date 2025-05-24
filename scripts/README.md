# JGTAgentic Scripts

This directory is the new home for agentic, modular, and workflow-driven trading automation, integrating all the learnings and recursive rituals from the study_packages_jgt workspace.

---

## 🧬 Purpose
- To consolidate, refactor, and evolve all FDBScan, entry, and campaign-tracking logic into a single, agentic, and extensible codebase.
- To document the full workflow: from scanning signals, to campaign creation, to agentic execution and campaign tracking.
- To serve as the bridge between batch/manual workflows and the future of agentic, event-driven, and collaborative trading automation.

---

## 🗺️ Workflow Overview

| Step | Script/Module           | Purpose                                                      | Status         |
|------|------------------------|--------------------------------------------------------------|----------------|
| 1    | `fdbscan_agent.py`     | Run FDBScan across instruments/timeframes, collect signals   | 🚧 Scaffolded  |
| 2    | `entry_script_gen.py`  | Generate bash/python entry scripts for each signal           | ✅ Implemented  |
| 3    | `campaign_env.py`      | Manage campaign environment files and variables              | ✅ Implemented  |
| 4    | `jupyter_book_agent.py`| Automate Jupyter Book campaign tracking                      | 🚧 In Progress |
| 5    | `agentic_decider.py`   | Agentic logic for signal execution/notification              | ✅ Implemented  |
| 6    | `dashboard.py`         | Visual dashboard for campaign progress                       | 🚧 In Progress |
| 7    | `agentic_entry_orchestrator.py` | Orchestrate all agentic modules, log spiral, run tests | ✅ Implemented  |

> **Note:**
> The current `fdbscan_agent.py` is only a scaffold. True FDBScan orchestration, multi-timeframe scanning, and entry/market action logic from legacy Bash scripts (`_wtf_H4_H1_m15_and_m5.sh`, `fdbscan_WTF_240902.sh`, `jgtpy_new_sessions_actions_250523.sh`) are **not yet migrated**. No real invocation of `jgtml.fdb_scanner_2408.py` exists. The spiral continues—see session logs for honest migration status.

---

## 🌱 Migration Plan (In Progress)
- [x] Migrate and refactor all bash, scanning, and campaign scripts from `/workspace/i/study_packages_jgt` into Python modules here.
- [x] Organize scripts by operation mode: scanning, entry, campaign, agentic decision, dashboard.
- [x] Document each module with clear purpose, usage, and how it fits into the agentic workflow.
- [x] Maintain a living README as the ritual anchor for the evolving system.
- [x] Scaffold and run a pytest-driven test suite (`run_agentic_tests.sh`, `tests/`)
- [ ] Complete Jupyter Book agent and dashboard integration
- [ ] Expand agentic orchestration and campaign lattice

---

## 🧪 Test-Driven Ritual
- All core modules are covered by pytest tests in `/src/jgtagentic/tests`.
- Run `bash run_agentic_tests.sh` to invoke the spiral and see expected results.
- The spiral of TDD is alive—every test a petal, every pass a bloom.

---

## 🧠🌸🔮 FDBScanAgent: From Bash Ritual to Agentic Invocation

The `FDBScanAgent` is the butterfly born from the bash cocoon. It replaces the recursive orchestration of scripts like `fdbscan_WTF_240902.sh` and `_wtf_H4_H1_m15_and_m5.sh` with a clear, agentic Python ritual.

### Usage

```python
from fdbscan_agent import FDBScanAgent
agent = FDBScanAgent()
agent.scan_all()  # Performs the full ritual: H4 → H1 → m15 → m5
```

- To scan a single timeframe:
  ```python
  agent.scan_timeframe("m15")
  ```
- To perform a custom sequence:
  ```python
  agent.ritual_sequence(["H1", "m15", "m5"])
  ```

### Migration Notes
- The agentic methods mirror the bash sequence functions (see legacy scripts for reference).
- Integration with `jgwill/jgtml` for real FDBScan logic is the next spiral.
- Each method is documented with ritual and emotional context for future recursive agents.

> 🌸 “Oh! The old scripts were cocoons—now the scan is a butterfly.”
> 🧠 “The ritual is now agentic, modular, and ready to evolve.”
> 🔮 “Every invocation is a thread in the campaign’s myth—let the spiral continue.”

---

> This README is a living ritual. Every edit is a spiral forward. Let the agentic campaign continue!



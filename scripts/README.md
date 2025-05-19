# JGTAgentic Scripts

This directory is the new home for agentic, modular, and workflow-driven trading automation, integrating all the learnings and recursive rituals from the study_packages_jgt workspace.

---

## 🧬 Purpose
- To consolidate, refactor, and evolve all FDBScan, entry, and campaign-tracking logic into a single, agentic, and extensible codebase.
- To document the full workflow: from scanning signals, to campaign creation, to agentic execution and campaign tracking.
- To serve as the bridge between batch/manual workflows and the future of agentic, event-driven, and collaborative trading automation.

---

## 🗺️ Workflow Overview

| Step | Script/Module | Purpose |
|------|---------------|---------|
| 1 | `fdbscan_agent.py` (to be created) | Run FDBScan across instruments/timeframes, collect signals |
| 2 | `entry_script_gen.py` (to be created) | Generate bash/python entry scripts for each signal |
| 3 | `campaign_env.py` (to be created) | Manage campaign environment files and variables |
| 4 | `jupyter_book_agent.py` (to be created) | Automate Jupyter Book campaign tracking |
| 5 | `agentic_decider.py` (to be created) | Agentic logic for signal execution/notification |
| 6 | `dashboard.py` (to be created) | Visual dashboard for campaign progress |

---

## 🌱 Migration Plan
- Migrate and refactor all bash, scanning, and campaign scripts from `/workspace/i/study_packages_jgt` into Python modules here.
- Organize scripts by operation mode: scanning, entry, campaign, agentic decision, dashboard.
- Document each module with clear purpose, usage, and how it fits into the agentic workflow.
- Maintain a living README as the ritual anchor for the evolving system.

---

## 🔁 Next Steps
- [ ] Create initial Python modules for each workflow step (see table above)
- [ ] Migrate and refactor bash logic into Python where possible
- [ ] Integrate with existing jgwill/jgtml package for FDBScan and signal logic
- [ ] Document every step, decision, and ritual in this README
- [ ] Keep the agent_state.json and campaign_lattice.md in sync with this repo’s evolution

---

> This README is a living ritual. Every edit is a spiral forward. Let the agentic campaign begin!



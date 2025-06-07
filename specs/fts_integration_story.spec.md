# FTS Integration Story

This living story connects all specifications under `specs/` into a single narrative. It outlines how the upcoming **Fractal Trading System** (FTS) pieces will merge into `jgtagentic`.

## Prelude
- `jgtml_integration.spec.md` anchors dependency expectations for using the `jgwill/jgtml` package. FTS scanning agents rely on this compatibility.
- `fractal-database.spec.md` describes the QuestDB and Pinecone setup for storing fractal patterns and signals.
- `reinforcement-learning.spec.md` defines RLlib PPO usage and how drift detection ties into trade decisions.
- `use-case-automation.spec.md` covers automated workflows like scanning and backtesting.
- `seven-step-process.spec.md` translates the FTS workflow into actionable phases for this repo.

## How the Pieces Fit
1. **Database** — Signals captured from `jgtml` flow into QuestDB and Redis as outlined in `fractal-database.spec.md`.
2. **RL Agents** — Scripts in `ftsrl/` will train using the datasets produced by step 1, per `reinforcement-learning.spec.md`.
3. **Automation** — Batch scanners and orchestrator scripts rely on `use-case-automation.spec.md` to produce entry scripts and update the dashboard.
4. **Documentation** — `documentation.spec.md` and `jupyter_book_agent.spec.md` guide contributors to keep the Jupyter Book and Sphinx docs in sync with code changes.
5. **CLI & Modules** — Specs such as `jgtagenticcli.spec.md`, `agentic_entry_orchestrator.spec.md`, and `dashboard.spec.md` describe command-line tools and services that wrap the new components.

## Outcome
When all specs are implemented, contributors will be able to:
- Ingest fractal market data, store it in QuestDB, and query similar patterns via Pinecone.
- Train RL agents that adapt to market drift and feed decisions back into the orchestrator.
- Automate scanning, backtesting, and live execution while logging results for analysis.
- Generate documentation explaining every step of the trading spiral.

This story is a compass. Each specification referenced above is a chapter, guiding developers toward a cohesive Fractal Trading System within the jgtagentic codebase.

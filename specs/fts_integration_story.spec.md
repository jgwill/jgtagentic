# FTS Integration Story

Within **jgtagentic** rests a garden of intentions. Each specification under `specs/` is a seed awaiting the Fractal Trading System (FTS) to bring soil and sunlight. This story traces how those seeds will sprout into a unified trading spiral.

## Prologue
- `jgtml_integration.spec.md` anchors our dependency on `jgwill/jgtml`. Without this root, FTS scanners cannot grow.
- `fractal-database.spec.md` sketches the terraces of QuestDB and Pinecone where patterns and signals will live.
- `reinforcement-learning.spec.md` reveals how RLlib PPO agents will wander through those patterns, learning their rhythm and drifting with the market winds.
- `use-case-automation.spec.md` covers the daily rituals—scans, backtests, and orchestrated tasks—that keep the system moving.
- `seven-step-process.spec.md` transforms the abstract FTS workflow into steps we can follow right here.

## Weaving the Chapters
1. **Database Roots** — Signals from `jgtml` flow into QuestDB and Redis, grounding the system in fast persistence.
2. **Learning Branches** — Scripts in `ftsrl/` train on that data, as detailed in `reinforcement-learning.spec.md`.
3. **Automation Leaves** — Batch scanners and orchestrator scripts rely on `use-case-automation.spec.md` to produce entry scripts and feed the dashboard.
4. **Documentation Blossoms** — `documentation.spec.md` and `jupyter_book_agent.spec.md` keep our knowledge garden tidy and accessible.
5. **CLI Pathways** — Tools described in `jgtagenticcli.spec.md`, `agentic_entry_orchestrator.spec.md`, and `dashboard.spec.md` guide users through the maze.

## Harvest
When all chapters converge, contributors will:
- Ingest fractal data, store it in QuestDB, and search for echoes in Pinecone.
- Train RL agents that adapt to market changes and guide the orchestrator.
- Automate scanning, backtesting, and live execution while logging every spiral.
- Document each growth ring in the Jupyter Book for others to study.

This story is both compass and invitation. As the FTS repository sends new pieces, they will find ready soil here—each spec a plot, each module a sprout—until `jgtagentic` blossoms into a full Fractal Trading System.

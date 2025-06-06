# Project Roadmap

This roadmap highlights upcoming features for the agentic trading tools.

## Intent-Driven Trading (Planned)

- **IntentSpecParser** — parse `.jgtml-spec` files describing trading intent and signals.
- **CLI Integration** — new `spec` command in `jgtagenticcli` to load and echo intent specifications.
- **Future Goals**
  - Map parsed intent directly into FDBScan and entry workflows.
  - Store intent-driven performance metrics for recursive learning.
  - Develop a translator LLM that converts trader narration into `.jgtml-spec` files (see `docs/Trader_Analysis_to_Spec.md`).

## Fractal Trading System Integration

- Integrate time-series storage via QuestDB and vector matching via Pinecone.
- Add reinforcement learning agents using RLlib PPO with drift detection (EDDM).
- Implement automation modules for scanning, backtesting, and real-time trading as described in the FTS Enhancement Blueprint.


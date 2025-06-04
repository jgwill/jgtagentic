# Project Roadmap

This roadmap highlights upcoming features for the agentic trading tools.

## Intent-Driven Trading (Planned)

- **IntentSpecParser** — parse `.jgtml-spec` files describing trading intent and signals.
- **CLI Integration** — new `spec` command in `jgtagenticcli` to load and echo intent specifications.
- **Future Goals**
  - Map parsed intent directly into FDBScan and entry workflows.
  - Store intent-driven performance metrics for recursive learning.
  - Develop a translator LLM that converts trader narration into `.jgtml-spec` files (see `docs/Trader_Analysis_to_Spec.md`).


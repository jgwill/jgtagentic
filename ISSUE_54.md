# Issue 54 — Agentic Integration of ML Signals

This issue tracks the *jgtagentic* side of the ML-powered trading enhancement driven by *jgtml* (Issue 62).

## Objectives
1. Receive higher-level ML signals (prediction, confidence, metadata) and incorporate them when generating entry orders.
2. Extend CLI & dashboard to display ML diagnostics.
3. Ensure backward compatibility: if no ML prediction is available, fall back to current rule-based flow.

## Task Board

- [ ] Data Contract
  - [ ] Define JSON schema exchanged between jgtservice ↔ jgtagentic
  - [ ] Implement pydantic model in `agentic_entry_orchestrator.py`
- [ ] Entry Logic
  - [ ] Inject prediction into `fdbscan_agent.py` decision path
  - [ ] Add configurable weight/threshold via CLI flag
- [ ] Dashboard
  - [ ] Display prediction & confidence next to signal summary
  - [ ] Provide toggle to show rule-only vs ML-assisted view
- [ ] CLI Enhancements
  - [ ] `jgtagenticcli --ml` to enable ML integration
  - [ ] Forward unknown flags to `jgtservice predict` endpoint
- [ ] Testing
  - [ ] Unit tests for contract parsing
  - [ ] Integration test with mocked jgtservice
- [ ] Documentation
  - [ ] Update `ROADMAP.md`
  - [ ] Add examples in `docs/`

---
Sync regularly with [Issue 62](../jgtml/ISSUE_62.md) for upstream progress.




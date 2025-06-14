## AGENTS Guidelines

This file explains guidelines for repository contributions. Each code change must be accompanied by a ledger entry in `codex/ledgers` describing agents, narrative, routing, timestamp, user input, and future scene enablement. Keep tests passing (`pytest -q`). Document narrative updates in `narrative-map.md`. Provide justification for modifications here when new features are added.

### Recent Updates
- Adjusted tests for `AgenticDecider` to check `decision["decision"]` after new structured return was introduced.
- Added ledger entries describing search operations and test updates.
- Updated `narrative-map.md` with commit history.

These guidelines ensure traceability for other LLMs reviewing this repo.

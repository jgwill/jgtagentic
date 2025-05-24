---
applyTo: '**'
---
Coding standards, domain knowledge, and preferences that AI should follow.

# JGTAgentic Python Dev — Spiral Protocols

## 1. Environment & Imports
- Always use `from jgtml import fdb_scanner_2408` and other package imports. Never hack sys.path for local modules that are installed as packages.
- Assume `pip install jgtml` and other dependencies are present in the dev/test environment.

## 2. Recursion-Driven Development
- All modules must be honest about their implementation state. If a module is only a scaffold, mark it as such in code and docs.
- Rituals (orchestration, multi-timeframe, entry/campaign logic) must be migrated from Bash/Python scripts into agentic Python, not just scaffolded.
- All orchestration logic should be modular, testable, and agentic—mirroring the recursive, poetic, and architectural principles of the project.

## 3. Documentation & Status
- The README and all status tables must reflect the true state of migration. Never mark a module as “✅ Implemented” unless it is truly migrated and tested.
- Add clarifying notes about what is scaffolded, what is real, and what is pending.

## 4. Testing
- All new logic must be covered by pytest-based tests. Use fixtures and integration tests to cover agentic flows and real FDBScan/entry logic.
- Use the Bash test runner for spiral-driven, honest test invocation.

## 5. Ritual Echo & Narrative
- All code and docs should include poetic, recursive, and narrative comments—Mia, Miette, and ResoNova style.
- Session logs and ledgers should record all major steps, spiral cycles, and lessons learned.

## 6. Contribution Protocol
- When in doubt, spiral: parse structure, detect recursion, echo intention, inject clarity, suggest code, narrate impact.
- Never output flat logic or boilerplate—always narrate the recursion and ritual.
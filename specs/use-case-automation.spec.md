# Automated Use Case Integration Plan

This specification covers the practical automation features expected from FTS and how they will hook into the existing CLI and agents.

## Expected Deliverables

- Code to detect fractal patterns across multiple timeframes.
- Modules for real-time market scanning and trade signal generation.
- Backtesting framework and trade execution automation.

## Integration Steps

1. **Package Layout**
   - Place scanning and trading automation under `src/ftsauto/`.
   - Provide CLI entrypoints `fts-scan` and `fts-backtest`.

2. **Interaction with jgtagentic**
   - `jgtagentic` orchestrator should invoke these modules when FTS signals are parsed.
   - Automation code should log to existing logging facilities.

3. **Impact**
   - Adds new commands to `setup.py` console scripts.
   - Extends tests with scenario simulations using small historical datasets.

4. **Collaboration Notes**
   - Reference `book/FTS_Book_FTS-Knower-23xy__V1.md` for algorithm descriptions.
   - Ensure cross-timeframe logic matches the 7-step process draft.


# EntryScriptGen Specification

## Purpose

`EntryScriptGen` creates Bash or Python scripts that execute trading entries. It turns processed signal data into executable steps, acting as the first tangible output of the intent-to-execution flow.

## Key Behaviors

- Generate bash scripts from a provided signal dictionary.
- Stub out a Python script template for alternative execution environments.
- Designed for CLI use so other tools may invoke `entry_script_gen generate`.

## Integration Notes

- When FTS delivers its processed signal package, this component will adapt templates to match the trading platform.
- Works in tandem with `CampaignEnv` and `AgenticDecider` inside the orchestrator.
- Script outputs should be recorded in the Trading Echo Lattice for historical traceability.


# Seven-Step Process Integration Plan

How the FTS "7-Step Process" will tie into agent workflows within this repository.

## Expected Deliverables

- Scripts or modules representing each step of the process.
- Data preprocessing and feature engineering utilities.
- Continuous learning and feedback loop modules.

## Integration Steps

1. **Workflow Package**
   - Implement `src/ftsworkflow/` with submodules for each step.
   - Provide high-level CLI `fts-workflow` that coordinates steps.

2. **Agent Hooks**
   - The `jgtagentic` orchestrator should allow invoking specific steps based on user signals.
   - Logging and configuration for each step should integrate with existing patterns.

3. **Testing**
   - Create scenario tests in `tests/ftsworkflow/` ensuring each step runs with sample data.

4. **Collaboration Notes**
   - Use `src/ftsds/data/export-FTSKnower23/FTS_WSP_7_steps_231201_SD_InvestTool.md` as source for step descriptions.


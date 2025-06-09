# CampaignEnv Specification

## Purpose

`CampaignEnv` manages directories and environment files for trading campaigns. It ensures that each signal has a clean workspace and consistent configuration before execution.

## Key Behaviors

- Prepare or create directories for a new campaign.
- Maintain environment variables or state files for each run.
- Provide simple logging of setup actions.

## Integration Notes

- Will store state alongside FTS-generated datasets so agents can resume or audit previous campaigns.
- Used by `agentic_entry_orchestrator` before script generation and scanning.
- Future versions may coordinate with database migrations described in the FTS specs.


# AgenticDecider Specification

## Purpose

`AgenticDecider` encapsulates decision logic for whether a detected signal should trigger a trade. It acts as the "oracle" within the jgtagentic stack.

## Key Behaviors

- Evaluate a signal dictionary and produce a textual decision.
- Log each decision to aid reproducibility and debugging.
- Placeholder implementation for future reinforcement learning policies.

## Integration Notes

- Intended to consume RL models and reward functions defined by the FTS project.
- Works with `FDBScanAgent` output and feeds results to `Dashboard` or logging services.
- Decisions should be archived in the Trading Echo Lattice for long-term analysis.


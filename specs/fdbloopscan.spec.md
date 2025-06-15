# FDBLoopScan Specification

## Purpose

`fdbloopscan.py` is a minimal script intended to wrap FDBScan execution in a loop. It is currently a placeholder for more robust batch-scanning utilities.

## Key Behaviors

- Call into `jgtml` scanning functions repeatedly over a predefined set of inputs.
- Replace shell-based looping scripts from earlier prototypes.

## Integration Notes

- May be deprecated in favor of `batch_fdbscan.py` once FTS integration stabilizes.
- Serves as a simple example script when exploring automated scan loops in testing environments.


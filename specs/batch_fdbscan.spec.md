# Batch FDBScan Runner Specification

## Purpose

`batch_fdbscan.py` loops over instruments and timeframes to automate bulk scanning. It replicates the legacy shell scripts in a Python-friendly form.

## Key Behaviors

- Accept lists of instruments and timeframes.
- Invoke `FDBScanAgent` for each combination, writing logs to disk.
- Honour the `JGT_CACHE` environment variable and produce markdown logs for other tools to consume.

## Integration Notes

- Useful for populating the FTS database with historical patterns.
- Logs generated here are a primary data source for the trading dashboard and the Jupyter Book.
- Should run inside CI or scheduled jobs once the RL feedback loop is established.


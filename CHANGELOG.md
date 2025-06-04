# Changelog

## [0.0.3] - 2025-06-04
### Added
- `batch_fdbscan.py` replicating the legacy shell script to scan instruments and timeframes.
- Optional placeholder mode in `FDBScanAgent` when `jgtml` is unavailable.

### Changed
- `FDBScanAgent` now accepts an instrument and prints actions when real scanning is disabled.
- `agentic_entry_orchestrator.py` imports packages relatively.
- Tests import modules from the package.


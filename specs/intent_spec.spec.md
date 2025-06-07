# IntentSpecParser Specification

## Purpose

`IntentSpecParser` reads `.jgtml-spec` files and extracts structured signal definitions. It is a lightweight gateway between human-written intent and automated processing.

## Key Behaviors

- Load YAML or JSON spec files from disk.
- Return signal dictionaries via the `signals()` helper method.
- Designed for extension as new fields or validation rules emerge.

## Integration Notes

- Parses output from the Trader Intent prototype in `agentictraderintenttojgtmlspec2chatpto250605`.
- Downstream services such as `FDBScanAgent` and RL modules interpret the parsed signals.
- Future versions may validate specs against schemas provided by the FTS repository.


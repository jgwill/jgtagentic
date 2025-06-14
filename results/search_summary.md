# Search Results - jgtagentic repo

## FDB Scanner references
- `ROADMAP.md` line 10: Map parsed intent directly into FDBScan workflows.
- `INTEGRATION_ROADMAP.md` lines 33-155: describes Enhanced FDB Scanner with intent context.
- `scripts/fdbscan_m15_m5.sh`: script uses `fdbscan` command.
- `jgtagentic/jgtagenticcli.py`: CLI includes enhanced FDBScan features.

## CLI file
`jgtagentic/jgtagenticcli.py` implements subcommands like `orchestrate`, `fdbscan`, `observe`, `spec`, `campaign`. Supports observation-based scanning and spec parsing.

## Intent Spec connection
`intent_spec.py` (not shown) presumably parses YAML spec. `jgtagenticcli` loads `IntentSpecParser`.


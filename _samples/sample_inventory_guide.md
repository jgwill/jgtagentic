# Sample Inventory Mapping

This document summarizes the sample Jupyter Book directories listed in [CampaignLauncher-fdbscan.jgtnewsession.jupyterbook.240911000713.filelist.md](CampaignLauncher-fdbscan.jgtnewsession.jupyterbook.240911000713.filelist.md) and maps each major file set to the Bash functions from `jgt_new_sessions_actions_250523.sh` that generated them.

## Session Directories
- `samples/trading/240822190651`
- `samples/trading/240829114509`

## Function Origins
| Script Function | Files/Directories Generated |
|-----------------|-----------------------------|
| `_jgtnewsession_book_create` | Creates the base Jupyter Book folder and default files (`_config.yml`, `_toc.yml`, `intro.md`, etc.) under `samples/trading/<tlid_id>` |
| `jgtinitsession_dir` | Initializes `charts/`, `output/`, `data/`, `.jgt` and copies template notebooks, markdown pages, and placeholder images for all timeframes |
| `_jgtsession_migrate_signal` | Copies any existing signal files to `/tmp/jgtsession/<tlid_id>` (not visible in the sample) |
| `_jgtnewsession_create_env` | Generates `.jgt/env.sh` inside each session folder, capturing entry parameters |
| `_jgtsession_entry_ordering` | Writes `.jgt/entry.sh` and logs the executed order command to `output/o.txt` |
| `_jgtnewsession_post_created` | Placeholder for workspace and book build actions (no direct files shown) |

Each session folder contains the artifacts from these steps: environment files, entry scripts, charts, notebooks, and data captured when the session was created.

## jgtapp Commands and JSON Outputs

The `jgtnewsession` workflow ultimately relies on the `jgtapp` CLI (from
`jgtml.jgtapp`) to interact with the trading backend. When
`_jgtsession_entry_ordering` runs, it invokes `fxaddorder` which generates
JSON logs in `data/jgt/`. Examples include:

- `fxaddorder_69543300.json` for the order placed in session `240822190651`.
- `fxaddorder_170114197.json` for the order placed in session `240829114509`.

Further JSON files like `trade_<id>.json` or `fxtransact_<id>.json` appear when
`jgtapp fxtr`, `jgtapp fxrmtrade`, or other commands execute from notebooks or
follow-up scripts. Values stored in `.jgt/env.sh` (such as `OrderID` and
`trade_id`) are used by these commands to manage open positions.

### Notebook Integration

The session notebooks (`jgtaction.ipynb`) import `jgtml.jgtapp` functions such as
`fxaddorder`, `fxrmtrade`, and `fxmvstopfdb` to execute trading actions directly
from Python. Environment values from `.jgt/env.sh` provide the IDs and
parameters for these calls, ensuring that notebook execution mirrors the CLI.

### CLI Commands in `entry.md`

Within each session's `entry.md`, a code block lists the commands that ran when
the session was created:

```
#fxtr -id $OrderID $demo_arg
#fxrmorder -id $OrderID $demo_arg
#fxclosetrade -tid $trade_id $demo_arg
#fxtr -id $OrderID $demo_arg
#jgtapp fxwatchorder -id $OrderID  -d $bs \$demo_arg
#jgtapp fxmvstop -tid $trade_id -x $1 $demo_arg
#jgtapp fxrmtrade -tid $trade_id  $demo_arg
#jgtapp fxmvstopgator -tid $trade_id -i $instrument -t $timeframe --lips $demo_arg
#jgtapp fxmvstopfdb -tid $trade_id -i $instrument -t $timeframe  $demo_arg
#jgtapp fxstatusorder -id $OrderID  $demo_arg
```

This sequence documents the raw `jgtapp` interactions that produced the JSON
files in `data/jgt/` and serves as a reference for replaying the workflow.

Together, the CLI scripts and notebook calls explain how the JSON data in
`data/jgt/` was produced during each sample session.


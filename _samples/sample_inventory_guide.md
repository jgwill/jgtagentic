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


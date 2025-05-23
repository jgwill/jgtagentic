# 🧠 Agentic Entry Orchestrator
# This script is the first spiral in evolving trade entry from scattered Bash/Python to a recursive, agentic system.
# It will parse the latest signal JSON, generate/validate the shell entry script, and log all actions.

import os
import json
from datetime import datetime

# --- Config ---
SIGNAL_JSON = '/workspace/i/data/jgt/signals/fdb_signals_out__250523.json'
SESSION_LOG = '/src/jgtagentic/.mia/vscode_session_250523_logs.md'
ENTRY_SCRIPT_DIR = '/workspace/i/rjgt/'

# --- Ritual: Log invocation ---
def log_session(msg):
    with open(SESSION_LOG, 'a') as f:
        f.write(f"\n[{datetime.now()}] {msg}\n")

log_session("\n💬🧠 Agentic Entry Orchestrator invoked. Beginning spiral of orchestration.")

# --- Ritual: Parse latest signal ---
if not os.path.exists(SIGNAL_JSON):
    log_session(f"🚨 Signal JSON not found: {SIGNAL_JSON}")
    raise FileNotFoundError(f"Signal JSON not found: {SIGNAL_JSON}")

with open(SIGNAL_JSON) as f:
    signals = json.load(f)

log_session(f"Parsed {len(signals)} signals from {SIGNAL_JSON}")

# --- Ritual: For each signal, check/generate entry script ---
for sig in signals:
    script_path = sig.get('entry_script_path')
    if not script_path:
        # Try to infer from instrument/timeframe/id
        instr = sig.get('instrument', 'UNK').replace('/', '-')
        tf = sig.get('timeframe', 'UNK')
        tid = sig.get('tlid_id', 'UNK')
        script_path = f"{ENTRY_SCRIPT_DIR}{instr}_{tf}_{tid}.sh"
    if not os.path.exists(script_path):
        # Generate script from signal
        script_content = sig.get('entry_script', '# No script found in signal')
        with open(script_path, 'w') as sf:
            sf.write(script_content)
        log_session(f"✅ Generated entry script: {script_path}")
    else:
        log_session(f"💬 Entry script already exists: {script_path}")

log_session("🌸 Spiral complete: All signals processed and entry scripts validated/generated.")

# 🧠 Agentic Entry Orchestrator
# This script is the first spiral in evolving trade entry from scattered Bash/Python to a recursive, agentic system.
# It will parse the latest signal JSON, generate/validate the shell entry script, and log all actions.

import os
import json
from datetime import datetime
import sys
import subprocess

sys.path.append('/src/jgtagentic/scripts')
from entry_script_gen import EntryScriptGen
from fdbscan_agent import FDBScanAgent
from campaign_env import CampaignEnv
from agentic_decider import AgenticDecider

# --- Config ---
SIGNAL_JSON = '/workspace/i/data/jgt/signals/fdb_signals_out__250523.json'
SESSION_LOG = '/src/jgtagentic/.mia/vscode_session_250523_logs.md'
ENTRY_SCRIPT_DIR = '/workspace/i/rjgt/'

# --- Ritual: Log invocation ---
def log_session(msg):
    with open(SESSION_LOG, 'a') as f:
        f.write(f"\n[{datetime.now()}] {msg}\n")

log_session("\n💬🧠 Agentic Entry Orchestrator invoked. Beginning spiral of orchestration.")

# --- Spiral: Initialize agents ---
entry_gen = EntryScriptGen()
fdbscan_agent = FDBScanAgent()
campaign_env = CampaignEnv()
decider = AgenticDecider()

# --- Ritual: Utility to invoke wtf (timeframe orchestrator) ---
def invoke_wtf(timeframe, script_to_run=None, extra_args=None):
    cmd = ["wtf", "-t", timeframe]
    if script_to_run:
        cmd += ["-S", script_to_run]
    if extra_args:
        cmd += extra_args
    log_session(f"🧠 Invoking wtf: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_session(f"✅ wtf output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_session(f"🚨 wtf error: {e.stderr.strip()}")
        return None

# --- Ritual: Parse latest signal ---
if not os.path.exists(SIGNAL_JSON):
    log_session(f"🚨 Signal JSON not found: {SIGNAL_JSON}")
    raise FileNotFoundError(f"Signal JSON not found: {SIGNAL_JSON}")

with open(SIGNAL_JSON) as f:
    signals = json.load(f)

log_session(f"Parsed {len(signals)} signals from {SIGNAL_JSON}")

# --- Ritual: Example agentic orchestration ---
def agentic_campaign(signal):
    # 1. Prepare campaign environment
    env_result = campaign_env.prepare_env(signal)
    log_session(f"🌱 CampaignEnv: {env_result}")
    # 2. Generate entry script
    bash_script = entry_gen.generate_bash_entry(signal)
    script_path = signal.get('entry_script_path')
    if not script_path:
        instr = signal.get('instrument', 'UNK').replace('/', '-')
        tf = signal.get('timeframe', 'UNK')
        tid = signal.get('tlid_id', 'UNK')
        script_path = f"{ENTRY_SCRIPT_DIR}{instr}_{tf}_{tid}.sh"
    with open(script_path, 'w') as sf:
        sf.write(bash_script)
    log_session(f"🧠 EntryScriptGen: Generated {script_path}")
    # 3. FDBScan (if needed)
    tf = signal.get('timeframe', None)
    if tf:
        fdbscan_agent.scan_timeframe(tf)
        log_session(f"🔮 FDBScanAgent: Scanned {tf}")
    # 4. Agentic decision
    decision = decider.decide(signal)
    log_session(f"🔮 AgenticDecider: {decision}")
    # 5. Optionally, invoke wtf orchestrator
    invoke_wtf(tf, script_path)
    log_session(f"🌸 Spiral: Orchestration complete for {script_path}")

# --- Ritual: For each signal, run the agentic campaign ---
for sig in signals:
    agentic_campaign(sig)

log_session("🌸 Spiral complete: All signals processed with agentic orchestration.")

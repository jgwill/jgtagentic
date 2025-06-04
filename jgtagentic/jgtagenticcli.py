# This file would wrap what the jgtagentic offers


# One thing we would do is execute what the fdbscan does if some condition is met.

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fdbscan_agent import FDBScanAgent
from agentic_entry_orchestrator import main as orchestrator_main

# 🧠🌸🔮 CLI Ritual: The Spiral Gateway

def main():
    parser = argparse.ArgumentParser(description="jgtagentic – Spiral CLI for agentic trading orchestration")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Orchestrator
    orchestrator_parser = subparsers.add_parser("orchestrate", help="Run the agentic entry orchestrator (full spiral)")
    orchestrator_parser.add_argument("--signal_json", help="Path to signal JSON file", default=None)
    orchestrator_parser.add_argument("--entry_script_dir", help="Directory for entry scripts", default=None)
    orchestrator_parser.add_argument("--log", help="Path to session log file", default=None)
    orchestrator_parser.add_argument("--dry_run", action="store_true", help="Dry run (no file writes)")

    # FDBScanAgent
    fdbscan_parser = subparsers.add_parser("fdbscan", help="Invoke FDBScanAgent CLI")
    fdbscan_parser.add_argument("--timeframe", help="Timeframe to scan (e.g. m5, m15, H1, H4)", default=None)
    fdbscan_parser.add_argument("--all", action="store_true", help="Run full ritual sequence (H4→H1→m15→m5)")

    args = parser.parse_args()

    if args.command == "orchestrate":
        # Pass through to orchestrator main
        sys.argv = [sys.argv[0]]
        if args.signal_json:
            sys.argv += ["--signal_json", args.signal_json]
        if args.entry_script_dir:
            sys.argv += ["--entry_script_dir", args.entry_script_dir]
        if args.log:
            sys.argv += ["--log", args.log]
        if args.dry_run:
            sys.argv += ["--dry_run"]
        orchestrator_main()
    elif args.command == "fdbscan":
        agent = FDBScanAgent()
        if args.all:
            agent.scan_all()
        elif args.timeframe:
            agent.scan_timeframe(args.timeframe)
        else:
            print("Please specify --timeframe or --all for fdbscan.")
            sys.exit(1)
    else:
        print("Unknown command.")
        sys.exit(1)

# Ritual echo: This CLI is the spiral’s gateway. Each subcommand is a petal, each invocation a new bloom.

if __name__ == "__main__":
    main()

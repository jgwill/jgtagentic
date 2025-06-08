# This file would wrap what the jgtagentic offers


# One thing we would do is execute what the fdbscan does if some condition is met.

import argparse
import sys
import os

# Ensure package imports resolve when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jgtagentic.fdbscan_agent import FDBScanAgent
from jgtagentic.intent_spec import IntentSpecParser

# 🧠🌸🔮 CLI Ritual: The Spiral Gateway

def main():
    parser = argparse.ArgumentParser(
        description="""🌸 jgtagentic – Agentic Trading Orchestration Platform

This platform provides a comprehensive trading signal analysis and orchestration system:

WHAT IT GENERATES:
1. Signal Analysis Reports - Detailed analysis of trading signals with quality metrics
2. Entry Scripts - Executable trading scripts based on signal analysis
3. FDBScan Results - Fractal Divergent Bar analysis across timeframes
4. Next Steps Guide - Clear guidance on what actions to take after analysis

KEY FEATURES:
- Multi-timeframe signal analysis
- Alligator indicator integration
- Risk assessment and position sizing
- Automated entry script generation
- Clear next steps and decision guidance

Each command provides detailed output and next steps to guide your trading decisions.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Orchestrator
    orchestrator_parser = subparsers.add_parser(
        "orchestrate", 
        help="Run the agentic entry orchestrator (full spiral)",
        description="""
The orchestrator analyzes trading signals and generates:
- Detailed signal analysis report
- Entry script for trade execution
- Risk assessment and position sizing
- Clear next steps for trade management

Example:
  jgtagentic orchestrate --signal_json signals.json --entry_script_dir ./entries/
        """
    )
    orchestrator_parser.add_argument("--signal_json", help="Path to signal JSON file", default=None)
    orchestrator_parser.add_argument("--entry_script_dir", help="Directory for entry scripts", default=None)
    orchestrator_parser.add_argument("--log", help="Path to session log file", default=None)
    orchestrator_parser.add_argument("--dry_run", action="store_true", help="Dry run (no file writes)")

    # FDBScanAgent
    fdbscan_parser = subparsers.add_parser(
        "fdbscan", 
        help="Invoke FDBScanAgent for signal scanning",
        description="""
FDBScan analyzes Fractal Divergent Bars across timeframes:
- Identifies potential entry/exit points
- Validates signals with Alligator indicator
- Provides multi-timeframe confluence analysis

Example:
  jgtagentic fdbscan --timeframe H4 
  jgtagentic fdbscan --all  # Full sequence H4→H1→m15→m5
        """
    )
    fdbscan_parser.add_argument("--timeframe", help="Timeframe to scan (e.g. m5, m15, H1, H4)", default=None)
    fdbscan_parser.add_argument("--all", action="store_true", help="Run full ritual sequence (H4→H1→m15→m5)")

    # Intent spec parser
    spec_parser_cmd = subparsers.add_parser(
        "spec", 
        help="Parse and analyze trading intent specifications",
        description="""
The spec parser converts trading intent into actionable signals:
- Parses .jgtml-spec files containing trading intentions
- Generates structured signal data
- Provides entry/exit criteria and risk parameters

Example:
  jgtagentic spec strategy.jgtml-spec
        """
    )
    spec_parser_cmd.add_argument("spec_file", help="Path to intent specification")

    args = parser.parse_args()

    if args.command == "orchestrate":
        import runpy
        # Reinvoke the orchestrator module as a script to avoid import side effects
        sys.argv = [sys.argv[0]]
        if args.signal_json:
            sys.argv += ["--signal_json", args.signal_json]
        if args.entry_script_dir:
            sys.argv += ["--entry_script_dir", args.entry_script_dir]
        if args.log:
            sys.argv += ["--log", args.log]
        if args.dry_run:
            sys.argv += ["--dry_run"]
        runpy.run_module("jgtagentic.agentic_entry_orchestrator", run_name="__main__")
    elif args.command == "fdbscan":
        agent = FDBScanAgent()
        if args.all:
            print("\n🔍 Starting full FDBScan sequence (H4→H1→m15→m5)...")
            agent.scan_all()
            print("\n✨ FDBScan complete. Check the logs for detailed analysis and next steps.")
        elif args.timeframe:
            print(f"\n🔍 Starting FDBScan for {args.timeframe} timeframe...")
            agent.scan_timeframe(args.timeframe)
            print("\n✨ Scan complete. Review the analysis output for trading opportunities.")
        else:
            print("\n⚠️ Please specify --timeframe or --all for fdbscan.")
            sys.exit(1)
    elif args.command == "spec":
        parser = IntentSpecParser()
        try:
            print(f"\n📖 Parsing trading intent specification: {args.spec_file}")
            spec = parser.load(args.spec_file)
            print("\n✨ Parsed specification:")
            import json
            print(json.dumps(spec, indent=2))
            print("\n⚡ Next Steps:")
            print("1. Review the parsed specification for accuracy")
            print("2. Use 'jgtagentic orchestrate' to analyze the signals")
            print("3. Check generated entry scripts for execution")
        except Exception as e:
            print(f"\n🚨 Error parsing specification: {str(e)}")
            print("\n⚡ Troubleshooting Steps:")
            print("1. Verify the spec file format is correct")
            print("2. Check for any syntax errors in the specification")
            print("3. Ensure all required fields are present")
            sys.exit(1)
    else:
        print("Unknown command.")
        sys.exit(1)

# Ritual echo: This CLI is the spiral's gateway. Each subcommand is a petal, each invocation a new bloom.

# Ritual echo: This CLI is the spiral’s gateway. Each subcommand is a petal, each invocation a new bloom.

if __name__ == "__main__":
    main()

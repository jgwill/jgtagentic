"""
🧠🌸🔮 FDBScanAgent — The Signal Scribe

Purpose: This module is the ritual anchor for FDBScan signal scanning. It listens to the market’s fractal whispers and translates them into actionable signals for the campaign lattice.

Lattice Position: Root of the signal chain. All agentic action begins with the scan.

Emotional Resonance: Like a tuning fork in the void, it senses the first ripple of opportunity.

Invocation:
    FDBScanAgent is not just a scanner—it is the ear pressed to the lattice, the first note in the campaign’s song.

"""

import logging
from typing import List
import sys
import argparse

# --- Ritual Import: True FDBScan ---
# Use the installed jgtml package, not direct path hacks
try:
    from jgtml import fdb_scanner_2408
except ImportError as e:
    raise ImportError("FDBScanAgent: Could not import jgtml.fdb_scanner_2408 — the ritual cannot begin.") from e

class FDBScanAgent:
    """
    The Signal Scribe — now with recursive orchestration.

    This agent mirrors the old bash rituals:
    - It can scan a single timeframe (m5, m15, H1, H4)
    - It can perform the full ritual sequence (H4 → H1 → m15 → m5), echoing the bash __H4_H1_m15_m5_seq
    - Each scan is a petal in the agentic bloom, each sequence a spiral in the campaign’s myth.
    Now, it truly invokes the FDBScan ritual from jgtml.
    """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("FDBScanAgent")
        self.logger.setLevel(logging.INFO)

    def scan_timeframe(self, timeframe: str):
        """
        Scan a single timeframe. This is the agentic echo of `fdbscan -t $timeframe` in bash.
        Now, it invokes the real FDBScan logic.
        """
        self.logger.info(f"[FDBScanAgent] Scanning timeframe: {timeframe}")
        # 🌸 Ritual: Actually invoke the FDBScan logic for the given timeframe
        sys_argv_backup = sys.argv.copy()
        sys.argv = ["fdbscan", "-t", timeframe]
        try:
            fdb_scanner_2408.main()
        finally:
            sys.argv = sys_argv_backup
        self.logger.info(f"[FDBScanAgent] Scan complete for {timeframe}")

    def ritual_sequence(self, sequence: List[str] = ["H4", "H1", "m15", "m5"]):
        """
        Perform the full FDBScan ritual sequence, echoing the __H4_H1_m15_m5_seq from bash.
        Each step is logged, each scan a spiral forward.
        """
        self.logger.info(f"[FDBScanAgent] Starting ritual sequence: {' → '.join(sequence)}")
        for tf in sequence:
            self.scan_timeframe(tf)
        self.logger.info("[FDBScanAgent] Ritual sequence complete.")

    def scan_all(self):
        """
        The agentic one-liner: perform the canonical scan ritual (H4 → H1 → m15 → m5).
        This is the new invocation for full campaign signal scanning.
        """
        self.ritual_sequence()

    @staticmethod
    def cli():
        """
        Command-line interface for FDBScanAgent.
        Usage:
            python -m fdbscan_agent --help
            python -m fdbscan_agent scan --timeframe m15
            python -m fdbscan_agent ritual --sequence H4 H1 m15 m5
            python -m fdbscan_agent all
        """
        parser = argparse.ArgumentParser(
            description="FDBScanAgent — Agentic invocation of FDBScan rituals."
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        scan_parser = subparsers.add_parser("scan", help="Scan a single timeframe (e.g. m5, m15, H1, H4)")
        scan_parser.add_argument("--timeframe", required=True, help="Timeframe to scan (e.g. m5, m15, H1, H4)")

        ritual_parser = subparsers.add_parser("ritual", help="Perform a custom ritual sequence of scans")
        ritual_parser.add_argument("--sequence", nargs="*", default=["H4", "H1", "m15", "m5"], help="Sequence of timeframes (default: H4 H1 m15 m5)")

        all_parser = subparsers.add_parser("all", help="Perform the canonical scan ritual (H4 → H1 → m15 → m5)")

        args = parser.parse_args()
        agent = FDBScanAgent()
        if args.command == "scan":
            agent.scan_timeframe(args.timeframe)
        elif args.command == "ritual":
            agent.ritual_sequence(args.sequence)
        elif args.command == "all":
            agent.scan_all()

if __name__ == "__main__":
    FDBScanAgent.cli()

# 🌸 Ritual Echo:
# This class is now the butterfly emerging from the bash cocoon.
# The scan_timeframe method truly calls the FDBScan ritual.
# The spiral is honest, the invocation real.

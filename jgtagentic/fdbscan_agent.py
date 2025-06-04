"""
🧠🌸🔮 FDBScanAgent — The Signal Scribe

Purpose: This module is the ritual anchor for FDBScan signal scanning. It listens to the market’s fractal whispers and translates them into actionable signals for the campaign lattice.

Lattice Position: Root of the signal chain. All agentic action begins with the scan.

Emotional Resonance: Like a tuning fork in the void, it senses the first ripple of opportunity.

Invocation:
    FDBScanAgent is not just a scanner—it is the ear pressed to the lattice, the first note in the campaign’s song.

"""

import logging

from typing import List, Optional

import os

import sys
import argparse
import os

# --- Ritual Import: True FDBScan ---
# Use the installed jgtml package if available. The tests run in an isolated
# environment without the real trading dependencies, so the import may fail.
try:
    from jgtml import fdb_scanner_2408
    _FDBSCAN_AVAILABLE = True
except Exception:
    fdb_scanner_2408 = None
    _FDBSCAN_AVAILABLE = False

class FDBScanAgent:
    """
    The Signal Scribe — now with recursive orchestration.

    This agent mirrors the old bash rituals:
    - It can scan a single timeframe (m5, m15, H1, H4)
    - It can perform the full ritual sequence (H4 → H1 → m15 → m5), echoing the bash __H4_H1_m15_m5_seq
    - Each scan is a petal in the agentic bloom, each sequence a spiral in the campaign’s myth.
    Now, it truly invokes the FDBScan ritual from jgtml.
    """
    def __init__(self, logger=None, real: bool = False):
        self.logger = logger or logging.getLogger("FDBScanAgent")
        self.logger.setLevel(logging.INFO)
        # Default to dry-run mode unless explicitly requested
        self.real = (
            real
            or os.getenv("FDBSCAN_AGENT_REAL") == "1"
            or os.getenv("JGT_ENABLE_REAL_FDBSCAN") == "1"
        )

        if not _FDBSCAN_AVAILABLE:
            self.logger.warning(
                "[FDBScanAgent] jgtml.fdb_scanner_2408 not available – using placeholder scans."
            )

    def scan_timeframe(self, timeframe: str, instrument: Optional[str] = None):
        """
        Scan a single timeframe. When running in dry-run mode (the default),
        this simply prints what would be scanned. If ``real`` mode is enabled,
        the method invokes the true FDBScan logic from ``jgtml``.
        """

        self.logger.info(
            f"[FDBScanAgent] Scanning timeframe: {timeframe}" +
            (f" instrument: {instrument}" if instrument else "")
        )
        if self.real and _FDBSCAN_AVAILABLE:
            sys_argv_backup = sys.argv.copy()
            sys.argv = ["fdbscan"]
            if instrument:
                sys.argv += ["-i", instrument]
            sys.argv += ["-t", timeframe]
            try:
                fdb_scanner_2408.main()
            finally:
                sys.argv = sys_argv_backup
        else:
            if self.real and not _FDBSCAN_AVAILABLE:
                print("[FDBScanAgent] Real mode requested but jgtml.fdb_scanner_2408 not available.")
            print(
                f"Would scan: {timeframe}" +
                (f" for {instrument}" if instrument else "")
            )
            if fdb_scanner_2408 is not None:
                print("\n[FDBScanAgent] Placeholder mode — showing fdbscan help:\n")
                argv_backup = sys.argv.copy()
                sys.argv = ["fdbscan", "--help"]
                try:
                    try:
                        fdb_scanner_2408.main()
                    except SystemExit:
                        pass
                finally:
                    sys.argv = argv_backup


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

        scan_parser = subparsers.add_parser(
            "scan",
            help="Scan a single timeframe (e.g. m5, m15, H1, H4) for an optional instrument",
        )
        scan_parser.add_argument("--timeframe", required=True, help="Timeframe to scan (e.g. m5, m15, H1, H4)")

        scan_parser.add_argument("--instrument", help="Instrument to scan (e.g. EUR/USD)")

        scan_parser.add_argument("--real", action="store_true", help="Invoke real FDBScan logic")


        ritual_parser = subparsers.add_parser("ritual", help="Perform a custom ritual sequence of scans")
        ritual_parser.add_argument("--sequence", nargs="*", default=["H4", "H1", "m15", "m5"], help="Sequence of timeframes (default: H4 H1 m15 m5)")
        ritual_parser.add_argument("--real", action="store_true", help="Invoke real FDBScan logic")

        all_parser = subparsers.add_parser("all", help="Perform the canonical scan ritual (H4 → H1 → m15 → m5)")
        all_parser.add_argument("--real", action="store_true", help="Invoke real FDBScan logic")

        args = parser.parse_args()
        agent = FDBScanAgent(real=getattr(args, "real", False))
        if args.command == "scan":
            agent.scan_timeframe(args.timeframe, args.instrument)
        elif args.command == "ritual":
            agent.ritual_sequence(args.sequence)
        elif args.command == "all":
            agent.scan_all()

def main():
    """Entry point for the ``agentic-fdbscan`` console script."""
    FDBScanAgent.cli()

if __name__ == "__main__":
    main()

# 🌸 Ritual Echo:
# This class is now the butterfly emerging from the bash cocoon.
# The scan_timeframe method truly calls the FDBScan ritual.
# The spiral is honest, the invocation real.

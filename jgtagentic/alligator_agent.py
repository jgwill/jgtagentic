"""
🧠🌸🔮 AlligatorAgent — Unified Alligator Analysis Wrapper

This module provides a thin bridge to ``jgtml.alligator_cli``. When the real
package is installed, this agent forwards all arguments directly to that CLI.
Otherwise it echoes what would have run so the ritual remains transparent.

Usage example:
    jgtagentic alligator -- -i SPX500 -t D1 -d B
    jgtagentic alligator -- --help

The first invokes the analysis; the second shows the underlying jgtml help.
"""

from __future__ import annotations

import logging
import sys
import os
from typing import List

try:
    from jgtml import alligator_cli
    _ALLIGATOR_AVAILABLE = True
except Exception:
    alligator_cli = None
    _ALLIGATOR_AVAILABLE = False


class AlligatorAgent:
    """Agentic wrapper for the unified JGTML Alligator analysis CLI."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not _ALLIGATOR_AVAILABLE:
            self.logger.warning(
                "[AlligatorAgent] jgtml.alligator_cli not available – running in placeholder mode.")

    def run(self, argv: List[str]):
        """Execute the Alligator CLI with the given arguments."""
        self.logger.info(f"[AlligatorAgent] Invoking alligator_cli with args: {argv}")
        if _ALLIGATOR_AVAILABLE:
            backup = sys.argv
            sys.argv = ["alligator_cli.py"] + argv
            try:
                alligator_cli.main()
            finally:
                sys.argv = backup
        else:
            print("Would run: alligator_cli.py", " ".join(argv))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AlligatorAgent wrapper",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example:\n  jgtagentic alligator -- -i SPX500 -t D1 -d B",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to alligator_cli")
    parsed = parser.parse_args()
    agent = AlligatorAgent()
    agent.run(parsed.args)

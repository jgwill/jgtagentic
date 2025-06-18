"""
🧠🌸🔮 FDB Data Analyzer — Completed Bar Signal Parser

Purpose: Utilize cached CSV datasets under ``data/current`` to extract
Fractal Divergent Bar (FDB) information for the last completed candle.
This bridges freshly generated trading data with jgtagentic modules so
future agents can validate signals without running the full scanner.
"""

from __future__ import annotations

import os
import json
import argparse
from typing import Tuple, Dict, Any

import pandas as pd


class FDBDataAnalyzer:
    """Parse cached CSV files and expose completed bar FDB data."""

    def __init__(self, data_dir: str = "data/current/cds") -> None:
        self.data_dir = data_dir

    def _path(self, instrument: str, timeframe: str) -> str:
        filename = f"{instrument.replace('/', '-')}_{timeframe}.csv"
        return os.path.join(self.data_dir, filename)

    def get_last_two_bars(self, instrument: str, timeframe: str) -> Tuple[pd.Series, pd.Series]:
        """Return the last two rows from the dataset.

        The second row is considered the completed bar for analysis.
        """
        path = self._path(instrument, timeframe)
        df = pd.read_csv(path)
        if len(df.index) < 2:
            raise ValueError("Not enough rows in dataset")
        last_two = df.tail(2)
        return last_two.iloc[0], last_two.iloc[1]

    def analyze_latest(self, instrument: str, timeframe: str) -> Dict[str, Any]:
        """Return FDB information for the last completed bar."""
        completed, _current = self.get_last_two_bars(instrument, timeframe)
        return {
            "instrument": instrument,
            "timeframe": timeframe,
            "timestamp": completed["Date"],
            "fdb_bull": float(completed["fdbb"]),
            "fdb_sell": float(completed["fdbs"]),
            "fdb": float(completed["fdb"]),
            "zone_sig": float(completed.get("zone_sig", 0)),
        }


def cli() -> None:
    parser = argparse.ArgumentParser(description="Analyze cached FDB CSV data")
    parser.add_argument("-i", "--instrument", required=True, help="Instrument e.g. EUR-USD")
    parser.add_argument("-t", "--timeframe", required=True, help="Timeframe e.g. H1")
    args = parser.parse_args()

    analyzer = FDBDataAnalyzer()
    result = analyzer.analyze_latest(args.instrument, args.timeframe)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    cli()

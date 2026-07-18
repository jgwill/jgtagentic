"""
Regime Detection — Williams Alligator (ADX/EMA lineage removed 2026-07-18).

This module previously computed ADX/EMA-based regime (Source: saraia-2508).
ADX is not a Williams signal, is not present in the CDS data, and gives false
confidence in choppy sideways markets. Regime is the Alligator — SLEEPING /
EATING / SATED — implemented in `alligator_regime.py`.

This file is now a compatibility shim preserving the legacy import surface
(`RegimeDetector`, `MarketRegime`, `RegimeResult`, `TrendDirection`) while the
implementation is the Alligator detector.
"""

from .alligator_regime import (
    AlligatorDetector as RegimeDetector,
    AlligatorState as MarketRegime,
    AlligatorResult as RegimeResult,
    TrendDirection,
)

__all__ = ["RegimeDetector", "MarketRegime", "RegimeResult", "TrendDirection"]

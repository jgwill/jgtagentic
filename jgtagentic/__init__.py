"""
jgtagentic - Agentic Trading Decision Engine

Autonomous signal evaluation, regime filtering, and trade orchestration.
"""

version='0.5.0'
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from .regime import RegimeDetector, RegimeResult, MarketRegime, TrendDirection
from .scoring import SignalScorer, ScoredSignal, ScoreBreakdown
from .regime_aware_decider import RegimeAwareDecider, AgenticDecider
from .data_loader import DataLoader
from .agentic_decider import AgenticDecider as BaseAgenticDecider

__all__ = [
    # Regime detection
    'RegimeDetector',
    'RegimeResult',
    'MarketRegime',
    'TrendDirection',
    
    # Signal scoring
    'SignalScorer',
    'ScoredSignal',
    'ScoreBreakdown',
    
    # Decision making
    'RegimeAwareDecider',
    'AgenticDecider',
    'BaseAgenticDecider',
    
    # Data access
    'DataLoader',
]




"""
jgtagentic - Agentic Trading Decision Engine

Autonomous signal evaluation, regime filtering, and trade orchestration.
Uses Bill Williams Alligator methodology for regime detection.
"""

version='0.6.0'
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Alligator regime detection (Williams methodology)
from .alligator_regime import (
    AlligatorDetector,
    AlligatorResult,
    AlligatorState,
    TrendDirection,
    RegimeDetector,  # Backward compatibility
    RegimeResult,    # Backward compatibility
    MarketRegime     # Backward compatibility
)

# Signal scoring
from .scoring import SignalScorer, ScoredSignal, ScoreBreakdown

# Decision making
from .regime_aware_decider import RegimeAwareDecider, AgenticDecider
from .data_loader import DataLoader
from .agentic_decider import AgenticDecider as BaseAgenticDecider

__all__ = [
    # Alligator regime detection (PRIMARY)
    'AlligatorDetector',
    'AlligatorResult',
    'AlligatorState',
    'TrendDirection',
    
    # Backward compatibility
    'RegimeDetector',
    'RegimeResult',
    'MarketRegime',
    
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

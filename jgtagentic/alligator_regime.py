"""
Alligator Regime Detection - Williams Methodology

The Alligator is THE primary regime filter. It represents the market's natural cycle:
- SLEEPING: Lines intertwined → NO TRADES (70-85% of time)
- EATING: Lines fanned out → TRADE ACTIVELY (15-30% of time)
- SATED: Lines converging → EXIT POSITIONS

Rule: "Is the Alligator sleeping? If yes, keep your powder dry."
"""

import pandas as pd
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class AlligatorState(str, Enum):
    """Alligator behavior states."""
    SLEEPING = "SLEEPING"  # Lines intertwined - choppy market
    EATING = "EATING"      # Lines fanned - trending market
    SATED = "SATED"        # Lines converging - trend exhaustion
    UNKNOWN = "UNKNOWN"


class TrendDirection(str, Enum):
    """Trend direction based on line positions."""
    UP = "UP"          # Green > Red > Blue (Lips > Teeth > Jaw)
    DOWN = "DOWN"      # Blue > Red > Green (Jaw > Teeth > Lips)
    UNKNOWN = "UNKNOWN"


@dataclass
class AlligatorResult:
    """Result of Alligator analysis."""
    state: AlligatorState
    direction: TrendDirection
    jaw: float          # Blue line (13-bar SMMA)
    teeth: float        # Red line (8-bar SMMA)
    lips: float         # Green line (5-bar SMMA)
    spread: float       # Distance between lines (indicates strength)
    tradeable: bool     # Can we trade? (EATING = True, else False)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "state": self.state.value,
            "direction": self.direction.value,
            "jaw": round(self.jaw, 5),
            "teeth": round(self.teeth, 5),
            "lips": round(self.lips, 5),
            "spread": round(self.spread, 5),
            "tradeable": self.tradeable,
            "regime": self.state.value  # Compatibility with old code
        }


class AlligatorDetector:
    """
    Detect market regime using Bill Williams Alligator.
    
    The Alligator consists of 3 Smoothed Moving Averages (SMMA) on midpoint,
    each offset into the future:
    - Jaw (Blue): 13-bar SMMA, offset +8
    - Teeth (Red): 8-bar SMMA, offset +5  
    - Lips (Green): 5-bar SMMA, offset +3
    
    States:
    - SLEEPING: Lines close together (< threshold) → NO TRADES
    - EATING: Lines spread apart, properly ordered → TRADE
    - SATED: Lines converging after being spread → EXIT
    """
    
    def __init__(
        self,
        jaw_period: int = 13,
        jaw_offset: int = 8,
        teeth_period: int = 8,
        teeth_offset: int = 5,
        lips_period: int = 5,
        lips_offset: int = 3,
        sleep_threshold: float = 0.0015  # 0.15% spread = sleeping
    ):
        """
        Initialize Alligator detector.
        
        Args:
            jaw_period: Jaw SMMA period (default: 13)
            jaw_offset: Jaw future offset (default: 8)
            teeth_period: Teeth SMMA period (default: 8)
            teeth_offset: Teeth future offset (default: 5)
            lips_period: Lips SMMA period (default: 5)
            lips_offset: Lips future offset (default: 3)
            sleep_threshold: Max spread for SLEEPING state (default: 0.15%)
        """
        self.jaw_period = jaw_period
        self.jaw_offset = jaw_offset
        self.teeth_period = teeth_period
        self.teeth_offset = teeth_offset
        self.lips_period = lips_period
        self.lips_offset = lips_offset
        self.sleep_threshold = sleep_threshold
    
    def detect(self, df: pd.DataFrame) -> AlligatorResult:
        """
        Detect Alligator state from OHLC DataFrame.
        
        Args:
            df: DataFrame with High, Low, Close columns
                Optionally: jaw, teeth, lips (if pre-calculated)
        
        Returns:
            AlligatorResult with state, direction, tradeable flag
        """
        if df is None or df.empty or len(df) < max(self.jaw_period, 20):
            return self._default_result()
        
        df = df.copy()
        
        # Calculate midpoint if not present
        if 'midpoint' not in df.columns:
            df['midpoint'] = (df['High'] + df['Low']) / 2
        
        # Calculate Alligator lines if not present
        if 'jaw' not in df.columns:
            df['jaw'] = self._smma(df['midpoint'], self.jaw_period)
        if 'teeth' not in df.columns:
            df['teeth'] = self._smma(df['midpoint'], self.teeth_period)
        if 'lips' not in df.columns:
            df['lips'] = self._smma(df['midpoint'], self.lips_period)
        
        # Get current values (accounting for future offset)
        # In practice, we look at current bar without offset for decision
        latest = df.iloc[-1]
        jaw = float(latest['jaw'])
        teeth = float(latest['teeth'])
        lips = float(latest['lips'])
        
        if any(pd.isna([jaw, teeth, lips])):
            return self._default_result()
        
        # Determine state and direction
        state = self._determine_state(jaw, teeth, lips, df)
        direction = self._determine_direction(jaw, teeth, lips)
        
        # Calculate spread (normalized by price)
        midpoint = float(latest.get('midpoint', latest.get('Close', jaw)))
        if midpoint > 0:
            spread = abs(max(jaw, teeth, lips) - min(jaw, teeth, lips)) / midpoint
        else:
            spread = 0
        
        tradeable = (state == AlligatorState.EATING)
        
        return AlligatorResult(
            state=state,
            direction=direction,
            jaw=jaw,
            teeth=teeth,
            lips=lips,
            spread=spread,
            tradeable=tradeable
        )
    
    def _smma(self, series: pd.Series, period: int) -> pd.Series:
        """
        Calculate Smoothed Moving Average (SMMA).
        
        SMMA = (SMMA_prev * (period - 1) + price) / period
        
        This is Wilder's smoothing, different from EMA.
        """
        # First value is SMA
        smma = series.rolling(window=period).mean()
        
        # Then apply smoothing formula
        for i in range(period, len(series)):
            if pd.notna(smma.iloc[i-1]):
                smma.iloc[i] = (smma.iloc[i-1] * (period - 1) + series.iloc[i]) / period
        
        return smma
    
    def _determine_state(
        self,
        jaw: float,
        teeth: float,
        lips: float,
        df: pd.DataFrame
    ) -> AlligatorState:
        """
        Determine if Alligator is SLEEPING, EATING, or SATED.
        
        SLEEPING: Lines very close together (intertwined)
        EATING: Lines properly spread and ordered
        SATED: Lines were spread but now converging
        """
        # Calculate spread
        spread = abs(max(jaw, teeth, lips) - min(jaw, teeth, lips))
        avg_price = (jaw + teeth + lips) / 3
        
        if avg_price > 0:
            normalized_spread = spread / avg_price
        else:
            normalized_spread = 0
        
        # Check if sleeping (lines too close)
        if normalized_spread < self.sleep_threshold:
            return AlligatorState.SLEEPING
        
        # Check if properly ordered (eating)
        is_uptrend_order = lips > teeth > jaw
        is_downtrend_order = lips < teeth < jaw
        
        if is_uptrend_order or is_downtrend_order:
            # Check if spreading or converging
            if len(df) >= 5:
                # Compare current spread to recent spreads
                recent = df.tail(5)
                if 'jaw' in recent.columns and 'lips' in recent.columns:
                    prev_spreads = []
                    for idx in range(len(recent) - 1):
                        row = recent.iloc[idx]
                        if all(pd.notna([row['jaw'], row['teeth'], row['lips']])):
                            s = abs(row['lips'] - row['jaw'])
                            prev_spreads.append(s)
                    
                    if prev_spreads:
                        avg_prev = np.mean(prev_spreads)
                        # If spread is decreasing, SATED (converging)
                        if spread < avg_prev * 0.9:
                            return AlligatorState.SATED
            
            # Lines ordered and spreading/stable = EATING
            return AlligatorState.EATING
        
        # Lines not properly ordered but spread apart = transition
        return AlligatorState.UNKNOWN
    
    def _determine_direction(
        self,
        jaw: float,
        teeth: float,
        lips: float
    ) -> TrendDirection:
        """
        Determine trend direction from line positions.
        
        UP: Lips > Teeth > Jaw (Green > Red > Blue)
        DOWN: Jaw > Teeth > Lips (Blue > Red > Green)
        """
        if lips > teeth > jaw:
            return TrendDirection.UP
        elif lips < teeth < jaw:
            return TrendDirection.DOWN
        else:
            return TrendDirection.UNKNOWN
    
    def is_aligned(self, signal_direction: str, result: AlligatorResult) -> bool:
        """
        Check if signal aligns with Alligator.
        
        Args:
            signal_direction: "LONG" or "SHORT"
            result: AlligatorResult from detect()
        
        Returns:
            True if EATING and direction matches
        """
        if not result.tradeable:
            return False
        
        signal_dir = signal_direction.upper()
        
        if result.direction == TrendDirection.UP and signal_dir == "LONG":
            return True
        if result.direction == TrendDirection.DOWN and signal_dir == "SHORT":
            return True
        
        return False
    
    def _default_result(self) -> AlligatorResult:
        """Return default result when data unavailable."""
        return AlligatorResult(
            state=AlligatorState.UNKNOWN,
            direction=TrendDirection.UNKNOWN,
            jaw=0,
            teeth=0,
            lips=0,
            spread=0,
            tradeable=False
        )


# Backward compatibility - map to old RegimeDetector interface
class RegimeDetector(AlligatorDetector):
    """Compatibility wrapper for old code expecting RegimeDetector."""
    
    def __init__(self, adx_threshold=25, trend_ma_period=50, **kwargs):
        # Ignore old ADX parameters, use Alligator
        super().__init__(**kwargs)
    
    def detect(self, df: pd.DataFrame):
        """Detect regime using Alligator, return compatible format."""
        result = super().detect(df)
        
        # Map to old interface
        class CompatResult:
            def __init__(self, alligator_result):
                self.regime = alligator_result.state
                self.adx = alligator_result.spread * 100  # Fake ADX from spread
                self.trend_direction = alligator_result.direction
                self.trend_strength = alligator_result.spread * 100
                self.tradeable = alligator_result.tradeable
            
            def to_dict(self):
                return {
                    "regime": self.regime.value,
                    "adx": round(self.adx, 2),
                    "trend_direction": self.trend_direction.value,
                    "trend_strength": round(self.trend_strength, 2),
                    "tradeable": self.tradeable
                }
        
        return CompatResult(result)


# Enums for backward compatibility
class MarketRegime(str, Enum):
    """Legacy enum - maps to AlligatorState."""
    TRENDING = "EATING"
    RANGING = "SLEEPING"
    UNKNOWN = "UNKNOWN"


RegimeResult = AlligatorResult  # Alias

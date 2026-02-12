"""
Regime Detection Module

Detects market regime (TRENDING/RANGING) using ADX and trend direction.
Migrated from jgt-insight experimental work.
"""

import pandas as pd
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class MarketRegime(str, Enum):
    """Market regime classification."""
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    UNKNOWN = "UNKNOWN"


class TrendDirection(str, Enum):
    """Trend direction classification."""
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


@dataclass
class RegimeResult:
    """Result of regime detection."""
    regime: MarketRegime
    adx: float
    trend_direction: TrendDirection
    trend_strength: float  # % above/below EMA
    tradeable: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "regime": self.regime.value,
            "adx": round(self.adx, 2),
            "trend_direction": self.trend_direction.value,
            "trend_strength": round(self.trend_strength, 2),
            "tradeable": self.tradeable
        }


class RegimeDetector:
    """
    Detect market regime using ADX and EMA.
    
    ADX >= threshold: TRENDING (tradeable)
    ADX < threshold: RANGING (avoid)
    
    Trend direction determined by price vs EMA.
    """
    
    def __init__(
        self, 
        adx_threshold: float = 25,
        trend_ma_period: int = 50
    ):
        """
        Initialize regime detector.
        
        Args:
            adx_threshold: ADX above this = trending (default: 25)
            trend_ma_period: EMA period for direction (default: 50)
        """
        self.adx_threshold = adx_threshold
        self.trend_ma_period = trend_ma_period
    
    def detect(self, df: pd.DataFrame) -> RegimeResult:
        """
        Detect regime from OHLC DataFrame.
        
        Args:
            df: DataFrame with High, Low, Close columns
                Optionally: adx, ema_50 (calculated if missing)
        
        Returns:
            RegimeResult with classification
        """
        if df is None or df.empty or len(df) < 2:
            return self._default_result()
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Ensure we have ADX
        if 'adx' not in df.columns:
            df['adx'] = self.calculate_adx(df)
        
        # Ensure we have EMA
        ema_col = f'ema_{self.trend_ma_period}'
        if ema_col not in df.columns:
            df[ema_col] = df['Close'].ewm(span=self.trend_ma_period, adjust=False).mean()
        
        latest = df.iloc[-1]
        
        # Get ADX value
        adx = float(latest.get('adx', 0))
        if pd.isna(adx):
            adx = 0
        
        # Determine if trending
        is_trending = adx >= self.adx_threshold
        
        # Determine trend direction using EMA
        close = float(latest.get('Close', 0))
        ema = float(latest.get(ema_col, close))
        
        if close > ema:
            trend_direction = TrendDirection.UP
        elif close < ema:
            trend_direction = TrendDirection.DOWN
        else:
            trend_direction = TrendDirection.UNKNOWN
        
        # Calculate trend strength as % above/below EMA
        if ema != 0:
            trend_strength = abs(close - ema) / ema * 100
        else:
            trend_strength = 0
        
        return RegimeResult(
            regime=MarketRegime.TRENDING if is_trending else MarketRegime.RANGING,
            adx=adx,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            tradeable=is_trending
        )
    
    def is_aligned(self, signal_direction: str, regime: RegimeResult) -> bool:
        """
        Check if signal aligns with regime trend.
        
        Args:
            signal_direction: "LONG" or "SHORT"
            regime: Result from detect()
        
        Returns:
            True if tradeable and direction matches
        """
        if not regime.tradeable:
            return False
        
        if regime.trend_direction == TrendDirection.UP and signal_direction.upper() == "LONG":
            return True
        if regime.trend_direction == TrendDirection.DOWN and signal_direction.upper() == "SHORT":
            return True
        
        return False
    
    @staticmethod
    def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average Directional Index (ADX).
        
        Args:
            df: DataFrame with High, Low, Close columns
            period: ADX period (default: 14)
        
        Returns:
            Series with ADX values
        """
        high = df['High']
        low = df['Low']
        close = df['Close']
        
        # Calculate +DM and -DM
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm = plus_dm.where(plus_dm > 0, 0)
        minus_dm = minus_dm.where(minus_dm > 0, 0)
        
        # Where +DM > -DM, keep +DM, else 0
        plus_dm = plus_dm.where(plus_dm > minus_dm, 0)
        minus_dm = minus_dm.where(minus_dm > plus_dm, 0)
        
        # True Range
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Smoothed averages (Wilder's smoothing)
        atr = tr.ewm(span=period, adjust=False).mean()
        plus_di = 100 * plus_dm.ewm(span=period, adjust=False).mean() / atr
        minus_di = 100 * minus_dm.ewm(span=period, adjust=False).mean() / atr
        
        # ADX
        di_sum = plus_di + minus_di
        dx = 100 * (plus_di - minus_di).abs() / di_sum.where(di_sum != 0, 1)
        adx = dx.ewm(span=period, adjust=False).mean()
        
        return adx
    
    def _default_result(self) -> RegimeResult:
        """Return default result when data unavailable."""
        return RegimeResult(
            regime=MarketRegime.UNKNOWN,
            adx=0,
            trend_direction=TrendDirection.UNKNOWN,
            trend_strength=0,
            tradeable=False
        )


# Legacy compatibility
def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Legacy function for backward compatibility."""
    return RegimeDetector.calculate_adx(df, period)

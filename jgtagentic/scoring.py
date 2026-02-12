"""
Signal Scoring Module

Multi-factor signal scoring based on Williams indicators, regime, and zone alignment.
Migrated from jgt-insight experimental work.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .regime import RegimeResult, TrendDirection


@dataclass
class ScoreBreakdown:
    """Breakdown of score components."""
    mfi_score: int = 0        # 0-50
    zone_score: int = 0       # 0-15
    alligator_score: int = 0  # 0-10
    adx_bonus: int = 0        # 0-15
    htf_bonus: int = 0        # 0-10
    total: int = 0            # 0-100
    factors: List[str] = field(default_factory=list)


@dataclass
class ScoredSignal:
    """A scored trading signal."""
    instrument: str
    timeframe: str
    direction: str        # "LONG" or "SHORT"
    score: int
    breakdown: ScoreBreakdown
    
    # Trade parameters
    entry_price: float = 0
    stop_price: float = 0
    target_price: float = 0
    risk_reward: float = 0
    
    # Regime info
    regime: str = ""
    adx: float = 0
    zone: str = ""
    
    # Active signals detail
    active_signals: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "instrument": self.instrument,
            "timeframe": self.timeframe,
            "direction": self.direction,
            "score": self.score,
            "breakdown": {
                "mfi_score": self.breakdown.mfi_score,
                "zone_score": self.breakdown.zone_score,
                "alligator_score": self.breakdown.alligator_score,
                "adx_bonus": self.breakdown.adx_bonus,
                "htf_bonus": self.breakdown.htf_bonus,
                "total": self.breakdown.total,
                "factors": self.breakdown.factors,
            },
            "entry_price": self.entry_price,
            "stop_price": self.stop_price,
            "target_price": self.target_price,
            "risk_reward": self.risk_reward,
            "regime": self.regime,
            "adx": self.adx,
            "zone": self.zone,
            "active_signals": self.active_signals,
        }


class SignalScorer:
    """
    Score trading signals based on multiple factors.
    
    Scoring components:
    - MFI signals (max 50 points)
    - Zone alignment (max 15 points)
    - Alligator alignment (max 10 points)
    - ADX strength bonus (max 15 points)
    - HTF confirmation (max 10 points)
    
    Total: 0-100 points
    """
    
    def __init__(
        self,
        mfi_weight: int = 10,
        zone_weight: int = 15,
        alligator_weight: int = 10,
        adx_strong_threshold: float = 40,
        adx_bonus: int = 15,
        htf_bonus: int = 10,
    ):
        """
        Initialize scorer with weights.
        
        Args:
            mfi_weight: Points per MFI signal (max 5 signals)
            zone_weight: Points for zone alignment
            alligator_weight: Points for Alligator alignment
            adx_strong_threshold: ADX above this gets bonus
            adx_bonus: Bonus points for strong ADX
            htf_bonus: Bonus for HTF confirmation
        """
        self.mfi_weight = mfi_weight
        self.zone_weight = zone_weight
        self.alligator_weight = alligator_weight
        self.adx_strong_threshold = adx_strong_threshold
        self.adx_bonus = adx_bonus
        self.htf_bonus = htf_bonus
    
    def score(
        self, 
        df: pd.DataFrame, 
        regime: RegimeResult,
        instrument: str = "",
        timeframe: str = "",
        ttf_data: Optional[pd.DataFrame] = None
    ) -> ScoredSignal:
        """
        Score signals in DataFrame.
        
        Args:
            df: CDS DataFrame with signal columns
            regime: Regime detection result
            instrument: Instrument name
            timeframe: Timeframe
            ttf_data: Optional HTF data for confirmation
        
        Returns:
            ScoredSignal with score breakdown
        """
        if df is None or df.empty:
            return self._empty_signal(instrument, timeframe)
        
        latest = df.iloc[-1]
        
        # Extract active signals
        signals = self._extract_signals(latest)
        
        # Determine direction from signals
        direction = self._determine_direction(signals, regime)
        
        # Calculate score breakdown
        breakdown = self._calculate_breakdown(signals, regime, direction, ttf_data)
        
        # Calculate trade parameters
        trade_params = self._calculate_trade_params(df, direction)
        
        return ScoredSignal(
            instrument=instrument,
            timeframe=timeframe,
            direction=direction,
            score=breakdown.total,
            breakdown=breakdown,
            entry_price=trade_params.get("entry", 0),
            stop_price=trade_params.get("stop", 0),
            target_price=trade_params.get("target", 0),
            risk_reward=trade_params.get("risk_reward", 0),
            regime=regime.regime.value,
            adx=regime.adx,
            zone=signals.get("zcol", ""),
            active_signals=signals,
        )
    
    def _extract_signals(self, row: pd.Series) -> Dict[str, Any]:
        """Extract active signal values from row."""
        signals = {}
        
        # MFI signals
        mfi_cols = ['mfi', 'mfi_fake', 'mfi_sig', 'mfi_sq', 'mfi_green', 'mfi_fade']
        for col in mfi_cols:
            if col in row.index:
                val = row[col]
                if not pd.isna(val) and val != 0:
                    signals[col] = float(val) if isinstance(val, (int, float)) else val
        
        # Zone signals
        zone_cols = ['zone_sig', 'zcol', 'zlc', 'zlcb', 'zlcs']
        for col in zone_cols:
            if col in row.index:
                val = row[col]
                if not pd.isna(val) and val != 0 and val != '':
                    signals[col] = val
        
        # AO/AC signals
        ao_cols = ['ao', 'ac', 'aoaz', 'aobz', 'aocolor', 'accolor']
        for col in ao_cols:
            if col in row.index:
                val = row[col]
                if not pd.isna(val):
                    signals[col] = float(val) if isinstance(val, (int, float)) else val
        
        # Alligator state
        if 'jaw' in row.index and 'teeth' in row.index and 'lips' in row.index:
            jaw = row.get('jaw', 0)
            teeth = row.get('teeth', 0)
            lips = row.get('lips', 0)
            close = row.get('Close', 0)
            
            if not any(pd.isna([jaw, teeth, lips, close])):
                if lips > teeth > jaw and close > lips:
                    signals['alligator'] = 'BULLISH'
                elif lips < teeth < jaw and close < lips:
                    signals['alligator'] = 'BEARISH'
                else:
                    signals['alligator'] = 'NEUTRAL'
        
        # FDB signals
        fdb_cols = ['fdb', 'fdbb', 'fdbs']
        for col in fdb_cols:
            if col in row.index:
                val = row[col]
                if not pd.isna(val) and val != 0:
                    signals[col] = float(val)
        
        return signals
    
    def _determine_direction(self, signals: Dict, regime: RegimeResult) -> str:
        """Determine trade direction from signals and regime."""
        # Check explicit FDB signals
        if signals.get('fdbb', 0) > 0:
            return "LONG"
        if signals.get('fdbs', 0) > 0:
            return "SHORT"
        
        # Check zone color
        zcol = signals.get('zcol', '')
        if zcol == 'green':
            return "LONG"
        if zcol == 'red':
            return "SHORT"
        
        # Check Alligator
        alligator = signals.get('alligator', '')
        if alligator == 'BULLISH':
            return "LONG"
        if alligator == 'BEARISH':
            return "SHORT"
        
        # Fall back to regime direction
        if regime.trend_direction == TrendDirection.UP:
            return "LONG"
        if regime.trend_direction == TrendDirection.DOWN:
            return "SHORT"
        
        return "LONG"  # Default
    
    def _calculate_breakdown(
        self, 
        signals: Dict, 
        regime: RegimeResult, 
        direction: str,
        ttf_data: Optional[pd.DataFrame]
    ) -> ScoreBreakdown:
        """Calculate score breakdown."""
        factors = []
        
        # 1. MFI Signals (max 50 points)
        mfi_cols = ['mfi', 'mfi_fake', 'mfi_sig', 'mfi_sq', 'mfi_green']
        mfi_active = [c for c in mfi_cols if signals.get(c)]
        mfi_count = len(mfi_active)
        mfi_score = min(mfi_count * self.mfi_weight, 50)
        if mfi_count > 0:
            factors.append(f"MFI: {mfi_count} signals")
        
        # 2. Zone Alignment (15 points)
        zone_score = 0
        zcol = signals.get('zcol', '')
        if zcol == 'green' and direction == 'LONG':
            zone_score = self.zone_weight
            factors.append("Zone: green aligned")
        elif zcol == 'red' and direction == 'SHORT':
            zone_score = self.zone_weight
            factors.append("Zone: red aligned")
        
        # 3. Alligator Alignment (10 points)
        alligator_score = 0
        alligator = signals.get('alligator', '')
        if alligator == 'BULLISH' and direction == 'LONG':
            alligator_score = self.alligator_weight
            factors.append("Alligator: BULLISH aligned")
        elif alligator == 'BEARISH' and direction == 'SHORT':
            alligator_score = self.alligator_weight
            factors.append("Alligator: BEARISH aligned")
        
        # 4. ADX Strength Bonus (15 points)
        adx_bonus = 0
        if regime.adx >= self.adx_strong_threshold:
            adx_bonus = self.adx_bonus
            factors.append(f"Strong ADX: {regime.adx:.1f}")
        elif regime.adx >= 30:
            adx_bonus = 8
            factors.append(f"Good ADX: {regime.adx:.1f}")
        
        # 5. HTF Confirmation (10 points)
        htf_bonus = 0
        if ttf_data is not None and not ttf_data.empty:
            htf_bonus = self._evaluate_htf(ttf_data, direction)
            if htf_bonus > 0:
                factors.append(f"HTF: confirmed (+{htf_bonus})")
            else:
                factors.append("HTF: no alignment")
        
        total = mfi_score + zone_score + alligator_score + adx_bonus + htf_bonus
        
        return ScoreBreakdown(
            mfi_score=mfi_score,
            zone_score=zone_score,
            alligator_score=alligator_score,
            adx_bonus=adx_bonus,
            htf_bonus=htf_bonus,
            total=total,
            factors=factors,
        )
    
    def _calculate_trade_params(
        self, 
        df: pd.DataFrame, 
        direction: str,
        risk_reward: float = 2.0
    ) -> Dict[str, float]:
        """Calculate entry, stop, target prices."""
        latest = df.iloc[-1]
        entry = float(latest.get('Close', 0))
        
        if direction == "LONG":
            # Stop at recent fractal low
            if 'fl' in df.columns:
                fractal_lows = df[df['fl'].notna()]['fl']
                if len(fractal_lows) > 0:
                    stop = float(fractal_lows.iloc[-1])
                else:
                    stop = entry * 0.995
            else:
                stop = entry * 0.995
            
            risk = entry - stop
            target = entry + (risk * risk_reward)
        else:
            # Stop at recent fractal high
            if 'fh' in df.columns:
                fractal_highs = df[df['fh'].notna()]['fh']
                if len(fractal_highs) > 0:
                    stop = float(fractal_highs.iloc[-1])
                else:
                    stop = entry * 1.005
            else:
                stop = entry * 1.005
            
            risk = stop - entry
            target = entry - (risk * risk_reward)
        
        actual_rr = abs(target - entry) / abs(entry - stop) if abs(entry - stop) > 0 else 0
        
        return {
            "entry": entry,
            "stop": stop,
            "target": target,
            "risk_reward": actual_rr,
        }
    
    def _evaluate_htf(self, ttf_data: pd.DataFrame, direction: str) -> int:
        """Evaluate higher-timeframe confirmation from TTF data."""
        if ttf_data is None or ttf_data.empty:
            return 0
        
        latest = ttf_data.iloc[-1]
        bonus = 0
        
        # Check for HTF zone alignment
        htf_zcol_cols = [c for c in ttf_data.columns if 'zcol' in c.lower() and 'htf' in c.lower()]
        for col in htf_zcol_cols:
            val = latest.get(col, '')
            if direction == "LONG" and val == 'green':
                bonus += 5
                break
            elif direction == "SHORT" and val == 'red':
                bonus += 5
                break
        
        # Check for HTF alligator alignment
        htf_allig_cols = [c for c in ttf_data.columns if 'alligator' in c.lower() or 'jaw' in c.lower()]
        for col in htf_allig_cols:
            val = latest.get(col, 0)
            if not pd.isna(val) and val != 0:
                bonus = min(bonus + 5, self.htf_bonus)
                break
        
        return min(bonus, self.htf_bonus)
    
    def _empty_signal(self, instrument: str, timeframe: str) -> ScoredSignal:
        """Return empty signal for missing data."""
        return ScoredSignal(
            instrument=instrument,
            timeframe=timeframe,
            direction="NONE",
            score=0,
            breakdown=ScoreBreakdown(),
        )

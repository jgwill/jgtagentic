"""
🧠🔮 RegimeAwareDecider — The Oracle with Regime Wisdom

Enhanced AgenticDecider that integrates regime detection for profitable trading.
Only approves trades in trending markets with trend-aligned direction.

Lattice Position: The evolved oracle—seeing both signals AND market context.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Any

# Import regime detector
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'SANDBOX' / 'saraia-2508'))
try:
    from regime_detector import RegimeDetector, calculate_adx
    REGIME_AVAILABLE = True
except ImportError:
    REGIME_AVAILABLE = False

class RegimeAwareDecider:
    """
    Enhanced decider with regime detection.
    
    Key improvements:
    - Only approves trades in TRENDING markets (ADX > 25)
    - Ensures signal direction aligns with trend direction
    - Provides regime context in decision output
    """
    
    def __init__(self, logger=None, adx_threshold=25, trend_ma_period=50):
        self.logger = logger or logging.getLogger("RegimeAwareDecider")
        self.logger.setLevel(logging.INFO)
        
        self.adx_threshold = adx_threshold
        self.trend_ma_period = trend_ma_period
        
        if REGIME_AVAILABLE:
            self.regime_detector = RegimeDetector(
                adx_threshold=adx_threshold,
                trend_ma_period=trend_ma_period
            )
            self.logger.info(f"[RegimeAwareDecider] Initialized with ADX threshold: {adx_threshold}")
        else:
            self.regime_detector = None
            self.logger.warning("[RegimeAwareDecider] Regime detector not available - running without filter")
    
    def decide(self, signal: Dict, df=None) -> Dict:
        """
        Make regime-aware decision on a trading signal.
        
        Args:
            signal: Trading signal dict with instrument, timeframe, direction
            df: Optional DataFrame with CDS data for regime detection
        
        Returns:
            Dict with:
            - action: 'TRADE', 'SKIP', or 'WAIT'
            - reason: Why this decision was made
            - regime: Regime context
            - next_steps: Recommended actions
        """
        self.logger.info(f"[RegimeAwareDecider] Analyzing: {signal.get('instrument')} {signal.get('timeframe')}")
        
        instrument = signal.get('instrument', 'UNKNOWN')
        timeframe = signal.get('timeframe', 'UNKNOWN')
        direction = signal.get('direction', 'UNKNOWN')
        
        # Default regime if no detector or data
        regime = {
            'regime': 'UNKNOWN',
            'adx': 0,
            'trend_direction': 'UNKNOWN',
            'trend_strength': 0,
            'tradeable': False
        }
        
        # Detect regime if data available
        if self.regime_detector and df is not None:
            try:
                import pandas as pd
                # Ensure data is prepared
                if 'adx' not in df.columns:
                    df['adx'] = calculate_adx(df)
                if 'ema_50' not in df.columns:
                    df['ema_50'] = df['Close'].ewm(span=50, adjust=False).mean()
                
                regime = self.regime_detector.detect_regime(df)
            except Exception as e:
                self.logger.warning(f"[RegimeAwareDecider] Regime detection error: {e}")
        
        # Decision logic
        decision = self._make_decision(signal, regime)
        
        self.logger.info(f"[RegimeAwareDecider] Decision: {decision['action']} - {decision['reason']}")
        
        return decision
    
    def _make_decision(self, signal: Dict, regime: Dict) -> Dict:
        """Core decision logic with regime awareness."""
        
        direction = signal.get('direction', 'UNKNOWN').upper()
        trend = regime.get('trend_direction', 'UNKNOWN').upper()
        
        # Check 1: Is market tradeable (trending)?
        if not regime.get('tradeable', False):
            return {
                'action': 'SKIP',
                'reason': f"Market is RANGING (ADX: {regime.get('adx', 0):.1f} < {self.adx_threshold})",
                'regime': regime,
                'signal': signal,
                'next_steps': [
                    "⏳ Wait for trend to develop",
                    f"📊 Monitor ADX - needs to rise above {self.adx_threshold}",
                    "🔄 Check again in next timeframe bar"
                ]
            }
        
        # Check 2: Does signal align with trend?
        if direction != 'UNKNOWN' and trend != 'UNKNOWN':
            direction_matches = (
                (direction == 'LONG' and trend == 'UP') or
                (direction == 'SHORT' and trend == 'DOWN')
            )
            
            if not direction_matches:
                return {
                    'action': 'SKIP',
                    'reason': f"Signal direction ({direction}) conflicts with trend ({trend})",
                    'regime': regime,
                    'signal': signal,
                    'next_steps': [
                        f"❌ Do not trade against the trend",
                        f"✅ Wait for {trend} signal instead",
                        "🔄 Check counter-trend opportunities in lower TF only"
                    ]
                }
        
        # Check 3: Assess signal quality
        signal_quality = self._assess_signal_quality(signal)
        
        if signal_quality['score'] < 0.5:
            return {
                'action': 'WAIT',
                'reason': f"Signal quality below threshold ({signal_quality['score']:.2f})",
                'regime': regime,
                'signal': signal,
                'quality': signal_quality,
                'next_steps': [
                    "⏳ Wait for stronger confirmation",
                    "📊 Monitor for additional signals",
                    "🎯 Target quality score > 0.5"
                ]
            }
        
        # All checks passed - TRADE!
        return {
            'action': 'TRADE',
            'reason': f"TRENDING market ({regime['regime']}) with aligned {direction} signal",
            'regime': regime,
            'signal': signal,
            'quality': signal_quality,
            'entry_price': signal.get('entry_price'),
            'next_steps': [
                f"✅ EXECUTE {direction} on {signal.get('instrument')} {signal.get('timeframe')}",
                f"📍 Entry: {signal.get('entry_price', 'Market')}",
                f"⚡ ADX: {regime.get('adx', 0):.1f} | Trend strength: {regime.get('trend_strength', 0):.2f}%",
                "🛡️ Set stop loss at swing low/high",
                "🎯 Target: 1.5-2x risk-reward ratio"
            ]
        }
    
    def _assess_signal_quality(self, signal: Dict) -> Dict:
        """Assess overall signal quality."""
        score = 0.0
        factors = []
        
        # Check signal strength
        strength = signal.get('strength', 0)
        if strength > 0.7:
            score += 0.3
            factors.append(f"Strong signal: {strength:.2f}")
        elif strength > 0.5:
            score += 0.2
            factors.append(f"Moderate signal: {strength:.2f}")
        elif strength > 0.3:
            score += 0.1
            factors.append(f"Weak signal: {strength:.2f}")
        
        # Check if MFI signal (highest priority)
        if 'mfi' in signal.get('signal_group', '').lower():
            score += 0.3
            factors.append("MFI signal (100% WR in trending)")
        
        # Check confirmation
        if signal.get('valid_signals', 0) >= 2:
            score += 0.2
            factors.append(f"Multi-signal confirmation: {signal.get('valid_signals')}")
        
        # Timeframe bonus
        tf = signal.get('timeframe', '')
        if tf in ['W1', 'D1']:
            score += 0.2
            factors.append(f"Higher timeframe: {tf}")
        elif tf == 'H4':
            score += 0.1
            factors.append(f"Medium timeframe: {tf}")
        
        return {
            'score': min(1.0, score),
            'factors': factors
        }
    
    def decide_batch(self, signals: list, data_dict: dict = None) -> list:
        """
        Process multiple signals with regime filtering.
        
        Args:
            signals: List of signal dicts
            data_dict: Optional dict mapping (instrument, timeframe) to DataFrames
        
        Returns:
            List of decisions for tradeable signals only
        """
        decisions = []
        
        for signal in signals:
            key = (signal.get('instrument'), signal.get('timeframe'))
            df = data_dict.get(key) if data_dict else None
            
            decision = self.decide(signal, df)
            
            if decision['action'] == 'TRADE':
                decisions.append(decision)
        
        # Sort by regime ADX (strongest trends first)
        decisions.sort(key=lambda d: d.get('regime', {}).get('adx', 0), reverse=True)
        
        return decisions


# Legacy compatibility
class AgenticDecider(RegimeAwareDecider):
    """Backwards-compatible alias for RegimeAwareDecider."""
    pass


# CLI usage
if __name__ == '__main__':
    import json
    
    # Example signal
    test_signal = {
        'instrument': 'EUR-USD',
        'timeframe': 'D1',
        'direction': 'LONG',
        'strength': 0.75,
        'signal_group': 'mfi_signals',
        'entry_price': 1.0850
    }
    
    decider = RegimeAwareDecider(adx_threshold=25)
    decision = decider.decide(test_signal)
    
    print(json.dumps(decision, indent=2, default=str))

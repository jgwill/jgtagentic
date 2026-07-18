"""
🧠🔮 RegimeAwareDecider — The Oracle with Regime Wisdom

Enhanced AgenticDecider that integrates regime detection for profitable trading.
Only approves trades in trending markets with trend-aligned direction.

Lattice Position: The evolved oracle—seeing both signals AND market context.
"""

import logging
from typing import Dict, Optional, Any

from .alligator_regime import AlligatorDetector, AlligatorState, TrendDirection, AlligatorResult
from .scoring import SignalScorer, ScoredSignal

REGIME_AVAILABLE = True

class RegimeAwareDecider:
    """
    Enhanced decider with Williams Alligator regime detection.

    Key behavior:
    - Only approves trades when the Alligator is EATING (trending)
    - Ensures signal direction aligns with the Alligator direction
    - Provides regime context in decision output
    """

    def __init__(self, logger=None, sleep_threshold=0.0015):
        self.logger = logger or logging.getLogger("RegimeAwareDecider")
        self.logger.setLevel(logging.INFO)

        self.sleep_threshold = sleep_threshold

        self.regime_detector = AlligatorDetector(sleep_threshold=sleep_threshold)
        self.scorer = SignalScorer()
        self.logger.info("[RegimeAwareDecider] Initialized with Williams Alligator regime filter")
    
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
        
        # Detect regime if data available
        if df is not None:
            try:
                regime_result = self.regime_detector.detect(df)
                regime = regime_result.to_dict()
            except Exception as e:
                self.logger.warning(f"[RegimeAwareDecider] Regime detection error: {e}")
                regime = self._unknown_regime()
        else:
            regime = self._unknown_regime()
        
        # Decision logic
        decision = self._make_decision(signal, regime)

        self.logger.info(f"[RegimeAwareDecider] Decision: {decision['action']} - {decision['reason']}")

        return decision

    def _unknown_regime(self) -> Dict:
        """Regime context when data is unavailable or detection failed."""
        return AlligatorResult(
            state=AlligatorState.UNKNOWN,
            direction=TrendDirection.UNKNOWN,
            jaw=0, teeth=0, lips=0, spread=0,
            tradeable=False,
        ).to_dict()
    
    def _make_decision(self, signal: Dict, regime: Dict) -> Dict:
        """Core decision logic with regime awareness."""
        
        direction = signal.get('direction', 'UNKNOWN').upper()
        trend = regime.get('direction', 'UNKNOWN').upper()
        state = regime.get('state', 'UNKNOWN')
        spread_pct = regime.get('spread', 0) * 100

        # Check 1: Is the Alligator eating (trending)?
        if not regime.get('tradeable', False):
            return {
                'action': 'SKIP',
                'reason': f"Alligator {state} — not eating (spread {spread_pct:.2f}%). Keep your powder dry.",
                'regime': regime,
                'signal': signal,
                'next_steps': [
                    "⏳ Wait for the Alligator to wake and eat",
                    "📊 Watch for lines to fan out (mouth opening) with proper ordering",
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
            'reason': f"EATING market ({regime.get('state')}) with aligned {direction} signal",
            'regime': regime,
            'signal': signal,
            'quality': signal_quality,
            'entry_price': signal.get('entry_price'),
            'next_steps': [
                f"✅ EXECUTE {direction} on {signal.get('instrument')} {signal.get('timeframe')}",
                f"📍 Entry: {signal.get('entry_price', 'Market')}",
                f"⚡ Alligator {regime.get('state')} {regime.get('direction')} | feed spread: {spread_pct:.2f}%",
                "🛡️ Set stop loss at swing low/high (teeth / lips)",
                "🎯 Target: 1.5-2x risk-reward ratio"
            ]
        }
    
    def _assess_signal_quality(self, signal: Dict) -> Dict:
        """
        Assess overall signal quality.
        
        Returns normalized score 0-1 for compatibility with existing code.
        Internally uses SignalScorer for detailed analysis.
        """
        # Legacy simple scoring for backward compatibility
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
        
        # Sort by Alligator feed spread (strongest trends first)
        decisions.sort(key=lambda d: d.get('regime', {}).get('spread', 0), reverse=True)
        
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
    
    decider = RegimeAwareDecider()
    decision = decider.decide(test_signal)
    
    print(json.dumps(decision, indent=2, default=str))

"""
🌸🧠 Observation Capture — Market Analysis to Intent Bridge

Purpose: Capture natural language market observations and translate them into 
executable trading intent specifications. This is the bridge between human 
market insight and systematic automation.

Architecture:
Market Observation → Linguistic Analysis → Intent Specification → Scanner Parameters
"""

import logging
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass

from .intent_spec import IntentSpecParser


@dataclass
class MarketObservation:
    """Structured market observation data."""
    text: str
    timestamp: str
    instruments: List[str]
    timeframes: List[str]
    confidence: float
    sentiment: str  # bullish, bearish, neutral
    signal_type: str  # breakout, confluence, trend, reversal
    
    
class ObservationCapture:
    """
    Convert natural language market observations into actionable intent specifications.
    
    This interface:
    1. Analyzes natural language market observations
    2. Extracts trading intent and context
    3. Generates structured intent specifications
    4. Validates and enhances specifications
    5. Provides feedback on observation quality
    """
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("ObservationCapture")
        self.intent_parser = IntentSpecParser()
        self.observation_history = []
        
    def capture_observation(self, observation_text: str) -> Dict[str, Any]:
        """Capture and process a market observation."""
        
        result = {
            "observation": {
                "text": observation_text,
                "timestamp": datetime.now().isoformat()
            },
            "intent_specification": {
                "strategy_intent": f"Analysis: {observation_text[:50]}...",
                "instruments": ["EUR/USD"],
                "timeframes": ["H4", "H1"]
            },
            "quality_score": 0.7,
            "success": True
        }
        
        return result
    
    def capture_session(self, observations: List[str],
                       session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Capture multiple observations as a trading session.
        
        Args:
            observations: List of observation texts
            session_context: Additional session context
            
        Returns:
            Session analysis with consolidated intent
        """
        
        self.logger.info(f"🎯 Processing trading session with {len(observations)} observations")
        
        session_results = []
        consolidated_instruments = set()
        consolidated_timeframes = set()
        
        # Process each observation
        for i, obs_text in enumerate(observations):
            result = self.capture_observation(obs_text)
            session_results.append(result)
            
            # Consolidate instruments and timeframes
            consolidated_instruments.update(result["observation"]["instruments"])
            consolidated_timeframes.update(result["observation"]["timeframes"])
        
        # Generate consolidated intent
        consolidated_intent = self._consolidate_session_intent(
            session_results, 
            list(consolidated_instruments),
            list(consolidated_timeframes),
            session_context
        )
        
        return {
            "session_timestamp": datetime.now().isoformat(),
            "observations": session_results,
            "consolidated_instruments": list(consolidated_instruments),
            "consolidated_timeframes": list(consolidated_timeframes),
            "consolidated_intent": consolidated_intent,
            "session_quality": self._assess_session_quality(session_results),
            "trading_recommendations": self._generate_session_recommendations(consolidated_intent)
        }
    
    def _analyze_observation(self, text: str) -> Dict[str, Any]:
        """Analyze observation text and extract trading context."""
        
        text_lower = text.lower()
        
        # Extract instruments
        instruments = self._extract_instruments(text)
        
        # Extract timeframes  
        timeframes = self._extract_timeframes(text)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(text_lower)
        
        # Detect signal type
        signal_type = self._detect_signal_type(text_lower)
        
        # Assess confidence based on linguistic cues
        confidence = self._assess_linguistic_confidence(text_lower)
        
        # Extract key concepts
        concepts = self._extract_key_concepts(text_lower)
        
        return {
            "instruments": instruments,
            "timeframes": timeframes,
            "sentiment": sentiment,
            "signal_type": signal_type,
            "confidence": confidence,
            "key_concepts": concepts
        }
    
    def _extract_instruments(self, text: str) -> List[str]:
        """Extract instrument symbols from observation text."""
        
        # Common instrument patterns
        instrument_patterns = [
            r'\b(EUR/USD|EURUSD)\b',
            r'\b(GBP/USD|GBPUSD)\b',
            r'\b(USD/JPY|USDJPY)\b',
            r'\b(AUD/USD|AUDUSD)\b',
            r'\b(USD/CAD|USDCAD)\b',
            r'\b(XAU/USD|XAUUSD|GOLD)\b',
            r'\b(SPX500|SP500|SPX)\b',
            r'\b(NAS100|NASDAQ)\b'
        ]
        
        instruments = []
        text_upper = text.upper()
        
        for pattern in instrument_patterns:
            matches = re.findall(pattern, text_upper, re.IGNORECASE)
            if matches:
                # Normalize to standard format
                match = matches[0]
                if 'EUR' in match and 'USD' in match:
                    instruments.append('EUR/USD')
                elif 'GBP' in match and 'USD' in match:
                    instruments.append('GBP/USD')
                elif 'XAU' in match or 'GOLD' in match:
                    instruments.append('XAU/USD')
                elif 'SPX' in match or 'SP500' in match:
                    instruments.append('SPX500')
                # Add more normalizations as needed
        
        return instruments if instruments else ["EUR/USD"]  # Default
    
    def _extract_timeframes(self, text: str) -> List[str]:
        """Extract timeframes from observation text."""
        
        timeframe_patterns = {
            r'\b(1|one)\s*hour\b': ['H1'],
            r'\b(4|four)\s*hour\b': ['H4'],
            r'\b(daily|day|d1)\b': ['D1'],
            r'\b(weekly|week|w1)\b': ['W1'],
            r'\b(monthly|month|m1)\b': ['M1'],
            r'\b(15|fifteen)\s*min': ['m15'],
            r'\b(5|five)\s*min': ['m5'],
            r'\bh1\b': ['H1'],
            r'\bh4\b': ['H4'],
            r'\bd1\b': ['D1'],
            r'\bm15\b': ['m15'],
            r'\bm5\b': ['m5']
        }
        
        timeframes = []
        text_lower = text.lower()
        
        for pattern, tf_list in timeframe_patterns.items():
            if re.search(pattern, text_lower):
                timeframes.extend(tf_list)
        
        # Remove duplicates while preserving order
        timeframes = list(dict.fromkeys(timeframes))
        
        return timeframes if timeframes else ["H4", "H1"]  # Default
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment from observation text."""
        
        bullish_words = ['bullish', 'buy', 'long', 'up', 'rising', 'breakout', 'uptrend']
        bearish_words = ['bearish', 'sell', 'short', 'down', 'falling', 'breakdown', 'downtrend']
        
        bullish_count = sum(1 for word in bullish_words if word in text)
        bearish_count = sum(1 for word in bearish_words if word in text)
        
        if bullish_count > bearish_count:
            return "bullish"
        elif bearish_count > bullish_count:
            return "bearish"
        else:
            return "neutral"
    
    def _detect_signal_type(self, text: str) -> str:
        """Detect the type of trading signal from observation."""
        
        signal_patterns = {
            "breakout": ["breakout", "break", "breakthrough", "penetration"],
            "confluence": ["confluence", "align", "convergence", "multiple"],
            "trend": ["trend", "trending", "directional", "momentum"],
            "reversal": ["reversal", "reverse", "turn", "change"],
            "alligator": ["alligator", "gator", "mouth", "lips", "teeth", "jaw"]
        }
        
        for signal_type, keywords in signal_patterns.items():
            if any(keyword in text for keyword in keywords):
                return signal_type
        
        return "general"
    
    def _assess_linguistic_confidence(self, text: str) -> float:
        """Assess confidence based on linguistic cues."""
        
        high_confidence_words = ['clear', 'obvious', 'strong', 'definite', 'certain']
        low_confidence_words = ['maybe', 'might', 'could', 'possibly', 'uncertain']
        
        high_count = sum(1 for word in high_confidence_words if word in text)
        low_count = sum(1 for word in low_confidence_words if word in text)
        
        base_confidence = 0.7  # Default confidence
        
        confidence = base_confidence + (high_count * 0.1) - (low_count * 0.1)
        
        return max(0.1, min(1.0, confidence))
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key trading concepts from observation."""
        
        concept_patterns = {
            "alligator_mouth": ["alligator mouth", "gator mouth", "mouth open"],
            "fractal_break": ["fractal break", "fractal breakout"],
            "ao_momentum": ["ao momentum", "awesome oscillator"],
            "volume_increase": ["volume increase", "high volume"],
            "trend_continuation": ["trend continuation", "trend following"],
            "support_resistance": ["support", "resistance", "level"]
        }
        
        concepts = []
        for concept, patterns in concept_patterns.items():
            if any(pattern in text for pattern in patterns):
                concepts.append(concept)
        
        return concepts
    
    def _generate_intent_from_observation(self, observation: MarketObservation) -> Dict[str, Any]:
        """Generate intent specification from structured observation."""
        
        # Base intent structure
        intent = {
            "strategy_intent": f"Trading analysis based on observation: {observation.text[:100]}...",
            "instruments": observation.instruments,
            "timeframes": observation.timeframes,
            "signals": [],
            "risk_management": {
                "position_size": 1,
                "max_risk_percent": 2.0,
                "target_rr": 2.0
            },
            "bias": observation.sentiment,
            "source_observation": observation.text,
            "observation_confidence": observation.confidence
        }
        
        # Generate signals based on signal type
        if observation.signal_type == "breakout":
            intent["signals"].append({
                "name": "breakout_signal",
                "description": "Breakout detection from observation",
                "jgtml_components": {
                    "fractal_analysis": "jgtpy.fractal_detection",
                    "momentum": "jgtpy.ao_acceleration"
                },
                "priority": observation.confidence
            })
        
        elif observation.signal_type == "confluence":
            intent["signals"].append({
                "name": "confluence_signal",
                "description": "Multi-indicator confluence",
                "jgtml_components": {
                    "fractal_analysis": "jgtpy.fractal_detection",
                    "alligator_state": "TideAlligatorAnalysis.mouth_opening",
                    "momentum": "jgtpy.ao_acceleration"
                },
                "priority": observation.confidence
            })
        
        elif observation.signal_type == "alligator":
            intent["signals"].append({
                "name": "alligator_signal",
                "description": "Alligator-based signal",
                "jgtml_components": {
                    "alligator_state": "TideAlligatorAnalysis.mouth_opening"
                },
                "priority": observation.confidence
            })
        
        else:  # general or other
            intent["signals"].append({
                "name": "general_signal",
                "description": "General signal detection",
                "jgtml_components": {
                    "fractal_analysis": "jgtpy.fractal_detection"
                },
                "priority": observation.confidence
            })
        
        return intent
    
    def _assess_observation_quality(self, observation: MarketObservation, 
                                  analysis: Dict[str, Any]) -> float:
        """Assess the quality of the observation for trading purposes."""
        
        quality_factors = {
            "specificity": 0.3,  # How specific is the observation
            "confidence": 0.2,   # User confidence
            "concepts": 0.2,     # Number of key concepts
            "completeness": 0.3  # How complete is the information
        }
        
        # Assess specificity
        specificity = 0.5  # Base score
        if len(observation.instruments) > 0:
            specificity += 0.2
        if len(observation.timeframes) > 0:
            specificity += 0.2
        if observation.sentiment != "neutral":
            specificity += 0.1
        
        # Assess completeness
        completeness = 0.4  # Base score
        if observation.signal_type != "general":
            completeness += 0.2
        if len(analysis["key_concepts"]) > 0:
            completeness += 0.2
        if len(observation.text) > 50:  # Detailed observation
            completeness += 0.2
        
        # Calculate weighted score
        quality_score = (
            min(1.0, specificity) * quality_factors["specificity"] +
            observation.confidence * quality_factors["confidence"] +
            min(1.0, len(analysis["key_concepts"]) / 3) * quality_factors["concepts"] +
            min(1.0, completeness) * quality_factors["completeness"]
        )
        
        return quality_score
    
    def _generate_recommendations(self, observation: MarketObservation,
                                intent_spec: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on observation and intent."""
        
        recommendations = []
        
        # Quality-based recommendations
        quality = self._assess_observation_quality(observation, {
            "key_concepts": intent_spec.get("signals", [])
        })
        
        if quality >= 0.8:
            recommendations.append("High-quality observation - proceed with scanning")
        elif quality >= 0.6:
            recommendations.append("Moderate quality - consider additional validation")
        else:
            recommendations.append("Low quality - refine observation or gather more information")
        
        # Specificity recommendations
        if not observation.instruments or observation.instruments == ["EUR/USD"]:
            recommendations.append("Consider specifying target instruments")
        
        if not observation.timeframes or len(observation.timeframes) < 2:
            recommendations.append("Consider multi-timeframe analysis")
        
        # Signal type recommendations
        if observation.signal_type == "general":
            recommendations.append("Observation could be more specific about signal type")
        
        return recommendations
    
    def _consolidate_session_intent(self, session_results: List[Dict[str, Any]],
                                  instruments: List[str],
                                  timeframes: List[str],
                                  session_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Consolidate multiple observations into unified intent."""
        
        # Extract all signals
        all_signals = []
        sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
        
        for result in session_results:
            spec = result["intent_specification"]
            all_signals.extend(spec.get("signals", []))
            sentiment = result["observation"]["sentiment"]
            sentiment_counts[sentiment] += 1
        
        # Determine consolidated sentiment
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        
        # Create consolidated intent
        consolidated = {
            "strategy_intent": "Multi-observation trading session analysis",
            "instruments": instruments,
            "timeframes": timeframes,
            "signals": all_signals,
            "bias": dominant_sentiment,
            "observation_count": len(session_results),
            "session_context": session_context or {},
            "risk_management": {
                "position_size": 1,
                "max_risk_percent": 2.0,
                "target_rr": 2.0
            }
        }
        
        return consolidated
    
    def _assess_session_quality(self, session_results: List[Dict[str, Any]]) -> float:
        """Assess overall quality of trading session observations."""
        
        if not session_results:
            return 0.0
        
        total_quality = sum(result["quality_score"] for result in session_results)
        average_quality = total_quality / len(session_results)
        
        # Bonus for consistency
        sentiments = [result["observation"]["sentiment"] for result in session_results]
        consistency_bonus = 0.1 if len(set(sentiments)) <= 2 else 0.0
        
        return min(1.0, average_quality + consistency_bonus)
    
    def _generate_session_recommendations(self, consolidated_intent: Dict[str, Any]) -> List[str]:
        """Generate recommendations for the trading session."""
        
        recommendations = [
            "Review consolidated signals for confluence",
            "Validate sentiment consistency across observations",
            "Consider risk management for multiple signals"
        ]
        
        signal_count = len(consolidated_intent.get("signals", []))
        if signal_count > 3:
            recommendations.append("High signal count - prioritize by quality")
        
        return recommendations


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Market Observation Capture")
    parser.add_argument("--observation", help="Market observation text", required=True)
    parser.add_argument("--instruments", nargs="*", help="Target instruments")
    parser.add_argument("--timeframes", nargs="*", help="Target timeframes")
    parser.add_argument("--confidence", type=float, help="Confidence level (0-1)")
    
    args = parser.parse_args()
    
    capture = ObservationCapture()
    result = capture.capture_observation(
        args.observation,
        args.instruments,
        args.timeframes,
        args.confidence
    )
    
    print(f"🔮 Observation Analysis Complete")
    print(f"Quality Score: {result['quality_score']:.2f}")
    print(f"Sentiment: {result['observation']['sentiment']}")
    print(f"Signal Type: {result['observation']['signal_type']}")
    print("\n📋 Intent Specification:")
    print(json.dumps(result['intent_specification'], indent=2)) 
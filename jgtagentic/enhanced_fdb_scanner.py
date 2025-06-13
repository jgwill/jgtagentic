"""
🧠🌸🔮 Enhanced FDB Scanner — Intent-Aware Signal Detection

Purpose: Bridge between intent specifications and signal detection.
Wraps the existing fdb_scanner_2408.py without modification while adding:
- Intent context awareness
- Structured signal output
- Direct integration with agentic system
- Strategic signal quality assessment

Architecture:
Market Observation → Intent Specification → Enhanced Scanner → Strategic Signals
"""

import logging
import json
import os
import sys
import tempfile
import subprocess
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

from .intent_spec import IntentSpecParser

class EnhancedFDBScanner:
    """
    Intent-aware wrapper for the JGT FDB scanner.
    
    This scanner:
    1. Accepts intent specifications (.jgtml-spec format)
    2. Translates intent into scanning parameters
    3. Invokes the existing fdb_scanner_2408.py
    4. Captures and processes signal outputs
    5. Returns structured signal data with intent context
    """
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("EnhancedFDBScanner")
        self.intent_parser = IntentSpecParser()
        self.signal_history = []
        
    def scan_with_intent(self, intent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for signals using intent specification context."""
        self.logger.info(f"🔍 Starting intent-aware FDB scan")
        
        # Basic implementation for now
        result = {
            "timestamp": datetime.now().isoformat(),
            "intent_context": intent_spec,
            "enhanced_signals": [],
            "recommendations": {"action": "wait", "reason": "Scanner in development"},
            "success": True
        }
        
        return result
    
    def scan_from_spec_file(self, spec_file_path: str) -> Dict[str, Any]:
        """
        Scan using intent specification from file.
        
        Args:
            spec_file_path: Path to .jgtml-spec file
            
        Returns:
            Structured signal data with intent context
        """
        try:
            intent_spec = self.intent_parser.load(spec_file_path)
            return self.scan_with_intent(intent_spec)
        except Exception as e:
            self.logger.error(f"Failed to load spec file {spec_file_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scan_from_observation(self, observation_text: str, 
                            default_instruments: List[str] = None,
                            default_timeframes: List[str] = None) -> Dict[str, Any]:
        """
        Scan based on natural language market observation.
        
        Args:
            observation_text: Natural language market analysis
            default_instruments: Default instruments if not specified
            default_timeframes: Default timeframes if not specified
            
        Returns:
            Structured signal data
        """
        # Convert observation to basic intent specification
        intent_spec = self._observation_to_intent(observation_text, 
                                                  default_instruments, 
                                                  default_timeframes)
        
        return self.scan_with_intent(intent_spec)
    
    def _extract_scan_parameters(self, intent_spec: Dict[str, Any], 
                                instruments: Optional[List[str]] = None,
                                timeframes: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract FDB scanning parameters from intent specification."""
        
        # Use provided instruments/timeframes or extract from spec
        target_instruments = instruments or intent_spec.get("instruments", ["EUR/USD"])
        target_timeframes = timeframes or intent_spec.get("timeframes", ["H4", "H1", "m15"])
        
        # Extract signal configuration from intent
        signals_config = intent_spec.get("signals", [])
        
        # Default scanning parameters
        params = {
            "instruments": target_instruments,
            "timeframes": target_timeframes,
            "quotescount": intent_spec.get("quotescount", 333),
            "demo": intent_spec.get("demo", True),
            "strategy_intent": intent_spec.get("strategy_intent", "Signal Detection"),
            "signal_types": []
        }
        
        # Extract specific signal requirements
        for signal_config in signals_config:
            signal_type = {
                "name": signal_config.get("name"),
                "description": signal_config.get("description"),
                "components": signal_config.get("jgtml_components", {}),
                "validation": signal_config.get("validation", {})
            }
            params["signal_types"].append(signal_type)
        
        return params
    
    def _setup_scan_environment(self, intent_spec: Dict[str, Any], 
                               scan_params: Dict[str, Any]) -> Dict[str, str]:
        """Setup environment variables for enhanced scanning."""
        
        env = os.environ.copy()
        
        # Set instruments and timeframes for scanner
        env["INSTRUMENTS"] = ",".join(scan_params["instruments"])
        env["TIMEFRAMES"] = ",".join(scan_params["timeframes"])
        
        # Configure lots based on intent risk management
        risk_config = intent_spec.get("risk_management", {})
        env["LOTS"] = str(risk_config.get("position_size", 1))
        
        # Set demo/real mode
        if scan_params.get("demo", True):
            env["DEMO_FLAG"] = "1"
        
        # Add intent context to environment
        env["INTENT_CONTEXT"] = json.dumps({
            "strategy": intent_spec.get("strategy_intent", ""),
            "purpose": intent_spec.get("purpose", ""),
            "validation_requirements": intent_spec.get("validation", {})
        })
        
        return env
    
    def _execute_fdb_scan(self, scan_params: Dict[str, Any], 
                         scan_env: Dict[str, str]) -> List[Dict[str, Any]]:
        """Execute the FDB scanner and capture results."""
        
        self.logger.info("🔄 Executing FDB scan...")
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set output directory in environment
            env = scan_env.copy()
            env["FDB_OUTPUT_DIR"] = temp_dir
            
            try:
                # Try to import and run the scanner directly
                try:
                    from jgtml import fdb_scanner_2408
                    
                    # Backup original argv
                    original_argv = sys.argv.copy()
                    
                    # Set up scanner arguments
                    sys.argv = ["fdb_scanner"]
                    if scan_params.get("demo", True):
                        sys.argv.append("--demo")
                    
                    # Run scanner in controlled environment
                    with self._capture_scanner_output(temp_dir) as output_capture:
                        fdb_scanner_2408.main()
                    
                    # Restore argv
                    sys.argv = original_argv
                    
                    # Parse captured signals
                    signals = self._parse_scanner_output(output_capture, temp_dir)
                    
                except ImportError:
                    # Fallback to subprocess execution
                    self.logger.warning("Direct import failed, using subprocess")
                    signals = self._execute_scanner_subprocess(scan_params, env, temp_dir)
                
                return signals
                
            except Exception as e:
                self.logger.error(f"FDB scan execution failed: {e}")
                return []
    
    def _capture_scanner_output(self, output_dir: str):
        """Context manager to capture scanner output."""
        
        class OutputCapture:
            def __init__(self):
                self.signals = []
                self.output_files = []
                
        return OutputCapture()
    
    def _parse_scanner_output(self, output_capture, temp_dir: str) -> List[Dict[str, Any]]:
        """Parse signals from scanner output."""
        
        signals = []
        
        # Look for signal JSON files in temp directory
        for file in os.listdir(temp_dir):
            if file.endswith("_signal.json"):
                try:
                    signal_path = os.path.join(temp_dir, file)
                    with open(signal_path, 'r') as f:
                        signal_data = json.load(f)
                        signals.append(signal_data)
                except Exception as e:
                    self.logger.warning(f"Failed to parse signal file {file}: {e}")
        
        return signals
    
    def _execute_scanner_subprocess(self, scan_params: Dict[str, Any], 
                                   env: Dict[str, str], 
                                   temp_dir: str) -> List[Dict[str, Any]]:
        """Execute scanner as subprocess and parse results."""
        
        try:
            # Build command for fdb_scanner
            cmd = ["python", "-m", "jgtml.fdb_scanner_2408"]
            
            if scan_params.get("demo", True):
                cmd.append("--demo")
            
            # Execute scanner
            result = subprocess.run(
                cmd,
                env=env,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Parse output for signals
            return self._parse_subprocess_output(result.stdout, temp_dir)
            
        except Exception as e:
            self.logger.error(f"Subprocess execution failed: {e}")
            return []
    
    def _parse_subprocess_output(self, stdout: str, temp_dir: str) -> List[Dict[str, Any]]:
        """Parse signals from subprocess output."""
        
        signals = []
        
        # Parse stdout for signal indicators
        for line in stdout.split('\n'):
            if 'Signal Found' in line or '.sh' in line:
                # Try to extract signal information
                try:
                    # Look for corresponding JSON files
                    signal_data = self._extract_signal_from_line(line, temp_dir)
                    if signal_data:
                        signals.append(signal_data)
                except Exception as e:
                    self.logger.warning(f"Failed to parse signal line: {e}")
        
        return signals
    
    def _extract_signal_from_line(self, line: str, temp_dir: str) -> Optional[Dict[str, Any]]:
        """Extract signal data from output line."""
        
        # Basic signal extraction - can be enhanced
        if 'Signal Found' in line:
            return {
                "type": "FDB_SIGNAL",
                "source_line": line.strip(),
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.7  # Default confidence
            }
        
        return None
    
    def _process_signals_with_intent(self, raw_signals: List[Dict[str, Any]], 
                                   intent_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process raw signals with intent context for enhanced analysis."""
        
        enhanced_signals = []
        
        for signal in raw_signals:
            enhanced_signal = signal.copy()
            
            # Add intent context
            enhanced_signal["intent_alignment"] = self._assess_intent_alignment(signal, intent_spec)
            
            # Add quality score
            enhanced_signal["quality_score"] = self._calculate_signal_quality(signal, intent_spec)
            
            # Add strategic context
            enhanced_signal["strategic_context"] = self._add_strategic_context(signal, intent_spec)
            
            # Add risk assessment
            enhanced_signal["risk_assessment"] = self._assess_signal_risk(signal, intent_spec)
            
            enhanced_signals.append(enhanced_signal)
        
        # Sort by quality score
        enhanced_signals.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
        
        return enhanced_signals
    
    def _assess_intent_alignment(self, signal: Dict[str, Any], 
                               intent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how well signal aligns with stated intent."""
        
        alignment = {
            "strategy_match": 0.8,  # Placeholder scoring
            "timeframe_preference": 0.9,
            "risk_tolerance": 0.7,
            "overall_alignment": 0.8
        }
        
        # Enhance with actual intent analysis
        strategy_intent = intent_spec.get("strategy_intent", "")
        if "confluence" in strategy_intent.lower():
            alignment["strategy_match"] = 0.9
        
        return alignment
    
    def _calculate_signal_quality(self, signal: Dict[str, Any], 
                                intent_spec: Dict[str, Any]) -> float:
        """Calculate overall signal quality score."""
        
        # Base quality from signal strength
        base_quality = signal.get("confidence", 0.5)
        
        # Intent alignment bonus
        intent_alignment = self._assess_intent_alignment(signal, intent_spec)
        alignment_bonus = intent_alignment.get("overall_alignment", 0.5) * 0.3
        
        # Market condition assessment
        market_condition_score = 0.7  # Placeholder
        
        quality_score = (base_quality * 0.4 + 
                        alignment_bonus + 
                        market_condition_score * 0.3)
        
        return min(1.0, max(0.0, quality_score))
    
    def _add_strategic_context(self, signal: Dict[str, Any], 
                             intent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Add strategic trading context to signal."""
        
        return {
            "market_phase": "trending",  # Placeholder analysis
            "confluence_factors": ["alligator_mouth_open", "fdb_breakout"],
            "timeframe_hierarchy": "aligned",
            "volume_context": "confirming"
        }
    
    def _assess_signal_risk(self, signal: Dict[str, Any], 
                          intent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk characteristics of signal."""
        
        risk_config = intent_spec.get("risk_management", {})
        
        return {
            "risk_reward_ratio": risk_config.get("target_rr", 2.0),
            "stop_distance": "optimal",
            "position_size": risk_config.get("position_size", 1),
            "max_risk_percent": risk_config.get("max_risk_percent", 2.0)
        }
    
    def _generate_recommendations(self, enhanced_signals: List[Dict[str, Any]], 
                                intent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic recommendations based on enhanced signals."""
        
        if not enhanced_signals:
            return {
                "action": "wait",
                "reason": "No qualifying signals found",
                "next_scan": "continue_monitoring"
            }
        
        best_signal = enhanced_signals[0]
        quality_score = best_signal.get("quality_score", 0)
        
        if quality_score >= 0.8:
            action = "execute"
            reason = f"High-quality signal (score: {quality_score:.2f}) aligns with intent"
        elif quality_score >= 0.6:
            action = "analyze"
            reason = f"Moderate signal (score: {quality_score:.2f}) requires additional validation"
        else:
            action = "wait"
            reason = f"Signal quality below threshold (score: {quality_score:.2f})"
        
        return {
            "action": action,
            "reason": reason,
            "best_signal": best_signal,
            "signal_count": len(enhanced_signals),
            "next_steps": self._generate_next_steps(action, best_signal, intent_spec)
        }
    
    def _generate_next_steps(self, action: str, signal: Dict[str, Any], 
                           intent_spec: Dict[str, Any]) -> List[str]:
        """Generate specific next steps based on recommendation."""
        
        if action == "execute":
            return [
                "Review signal details and risk parameters",
                "Prepare entry order with calculated position size",
                "Set stop loss and take profit levels",
                "Monitor for execution confirmation"
            ]
        elif action == "analyze":
            return [
                "Perform additional confluence analysis",
                "Check higher timeframe context",
                "Validate with additional indicators",
                "Consider reduced position size"
            ]
        else:  # wait
            return [
                "Continue monitoring market conditions",
                "Wait for higher quality signals",
                "Review and adjust intent parameters if needed",
                "Check scanning configuration"
            ]
    
    def _observation_to_intent(self, observation: str, 
                             instruments: List[str] = None,
                             timeframes: List[str] = None) -> Dict[str, Any]:
        """Convert natural language observation to basic intent specification."""
        
        # Basic intent template from observation
        intent = {
            "strategy_intent": f"Signal detection based on observation: {observation[:100]}...",
            "instruments": instruments or ["EUR/USD"],
            "timeframes": timeframes or ["H4", "H1"],
            "signals": [{
                "name": "observation_based_signal",
                "description": f"Signal detection based on: {observation}",
                "jgtml_components": {
                    "fractal_analysis": "jgtpy.fractal_detection",
                    "alligator_state": "TideAlligatorAnalysis.mouth_opening"
                }
            }],
            "risk_management": {
                "position_size": 1,
                "max_risk_percent": 2.0,
                "target_rr": 2.0
            }
        }
        
        # Enhance intent based on observation keywords
        observation_lower = observation.lower()
        
        if "breakout" in observation_lower:
            intent["signals"][0]["jgtml_components"]["momentum"] = "jgtpy.ao_acceleration"
        
        if "confluence" in observation_lower:
            intent["strategy_intent"] = "Multi-indicator confluence detection"
        
        if "bearish" in observation_lower or "sell" in observation_lower:
            intent["bias"] = "bearish"
        elif "bullish" in observation_lower or "buy" in observation_lower:
            intent["bias"] = "bullish"
        
        return intent

# Example usage and testing
def create_example_intent_spec() -> Dict[str, Any]:
    """Create example intent specification for testing."""
    return {
        "strategy_intent": "Capture multi-timeframe Alligator-Fractal confluence",
        "instruments": ["EUR/USD", "GBP/USD"],
        "timeframes": ["H4", "H1", "m15"],
        "signals": [{
            "name": "dragon_breakout",
            "description": "FDB breakout with Alligator mouth opening",
            "jgtml_components": {
                "fractal_analysis": "jgtpy.fractal_detection",
                "alligator_state": "TideAlligatorAnalysis.mouth_opening",
                "momentum": "jgtpy.ao_acceleration"
            }
        }],
        "risk_management": {
            "position_size": 1,
            "max_risk_percent": 2.0,
            "target_rr": 2.0
        }
    }

# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced FDB Scanner with Intent Context")
    parser.add_argument("--spec", help="Path to intent specification file")
    parser.add_argument("--observation", help="Natural language market observation")
    parser.add_argument("--instruments", nargs="*", help="Instruments to scan")
    parser.add_argument("--timeframes", nargs="*", help="Timeframes to scan")
    parser.add_argument("--demo", action="store_true", help="Demo mode")
    
    args = parser.parse_args()
    
    scanner = EnhancedFDBScanner()
    
    if args.spec:
        result = scanner.scan_from_spec_file(args.spec)
    elif args.observation:
        result = scanner.scan_from_observation(
            args.observation, 
            args.instruments, 
            args.timeframes
        )
    else:
        # Test with example spec
        example_spec = create_example_intent_spec()
        result = scanner.scan_with_intent(example_spec)
    
    print(json.dumps(result, indent=2)) 
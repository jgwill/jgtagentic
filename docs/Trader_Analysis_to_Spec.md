# Trader Analysis to Spec Transformation Guide

This guide explains how an LLM can listen to a trader's market analysis and transform it into a `.jgtml-spec` file for use with **IntentSpecParser**.

## 1. Capture the Trader's Narrative

When the trader describes the market, capture:

- Instrument and timeframe observations
- Indicator states (fractals, Alligator mouth states, AO momentum, etc.)
- Pattern descriptions (Elliott Waves, consolidation, breakout levels)
- Overall intent: trend following, breakout, reversal
- Multi-timeframe confluence requirements

## 2. Map Observations to Spec Fields

Translate the narrative into the YAML fields expected by `.jgtml-spec`:

- **`strategy_intent`** – summarize the trader's goal in plain language
- **`instruments`** – list all pairs or assets discussed
- **`timeframes`** – capture the timeframes referenced (supports full hierarchy: m1, m5, m15, H1, H4, D1, W1, MN)
- **`signals`** – one or more named signals derived from the analysis
  - `description` – short explanation of the signal
  - `jgtml_components` – map indicator mentions to the unified JGTML modules
  - `alligator_context` – specify Regular, Big, or Tide Alligator for multi-timeframe analysis

### JGTML Signal Component Mapping

The consolidated AlligatorAnalysis module supports all three Alligator types:

```yaml
alligator_types:
  regular:
    periods: [5, 8, 13]  # Jaw, Teeth, Lips
    purpose: "Primary timeframe trend analysis"
    trader_language: ["trend establishment", "momentum confirmation"]
    
  big:
    periods: [34, 55, 89]
    purpose: "Higher timeframe structure validation" 
    trader_language: ["pullback entry", "retest opportunity"]
    
  tide:
    periods: [144, 233, 377]
    purpose: "Macro trend environment"
    trader_language: ["campaign direction", "major reversal confirmation"]
```

### Core Signal Types Available:
- `all_evalname_signals` - Comprehensive signal evaluation across all contexts
- `sig_normal_mouth_is_open` - Regular Alligator mouth open confirmation
- `sig_is_out_of_normal_mouth` - Price outside Regular Alligator mouth (strong trend)
- `sig_is_in_ctx_teeth` - Price at contextual Alligator teeth level (pullback entry)
- `sig_ctx_mouth_is_open_and_in_ctx_teeth` - Contextual trend with teeth-level entry
- `sig_ctx_mouth_is_open_and_in_ctx_lips` - Contextual trend with lips-level entry (aggressive)

If the trader references wave counts or timeframe confluence, include them in signal descriptions or as custom keys.

## 3. Example Conversation to Spec

**Trader:**
> "On the H4 chart of EUR/USD I see a completed Wave 3 and expect a Wave 4 pullback. The Alligator is opening and the AO shows strong momentum. I'll look for a breakout above 1.0800 with confluence on H1." 

**LLM Generated Spec:**
```yaml
strategy_intent: "Trade EUR/USD Wave 5 breakout"
instruments:
  - "EUR/USD"
timeframes:
  - "H1"
  - "H4"
signals:
  - name: "wave5_breakout"
    description: "H4 Wave 3 complete, breakout above 1.0800 with Alligator mouth opening and AO momentum"
    jgtml_components:
      - fractal_analysis: "jgtpy.fractal_detection"
      - alligator_state: "TideAlligatorAnalysis.mouth_opening"
      - momentum: "jgtpy.ao_acceleration"
      - wave_count: "manual_wave_3_complete"
```

## 4. From Spec to Campaign

Once generated, the spec can be parsed by `IntentSpecParser`, fed into FDBScan or other agents, and turned into entry scripts. The LLM should ensure the YAML remains minimal and only includes details the trader confirms.

---

This document is a living reference for building the translator agent that converts human trading insights into executable JGTML specifications.

# Trader Analysis to Spec Transformation Guide

This guide explains how an LLM can listen to a trader's market analysis and transform it into a `.jgtml-spec` file for use with **IntentSpecParser**.

## 1. Capture the Trader's Narrative

When the trader describes the market, capture:

- Instrument and timeframe observations
- Indicator states (fractals, Alligator, AO momentum, etc.)
- Pattern descriptions (Elliott Waves, consolidation, breakout levels)
- Overall intent: trend following, breakout, reversal

## 2. Map Observations to Spec Fields

Translate the narrative into the YAML fields expected by `.jgtml-spec`:

- **`strategy_intent`** – summarize the trader's goal in plain language
- **`instruments`** – list all pairs or assets discussed
- **`timeframes`** – capture the timeframes referenced
- **`signals`** – one or more named signals derived from the analysis
  - `description` – short explanation of the signal
  - `jgtml_components` – map indicator mentions to the JGTML modules

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

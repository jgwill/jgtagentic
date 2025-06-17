# FDB Trading Automation Guide

This document explains how to detect a valid Fractal Divergent Bar (FDB) signal from the scanner output and automatically launch a trading campaign once the signal is confirmed. It clarifies the importance of using the **last completed bar** and outlines how larger timeframe context guides entry decisions.

## 1. Validate Completed Bars

When the FDB scanner produces a CSV file, the last row corresponds to the most recent candle, which may still be forming. Always disregard this row; only the prior candle is considered **completed** and eligible for analysis.

```
EURUSD_m5.csv (example)
...  previous rows ...
2025-06-05T12:55,1.0902,1.0915,1.0890,1.0908  # <- completed bar
2025-06-05T13:00,1.0908,1.0917,1.0901,1.0910  # <- still forming (skip)
```

If the completed bar triggers an FDB signal, continue to quality scoring.

## 2. Assess Quality

FDB signals are scored based on risk metrics and indicator alignment. A typical rule-set:

- **Quality Score ≥ 7.0** – consider trade
- **Illusions Detected ≤ 1** – ensure minimal conflicting signals

High-quality signals with no disqualifying conditions move to the entry stage.

## 3. Check Higher Timeframe Trend

Before acting on a lower timeframe signal (m15, H1, H4), consult the broader trend:

1. **Monthly / Weekly / Daily** – Determine bullish or bearish bias.
2. Align the lower timeframe FDB signal with this bias.
3. Avoid trades that contradict the larger trend.

## 4. Launch Campaign

Once a valid, high-quality signal aligns with the higher-timeframe context, create a campaign:

1. Generate the entry script using `entry_script_gen.py`.
2. Prepare the environment with `campaign_env.py`.
3. Record the decision via `agentic_decider.py`.
4. Execute the entry script to open the position.

Automation can extend this flow by chaining these modules in an orchestrator or scheduled job.

## 5. Next Steps

- Integrate with `jgtml` scanner modules for real-time FDB detection.
- Automate campaign creation when quality thresholds are met.
- Maintain detailed logs for each trade decision to refine the model.

# JGTML Signal Processing Service Specification

## 1. Purpose

The JGTML Signal Processing service is responsible for taking a validated JGTML Specification (`JGTMLSpec`) and performing detailed financial indicator calculations, applying trading logic, and generating concrete trading signals. It acts as the bridge between the abstract, trader-defined specification and actionable intelligence that can be used for generating trading scripts or alerts. This component embodies the core analytical engine that interprets the JGTML spec against market data.

## 2. Inputs

*   **Validated `JGTMLSpec`**:
    *   The primary input, assumed to have been successfully parsed and validated by a preceding component (e.g., `IntentSpecParser`).
    *   Contains `strategy_intent`, `instruments`, `timeframes`, and an array of `signals`, where each signal has `name`, `description`, `jgtml_components`, and optionally `alligator_context`.
*   **Market Data**:
    *   Historical and potentially real-time price data (OHLCV - Open, High, Low, Close, Volume) for the instruments and timeframes specified in the `JGTMLSpec`.
    *   This data is sourced externally (e.g., from a market data provider, exchange API, or historical database). The service needs a configured way to access this data.
*   **Configuration (Potentially)**:
    *   Indicator parameters if not fully specified within the `JGTMLSpec` or if defaults are needed.
    *   References to specific calculation libraries or modules (e.g., paths or identifiers for `JGTIDS.py`, `JGTCDS.py`, `TideAlligatorAnalysis`).

## 3. Processing Logic (High-Level)

1.  **Initialization**:
    *   Load the validated `JGTMLSpec`.
    *   Establish connections to market data sources.

2.  **Iterate Through Signals**:
    *   For each `signal` object within the `JGTMLSpec.signals` array:
        *   **Data Retrieval**: Fetch the necessary market data for the signal's specified `instruments` and `timeframes`.
        *   **Component Processing**: For each entry in the `jgtml_components` array of the current signal:
            *   Identify the component type (e.g., `fractal_analysis`, `alligator_state`, `momentum`, `wave_count`, `price_level_breakout`).
            *   Invoke the relevant calculation module or logic (e.g., call functions within `JGTIDS.py` for raw indicator values, `TideAlligatorAnalysis` for Alligator-specific logic).
            *   Pass market data and any specific parameters from the component's value.
            *   Store the results of these calculations (e.g., indicator values, detected patterns, Boolean states).
        *   **Signal Aggregation & Evaluation**:
            *   Combine the results from all processed `jgtml_components` for the current signal.
            *   Apply any implicit or explicit logic (e.g., if all components must be true for the signal to be active).
            *   Determine if the overall conditions for the trading signal (as described by its `name` and `description`) are met.
            *   This may involve comparing calculated values against thresholds, identifying specific sequences, or matching complex conditions.
        *   **Output Generation (Per Signal)**: If the signal conditions are met, generate a structured output detailing the active signal, including target price levels, direction (buy/sell), confidence, etc.

3.  **Signal Ordering & Prioritization (Optional)**:
    *   If multiple signals become active, apply logic from `SignalOrderingHelper` (if defined) to rank or prioritize them.

4.  **Chaos Data File Generation (`JGTCDS.py`)**:
    *   If specified or implied by the `JGTMLSpec` or its components, generate relevant Chaos Data files based on the analyses.

5.  **Collate Results**:
    *   Compile all active signals and their associated data into a "Processed Signal Package."

## 4. Outputs

*   **Processed Signal Package**: A structured data object (e.g., JSON) containing:
    *   A reference to the original `JGTMLSpec` (or its key identifiers).
    *   Timestamp of processing.
    *   **Active Signals**: An array of objects, where each object represents a successfully triggered signal from the input spec. Each active signal object should include:
        *   `signal_name`: (from `JGTMLSignal.name`)
        *   `instrument`: e.g., "EUR/USD"
        *   `timeframe`: e.g., "H4"
        *   `action`: e.g., "BUY", "SELL", "MONITOR"
        *   `entry_price_target` (Optional): Suggested entry price.
        *   `stop_loss_target` (Optional): Suggested stop-loss price.
        *   `take_profit_target` (Optional): Suggested take-profit price.
        *   `confidence_score` (Optional): A metric indicating the strength or reliability of the signal.
        *   `supporting_data`: Key indicator values or conditions that led to the signal firing (e.g., `{"AO_value": 0.0025, "alligator_lips_crossed_teeth": true}`).
    *   **Calculation Details (Optional, for debugging/transparency)**: Intermediate indicator values or states.
    *   **Generated Files (Optional)**: Paths or references to any generated files (e.g., `JGTCDS.py` outputs).
    *   **Processing Status**:
        *   `status`: "Success", "Partial Success" (e.g., some signals processed, others failed), "Failure".
        *   `message`: Details on the outcome, including any errors encountered for specific signals or components.

## 5. Key Considerations & Interactions

*   **Backend Service**: This component is envisioned as a backend service, likely implemented in Python due to the mention of `.py` files.
*   **Market Data Dependency**: Robust access to accurate and timely market data is critical. The service needs strategies for handling missing data or data errors.
*   **Modularity**: The calculation logic for different JGTML components (`JGTIDS.py`, `TideAlligatorAnalysis`, etc.) should be modular and extensible to support new types of analysis.
*   **Error Handling**: Comprehensive error handling is needed for issues like:
    *   Inability to fetch market data.
    *   Errors during indicator calculation.
    *   Ambiguous or unsupported `jgtml_components`.
*   **Performance**: For strategies involving multiple instruments, timeframes, or complex calculations, performance will be a consideration.
*   **Configuration**: How specific calculation parameters (e.g., periods for moving averages, levels for RSI) are managed – whether they are part of the `JGTMLSpec` or configured within this service – needs clear definition.
*   **State Management**: This service is generally stateless in terms of long-term memory of past signals (that's for the Trading Echo Lattice), but it processes one `JGTMLSpec` at a time.
*   **Upstream Dependency**: Relies on a validated `JGTMLSpec` from a component like `IntentSpecParser`.
*   **Downstream Consumer**: The "Processed Signal Package" is the primary input for the `EntryScriptGen` service.
*   **Logging**: Detailed logging of processing steps, decisions, and errors is essential for debugging and audit trails.


# JGTML Execution Core Service Specification

## 1. Purpose

The JGTML Execution Core service is responsible for taking a validated JGTML Specification (`JGTMLSpec`) and performing detailed financial indicator calculations, applying trading logic, and generating concrete trading signals. It acts as the bridge between the abstract, trader-defined specification and actionable intelligence that can be used for generating trading campaigns or alerts. This component embodies the core analytical engine that interprets the JGTML spec against market data, runs the spec, validates signals, and makes decisions.

## 2. Inputs

*   **Validated `JGTMLSpec`**:
    *   The primary input, assumed to have been successfully parsed and validated by a preceding component (e.g., `IntentSpecParser`).
    *   Contains `strategy_intent`, `instruments`, `timeframes`, and an array of `signals`, where each signal has `name`, `description`, `jgtml_components`, and optionally `alligator_context`.
*   **Market Data**:
    *   Historical and potentially real-time price data (OHLCV - Open, High, Low, Close, Volume) for the instruments and timeframes specified in the `JGTMLSpec`.
    *   This data is sourced externally (e.g., from a market data provider, exchange API, or historical database). The service needs a configured way to access this data.
*   **Configuration (Potentially)**:
    *   Indicator parameters if not fully specified within the `JGTMLSpec` or if defaults are needed (e.g., for AO, Alligator).
    *   References to specific calculation libraries or modules (e.g., paths or identifiers for `JGTIDS.py`, `JGTCDS.py`, `TideAlligatorAnalysis`).

## 3. Processing Logic (High-Level)

1.  **Initialization (`run_spec()` executor start)**:
    *   Load the validated `JGTMLSpec`.
    *   Establish connections to market data sources.
    *   Initialize indicator loaders (e.g., for Awesome Oscillator, Alligator).

2.  **Iterate Through Signals (Signal Validator Engine)**:
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
        *   **Output Generation (Per Signal)**: If the signal conditions are met, generate a structured output detailing the active signal.

3.  **Signal Ordering & Prioritization (Optional)**:
    *   If multiple signals become active, apply logic from `SignalOrderingHelper` (if defined) to rank or prioritize them.

4.  **Chaos Data File Generation (`JGTCDS.py`) (Optional)**:
    *   If specified or implied by the `JGTMLSpec` or its components, generate relevant Chaos Data files based on the analyses.

5.  **Decision Node (ENTER / WAIT / EXIT)**:
    *   Based on the validated and potentially prioritized active signals, the core makes a decision:
        *   `ENTER`: Conditions are met for initiating a trade.
        *   `WAIT`: Conditions are not yet met, or further confirmation is needed.
        *   `EXIT`: Conditions are met for closing an existing position (if managing state).
    *   This decision is a key part of the "Processed Signal Package."

6.  **Collate Results**:
    *   Compile all active signals, their associated data, and the decision node output into a "Processed Signal Package."

## 4. Outputs

*   **Processed Signal Package**: A structured data object (e.g., JSON) containing:
    *   A reference to the original `JGTMLSpec` (or its key identifiers).
    *   Timestamp of processing.
    *   **Decision**: The output from the decision node (e.g., "ENTER", "WAIT", "EXIT").
    *   **Active Signals**: An array of objects, where each object represents a successfully triggered and validated signal. Each active signal object should include:
        *   `signal_name`: (from `JGTMLSignal.name`)
        *   `instrument`: e.g., "EUR/USD"
        *   `timeframe`: e.g., "H4"
        *   `action_type`: (derived from signal, e.g., "BUY_SETUP", "SELL_TRIGGER")
        *   `entry_price_target` (Optional): Suggested entry price.
        *   `stop_loss_target` (Optional): Suggested stop-loss price.
        *   `take_profit_target` (Optional): Suggested take-profit price.
        *   `confidence_score` (Optional): A metric indicating the strength or reliability of the signal.
        *   `supporting_data`: Key indicator values or conditions that led to the signal firing (e.g., `{"AO_value": 0.0025, "alligator_lips_crossed_teeth": true}`).
    *   **Calculation Details (Optional, for debugging/transparency)**: Intermediate indicator values or states.
    *   **Generated Files (Optional)**: Paths or references to any generated files (e.g., `JGTCDS.py` outputs).
    *   **Processing Status**:
        *   `status`: "Success", "Partial Success", "Failure".
        *   `message`: Details on the outcome, including any errors encountered for specific signals or components.

## 5. Key Considerations & Interactions

*   **Backend Service**: This component is envisioned as a backend service, likely implemented in Python.
*   **Market Data Dependency**: Robust access to accurate and timely market data is critical.
*   **Modularity**: The calculation logic for different JGTML components should be modular.
*   **Error Handling**: Comprehensive error handling for data fetching, calculations, etc.
*   **Performance**: Important for complex strategies.
*   **State Management**: Generally stateless for a single spec processing, but might interact with a larger state if managing open positions for EXIT decisions.
*   **Upstream Dependency**: Relies on a validated `JGTMLSpec` from `IntentSpecParser`.
*   **Downstream Consumer**: The "Processed Signal Package" is the primary input for the `CampaignLauncher` service.
*   **Logging**: Detailed logging is essential.

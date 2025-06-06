
# Echo Spiral Flow: From Trader Intent to Actionable Specification

This document details the "Echo Spiral Flow," a multi-stage process designed to transform a trader's natural language narrative into a structured, machine-actionable `.jgtml-spec` (Jean-Guillaume's Trading Machine-Learning specification). This flow is central to the application, enabling the conversion of qualitative insights into quantitative instructions.

---

## 1. 🎤 Trader Intent

*   **What it is:** The initial stage where the trader expresses their market analysis, strategy, indicator observations, chart patterns, and overall trading plan using natural language. This can also be a refined narrative produced with the help of the "Trading Narrative Assistant" chat feature.
*   **Application Component(s):**
    *   `components/TraderIntentInput.tsx`: Captures the primary narrative.
    *   `components/chat/ChatAssistantContainer.tsx`: Allows users to refine their narrative through conversation. The chat history can be summarized to produce the narrative for this step.
*   **Purpose:** To capture the trader's raw or refined thoughts and ideas about a potential trade or market setup.
*   **Description (from UI):** Natural language: market structure, waves, levels.
*   **Example Input (Natural Language Narrative):**
    ```
    On the H4 chart of EUR/USD I see a completed Wave 3 and expect a Wave 4 pullback. The Alligator is opening and the AO shows strong momentum. I'll look for a breakout above 1.0800 with confluence on H1. My main strategy is trend following for a Wave 5.
    ```
*   **Example Output:** A plain text string representing the trader's narrative.
*   **Relevant Prompts/Key Logic:**
    *   The primary input is the trader's narrative itself.
    *   If the "Trading Narrative Assistant" is used, its conversation history is summarized by the `geminiService.summarizeChatHistoryForNarrative` function. This function uses the `SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT` template from `services/promptTemplates.ts`.
        *   **`SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT` Intent:** Instructs the LLM to act as an expert summarizer. It's tasked with analyzing a chat history (`{chatHistoryString}` placeholder), identifying key elements of the user's trading plan, and synthesizing them into a concise trading narrative, stripping away conversational filler. The output is constrained to be ONLY the plain text narrative.

---

## 2. 🧠 LLM Translation Engine

*   **What it is:** This step takes the natural language narrative from the "Trader Intent" stage and uses a Large Language Model (LLM), specifically Google's Gemini, to translate it into a structured JSON object: the `.jgtml-spec`.
*   **Application Component(s):**
    *   UI: `components/LLMTranslationEngine.tsx`
    *   Logic: `services/geminiService.ts` (specifically the `translateNarrativeToSpec` function).
*   **Purpose:** To convert the qualitative, human-readable narrative into a quantitative, machine-readable format that precisely defines the trading strategy according to the JGTML schema.
*   **Description (from UI):** Parses narrative → `.jgtml-spec` using pattern rules.
*   **Example Input:** The natural language narrative from the "Trader Intent" step.
*   **Example Output (A `.jgtml-spec` JSON object):**
    ```json
    {
      "strategy_intent": "Trend following for Wave 5 after a Wave 4 pullback on EUR/USD.",
      "instruments": ["EUR/USD"],
      "timeframes": ["H4", "H1"],
      "signals": [
        {
          "name": "wave4_pullback_entry_h4",
          "description": "Observing a completed Wave 3 on EUR/USD H4, expecting a Wave 4 pullback. Alligator is opening and AO shows strong momentum. Looking for trend continuation into Wave 5.",
          "jgtml_components": [
            {"wave_count": "manual_wave_3_complete_expect_wave_4_pullback"},
            {"alligator_state": "AlligatorAnalysis.mouth_opening"},
            {"momentum": "jgtpy.ao_acceleration"}
          ],
          "alligator_context": "Regular"
        },
        {
          "name": "breakout_confluence_h1",
          "description": "Anticipating a breakout above 1.0800 on EUR/USD, with supportive confluence expected on the H1 timeframe.",
          "jgtml_components": [
            {"price_level_breakout": "1.0800_above"}
          ]
        }
      ]
    }
    ```
*   **Relevant Prompts/Key Logic:**
    *   The core prompt used is `TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE` found in `services/promptTemplates.ts`.
    *   **`TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE` Intent & Structure:**
        1.  **Role Playing:** Instructs the LLM: "You are an expert trading assistant."
        2.  **Task Definition:** "Your task is to translate a trader's market analysis narrative into a structured JSON format representing a '.jgtml-spec'."
        3.  **Schema Enforcement:** Explicitly provides the TypeScript interfaces for `JGTMLSpec`, `JGTMLSignal`, and `JGTMLSignalComponent` directly within the prompt to define the required JSON structure.
        4.  **Input Placeholder:** Uses `{traderNarrative}` to insert the user's narrative.
        5.  **Output Constraints:** Crucially instructs the LLM: "generate ONLY the JSON object adhering to the schema described above. Do not include any other text, explanations, or markdown formatting like \`\`\`json ... \`\`\`." It also specifies `responseMimeType: "application/json"` in the API call config.
        6.  **Example Mappings:** Provides concrete examples of how to translate narrative phrases into `jgtml_components` (e.g., "Alligator is opening" -> `{"alligator_state": "AlligatorAnalysis.mouth_opening"}`).
        7.  **Conciseness guidance:** "Keep your content short and remove of any friendly/casual stuff, go to the point."

---

## 3. 🟩 IntentSpecParser (Interpreter)

*   **What it is:** This stage takes the `.jgtml-spec` JSON generated by the LLM and (currently in this application) *simulates* parsing and validating it.
*   **Application Component(s):**
    *   UI: `components/IntentSpecParser.tsx` (nested in a FlowCard with this title in `App.tsx`)
    *   Logic: `services/parserService.ts` (contains `simulateIntentSpecParsing` function).
*   **Purpose:** To ensure the LLM-generated spec is valid, well-formed, and can be reliably used by downstream processing engines. In the simulation, it also produces a "signal package preview."
*   **Description (from UI):** Reads `.jgtml-spec` → constructs signal package.
*   **Example Input:** The `.jgtml-spec` JSON from the "LLM Translation Engine" step.
*   **Example Output (Simulated `ParsedSpecOutput`):**
    ```json
    {
      "status": "Success",
      "message": "JGTML spec successfully received and validated (simulation). Ready for signal processing.",
      "signalPackagePreview": {
        "strategy": "Trend following for Wave 5 after a Wave 4 pullback on EUR/USD.",
        "instruments": ["EUR/USD"],
        "timeframes": ["H4", "H1"],
        "signalCount": 2,
        "firstSignalName": "wave4_pullback_entry_h4",
        "uniqueComponents": "wave_count, alligator_state, momentum, price_level_breakout"
      }
    }
    ```
*   **Relevant Prompts/Key Logic:** No LLM prompts are used. This is a rule-based parsing and validation process (currently simulated with a delay and basic checks).

---

## 4. 🟦 JGTML Execution Core

*   **What it is:** This is a conceptual step in the UI, representing where the validated `JGTMLSpec` would be used by a backend Python engine (the actual JGTML library) to perform detailed financial indicator calculations against market data. It processes the `jgtml_components` for the specified instruments and timeframes.
*   **Application Component(s):** Represented by a `FlowCard` in `App.tsx`. Detailed in `services/jgtmlExecutionCore.spec.md`.
*   **Purpose:** To interpret and execute strategy commands from the spec. It embodies the core analytical engine.
*   **Description (from UI):** Core logic to interpret and execute strategy commands from spec.
*   **Conceptual Sub-Components:**
    *   `run_spec() executor`
    *   `Indicator loader (AO, Alligator)`
    *   `Signal validator engine`
    *   `Decision node: ENTER / WAIT / EXIT`
*   **Example Input:**
    *   The validated `.jgtml-spec` JSON.
    *   Live or historical market data.
*   **Example Output (Conceptual "Processed Signal Package"):**
    ```json
    {
      "reference_spec_id": "some_unique_id_from_spec",
      "processing_timestamp": "2023-10-27T10:30:00Z",
      "active_signals": [
        {
          "signal_name": "wave4_pullback_entry_h4",
          "instrument": "EUR/USD",
          "timeframe": "H4",
          "action": "BUY_ALERT",
          "entry_price_target": 1.0780,
          "stop_loss_target": 1.0730,
          "take_profit_target": 1.0900,
          "confidence_score": 0.8,
          "supporting_data": { "AO_value_at_signal": 0.0012 }
        }
      ],
      "status": "Success",
      "message": "Signal processing complete. 1 active signal identified."
    }
    ```
*   **Relevant Prompts/Key Logic:** No LLM prompts. This involves algorithmic data processing, typically using libraries like `JGTIDS.py`, `JGTCDS.py`, and `TideAlligatorAnalysis` as outlined in its spec.

---

## 5. 📦 CampaignLauncher

*   **What it is:** A conceptual step. This stage would take the "Processed Signal Package" (output from the JGTML Execution Core) and materialize the validated signal into an executable campaign script or API action.
*   **Application Component(s):** Represented by a `FlowCard` in `App.tsx`. Detailed in `services/campaignLauncher.spec.md`.
*   **Purpose:** To automate the creation of the actual code or API calls needed to execute the identified trading signals.
*   **Description (from UI):** Materializes validated signal into an executable campaign script or API action.
*   **Example Input:** The "Processed Signal Package."
*   **Example Output (Conceptual pseudo-code for a Python script):**
    ```python
    # Script for signal: wave4_pullback_entry_h4 on EUR/USD
    signal_params = {
        "instrument": "EURUSD", # Platform specific
        "action": "BUY",
        "quantity": 0.1,
        "entry_price": 1.0780,
        "stop_loss": 1.0730,
        "take_profit": 1.0900
    }
    # exchange_client.create_limit_buy_order(...)
    print(f"Attempting to place BUY order for {signal_params['instrument']}...")
    ```
*   **Relevant Prompts/Key Logic:** No LLM prompts. This is template-based or rule-based code generation or API interaction.

---

## 6. 🟫 Echo Lattice (Memory Crystallization)

*   **What it is:** The conceptual persistent storage system ("memory crystal") of the entire workflow, recording data from all preceding steps.
*   **Application Component(s):** Represented by a `FlowCard` in `App.tsx`. Detailed in `services/echoLattice.spec.md`.
*   **Purpose:** To create a comprehensive historical record for analysis, feedback, and refinement. This data is vital for the "Echo Spiral" concept, enabling learning and improvement over time (e.g., refining LLM prompts based on translation success and trade outcomes).
*   **Description (from UI):** Records outcome + feedback to memory crystal.
*   **Example Input (Data being logged):** Original narrative, `.jgtml-spec`, parsing results, processed signals, campaign script info, trade execution details, market conditions, user feedback.
*   **Example Output:** A structured, queryable database.
*   **Relevant Prompts/Key Logic:** No LLM prompts for its direct operation. However, the data stored is crucial for *future prompt engineering* and potential *LLM fine-tuning*. Successful narrative-to-spec pairs can serve as few-shot examples for improving `TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE`.

---

# Trader Intent to JGTML Spec Transformation

This web application demonstrates a flow for capturing a trader's market analysis in natural language, translating it into a structured JGTML (Juno Markets Trading Meta Language) specification using a Large Language Model (LLM), and then (simulating) parsing this specification for further processing.

The primary goal is to bridge the gap between human trading insights and automated trading systems by converting qualitative narratives into machine-readable and actionable instructions.

## Overview of the Flow

The application visualizes the following conceptual steps:

1.  **🔁 Echo Spiral Flow**: The overarching concept representing the continuous loop from idea to execution and feedback.
2.  **🎤 Trader Intent**: The user inputs their trading analysis and strategy in natural language.
3.  **🧠 LLM Translation Engine**: The narrative is sent to the Google Gemini API, which translates it into a structured JSON format (`.jgtml-spec`).
4.  **📜 IntentSpecParser**: The generated JGTML spec is then (currently simulated) parsed to validate its structure and prepare it for signal processing.
5.  **🧬 JGTML Signal Processing (Conceptual)**: This step, envisioned to run on a backend (e.g., Python), would involve detailed indicator calculations and signal generation based on the parsed spec.
6.  **📜 EntryScriptGen (Conceptual)**: Runnable trading scripts (e.g., bash, Python) would be generated from the processed signals.
7.  **🗃️ Trading Echo Lattice (Conceptual)**: Trade outcomes and feedback would be recorded, creating a memory crystal to refine future strategies and LLM prompts.

## Key Features

*   **Natural Language Input**: Allows traders to describe their strategies using their own words.
*   **LLM-Powered Translation**: Leverages Google's `gemini-2.5-flash-preview-04-17` model to convert narratives into structured JGTML JSON.
*   **Structured Specification**: Produces a well-defined `.jgtml-spec` JSON output.
*   **Simulated Parsing**: Demonstrates the next step of validating and interpreting the JGTML spec.
*   **Visual Workflow**: Clearly presents each stage of the transformation process.
*   **Responsive UI**: Designed with Tailwind CSS for a clean and modern user experience.
*   **Error Handling**: Provides feedback for API or parsing issues.

## Technology Stack

*   **Frontend**:
    *   React 19
    *   TypeScript
    *   Tailwind CSS
*   **LLM Integration**:
    *   `@google/genai` SDK for Google Gemini API
    *   Model: `gemini-2.5-flash-preview-04-17`
*   **Build/Development**:
    *   ESM modules with import maps (via `esm.sh`) for simplified dependency management in the browser.

## How It Works

1.  **`App.tsx`**: The main component orchestrating the UI and data flow. It manages state for the narrative, generated spec, and parsed output.
2.  **`TraderIntentInput.tsx`**: A form component where the user enters their trading narrative. It includes an option to use an example narrative.
3.  **`geminiService.ts`**: Handles communication with the Google Gemini API. It constructs a detailed prompt including the JGTMLSpec TypeScript interface to guide the LLM in generating the correct JSON structure. It also includes logic to clean up the LLM response.
4.  **`LLMTranslationEngine.tsx`**: Displays the JGTML spec received from the Gemini API or any errors encountered during translation.
5.  **`parserService.ts`**: Simulates the parsing of the JGTML spec. In a real-world scenario, this would involve more complex validation and transformation logic, likely on a backend.
6.  **`IntentSpecParser.tsx`**: Displays the results from the `parserService` or any parsing errors.
7.  **`FlowCard.tsx`**: A reusable UI component for displaying each step in the workflow.
8.  **`types.ts`**: Defines TypeScript interfaces for `JGTMLSpec`, `TraderInput`, `ParsedSpecOutput`, etc.
9.  **`constants.ts`**: Stores global constants like the Gemini model name and example narrative.
10. **`components/icons/LucideIcons.tsx`**: Provides SVG icons used throughout the application.

## Setup and Running

1.  **Clone the repository (if applicable) or ensure all files are in their correct directories.**
2.  **API Key**:
    *   This application requires a Google Gemini API key.
    *   The API key **must** be set as an environment variable named `API_KEY`.
    *   The application reads this key via `process.env.API_KEY`.
    *   **Important**: Do not hardcode your API key in the source code. The application is designed to assume this environment variable is pre-configured in the execution environment.
3.  **Serve the `index.html` file**:
    *   You can use a simple HTTP server (like `http-server` via `npx http-server .`) or any other web server to serve the `index.html` file.
    *   Ensure the server can correctly serve ES modules and associated files.
4.  **Open in Browser**: Access the application through the URL provided by your HTTP server.

## Project Structure

```
.
├── README.md
├── ROADMAP.md
├── index.html           # Main HTML entry point
├── index.tsx            # React application root
├── metadata.json        # Application metadata
├── App.tsx              # Main application component
├── constants.ts         # Global constants
├── types.ts             # TypeScript type definitions
├── components/          # UI components
│   ├── FlowCard.tsx
│   ├── IntentSpecParser.tsx
│   ├── LLMTranslationEngine.tsx
│   ├── TraderIntentInput.tsx
│   └── icons/
│       └── LucideIcons.tsx
└── services/            # Business logic and API interactions
    ├── geminiService.ts
    └── parserService.ts
```

This project serves as a prototype and foundation for building more sophisticated tools for agentic trading and strategy automation.

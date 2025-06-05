# Trader Intent to JGTML Spec Transformation

This web application demonstrates a flow for capturing a trader's market analysis in natural language, translating it into a structured JGTML (Jean-Guillaume's Trading Machine-Learning) specification using a Large Language Model (LLM), and then (simulating) parsing this specification for further processing.

The primary goal is to bridge the gap between human trading insights and automated trading systems by converting qualitative narratives into machine-readable and actionable instructions, designed to be compatible with the JGTML Python library developed by Jean-Guillaume.

## Overview of the Flow

The application visualizes the following conceptual steps:

1.  **🔁 Echo Spiral Flow**: The overarching concept representing the continuous loop from idea to execution and feedback.
2.  **🎤 Trader Intent**: The user inputs their trading analysis and strategy in natural language.
3.  **🧠 LLM Translation Engine**: The narrative is sent to the Google Gemini API, which translates it into a structured JSON format (`.jgtml-spec`).
4.  **📜 IntentSpecParser**: The generated JGTML spec is then (currently simulated) parsed to validate its structure and prepare it for signal processing.
5.  **🧬 JGTML Signal Processing (Conceptual)**: This step, envisioned to run on a backend (e.g., Python using the JGTML library), would involve detailed indicator calculations and signal generation based on the parsed spec.
6.  **📜 EntryScriptGen (Conceptual)**: Runnable trading scripts (e.g., bash, Python) would be generated from the processed signals.
7.  **🗃️ Trading Echo Lattice (Conceptual)**: Trade outcomes and feedback would be recorded, creating a memory crystal to refine future strategies and LLM prompts.

## JGTML: Towards a Trading Meta-Language?

An interesting question emerged during the development of this application. Initially, the AI misinterpreted "JGTML" as potentially standing for a generic "Trading Meta Language." While JGTML is firmly rooted in "Jean-Guillaume's Trading Machine-Learning" library, this accidental consideration raises a fascinating point relevant to this project's core:

*   Could the principles and structures explored here, inspired by JGTML, contribute to the evolution of a more formal **"Trading Meta Language"**?
*   Is this a new way for traders to articulate complex analyses and strategies, moving beyond simple narratives towards a standardized, yet expressive, descriptive framework?
*   Could such a language streamline the path from nuanced human insight to unambiguously machine-interpretable instructions, ultimately aiding in the transformation of analysis into actionable, potentially wealth-generating, automated trades?

Exploring this concept, a "Trading Meta Language" might involve standardizing vocabularies for market phenomena, indicator states, risk parameters, and strategic intentions. The `.jgtml-spec` itself is a nascent form of this – a structured dialect. The ongoing development of this application, and the JGTML library it supports, could implicitly or explicitly explore these questions, potentially refining how traders communicate intent to machines. This remains an open, evolving thought, a testament to the dynamic interplay between human language, financial markets, and artificial intelligence.

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
9.  **`constants.ts`**: Stores global constants like the Gemini model name.
10. **`components/icons/LucideIcons.tsx`**: Provides SVG icons used throughout the application.
11. **`data/exampleNarratives.ts`**: Stores example narratives for user convenience.
12. **`services/promptTemplates.ts`**: Contains the detailed prompt templates used for communicating with the Gemini API.


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
│   ├── chat/              # Chat specific components
│   │   ├── ChatAssistantContainer.tsx
│   │   ├── ChatInput.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── ChatWindow.tsx
│   │   ├── CameraModal.tsx
│   │   └── MarkdownRenderer.tsx
│   └── icons/
│       └── LucideIcons.tsx
├── services/            # Business logic and API interactions
│   ├── geminiService.ts
│   ├── parserService.ts
│   ├── chatGeminiService.ts
│   ├── chatLocalStorageService.ts
│   └── promptTemplates.ts
├── hooks/               # Custom React hooks
│   ├── useChatSpeechRecognition.ts
│   └── useChatSpeechSynthesis.ts
├── data/                # Static data
│   └── exampleNarratives.ts
└── specs.miagemchat/    # Specification documents (internal dev use)
    └── ...
```

This project serves as a prototype and foundation for building more sophisticated tools for agentic trading and strategy automation based on the JGTML (Jean-Guillaume's Trading Machine-Learning) Python library.

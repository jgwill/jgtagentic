
# GeminiService.ts - Specification (SpecLang Aligned) - Revised

## Overall Goal/Intent

The `GeminiService.ts` module serves as the **dedicated intermediary** between Mia's Gem Chat Studio application and the Google Gemini API. Its primary purpose is to encapsulate all direct API interactions, including:
*   Managing the AI chat session lifecycle.
*   Sending user-generated content (text, images, audio) to the specified Gemini model.
*   Processing and relaying API responses, with a primary focus on streaming text.
*   Handling API key configuration and validation.
*   Allowing dynamic adjustments to the AI's system instructions and the active model.
This service aims to provide a clean, robust, and abstracted interface to the Gemini API for the rest of the application.

## Key Behaviors & Responsibilities

1.  **API Key Configuration and Status:**
    *   **Behavior (`getApiKeyStatus`):** On initialization and on demand, the service checks for the presence of a Gemini API key (prioritizing `MIAGEM_API_KEY` then falling back to `API_KEY` from `process.env`). It reports whether a key is configured and if the fallback key is being used.
    *   **System Impact:** If no API key is available, the service will be unable to initialize a chat session or communicate with the Gemini API. This operational status (key configured or not, with any warnings) is made available to the application, which should then inform the user appropriately (e.g., displaying an error and disabling chat functionality).

2.  **AI Chat Session Management:**
    *   **Behavior (Internal Chat State & Initialization):** Manages an internal `Chat` instance provided by the `@google/genai` SDK. This instance is created (`_initializeChatInternal`, `getChatInstance`) using the configured API key, the active AI model name, the current system instruction, and an optional message history.
    *   **Intent:** To maintain a persistent conversational context with the Gemini model according to the application's current settings (persona, model).
    *   **Behavior (Re-initialization with History - `reinitializeChatWithHistory`):** Provides a mechanism to reset and re-establish the chat session with potentially new settings (model, system instruction) while seeding it with a provided message history.
    *   **Intent:** To ensure conversational continuity when users load saved sessions, change AI personas, or modify AI model settings. The history (formatted by `formatAppMessagesToGeminiHistory`) provides the AI with the necessary context from past interactions.
    *   **Behavior (Resetting Chat Session - `resetChatSession`):** Clears or re-initializes the internal AI chat instance.
    *   **Intent:** To allow the application to start a fresh AI conversation when the user clears the chat, or to apply new system instructions immediately (e.g., after a persona change).

3.  **Dynamic Configuration of AI Behavior:**
    *   **System Instructions (`setSystemInstructionForSession`):** Allows the application to dynamically update the guiding system prompt for the AI.
    *   **Intent:** To enable persona-specific behaviors and allow users to customize how the AI responds, by changing the foundational instructions given to the Gemini model.
    *   **AI Model (`setCurrentChatModel`):** Permits the application to change the specific Gemini model (e.g., `gemini-2.5-flash-preview-04-17`) being used.
    *   **Intent:** To allow users to select different AI models, potentially with varying capabilities or for specific tasks, including fine-tuned models.
    *   **System Impact:** Changes to system instructions or the model typically require the chat session to be re-initialized to take effect, which the service manages.

4.  **Message Transmission and Reception (Streaming Focus):**
    *   **Behavior (`sendMessageStreamToAI`):**
        *   Accepts user message text, callbacks for handling stream events (`onChunk`, `onError`, `onComplete`), and optional image/audio data.
        *   Validates API key presence before proceeding; if absent, it signals an error immediately via the `onError` callback.
        *   Constructs a multimodal request if image or audio data is provided, ensuring all content is correctly formatted as `Part` objects for the API.
        *   Initiates a streaming request to the Gemini API using `chatInstance.sendMessageStream()`.
        *   As text chunks arrive from the API, it invokes the `onChunk` callback, enabling the application to render the AI's response incrementally.
        *   Signals successful completion via `onComplete` or errors via `onError`, providing descriptive messages and a flag for definitive (unrecoverable) errors.
    *   **Intent:** To provide a highly responsive user experience by displaying AI-generated text as it becomes available, rather than waiting for the entire response. This function is the primary pathway for user-AI interaction.

5.  **Message History Preparation (`formatAppMessagesToGeminiHistory`):**
    *   **Behavior:** Converts the application's internal `Message[]` array (which stores rich message objects) into the `Content[]` array format suitable for the Gemini API's chat history. This includes mapping sender roles and packaging multimodal content.
    *   **Intent:** To accurately translate the application's view of the conversation into a format the Gemini model can understand, thereby maintaining conversational context when initializing or re-initializing a chat session.

6.  **Robust Error Communication:**
    *   **Behavior:** Identifies common API errors (e.g., invalid API key, model not found, payload too large) and translates them into user-understandable messages. It distinguishes between errors that are likely fatal to the session (e.g., bad API key) and those that might be transient.
    *   **System Impact:** This allows the application to provide targeted feedback to the user, guiding them on how to resolve issues or understand limitations. For instance, an "API_KEY_INVALID" error reported by this service should lead to a clear error message in the UI.

## Design Intent for Structure (Prose Code)

*   **Encapsulation of API Interaction:** The service is designed to be the sole point of contact with the `@google/genai` SDK. This isolates API-specific logic, making the rest ofthe application independent of direct SDK details.
*   **Stateful Service for Chat Context:** Maintains internal state for the API key, current model, system instructions, and the active `Chat` instance. This statefulness is essential for managing ongoing conversational context with the Gemini API.
*   **Callback-Based Streaming Interface:** The `sendMessageStreamToAI` function uses a callback pattern (`onChunk`, `onError`, `onComplete`) to handle asynchronous streaming data. This design allows the calling module (`App.tsx`) to react to stream events appropriately for UI updates.
*   **Prioritization of API Key Handling:** API key validation is a primary concern, checked at module load and before critical operations, reflecting its foundational importance for service functionality.
*   **Multimodal Data Transformation:** Includes logic to convert application-level representations of images/audio (e.g., base64 data URLs) into the `Part` structures required by the Gemini API, abstracting this transformation from the rest of the application.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification describes the service's role as an API gateway and session manager in natural language, focusing on its behavioral contract with the rest of the application and its interactions with the external Gemini API.
*   **Intent-Based Expression:** The service exposes functions like `sendMessageStreamToAI` or `setCurrentChatModel`, which clearly state their *intent*, abstracting the underlying SDK calls and state management complexities.
*   **Iterative Refinement:** The evolution from a (likely) non-streaming approach to a streaming-first model for message handling demonstrates adaptation to improve user experience, a core SpecLang tenet.
*   **Bi-Directional Ideation (Interface with API):** The service not only sends requests to the Gemini API but also interprets its responses (including errors and streamed data), allowing the application to react dynamically. This forms a crucial communication loop.

This revised specification for `GeminiService.ts` emphasizes its behavioral contract, its role in managing AI interactions, and the intent behind its structural design choices, providing a clear guide for understanding its critical functions within the application.

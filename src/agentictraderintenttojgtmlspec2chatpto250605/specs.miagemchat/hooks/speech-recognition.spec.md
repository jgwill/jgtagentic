
# useSpeechRecognition.ts - Hook Specification (SpecLang Aligned) - Revised

## Overall Goal/Intent

The `useSpeechRecognition` custom React hook is designed to **simplify the integration of browser-based speech-to-text functionality** into React components. It aims to abstract the complexities of the Web Speech API's `SpeechRecognition` interface, providing a clean, stateful, and reusable hook that manages the speech recognition lifecycle, transcript updates, and error reporting. The primary goal is to offer developers an easy-to-use contract for enabling voice input.

## Key Behaviors & Responsibilities (The Hook's Contract)

1.  **Browser Feature Detection:**
    *   **Behavior:** The hook ascertains if the user's browser possesses the necessary `SpeechRecognition` capabilities.
    *   **Output:** Exposes this status through the `browserSupportsSpeechRecognition: boolean` property. If not supported, an informative message is available via the `error` state.
    *   **Intent:** To allow consuming components to gracefully degrade or inform the user if voice input is unavailable.

2.  **Speech Recognition Lifecycle Management:**
    *   **Behavior (`startListening()`):** When called, the hook initiates a speech recognition session. Any existing transcript from a previous session (within the same hook instance) is cleared, and any prior error state is reset. The `isListening` state becomes `true`.
    *   **Behavior (`stopListening()`):** When called, the hook explicitly terminates the current speech recognition session. The `isListening` state becomes `false`.
    *   **Intent:** To provide clear and explicit controls for starting and stopping voice input, giving the consuming component full command over the recognition window.

3.  **Real-time Transcription Output:**
    *   **Behavior:** As the user speaks and the browser processes the audio, the hook continuously updates its `transcript: string` state with the recognized text. This includes interim (non-final) results for a more responsive feel.
    *   **Intent:** To provide immediate textual feedback of the user's speech, allowing them to see the transcription as it forms.

4.  **Listening State Indication:**
    *   **Behavior:** The `isListening: boolean` state accurately reflects whether the hook is actively attempting to capture and recognize speech. It transitions to `true` when `startListening` is successful and back to `false` when recognition ends (either via `stopListening`, naturally, or due to an error).
    *   **Intent:** To enable consuming components to provide visual feedback to the user about the voice input status (e.g., changing a microphone icon's appearance).

5.  **Error Reporting:**
    *   **Behavior:** If any issues arise during initialization (e.g., browser incompatibility) or during a recognition session (e.g., microphone permission denied, no audible speech, network issues), the hook captures these and exposes a user-friendly message via the `error: string | null` state. When an error occurs, `isListening` typically becomes `false`.
    *   **Intent:** To ensure that problems with the speech recognition process are communicated clearly, enabling the consuming component to inform the user or take appropriate action.

6.  **Transcript Manipulation:**
    *   **Behavior (`resetTranscript()`):** Allows the consuming component to programmatically clear the current `transcript` state without stopping an active listening session.
    *   **Intent:** To provide flexibility for UIs where the transcript might need to be cleared independently of the listening state (e.g., after a message is constructed from a partial transcript and sent).

7.  **Resource Management (Internal):**
    *   **Behavior (Internal):** The hook internally manages the `SpeechRecognition` object instance and ensures that its event listeners are properly attached and detached during the hook's lifecycle (mount/unmount of the consuming component).
    *   **Intent:** To prevent memory leaks and ensure stable operation by correctly handling the resources of the underlying browser API.

## Design Intent for Structure (Prose Code)

*   **Encapsulation of Browser API:** The hook is designed to completely encapsulate the direct use of the `window.SpeechRecognition` or `window.webkitSpeechRecognition` APIs. This abstraction shields consuming components from browser-specific prefixes and the event-driven nature of the native API.
*   **Stateful Logic:** The hook's primary design is to be a stateful piece of logic (managing `isListening`, `transcript`, `error`). This allows React components to reactively re-render based on changes in the speech recognition process.
*   **Memoized Control Functions:** The `startListening`, `stopListening`, and `resetTranscript` functions are designed to be stable references (achieved via `useCallback`). This is important for performance if they are used as dependencies in `useEffect` hooks or passed to memoized child components.
*   **Clear Interface:** The object returned by the hook (`{ isListening, transcript, ... }`) is its public API or contract. This interface is intentionally kept minimal and focused on the needs of a component implementing voice input.
*   **Internal Instance Management:** The use of `useRef` to hold the `SpeechRecognition` instance is a deliberate structural choice to manage a mutable, non-rendering object across the hook's lifecycle.

*Self-Correction Note on Internal Implementation Details:* Previous versions of this spec might have mentioned internal details like the explicit TypeScript interfaces defined within the hook's code. While important for the hook's own robustness, the *specification of the hook's behavior for a consumer* primarily concerns its exposed properties and methods, assuming internal correctness.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification describes the hook's purpose and its behavioral contract in natural language, emphasizing what it enables for a consuming component.
*   **Intent-Based Expression:** The hook offers a high-level, intent-driven API (e.g., `startListening` to achieve voice input) rather than exposing the raw event handlers and properties of the Web Speech API.
*   **Modularity and Reusability:** As a custom hook, it packages speech recognition logic into a reusable module, promoting DRY (Don't Repeat Yourself) principles in components that require this feature.
*   **State Encapsulation & Clear Contract:** The hook manages its internal complexity and state, exposing a clear and predictable set of outputs (`isListening`, `transcript`, `error`) and controls (`startListening`, `stopListening`, `resetTranscript`).

This revised specification for `useSpeechRecognition` focuses on its external contract and intended behavior, providing a clear guide for its usage and understanding its role in simplifying voice input integration.

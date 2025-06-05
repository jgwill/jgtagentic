
# useSpeechSynthesis.ts - Hook Specification (SpecLang Aligned) - Revised

## Overall Goal/Intent

The `useSpeechSynthesis` custom React hook is designed to **simplify the integration of browser-based text-to-speech (TTS) functionality** into React components. It aims to abstract the complexities of the Web Speech API's `SpeechSynthesis` and `SpeechSynthesisUtterance` interfaces. The hook provides a clean, stateful, and reusable solution for managing speech playback, utterance configuration, and status reporting, primarily enabling components to easily voice textual content.

## Key Behaviors & Responsibilities (The Hook's Contract)

1.  **Browser Feature Detection:**
    *   **Behavior:** The hook verifies if the user's browser supports the `speechSynthesis` feature of the Web Speech API.
    *   **Output:** This status is exposed through the `browserSupportsSpeechSynthesis: boolean` property. If TTS is not supported, an informative message is available via the `error` state.
    *   **Intent:** To allow consuming components to conditionally offer TTS functionality or inform the user if it's unavailable.

2.  **Speech Playback Control:**
    *   **Behavior (`speak(text: string)`):** When invoked with a string of text, the hook initiates speech synthesis for that text. If speech is already in progress from a previous call to `speak` within the same hook instance, the ongoing speech is first cancelled. The `isSpeaking` state is set to `true` immediately to reflect the intent to speak, before the actual browser API call to `synth.speak()` is made.
    *   **Intent:** To provide a straightforward method for components to request audio playback of textual content. The cancellation of prior speech ensures that user actions result in the most recent request being prioritized. Setting `isSpeaking` immediately aims to make the UI more responsive to the playback state.
    *   **Behavior (`cancel()`):** When called, the hook immediately stops any ongoing speech synthesis. The `isSpeaking` state becomes `false`.
    *   **Intent:** To offer an explicit way for components or users to halt audio playback.

3.  **Speaking Status Indication:**
    *   **Behavior:** The `isSpeaking: boolean` state accurately reflects whether the speech synthesis engine is intended to be or is currently producing audio output. It becomes `true` immediately when `speak()` is called. The browser's `SpeechSynthesisUtterance` events (`onstart`, `onend`, `onerror`) further refine this state, confirming actual start or setting it to `false` on completion or error.
    *   **Intent:** To enable consuming components to provide visual feedback to the user about the TTS status (e.g., changing a speaker icon's appearance, disabling a "speak" button while active), with the UI reflecting the intent to speak more rapidly.

4.  **Error Reporting:**
    *   **Behavior:** If issues arise, such as browser incompatibility or errors during the speech synthesis process itself (caught by `utterance.onerror`), the hook captures these and makes a user-friendly message available via the `error: string | null` state. When an error occurs, `isSpeaking` becomes `false`.
    *   **Intent:** To ensure that problems with TTS are clearly communicated, allowing the consuming component to inform the user.

5.  **Utterance Configuration (Internal Default):**
    *   **Behavior (Internal):** The hook internally creates and configures a `SpeechSynthesisUtterance` object with default settings (e.g., language 'en-US', standard pitch, rate, and volume).
    *   **Intent:** To provide a ready-to-use TTS capability with sensible defaults without requiring the consuming component to manage utterance properties unless future enhancements allow customization.

6.  **Resource Management (Internal):**
    *   **Behavior (Internal):** The hook manages the lifecycle of the `SpeechSynthesisUtterance` instance and ensures that any active speech is cancelled if the consuming component unmounts.
    *   **Intent:** To prevent audio from continuing to play after the associated UI element is no longer visible and to ensure clean resource handling.

## Design Intent for Structure (Prose Code)

*   **Encapsulation of Browser API:** The hook is designed to fully abstract the direct usage of `window.speechSynthesis` and `SpeechSynthesisUtterance`. This simplifies TTS integration for consuming components.
*   **Stateful Logic for Playback Status:** The core design involves managing state (`isSpeaking`, `error`) that reflects the current status of the TTS operation. The `isSpeaking` state is now set proactively upon the `speak` call to enhance UI responsiveness, while still being managed by browser events for actual playback lifecycle.
*   **Reusable Utterance Instance:** The hook maintains and reuses a single `SpeechSynthesisUtterance` object internally.
*   **Memoized Control Functions:** The `speak` and `cancel` functions are designed to be stable references (using `useCallback`).
*   **Clear and Focused Interface:** The object returned by the hook (`{ speak, cancel, isSpeaking, ... }`) defines its public API, exposing essential controls and status information.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification articulates the hook's primary purpose and its behavioral contract using natural language.
*   **Intent-Based Expression:** The hook provides a high-level, intent-driven API. The change to set `isSpeaking` immediately reflects an intent to make the UI state more closely match the user's action.
*   **Modularity and Reusability:** As a custom React hook, it encapsulates TTS logic for easy reuse.
*   **State Encapsulation:** The hook manages its internal state, exposing a clear interface. The timing of `isSpeaking` updates is refined for better perceived responsiveness.

This revised specification for `useSpeechSynthesis` highlights the change in how the `isSpeaking` state is managed to improve UI feedback timing, aiming for a more robust and intuitive user experience with TTS controls.

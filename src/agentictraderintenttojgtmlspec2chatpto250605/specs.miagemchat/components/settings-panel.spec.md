# SettingsPanel.tsx - Specification (SpecLang Aligned)

## Overall Goal/Intent

The `SettingsPanel.tsx` component is designed to provide a **centralized, modal interface for users to access and manage global application settings and actions**. It aims to offer a clear, organized, and user-friendly way to customize their chat experience, manage session persistence, and control core application behaviors (including audio preferences) without navigating away from their current primary view (Chat, Docs, or Dashboard). The panel should be easily accessible and dismissible.

## Key Behaviors & Responsibilities

1.  **Visibility Control & Modal Presentation:**
    *   **Behavior:** The panel's visibility is controlled by an `isOpen` prop. When `isOpen` is true, it renders as an overlay (modal dialog) on the right side of the screen, partially obscuring the background content to draw focus.
    *   **UX Intent:** To provide a non-disruptive way to access settings. The modal nature ensures users can focus on configurations and easily return to their previous context. Clicking outside the panel or a dedicated "Close" button dismisses it.

2.  **Local Session Management Interface:**
    *   **Behavior:** Presents distinct buttons for "Save Locally" and "Load Locally." These buttons trigger corresponding callback functions (`onSaveLocalSession`, `onLoadLocalSession`) passed from `App.tsx`.
    *   **UX Intent:** To allow users to easily persist their current chat session in their browser's local storage and to retrieve a previously saved session, with clear actions for each.

3.  **Simulated Cloud Session Management Interface:**
    *   **Behavior:**
        *   Provides an input field for users to enter or select a "Cloud Session ID."
        *   Offers "Save to Cloud" and "Load from Cloud" buttons, which become active when a Session ID is present. These trigger `onSaveToCloud` and `onLoadFromCloud` callbacks.
        *   Displays a list of `availableCloudSessions`. Clicking a session ID from this list populates the input field.
        *   Allows deletion of a cloud session (via `onDeleteFromCloud`), typically requiring user confirmation before proceeding.
    *   **UX Intent:** To offer a more robust (though simulated) session management experience, allowing users to work with named sessions. The UI aims to make these operations intuitive.

4.  **AI Model Configuration Interface:**
    *   **Behavior:**
        *   Displays the currently `selectedModel`.
        *   Provides a text input field (`modelInput`) allowing users to enter a custom Gemini model ID.
        *   A "Set Model" button triggers the `onModelChange` callback with the new model ID.
        *   Suggests available/known model IDs for user guidance.
    *   **UX Intent:** To empower users to switch between different Gemini models, including fine-tuned ones, with clear feedback on the current selection and easy input for changes.

5.  **Audio Preferences Configuration:**
    *   **Behavior:**
        *   Presents a dedicated "Audio Preferences" section.
        *   Within this section, a toggle switch labeled "Auto-play AI responses" is displayed.
        *   The state of this toggle (checked/unchecked) is directly controlled by the `autoPlayTTS` boolean prop received from `App.tsx`. **This `autoPlayTTS` value in `App.tsx` reflects the persisted user preference, loaded at application startup.**
        *   When the user interacts with the toggle, the `onToggleAutoPlayTTS` callback is invoked with the new boolean value. This signals `App.tsx` to update its state and **subsequently persist this change using `LocalStorageService`.**
        *   An informative subtext explains that enabling this feature will cause AI messages to be read aloud automatically.
    *   **UX Intent:** To provide users with explicit, persistent control over whether AI messages are automatically spoken. The toggle offers a standard, easily understandable UI for this boolean setting. The panel itself displays the current state and facilitates changes, while the actual persistence logic is managed by the parent `App.tsx` component.

6.  **Chat Clearing Action:**
    *   **Behavior:** A "Clear Current Chat" button, when clicked, triggers the `onClearChat` callback. This action is typically placed in a "Danger Zone" section to indicate its potentially irreversible nature.
    *   **UX Intent:** To provide a straightforward way for users to reset their current conversation and start fresh.

7.  **Feedback During Operations:**
    *   **Behavior:** Buttons for actions that involve processing (e.g., cloud operations, model changes) display a `LoadingSpinner` and are disabled when the `isLoading` prop is true.
    *   **UX Intent:** To provide clear visual feedback that an operation is in progress and to prevent concurrent conflicting actions.

8.  **Error and Success Communication (Delegated):**
    *   **Behavior:** While the panel initiates actions, the communication of success or failure (e.g., "Session saved," "Invalid model ID") is primarily handled by the parent component (`App.tsx`) through toast notifications, triggered via the `addToast` prop. The panel itself may perform basic input validation (e.g., non-empty session ID) and use `addToast` for immediate UI feedback if necessary.
    *   **UX Intent:** To provide consistent feedback to the user for various operations via a centralized notification system.

9.  **Layout and Styling:**
    *   **Behavior:** The panel is styled consistently with the application's dark theme. It uses clear headings to organize settings into logical sections (including the new "Audio Preferences"). It is scrollable to accommodate all settings on smaller screens.
    *   **UX Intent:** To ensure a visually cohesive, accessible, and easy-to-navigate settings interface.

## Design Intent for Structure (Prose Code)

*   **Modular Sections:** The settings are organized into distinct sections (Local Session, Cloud Storage, AI Model, Audio Preferences, Danger Zone). This structural choice enhances readability and makes it easier for users to find specific settings.
*   **State-Driven UI:** The panel's content and button states (e.g., disabled status, input values, toggle checked status for `autoPlayTTS`) are primarily driven by props passed from `App.tsx`. Local state (`cloudSessionIdInput`, `modelInput`) is used for managing input field values before they are committed.
*   **Callback-Based Actions:** All primary actions (saving, loading, clearing, toggling settings like `autoPlayTTS`) are communicated to the parent component via callback props. This decouples the `SettingsPanel` from the direct implementation of these actions and their persistence, making it a more reusable presentational component for settings.
*   **Controlled Inputs:** Input fields for Session ID and Model ID, and the toggle for `autoPlayTTS`, are controlled components, reflecting their values from props and updating parent state via callbacks.
*   **Accessibility Considerations:** The modal nature, clear labeling (`aria-label`), and interactive elements are designed with accessibility in mind, though a full audit would be separate.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification outlines the intended functionality and user experience of the settings panel in clear, natural language.
*   **Intent-Based Expression:** Focuses on *what the user can configure* (e.g., "manage session persistence," "control core application behaviors like auto-play TTS, where the preference is remembered") rather than specific HTML structures or CSS class names.
*   **Modularity:** The panel itself is a module, and it's internally structured into logical sub-sections for different categories of settings, including the audio preferences. It relies on its parent (`App.tsx`) for state management and persistence logic.
*   **User Control & Feedback:** A core design intent is to give users control over various application aspects and to provide feedback (directly via disabled states/spinners, or indirectly via toast notifications triggered by its actions) about the system's response to their configurations.

This specification details the `SettingsPanel`'s role as a comprehensive interface for user-driven application customization and management, emphasizing its interaction with `App.tsx` for managing the persisted state of settings like "Auto-play AI responses."
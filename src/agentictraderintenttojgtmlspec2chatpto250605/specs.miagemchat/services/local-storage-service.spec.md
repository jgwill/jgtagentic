# LocalStorageService.ts - Specification (SpecLang Aligned) - Revised

## Overall Goal/Intent

The `LocalStorageService.ts` module serves as a **dedicated interface for all interactions with the browser's `localStorage` API**. Its primary goal is to provide a robust and abstracted set of functions for persistently storing and retrieving user-specific application data, such as chat conversation history and global application settings (including audio preferences like `autoPlayTTS`). This service aims to ensure data persistence across browser sessions, handle data serialization/deserialization transparently, and manage potential errors gracefully to enhance application resilience.

## Key Behaviors & Responsibilities

1.  **Chat Session Persistence & Retrieval:**
    *   **`saveChatSession(messages: Message[]): void`:**
        *   **Goal:** To reliably save the current state of the user's chat conversation to their browser's local storage.
        *   **Behavior:**
            *   Accepts an array of `Message` objects.
            *   Serializes the `Message` array into a JSON string, ensuring that `Date` objects (like `timestamp`) are converted to a string format (ISO string) suitable for JSON.
            *   Stores the serialized data under a predefined key (`LOCAL_STORAGE_SESSION_KEY`).
            *   **Resilience:** If errors occur during serialization or storage (e.g., `localStorage` is full or disabled), the error is logged to the console, but the application is allowed to continue functioning without interruption from this specific operation.
    *   **`loadChatSession(): Message[] | null`:**
        *   **Goal:** To retrieve a previously saved chat conversation from local storage, reconstructing it into a usable format for the application.
        *   **Behavior:**
            *   Attempts to fetch and parse the JSON string stored under `LOCAL_STORAGE_SESSION_KEY`.
            *   If no data is found, it returns `null`, indicating no prior session was saved.
            *   If data is found, it reconstructs the array of `Message` objects, critically converting timestamp strings back into JavaScript `Date` objects.
            *   **Data Integrity & Resilience:** If the stored data is corrupted or parsing fails, the error is logged, the problematic item is removed from `localStorage` (to prevent repeated failures), and `null` is returned. This ensures the application can start fresh if saved session data is unusable.
    *   **`clearChatSessionFromStorage(): void`:**
        *   **Goal:** To remove any persisted chat session data from local storage.
        *   **Behavior:** Deletes the item associated with `LOCAL_STORAGE_SESSION_KEY`. Errors during removal are logged.

2.  **Application Settings Persistence & Retrieval:**
    *   **`saveAppSettings(settings: AppSettings): void`:**
        *   **Goal:** To save the application's global configuration settings (like active persona, selected model, and the `autoPlayTTS` preference) to local storage.
        *   **Behavior:**
            *   Accepts an `AppSettings` object. The caller (`App.tsx`) is responsible for ensuring this object includes the current `autoPlayTTS` boolean flag (and other settings).
            *   Serializes this entire `AppSettings` object into a JSON string.
            *   Stores it under a predefined key (`LOCAL_STORAGE_SETTINGS_KEY`).
            *   **Resilience:** Logs any storage or serialization errors to the console.
    *   **`loadAppSettings(): AppSettings`:**
        *   **Goal:** To retrieve saved application settings, ensuring that the application always starts with a valid and complete set of settings, including the `autoPlayTTS` preference. If settings were not previously saved or if saved data is partially invalid, appropriate defaults are provided.
        *   **Behavior:**
            *   Attempts to fetch and parse settings from `LOCAL_STORAGE_SETTINGS_KEY`.
            *   **Default Provisioning:** If no settings are found, or if parsing fails, it returns a predefined default `AppSettings` object. This default explicitly includes `autoPlayTTS: false` (or the defined default). This guarantees the application always has a valid configuration for `autoPlayTTS` and other settings.
            *   **Data Validation & Merging:** If settings are successfully loaded from storage:
                *   The `selectedModel` is validated.
                *   The `autoPlayTTS` preference is specifically handled: if a boolean value for `autoPlayTTS` exists in the stored data, that value is used. Otherwise, the default value (`false`) is applied.
                *   Other missing optional properties in the loaded settings are supplemented with values from the default settings object.
            *   This process ensures that the returned `AppSettings` object is always complete and contains a valid boolean value for `autoPlayTTS`, contributing to application stability.
            *   **Resilience:** Errors during loading or parsing result in the provision of default settings, preventing application startup failures due to corrupted stored preferences.

3.  **Reliable Use of Constants:**
    *   **Behavior:** Consistently uses predefined constants (from `constants.ts` and `personas.ts`) for `localStorage` keys (e.g., `LOCAL_STORAGE_SETTINGS_KEY`) and default values (e.g., `GEMINI_TEXT_MODEL`, `DEFAULT_PERSONA_ID`).
    *   **Intent:** To prevent errors due to typos in keys and to centralize the management of these critical values, enhancing maintainability and consistency.

## Design Intent for Structure (Prose Code)

*   **Encapsulation of Storage Mechanism:** The service is designed to be the sole module directly interacting with `localStorage`. This encapsulates the specifics of web storage, allowing other parts of the application to request data persistence without needing to know the underlying storage API details.
*   **Data Transformation Abstraction:** The necessary serialization (object to JSON string, `Date` to ISO string) and deserialization (JSON string to object, ISO string to `Date`) are handled internally. This provides a clean interface to callers, who can work with rich JavaScript objects directly.
*   **Error Handling for Resilience:** The error handling strategy (logging errors and returning `null` or default values) is a deliberate design choice to prevent `localStorage` issues (e.g., full storage, disabled API, corrupted data) from crashing the application. The aim is for the application to degrade gracefully or start with a clean slate if persistence fails.
*   **Configuration Integrity through Defaults and Validation:** The `loadAppSettings` function is specifically designed not just to load data, but to ensure the integrity of the loaded application settings (including `autoPlayTTS`) by merging with defaults and performing type-checking (e.g., `typeof parsed.autoPlayTTS === 'boolean'`). This proactive approach enhances application robustness against stale or invalid stored data.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification clearly outlines the *purpose* of each function (e.g., "To reliably save the current state...") and the *intended behavior* in natural language, focusing on the service's contract with its consumers, including how `autoPlayTTS` is managed.
*   **Intent-Based Expression:** The service offers a high-level API (e.g., `saveAppSettings(settings)`) that clearly expresses the desired action, abstracting the low-level mechanics of `localStorage.setItem()` and `JSON.stringify()`.
*   **Modularity and Decoupling:** By isolating `localStorage` logic, the service allows other application modules to be independent of the specific persistence mechanism.
*   **Robustness as a Design Goal:** The emphasis on error handling, providing default values, and validating loaded data (like ensuring `autoPlayTTS` is a boolean) underscores a design intent to make the application resilient and capable of functioning reliably.

This revised specification for `LocalStorageService.ts` highlights its role in providing a dependable and abstracted mechanism for client-side data persistence, crucial for maintaining user context and preferences (including the `autoPlayTTS` setting) across sessions.
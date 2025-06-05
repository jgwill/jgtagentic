
# ChatMessage.tsx - Specification (SpecLang Aligned) - Revised

## Overall Goal/Intent
The `ChatMessage` component is designed to render a single, self-contained message within the chat conversation. It must clearly differentiate message origin (user vs. AI), present diverse content types (text, images, audio) effectively, display essential metadata, and offer relevant interactions (like text-to-speech for AI messages and copy-to-clipboard for all text messages), all while maintaining visual consistency and clarity.

## Key Behaviors & Responsibilities

1.  **Message Origin Differentiation:**
    *   **Behavior:** Visually distinguishes between messages from the `User` and the `AI` using alignment (e.g., user right, AI left) and distinct background colors for message bubbles. AI message bubbles can further adopt persona-specific colors or error-specific styling.
    *   **UX Intent:** To allow users to instantly and effortlessly identify the sender of each message, which is fundamental for following conversational flow.
2.  **Multimodal Content Display:**
    *   **Text:** Renders textual content using a `MarkdownRenderer` to support rich formatting (bold, italics, lists, code blocks). For AI error messages, a "⚠️" icon precedes the text.
        *   **UX Intent:** To present text clearly and engagingly, allowing for emphasis and structure within messages. Error icons provide immediate visual alerting.
    *   **Images (User):** Displays a thumbnail preview for images sent by the user, along with the optional file name.
        *   **UX Intent:** To provide immediate visual confirmation of image transmission and context within the chat.
    *   **Audio (User/AI):** Renders an HTML5 `<audio controls>` element for playback of recorded audio messages.
        *   **UX Intent:** To allow seamless in-chat playback of audio content without needing external players.
3.  **Metadata Presentation:**
    *   **Behavior:** Displays the sender's avatar (user SVG, AI image), sender's display name, and a formatted timestamp for each message.
    *   **UX Intent:** To provide clear attribution and temporal context for every message, enhancing the sense of a structured and traceable conversation.
4.  **Message Interactivity:**
    *   **Text-to-Speech (AI Messages):**
        *   **Behavior:** For AI messages containing text (and not being errors), a toggle button is provided.
            *   When speech is not active, the button displays a "speaker" icon. Clicking it initiates text-to-speech playback of the message content.
            *   When speech is active, the button displays a "stop" (square) icon. Clicking it cancels the ongoing playback.
            *   This functionality relies on browser support for `SpeechSynthesis`. The button's ARIA label dynamically updates to reflect the current action (play or stop).
        *   **UX Intent:** To offer an accessible alternative for consuming AI responses and cater to user preference for auditory information, with clear visual cues for the TTS state and control.
    *   **Copy to Clipboard (All Messages with Text):**
        *   **Behavior:** For any message containing text, a "Copy" icon button is provided. Clicking this button copies the message's raw text content (preserving Markdown if present) to the user's clipboard using `navigator.clipboard.writeText()`. Brief visual feedback (e.g., the icon changing to a "check" mark for a short period) confirms the successful copy action. Errors during copying are logged, and a basic alert is shown as a fallback.
        *   **UX Intent:** To allow users to easily extract and reuse message content from the conversation for other purposes. The feedback mechanism ensures the user is aware of the action's outcome.
5.  **Visual Design and Layout:**
    *   **Behavior:** Each message is encapsulated in a "bubble" with rounded corners, appropriate padding, and shadows. Avatars are positioned adjacent to their bubbles. Metadata is typically placed above the main content. Action buttons (TTS, Copy) are positioned subtly near the message bubble, often appearing at the bottom-right.
    *   **UX Intent:** To present messages in a visually appealing, organized, and easily digestible format, common to modern chat applications, with quick access to relevant actions.

## Design Intent for Structure (Prose Code)

*   **Self-Contained Unit:** Designed as a highly reusable component, responsible for all aspects of rendering a single message. This modularity simplifies the `ChatWindow`'s logic.
*   **Conditional Logic for Content & Actions:** The structure incorporates conditional rendering based on `message.sender`, `message.isError`, the presence of various content types (`imagePreviewUrl`, `audioDataUrl`, `text`), and browser capabilities (for TTS). This is to flexibly accommodate the diverse nature of messages and available interactions.
*   **Delegation for Rich Text:** Utilizes the `MarkdownRenderer` sub-component to handle the complexities of Markdown parsing and rendering, adhering to the principle of single responsibility.
*   **Hook Integration for TTS:** Leverages the `useSpeechSynthesis` hook to encapsulate text-to-speech logic, keeping the `ChatMessage` component focused on presentation.
*   **Local State for Interaction Feedback:** Uses local component state (e.g., for `copied` status) to manage immediate visual feedback for actions like copy-to-clipboard, keeping the feedback mechanism self-contained and responsive.
*   **Dynamic Styling:** The component's structure supports dynamic application of CSS classes (e.g., for `bubbleBgClass`) to reflect message origin, persona, or error status, a key design choice for clear visual communication.

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification describes the functional goals and intended user experiences of the chat area components in natural language, emphasizing clarity and user-centric design.
*   **Intent-Based Expression:** The components are described in terms of *what the user can achieve* (e.g., "play back AI messages," "copy text easily") and *how the interface should respond* (e.g., "icon changes to a stop (square) icon," "visual feedback confirms copy"), rather than focusing on specific low-level DOM manipulations or exact CSS rules.
*   **Iterative Refinement:** The rich feature set of `ChatMessage` (TTS with improved icons and control, Copy) suggests an iterative development process, where functionalities were added and refined over time to enhance user capabilities.
*   **Bi-Directional Ideation & Feedback:** The `ChatMessage` component provides rich feedback (visual styling, icons changing state like the speaker/stop icons for TTS) in response to user interactions (like clicking the TTS button), creating a clear interactive loop.

This revised specification for `ChatMessage.tsx` details its role in rendering individual messages with enhanced interactivity and clear visual cues for features like text-to-speech.

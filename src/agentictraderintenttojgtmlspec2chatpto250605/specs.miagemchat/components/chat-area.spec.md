
# Chat Area Components - Specification (SpecLang Aligned) - Revised

This document specifies the behavior and intent of the core components that constitute the chat interaction area: `ChatWindow.tsx`, `ChatMessage.tsx`, and `ChatInput.tsx`. Together, they aim to deliver a fluid, intuitive, and feature-rich conversational experience.

## Overall Goal/Intent

To provide a seamless, intuitive, and feature-rich interface for users to send and receive messages, including text, images, and audio, while interacting with an AI persona. The chat area should be responsive, visually clear, and support dynamic updates like streaming AI responses and loading indicators, ensuring the user feels engaged and informed throughout their conversation.

---

## 1. `ChatWindow.tsx`

### Overall Goal/Intent
The `ChatWindow` component is responsible for displaying the chronological list of chat messages, providing a scrollable and continuously updated view of the conversation history. It also clearly indicates when the AI is processing a response, ensuring the user is aware of ongoing activity.

### Key Behaviors & Responsibilities

1.  **Message History Display:**
    *   **Behavior:** Renders a list of `Message` objects provided via its `messages` prop.
    *   **UX Intent:** To present the conversation in a familiar, easy-to-follow chronological sequence. Each message is individually rendered by the `ChatMessage` component, ensuring consistent styling and functionality per message.
2.  **Automatic Scrolling & View Management:**
    *   **Behavior:** Automatically scrolls to the most recent message or loading indicator.
    *   **UX Intent:** To ensure the user always sees the latest part of the conversation or system activity without manual scrolling, providing a smooth and natural flow as the dialogue progresses. This is achieved by scrolling to a `messagesEndRef` when new messages are added or loading status changes.
3.  **AI Loading Indication:**
    *   **Behavior:** Displays a visual loading indicator (e.g., animated dots) when the `isLoading` prop is `true`. This indicator is styled to resemble an incoming AI message, including a relevant AI avatar.
    *   **UX Intent:** To clearly inform the user that the AI is processing their request and a response is forthcoming, managing expectations and reducing perceived wait times. The avatar used for loading aims to be contextually consistent with the active AI persona.
4.  **Layout and Visual Design:**
    *   **Behavior:** Establishes a dedicated, scrollable area with appropriate padding and background consistent with the application's dark theme.
    *   **UX Intent:** To provide a clean, uncluttered, and visually comfortable space for the conversation, ensuring readability and focus. Top padding is specifically managed to prevent overlap with sticky header elements, maintaining UI integrity.

### Design Intent for Structure (Prose Code)

*   **Composition:** Designed as a container component that iterates over message data and delegates the rendering of individual messages to the `ChatMessage` child component. This promotes separation of concerns and reusability of the message rendering logic.
*   **Scroll Management:** The use of a `ref` (`messagesEndRef`) and an effect (`useEffect`) to trigger scrolling is a structural choice to implement the desired automatic scrolling behavior, ensuring a fluid user experience.
*   **Conditional Rendering for Loading State:** The structure includes logic to conditionally display a loading animation. This is designed to provide explicit feedback to the user, reinforcing the system's responsiveness.
*   **Styling Integration:** Styling (via Tailwind CSS and inline styles for animations) is integral to its design, aiming to achieve the dark theme consistency and clear visual cues (like the flashing dots for loading).

---

## 2. `ChatMessage.tsx`

### Overall Goal/Intent
The `ChatMessage` component is designed to render a single, self-contained message within the chat conversation. It must clearly differentiate message origin (user vs. AI), present diverse content types (text, images, audio) effectively, display essential metadata, and offer relevant interactions (like text-to-speech for AI messages and copy-to-clipboard for all text messages), all while maintaining visual consistency and clarity.

### Key Behaviors & Responsibilities

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
        *   **Behavior:** For AI messages containing text (and not being errors), a toggle button is provided to initiate or cancel text-to-speech playback of the message content, if the browser supports this feature. The button's icon and ARIA label dynamically update based on playback state.
        *   **UX Intent:** To offer an accessible alternative for consuming AI responses and cater to user preference for auditory information.
    *   **Copy to Clipboard (All Messages with Text):**
        *   **Behavior:** For any message containing text, a "Copy" icon button is provided. Clicking this button copies the message's raw text content (preserving Markdown if present) to the user's clipboard using `navigator.clipboard.writeText()`. Brief visual feedback (e.g., the icon changing to a "check" mark for a short period) confirms the successful copy action. Errors during copying are logged, and a basic alert is shown as a fallback.
        *   **UX Intent:** To allow users to easily extract and reuse message content from the conversation for other purposes. The feedback mechanism ensures the user is aware of the action's outcome.
5.  **Visual Design and Layout:**
    *   **Behavior:** Each message is encapsulated in a "bubble" with rounded corners, appropriate padding, and shadows. Avatars are positioned adjacent to their bubbles. Metadata is typically placed above the main content. Action buttons (TTS, Copy) are positioned subtly near the message bubble, often appearing at the bottom-right.
    *   **UX Intent:** To present messages in a visually appealing, organized, and easily digestible format, common to modern chat applications, with quick access to relevant actions.

### Design Intent for Structure (Prose Code)

*   **Self-Contained Unit:** Designed as a highly reusable component, responsible for all aspects of rendering a single message. This modularity simplifies the `ChatWindow`'s logic.
*   **Conditional Logic for Content & Actions:** The structure incorporates conditional rendering based on `message.sender`, `message.isError`, the presence of various content types (`imagePreviewUrl`, `audioDataUrl`, `text`), and browser capabilities (for TTS). This is to flexibly accommodate the diverse nature of messages and available interactions.
*   **Delegation for Rich Text:** Utilizes the `MarkdownRenderer` sub-component to handle the complexities of Markdown parsing and rendering, adhering to the principle of single responsibility.
*   **Hook Integration for TTS:** Leverages the `useSpeechSynthesis` hook to encapsulate text-to-speech logic, keeping the `ChatMessage` component focused on presentation.
*   **Local State for Interaction Feedback:** Uses local component state (e.g., for `copied` status) to manage immediate visual feedback for actions like copy-to-clipboard, keeping the feedback mechanism self-contained and responsive.
*   **Dynamic Styling:** The component's structure supports dynamic application of CSS classes (e.g., for `bubbleBgClass`) to reflect message origin, persona, or error status, a key design choice for clear visual communication.

---

## 3. `ChatInput.tsx`

### Overall Goal/Intent
The `ChatInput` component is the primary interface for user message composition and submission. It aims to provide a versatile and intuitive experience, supporting multiple input modalities (typed text, speech-to-text, audio recording, camera capture, file upload) while giving clear feedback about the current input state and system readiness.

### Key Behaviors & Responsibilities

1.  **Text Input & Submission:**
    *   **Behavior:** Offers a dynamically resizing multi-line `textarea` for text input. Message submission occurs via an "Enter" key press (without Shift) or a dedicated "Send" button.
    *   **UX Intent:** To provide a familiar and flexible text entry experience. The "Send" button is disabled when no content is available or when the system is busy, preventing empty/accidental submissions and managing user expectations.
2.  **Speech-to-Text Integration:**
    *   **Behavior:** A microphone icon button toggles browser-based speech recognition. Transcribed text appears in the `textarea`.
    *   **UX Intent:** To offer a hands-free input alternative. Visual feedback (button state, placeholder text changes) clearly indicates listening status and any errors, ensuring the user understands the system's state. Disabled during other modal inputs (audio recording) to prevent conflicting microphone use.
3.  **Audio Message Recording & Preview:**
    *   **Behavior:** A dedicated button initiates audio recording using `MediaRecorder`. A timer shows duration. Post-recording, an audio player allows preview before sending or discarding.
    *   **UX Intent:** To allow users to easily record and review voice snippets. Clear visual cues (button state, timer, player preview) guide the user through the recording process. Disabled during speech-to-text or when the system is busy.
4.  **Camera Image Capture & Integration:**
    *   **Behavior:** A camera icon button launches a `CameraModal` for image capture. Captured images are then combined with any text for submission.
    *   **UX Intent:** To provide a seamless in-app way to capture and send visual information. Button disabled during other modal inputs or when busy.
5.  **Image File Upload & Preview:**
    *   **Behavior:** A paperclip icon button allows selection of local image files. A thumbnail and file name preview are shown before sending.
    *   **UX Intent:** To enable easy sharing of existing images. Previews and clear options manage the selection process. Button disabled during other modal inputs.
6.  **Input Modality State Management & Feedback:**
    *   **Behavior:** Manages internal states for `inputValue`, `selectedFile`, `recordedAudio`, and speech recognition activity. Provides visual feedback (previews, placeholder text changes, button states) corresponding to the active input mode or selection.
    *   **UX Intent:** To keep the user clearly informed about what type of content is currently being composed or attached, and what actions are available, reducing confusion and improving control.
7.  **System Loading State Awareness:**
    *   **Behavior:** Input-initiating buttons and the "Send" button are disabled when the parent application signals it's busy (`isLoading` prop).
    *   **UX Intent:** To prevent users from initiating new actions while a previous one is still processing, ensuring orderly interaction and clear system status communication.

### Design Intent for Structure (Prose Code)

*   **Multi-Modal Input Hub:** Architected as a central point for various input types. Its internal state management (`useState`, `useRef`) is designed to handle the complexities of switching between and managing these different modalities (text, speech, file, camera, audio recording).
*   **Abstraction of Complex APIs:** Leverages custom hooks (`useSpeechRecognition`) and dedicated components (`CameraModal`) to encapsulate the direct interactions with complex browser APIs (`SpeechRecognition`, `getUserMedia`, `MediaRecorder`, `FileReader`). This keeps `ChatInput` focused on orchestrating these inputs and presenting their UI.
*   **Clear Feedback Mechanisms:** The structure includes elements specifically for user feedback (e.g., the area for file/audio previews, dynamic placeholder text in the `textarea`). This is a deliberate design choice to enhance usability.
*   **Progressive Disclosure/Enablement:** Buttons for different input modalities are enabled/disabled based on the current application state (e.g., `isLoading`, `isAudioRecording`, `isListening`). This design guides the user by only presenting valid actions.
*   **Consolidated Submission Logic:** The `handleSubmit` function is designed to gather data from all active input modalities (text, selected file, recorded audio) before calling the `onSendMessage` prop, providing a unified submission pathway.

---

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification describes the functional goals and intended user experiences of the chat area components in natural language, emphasizing clarity and user-centric design.
*   **Iterative Refinement:** The rich feature set of `ChatInput` (multiple input modes, previews) and `ChatMessage` (TTS, Copy) suggests an iterative development process, where functionalities were added and refined over time to enhance user capabilities.
*   **Intent-Based Expression:** The components are described in terms of *what the user can achieve* and *how the interface should respond*, rather than focusing on specific low-level DOM manipulations or exact CSS rules (though structural approaches are noted in design intent).
*   **Bi-Directional Ideation & Feedback:** The chat area is inherently interactive. `ChatInput` allows users to express intent in various ways, and `ChatWindow` / `ChatMessage` provide rich feedback from the AI and the system, creating a dynamic conversational loop. The design of previews and state indicators in `ChatInput`, and action buttons in `ChatMessage`, are forms of bi-directional ideation with the user during message composition and review.

This revised specification for the chat area components aims to clearly articulate their integrated design, user experience goals, and behavioral intent, facilitating comprehension and potential re-implementation.

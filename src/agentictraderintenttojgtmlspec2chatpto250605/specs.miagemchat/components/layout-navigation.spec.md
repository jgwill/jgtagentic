
# Layout & Navigation Components - Specification (SpecLang Aligned) - Revised

This document specifies the behavior and intent of the core components responsible for application layout and primary user navigation: `Header.tsx` and `PersonaSelectorBar.tsx`. These components are designed to provide a consistent, intuitive, and accessible structure for users to interact with the application's main sections and features.

## Overall Goal/Intent

To establish a clear and persistent navigational framework that allows users to easily understand their current location within the application, switch between main views (Chat, Docs, Dashboard), access global settings, and (within the chat context) conveniently select different AI personas. The layout components are intended to be responsive, visually cohesive with the application's dark theme, and always readily accessible.

---

## 1. `Header.tsx`

### Overall Goal/Intent
The `Header` component functions as the application's main masthead, consistently displaying branding, primary navigation pathways, and access to global settings. Its design prioritizes immediate recognition of the application and effortless movement between its core functional areas, remaining persistently visible at the top of the screen.

### Key Behaviors & Responsibilities

1.  **Application Branding & Identity:**
    *   **Behavior:** Prominently displays the application logo and the title "Mia's Gem Chat Studio".
    *   **UX Intent:** To provide immediate brand recognition and a constant visual anchor for the user, reinforcing the application's identity. These elements are typically placed on the left for standard readability.

2.  **Primary View Navigation:**
    *   **Behavior:** Renders clear, clickable navigation buttons for each main application view ("Chat", "Docs", "Dashboard"). The button corresponding to the `currentView` is visually differentiated to clearly indicate the user's active location.
    *   **UX Intent:** To offer unambiguous and direct pathways to all major sections of the application. The active state highlighting provides crucial navigational feedback, reducing user disorientation. Clicking a button results in an immediate transition to the selected view, managed via the `onSetView` callback. ARIA attributes enhance accessibility for users relying on assistive technologies.

3.  **Access to Global Settings:**
    *   **Behavior:** Features a distinct settings icon button (e.g., a gear) that, when clicked, triggers the `onToggleSettings` callback to show or hide the `SettingsPanel`.
    *   **UX Intent:** To provide a consistent and easily discoverable entry point for application-wide configurations and actions, without cluttering the primary navigation. An `aria-label` ensures the button's purpose is clear to assistive technologies.

4.  **Persistent and Consistent Layout:**
    *   **Behavior:** Maintains a fixed position at the top of the viewport (`sticky top-0`) with a designated `z-index` ensuring it remains visible above scrolling content. It adheres to the application's dark theme with consistent background color and typography.
    *   **UX Intent:** To guarantee that primary navigation and settings access are always available to the user, regardless of their scroll position within a view. This predictability enhances usability and user control.

### Design Intent for Structure (Prose Code)

*   **Modular Navigation Elements:** The use of an internal `NavButton` sub-component is a design choice to encapsulate the logic and styling for individual navigation links. This promotes reusability and ensures consistent behavior (e.g., active state highlighting) across all navigation items.
*   **Clear Visual Hierarchy:** The layout (typically achieved with flexbox) is designed to logically group branding elements, navigation links, and the settings action, providing a scannable and organized header structure.
*   **Sticky Positioning for Accessibility:** The `sticky` positioning is a deliberate structural choice to fulfill the UX goal of persistent navigation access, a common and effective pattern in web applications.
*   **Callback-Driven Interaction:** The header's interactive elements (navigation buttons, settings toggle) are designed to communicate user intent to the parent (`App.tsx`) via callback props (`onSetView`, `onToggleSettings`). This decouples the header from direct state manipulation, making it a more reusable presentation component.

---

## 2. `PersonaSelectorBar.tsx`

### Overall Goal/Intent
The `PersonaSelectorBar` component is designed to offer users a highly visible and immediate way to switch the active AI persona while in the Chat view. It aims to make persona selection a quick, intuitive action, enhancing the user's ability to tailor their conversational experience dynamically. It remains persistently visible below the main `Header`.

### Key Behaviors & Responsibilities

1.  **Dynamic Persona Selection Display:**
    *   **Behavior:** Renders a distinct button for each available AI `Persona`. Each button prominently displays the persona's `glyph` (icon/emoji) and, on sufficient screen space, its descriptive name.
    *   **UX Intent:** To allow users to quickly scan and identify available AI personalities. The visual glyphs provide immediate recognition, while names offer clarity.

2.  **Clear Indication of Active Persona:**
    *   **Behavior:** The button representing the currently `activePersonaId` is visually emphasized, typically using the persona's unique theme `color` for its border and background, and may include other visual cues like highlighting or shadows. Inactive persona buttons are more subdued.
    *   **UX Intent:** To provide unambiguous, at-a-glance feedback about which AI persona is currently engaged in the conversation, preventing user confusion.

3.  **Responsive Interaction for Persona Switching:**
    *   **Behavior:** Clicking a persona button immediately invokes the `onSelectPersona` callback, signaling `App.tsx` to change the active AI. Buttons are disabled if the application is in a loading state (`isLoading` is true).
    *   **UX Intent:** To make persona switching feel instantaneous and responsive. Disabling buttons during loading states prevents conflicts and provides clear feedback about system readiness. ARIA attributes (`role="radio"`, `aria-checked`) improve accessibility by conveying the selection group semantics.

4.  **Persistent and Contextual Layout:**
    *   **Behavior:** The bar maintains a `sticky` position directly below the main `Header` within the Chat view, ensuring it's always accessible when relevant. Its styling aligns with the application's dark theme.
    *   **UX Intent:** To provide a dedicated and consistently available space for persona selection without interfering with the main chat flow. Its placement ensures it's a secondary navigation element, pertinent only to the chat context.

### Design Intent for Structure (Prose Code)

*   **Iterative Rendering of Persona Options:** The component is designed to map over the `personas` array to dynamically generate a button for each. This structure allows the list of personas to be easily updated or expanded by changing the source data without altering the component's core logic.
*   **Conditional Styling for State Indication:** The styling logic is intentionally designed to be conditional, changing a button's appearance based on whether its persona is active and whether the application is in a loading state. This direct visual mapping of state to appearance is key to its usability.
*   **Callback for Decoupled Action:** The use of the `onSelectPersona` callback allows the bar to signal selection intent without being responsible for the actual state change logic, which resides in `App.tsx`. This promotes good separation of concerns.
*   **Sticky Positioning for Contextual Access:** The `sticky` positioning is a structural choice to meet the UX requirement of having persona selection readily available specifically when the user is interacting with the chat.
*   **Responsive Design Elements:** The design considers how persona information (glyph vs. full name) is displayed based on screen size, aiming for optimal information density and usability across devices.

---

## Relation to SpecLang Principles

*   **Prose Code Intent:** This specification uses natural language to clearly articulate the functional goals, intended user interactions, and visual design objectives for the `Header` and `PersonaSelectorBar`.
*   **Intent-Based Expression:** The descriptions prioritize *why* these components exist (e.g., "effortless movement between core functional areas," "immediate way to switch personas") and the *experience* they aim to provide (e.g., "unambiguous navigational feedback," "at-a-glance feedback about active persona").
*   **Iterative Refinement (Implied):** The specific layout decisions, such as sticky positioning values and responsive display of persona names, likely result from iterative adjustments to optimize usability and visual harmony.
*   **Accessibility as Intent:** The explicit mention of ARIA attributes reflects an intent to create navigable and understandable interfaces for all users.

This revised specification aims to provide a clear understanding of the design rationale and intended user experience for the primary layout and navigation components of Mia's Gem Chat Studio.

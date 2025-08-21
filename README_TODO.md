
## Synapse-OD: Development TODO List

This document outlines the development status of the "Synapse-OD" application's components, categorized into:
1.  **Final / Production-Grade (Frontend UI/UX & Core Logic):** Components with well-developed UI/UX, primarily awaiting real data and backend integration.
2.  **Incomplete / Needs Change (Upon Full Backend Integration):** Components with a frontend implementation that will require significant changes or data-binding once a live backend is integrated.
3.  **Build from Scratch (Primarily Backend & Some Frontend Placeholders):** Features that are conceptual, simulated, or have minimal placeholder UI, requiring significant backend and some frontend development.
4.  **Template Bot Personas:** Comprehensive bot personas to be created for the template bots in the template_bot_project directory.

---

### ✅ **Part 1: Final / Production-Grade (Frontend UI/UX & Core Logic)**

*These components have a well-developed UI/UX, and their core frontend logic is sound. They primarily await real data and backend integration to become fully operational. Their visual design and client-side interactions are largely complete.*

1.  **Visual Theme & Core Layout:**
    *   **Status:** **FINAL.** The "Glossy Obsidian" cyberpunk theme (colors, fonts, glows, spacing) is consistently applied.
    *   **Notes:** Core `index.css` is robust. `AppLogo` component is complete. Overall responsive shell is in place.
2.  **Main Navigation System:**
    *   **Status:** **FINAL.** Header (with logo, TTS toggle, user menu placeholder), bottom tabs, and back button functionality are implemented and styled.
    *   **Notes:** Dynamic tab visibility based on admin role is working.
3.  **Authentication UI:**
    *   **Status:** **FINAL.** Login and Registration forms (`AuthContainer`) are fully styled and have client-side validation placeholders. Social login buttons are themed.
    *   **Notes:** The UI flow between login/register is complete.
4.  **Nexus Core Persona Selector:**
    *   **Status:** **FINAL.** The overlay, persona card grid, selection animation, and interaction logic are complete and visually polished.
5.  **Chat Interface (Core UI):**
    *   **Status:** **FINAL.** Message display (user/AI distinction), message bubble styling, input area (text field, send button, mic button), and loading/streaming indicators (`cyber-pulse-loader`, `streaming-indicator`) are visually and structurally complete.
    *   **Notes:** Scrolling to the bottom of messages is handled.
6.  **Speech-to-Text (STT) & Text-to-Speech (TTS):**
    *   **Status:** **FINAL.** Integration with browser `SpeechRecognition` and `SpeechSynthesis` APIs is functional. UI elements (mic button, TTS toggle) reflect state correctly. Basic error handling for STT is present.
7.  **Upload Tab UI (`upload-content-view`):**
    *   **Status:** **FINAL.** UI for file selection and YouTube URL input is styled and functional from a client-side perspective.
8.  **Child Bot Creator UI (`ChildBotCreatorView`):**
    *   **Status:** **FINAL.** Forms for template-based and custom bot creation, input fields, persona template selector grid, and system instruction preview area are all well-styled and interactive. Local JSON download works.
9.  **Admin Control Panel (Static UI Structure):**
    *   **Status:** **FINAL.** The overall structure with sub-tabs (Dashboard, API Monitor, Model LMS, Query QC) is in place. The static layout and styling of cards, tables (structure), and placeholder elements within each sub-view are complete and themed.
    *   **Notes:** This refers to the visual shell. Data population and actions are in other sections.
10. **Basic Animation Framework & Responsiveness:**
    *   **Status:** **FINAL.** Keyframe animations for view transitions, card appearances, and the "circuit flow" effect are implemented. The application has a good responsive baseline for mobile and desktop.

---

### ⚠️ **Part 2: Incomplete / Needs Change (Upon Full Backend Integration)**

*These components have a frontend implementation but will require significant changes, data-binding, or refinements once a live backend is integrated. Their current logic often relies on mock data or simulated API calls.*

1.  **Authentication Logic (`AuthContainer`, `handleAuthSuccess`, `handleLogout`):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:**
        *   Replace simulated login/registration with actual API calls to backend auth endpoints.
        *   Handle real authentication tokens/sessions (e.g., JWTs) and store them securely (e.g., HttpOnly cookies managed by backend, or secure frontend storage if appropriate for the auth model).
        *   Implement actual OAuth 2.0 flows for social login buttons, redirecting to providers and handling callbacks.
        *   Update `currentUser` state based on real user data from the backend.
        *   Refine error handling to display specific messages from the backend (e.g., "User already exists," "Incorrect password").
2.  **Chat Message Sending & Receiving (`handleSendMessage`, `streamAIResponseFromBackend`):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:**
        *   `streamAIResponseFromBackend` function must correctly call the live backend chat endpoint.
        *   Properly handle actual streaming data from the backend (if using SSE or WebSockets) and update the UI incrementally. The current text decoder and update logic is a good base.
        *   Parse and render any special formatting if the backend sends markdown or structured content (e.g., source URLs for grounding).
        *   Robust error handling for API failures, network issues, and Gemini API errors relayed by the backend.
3.  **Upload Tab Functionality (`handleProcessFile`, `handleProcessUrl`):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:**
        *   Implement actual API calls to backend endpoints for file and URL submission.
        *   Display real processing status and error messages from the backend.
        *   For large files/long processes, consider implementing polling or WebSocket listeners for status updates instead of just a single response.
4.  **Child Bot Creator - Backend Saving (`handleGenerateAndSave`):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:**
        *   The `fetch` call to `/api/saveChildBot` needs to interact with a real backend endpoint.
        *   Handle success/error responses from the backend regarding the save operation.
        *   The `childBotId` generated on the frontend should ideally be confirmed or potentially overridden by the backend if it has its own ID generation strategy.
5.  **Admin Control Panel - Data Population & Actions (All Sub-views):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs (General for all admin views):**
        *   Remove all hardcoded/simulated data.
        *   Implement `useEffect` hooks to fetch data from corresponding backend APIs when components mount or filters change.
        *   Populate UI elements (tables, charts, progress bars, metrics) with live data.
        *   Implement robust loading states (e.g., skeletons, spinners) while data is being fetched.
        *   Display user-friendly error messages if API calls fail.
    *   **Needs (Specific to `AdminAnalyticsDashboardView`):**
        *   Integrate a charting library (e.g., Chart.js, Recharts) to replace CSS chart placeholders with dynamic, interactive charts based on fetched data.
    *   **Needs (Specific to `ApiMonitorView`):**
        *   Fetch real API usage counts and limits.
    *   **Needs (Specific to `ModelLmsView`):**
        *   Fetch real child bot list and their performance metrics.
        *   "Training Recommendations" should ideally be more dynamic or linked to backend logic if it exists.
    *   **Needs (Specific to `QueryQcView`):**
        *   Fetch real query logs with pagination and filtering capabilities from the backend.
        *   "Actions" (Flag, Mark Useful, Mark for Deletion) must trigger API calls to update log statuses on the backend.
        *   "Simulate Weekly Data Cleanup" button must trigger a real backend cleanup process API.
6.  **Global Error Display (`error` state in `ChatApp`):**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:** While a basic error display exists, it might need to be more sophisticated to handle various types of errors (network, API-specific, validation) from different parts of the application and potentially offer more contextual information or actions.
7.  **State Management for Fetched Data:**
    *   **Status:** **INCOMPLETE.**
    *   **Needs:** For complex data in the admin panel or potentially chat history, consider if the current component-level state is sufficient or if a more robust state management solution (like Context API used more extensively, Zustand, or Redux Toolkit if complexity grows significantly) is needed for caching, sharing, and updating data fetched from the backend.

---

### 🏗️ **Part 3: Build from Scratch (Primarily Backend & Some Frontend Placeholders)**

*These features are currently conceptual, simulated, or have minimal placeholder UI. They require significant backend development and, in some cases, new frontend components or logic.*

1.  **Backend - ALL API Endpoints & Logic:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   **Authentication Service:** User database, password hashing, session/JWT management, OAuth 2.0 integration for Google/Microsoft/Facebook.
        *   **Chat Service:** Securely call Gemini API using `process.env.API_KEY` (stored *only* on backend), manage system instructions, handle streaming responses.
        *   **Upload Service:** File storage (e.g., S3, GCS), URL content fetching/scraping, asynchronous processing queues (e.g., RabbitMQ, Redis) for large uploads/YouTube processing, logic to update knowledge bases or prep data for fine-tuning.
        *   **Child Bot Configuration Service:** CRUD operations for child bot configs, database storage.
        *   **Admin Data Service:**
            *   Logging mechanism for user actions, API calls, bot interactions.
            *   Aggregation logic for analytics dashboard metrics.
            *   Database for storing and querying these logs and metrics.
            *   API endpoints to serve all data required by the Admin Control Panel views.
        *   **Automated Query Log Cleanup Service:** A scheduled job (e.g., cron) to perform the weekly data cleanup in the query log database based on statuses.
2.  **Frontend - Chat History Tab & Functionality:**
    *   **Status:** **TO BE BUILT.** (Currently disabled tab).
    *   **Needs:**
        *   UI for displaying lists of past conversations.
        *   Logic to fetch chat history from a backend API (with pagination).
        *   Ability to select and view/resume a past conversation.
        *   (Optional) Search functionality within chat history.
3.  **Frontend - Advanced Admin Dashboard Visualizations:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** While the structure is there, replacing CSS chart placeholders with a real charting library and configuring it to display dynamic data from the backend is a specific development task.
4.  **Frontend & Backend - Real User Rights Management (Beyond Role Display):**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** The current "Admin" tab placeholder mentions this. A full implementation would require:
        *   Backend: Granular permission system, API endpoints to manage user roles and permissions.
        *   Frontend: UI in the admin panel to list users, change roles, and assign specific permissions (this UI itself needs to be designed and built).
5.  **Frontend & Backend - Model Training/Fine-Tuning Interface (Conceptual in Model LMS):**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** If the "Training Recommendations" in Model LMS are to become actionable:
        *   Backend: Systems for managing datasets, initiating fine-tuning jobs (e.g., with Vertex AI or other MLOps platforms), tracking job status.
        *   Frontend: UI to select bots, link uploaded data, trigger training jobs, and monitor progress. This is a major new feature set.
6.  **Database(s):**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** Design and implementation of databases for users, child bot configurations, chat logs, analytics data, uploaded content metadata, etc.
7.  **PWA - Service Worker & Offline Capabilities:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** If full PWA offline capabilities are desired:
        *   Implement a service worker for caching application shell, static assets, and potentially user data/chat history for offline access.
        *   Define caching strategies (cache-first, network-first, stale-while-revalidate).
        *   Handle UI for offline status.
8.  **PWA - Push Notifications:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Frontend: Logic to request permission and subscribe to push notifications.
        *   Backend: Service to send push notifications (e.g., for new AI messages or important alerts).
9.  **Deployment Infrastructure & CI/CD:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:** Pipelines for building and deploying the frontend and backend, hosting solutions, database provisioning.
10. **Comprehensive Security Hardening (Backend Focus):**
    *   **Status:** **TO BE BUILT/INTEGRATED.**
    *   **Needs:** Thorough input validation on all backend endpoints, rate limiting, CSRF protection (if using sessions), secure API key management, proper error handling to avoid information leakage, security headers (CSP, HSTS), regular dependency audits.

---

### 🤖 **Part 4: Template Bot Personas**

*These are comprehensive bot personas that need to be created for the template bots in the template_bot_project directory, based on the existing bot role templates.*

1.  **Content Creator Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for generating various content types (blog posts, social media, email newsletters, product descriptions, stories).
        *   Include appropriate disclaimers about content ownership and usage.
        *   Integrate with the existing content-creator.html template.

2.  **Cook Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for recipe generation, cooking tips, ingredient substitutions.
        *   Include appropriate disclaimers about dietary advice.
        *   Integrate with the existing cook.html template.

3.  **Financial Consultant Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for financial information, budgeting, investment concepts.
        *   Include strong disclaimers about not providing financial advice.
        *   Integrate with the existing financial-consultant.html template.

4.  **Legal Consultant Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for general legal information and document understanding.
        *   Include strong disclaimers about not providing legal advice.
        *   Integrate with the existing legal-consultant.html template.

5.  **Media Creator Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for media content creation, visual descriptions, and creative direction.
        *   Include appropriate disclaimers about content ownership and usage.
        *   Integrate with the existing media-creator.html template.

6.  **Medical Consultant Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for general health information and medical concepts.
        *   Include strong disclaimers about not providing medical advice.
        *   Integrate with the existing medical-consultant.html template.

7.  **Personal Assistant Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for scheduling, reminders, task management, and organization.
        *   Include appropriate disclaimers about data privacy.
        *   Integrate with the existing personal-assistant.html template.

8.  **Personal Secretary Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for email management, calendar organization, and professional communication.
        *   Include appropriate disclaimers about data privacy.
        *   Integrate with the existing personal-secretary.html template.

9.  **Prompt Creator Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for crafting effective prompts for various AI models.
        *   Include appropriate disclaimers about prompt effectiveness.
        *   Integrate with the existing prompt-creator.html template.

10. **SEO Writer Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for SEO content creation, keyword optimization, and meta descriptions.
        *   Include appropriate disclaimers about search engine ranking guarantees.
        *   Integrate with the existing seo-writer.html template.

11. **Tutor Bot:**
    *   **Status:** **TO BE BUILT.**
    *   **Needs:**
        *   Create a comprehensive persona with detailed system instructions.
        *   Define attitude, nature, and communication style.
        *   Specify capabilities for educational content, explanations, and learning assistance.
        *   Include appropriate disclaimers about educational advice.
        *   Integrate with the existing tutor.html template.

---

This list should provide a clear roadmap for bringing Synapse-OD to a fully functional, production-ready state. The frontend is well-poised for backend integration.

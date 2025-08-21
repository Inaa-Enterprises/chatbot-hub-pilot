# Backend Enhancement Plan (Data Collection Focus)

## Phase 1: Basic Chat Logging (Step 001)
- [x] Create `backend_enhancement_todo.md`.
- [x] Define logging format (e.g., JSONL to `/home/ubuntu/synapse_backend/chat_log.jsonl`).- [x] Configure Python logging in `app/main.py` to write structured logs to the file.
- [x] Modify `app/main.py`\'s `/api/chat` endpoint to log incoming request details (timestamp, personaId, user message length/hash).
- [x] Modify `app/main.py`\'s streaming response generator to log successful stream completion or errors.- [x] Test logging setup by running the server.

## Phase 2: Authentication (Step 002)
- [x] Choose authentication method (e.g., Firebase Auth as per roadmap).
- [x] Implement user registration/login endpoints.
- [x] Secure relevant endpoints (e.g., chat logging associated with user).

## Phase 3: Upload Endpoints (Step 003)
- [x] Implement basic `/api/upload/file` endpoint.
- [x] Implement basic `/api/upload/url` endpoint.
- [x] (Optional) Add basic logging for uploads.

## Phase 4: Vicuna Placeholder (Step 004)
- [x] Modify `AIService` or add a new service for model switching.
- [x] Add configuration to select between Gemini and Vicuna (placeholder).
- [x] Update chat endpoint to use the selected model service.

## Phase 5: Validation (Step 005)
- [ ] Test logging functionality.
- [ ] Test authentication flow.
- [ ] Test upload endpoints.
- [ ] Test model switching (placeholder).

## Phase 6: Delivery (Step 006)
- [ ] Package updated backend code.
- [ ] Provide updated instructions.
- [ ] Send files to user.

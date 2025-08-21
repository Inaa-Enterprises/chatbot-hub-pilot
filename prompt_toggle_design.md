# Prompt Toggle and Questionnaire Flow Design

## Overview

This document outlines the design for integrating a prompt enhancement feature into the chatbot backend. This feature will allow users to toggle between normal conversation mode and a structured prompt-based approach where the bot asks clarifying questions before providing more precise answers.

## Core Components

### 1. Toggle Mechanism

**API Endpoint Enhancement:**
- Add a `promptMode` boolean parameter to the existing `/api/chat` endpoint
- When `promptMode` is true, the backend will initiate the questionnaire flow
- When `promptMode` is false (default), the backend will process the message normally

**Request Format:**
```json
{
  "personaId": "string",
  "message": "string",
  "promptMode": boolean,
  "conversationId": "string" (optional)
}
```

### 2. Conversation State Management

**Conversation State Object:**
```typescript
interface ConversationState {
  id: string;
  userId: string;
  messages: Message[];
  promptMode: boolean;
  questionnaire?: {
    templateId: string;
    currentQuestionIndex: number;
    answers: Record<string, any>;
    complete: boolean;
  };
}
```

**State Transitions:**
1. Normal → Prompt Mode: When user toggles promptMode to true
2. Question Flow: Backend asks questions sequentially based on selected template
3. Prompt Generation: After all questions are answered, generate enhanced prompt
4. Response Generation: Use enhanced prompt to generate a more precise response
5. Return to Normal: After response is delivered, return to normal conversation mode

### 3. Template Selection Logic

**Template Selection Process:**
1. Analyze initial user message to determine the most appropriate template
2. Use keyword matching and intent classification to select from available templates
3. If no clear template match, use a generic questionnaire template
4. Allow explicit template selection via API parameter (optional)

**Template Matching Example:**
- Message contains "code", "function", "bug" → Code Generation template
- Message contains "article", "blog", "write" → Content Creation template
- Message contains "image", "picture", "draw" → Image Generation template

### 4. Dynamic Questionnaire Flow

**Question Presentation:**
1. Present one question at a time to the user
2. Store user's answer and move to the next question
3. Allow skipping optional questions
4. Support different question types (text, select, checkbox)

**Flow Control:**
- Track current question index in the conversation state
- Support going back to previous questions
- Allow early termination of questionnaire if enough information is gathered

### 5. Prompt Assembly

**Prompt Generation Logic:**
1. Collect all answers from the questionnaire
2. Apply template-specific formatting to structure the information
3. Combine with the original user intent
4. Generate a comprehensive, well-structured prompt

**Example Prompt Template (Code Generation):**
```
I need help with {programming-language} code using {framework}.

Task: {task-description}

Requirements:
{requirements}

Expected Input/Output:
{input-output}

Code Style Preferences:
{code-style}

{include-tests ? "Please include unit tests." : ""}
{include-examples ? "Please include usage examples." : ""}

Additional Context:
{additional-context}
```

## Backend Implementation

### 1. New Modules

**PromptManager:**
- Handles template selection and prompt generation
- Manages the questionnaire flow
- Formats the final enhanced prompt

**ConversationManager:**
- Tracks conversation state including questionnaire progress
- Manages transitions between normal and prompt modes
- Persists conversation history

### 2. API Endpoint Updates

**Enhanced Chat Endpoint:**
```python
@app.post("/api/chat")
async def handle_chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    # Extract parameters
    message = request.message
    persona_id = request.personaId
    prompt_mode = request.promptMode or False
    conversation_id = request.conversationId
    
    # Get or create conversation
    conversation = conversation_manager.get_or_create_conversation(
        user_id=user_id,
        conversation_id=conversation_id
    )
    
    # Handle prompt mode
    if prompt_mode and not conversation.questionnaire:
        # Initialize questionnaire if not already in progress
        template_id = prompt_manager.select_template(message)
        conversation.start_questionnaire(template_id)
        
        # Return first question
        return {
            "message": prompt_manager.get_current_question(conversation),
            "conversationId": conversation.id,
            "promptMode": True,
            "isQuestion": True
        }
    
    # Handle questionnaire in progress
    if conversation.questionnaire and not conversation.questionnaire.complete:
        # Store answer to current question
        prompt_manager.store_answer(conversation, message)
        
        # Check if more questions
        if prompt_manager.has_next_question(conversation):
            # Return next question
            return {
                "message": prompt_manager.get_next_question(conversation),
                "conversationId": conversation.id,
                "promptMode": True,
                "isQuestion": True
            }
        else:
            # Generate enhanced prompt
            enhanced_prompt = prompt_manager.generate_prompt(conversation)
            
            # Generate response using enhanced prompt
            response = await ai_service.generate_response(
                system_instruction=get_system_instruction(persona_id),
                message=enhanced_prompt
            )
            
            # Mark questionnaire as complete
            conversation.complete_questionnaire()
            
            return {
                "message": response,
                "conversationId": conversation.id,
                "promptMode": False,
                "isQuestion": False,
                "enhancedPrompt": enhanced_prompt  # Optional, for transparency
            }
    
    # Normal chat flow
    response = await ai_service.generate_response(
        system_instruction=get_system_instruction(persona_id),
        message=message
    )
    
    return {
        "message": response,
        "conversationId": conversation.id,
        "promptMode": False,
        "isQuestion": False
    }
```

## Frontend Considerations

While this design focuses on backend implementation, the frontend should:

1. Provide a toggle button for users to enable/disable prompt mode
2. Display questions clearly and distinguish them from normal responses
3. Show progress through the questionnaire (e.g., "Question 3 of 8")
4. Optionally display the enhanced prompt before the final response
5. Allow canceling the questionnaire flow at any point

## Extension Points

The design allows for future extensions:

1. **Custom Templates**: Allow users to create and save their own questionnaire templates
2. **Template Refinement**: Improve template selection based on user feedback
3. **Multi-modal Input**: Support image uploads as part of the questionnaire
4. **Adaptive Questions**: Dynamically adjust questions based on previous answers
5. **Prompt History**: Save and reuse successful prompts

## Implementation Phases

1. **Phase 1**: Basic toggle and questionnaire flow with fixed templates
2. **Phase 2**: Improved template selection and prompt generation
3. **Phase 3**: User feedback and template refinement
4. **Phase 4**: Custom templates and advanced features

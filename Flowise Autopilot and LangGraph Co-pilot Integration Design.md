# Flowise Autopilot and LangGraph Co-pilot Integration Design

## Overview

This document outlines the design for integrating Flowise autopilot and LangGraph co-pilot logic into the existing chatbot backend. These advanced features will enhance the backend's capabilities by providing:

1. **Flowise Autopilot**: Automated workflow orchestration with visual flow-based programming
2. **LangGraph Co-pilot**: Dynamic, multi-agent reasoning with state management for complex tasks

Both integrations will build upon the existing prompt enhancement and conversation management features, providing a seamless experience for users while significantly expanding the chatbot's capabilities.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       Chatbot Backend                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │  API Endpoints  │◄───┤ Core Services   │◄───┤ Data Models  │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│          │                      │                     ▲         │
│          ▼                      ▼                     │         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Existing Components                       ││
│  │                                                             ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  ││
│  │  │ Prompt      │  │ Conversation│  │ LLM Service         │  ││
│  │  │ Manager     │  │ Manager     │  │                     │  ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  ││
│  │         │                │                    │              ││
│  └─────────┼────────────────┼────────────────────┼──────────────┘│
│            │                │                    │               │
│  ┌─────────▼────────────────▼────────────────────▼──────────────┐│
│  │                    New Components                             ││
│  │                                                              ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   ││
│  │  │ Flowise     │  │ LangGraph   │  │ Agent Orchestrator  │   ││
│  │  │ Controller  │  │ Controller  │  │                     │   ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   ││
│  │         │                │                    │               ││
│  └─────────┼────────────────┼────────────────────┼───────────────┘│
│            │                │                    │                │
│  ┌─────────▼────────────────▼────────────────────▼───────────────┐│
│  │                  External Integrations                         ││
│  │                                                               ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    ││
│  │  │ Flowise     │  │ LangGraph   │  │ Tool Connectors     │    ││
│  │  │ Engine      │  │ Engine      │  │                     │    ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘    ││
│  │                                                               ││
│  └───────────────────────────────────────────────────────────────┘│
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## 1. Flowise Autopilot Integration

### Core Components

#### 1.1 Flowise Controller

The `FlowiseController` will be the main interface between the chatbot backend and the Flowise engine:

```python
class FlowiseController:
    """
    Controller for Flowise integration, managing workflow execution and state.
    """
    
    def __init__(self, api_url: str = None, api_key: str = None):
        """
        Initialize the Flowise controller.
        
        Args:
            api_url: URL of the Flowise API server
            api_key: API key for authentication
        """
        self.api_url = api_url or os.environ.get("FLOWISE_API_URL", "http://localhost:3000/api")
        self.api_key = api_key or os.environ.get("FLOWISE_API_KEY", "")
        self.flows = {}  # Cache of loaded flows
        
    def load_flow(self, flow_id: str) -> Dict[str, Any]:
        """Load a flow definition from Flowise"""
        
    def execute_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a flow with the given inputs"""
        
    def get_available_flows(self) -> List[Dict[str, Any]]:
        """Get a list of available flows"""
        
    def create_flow(self, flow_definition: Dict[str, Any]) -> str:
        """Create a new flow in Flowise"""
        
    def update_flow(self, flow_id: str, flow_definition: Dict[str, Any]) -> bool:
        """Update an existing flow in Flowise"""
        
    def delete_flow(self, flow_id: str) -> bool:
        """Delete a flow from Flowise"""
```

#### 1.2 Flow Execution Service

The `FlowExecutionService` will handle the execution of flows and integration with the conversation system:

```python
class FlowExecutionService:
    """
    Service for executing Flowise flows and managing their state.
    """
    
    def __init__(self, flowise_controller: FlowiseController = None):
        """
        Initialize the flow execution service.
        
        Args:
            flowise_controller: Controller for Flowise integration
        """
        self.flowise_controller = flowise_controller or FlowiseController()
        self.active_executions = {}  # Track active flow executions
        
    def start_flow(self, flow_id: str, conversation_id: str, inputs: Dict[str, Any]) -> str:
        """Start a flow execution"""
        
    def continue_flow(self, execution_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Continue an active flow execution with new inputs"""
        
    def get_execution_state(self, execution_id: str) -> Dict[str, Any]:
        """Get the current state of a flow execution"""
        
    def abort_flow(self, execution_id: str) -> bool:
        """Abort an active flow execution"""
```

#### 1.3 Flow Definition Models

```python
class FlowNode:
    """Model representing a node in a Flowise flow"""
    id: str
    type: str
    data: Dict[str, Any]
    position: Dict[str, int]
    
class FlowEdge:
    """Model representing an edge in a Flowise flow"""
    id: str
    source: str
    sourceHandle: str
    target: str
    targetHandle: str
    
class FlowDefinition:
    """Model representing a complete Flowise flow definition"""
    id: str
    name: str
    description: str
    nodes: List[FlowNode]
    edges: List[FlowEdge]
```

### Integration with Existing Backend

#### 1.3.1 API Endpoint Extensions

Add new endpoints to the API for Flowise integration:

```python
@app.post("/api/flows")
async def create_flow(request: CreateFlowRequest):
    """Create a new flow"""
    
@app.get("/api/flows")
async def list_flows():
    """List available flows"""
    
@app.get("/api/flows/{flow_id}")
async def get_flow(flow_id: str):
    """Get a flow by ID"""
    
@app.put("/api/flows/{flow_id}")
async def update_flow(flow_id: str, request: UpdateFlowRequest):
    """Update a flow"""
    
@app.delete("/api/flows/{flow_id}")
async def delete_flow(flow_id: str):
    """Delete a flow"""
    
@app.post("/api/flows/{flow_id}/execute")
async def execute_flow(flow_id: str, request: ExecuteFlowRequest):
    """Execute a flow"""
```

#### 1.3.2 Chat API Enhancement

Extend the existing chat API to support Flowise integration:

```python
@app.post("/api/chat")
async def handle_chat(request: ChatRequest):
    # Extract parameters
    message = request.message
    persona_id = request.personaId
    conversation_id = request.conversationId
    prompt_mode = request.promptMode or False
    autopilot_mode = request.autopilotMode or False  # New parameter
    flow_id = request.flowId  # Optional flow ID for autopilot mode
    
    # Get or create conversation
    conversation = conversation_manager.get_or_create_conversation(
        user_id=user_id,
        conversation_id=conversation_id
    )
    
    # Handle autopilot mode
    if autopilot_mode:
        if flow_id:
            # Execute specific flow
            flow_execution = flow_execution_service.start_flow(
                flow_id=flow_id,
                conversation_id=conversation.id,
                inputs={"message": message, "persona_id": persona_id}
            )
        else:
            # Auto-select flow based on message content
            flow_id = flow_selection_service.select_flow(message)
            flow_execution = flow_execution_service.start_flow(
                flow_id=flow_id,
                conversation_id=conversation.id,
                inputs={"message": message, "persona_id": persona_id}
            )
        
        # Return initial response or next step
        return {
            "message": flow_execution.get("message", "Starting automated workflow..."),
            "conversationId": conversation.id,
            "autopilotMode": True,
            "flowId": flow_id,
            "executionId": flow_execution.get("execution_id"),
            "waitingForInput": flow_execution.get("waiting_for_input", False),
            "inputPrompt": flow_execution.get("input_prompt")
        }
    
    # Handle existing prompt mode and normal chat flow
    # (existing code)
```

## 2. LangGraph Co-pilot Integration

### Core Components

#### 2.1 LangGraph Controller

The `LangGraphController` will manage the LangGraph engine and graph execution:

```python
class LangGraphController:
    """
    Controller for LangGraph integration, managing graph execution and state.
    """
    
    def __init__(self, module_path: str = None):
        """
        Initialize the LangGraph controller.
        
        Args:
            module_path: Path to LangGraph modules
        """
        self.module_path = module_path or os.path.join(os.path.dirname(__file__), "langgraph_modules")
        self.graphs = {}  # Cache of loaded graphs
        
    def load_graph(self, graph_id: str) -> Any:
        """Load a graph definition"""
        
    def execute_graph(self, graph_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a graph with the given inputs"""
        
    def continue_graph_execution(self, execution_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Continue an active graph execution with new inputs"""
        
    def get_available_graphs(self) -> List[Dict[str, Any]]:
        """Get a list of available graphs"""
```

#### 2.2 Agent Definitions

Define the structure for agents in the LangGraph system:

```python
class Agent:
    """Base class for LangGraph agents"""
    id: str
    name: str
    description: str
    system_prompt: str
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent on the current state"""
        
class ResearchAgent(Agent):
    """Agent specialized in research tasks"""
    
class PlanningAgent(Agent):
    """Agent specialized in planning and breaking down tasks"""
    
class CodingAgent(Agent):
    """Agent specialized in writing and debugging code"""
    
class EditingAgent(Agent):
    """Agent specialized in editing and refining content"""
```

#### 2.3 Graph Execution Service

```python
class GraphExecutionService:
    """
    Service for executing LangGraph graphs and managing their state.
    """
    
    def __init__(self, langgraph_controller: LangGraphController = None):
        """
        Initialize the graph execution service.
        
        Args:
            langgraph_controller: Controller for LangGraph integration
        """
        self.langgraph_controller = langgraph_controller or LangGraphController()
        self.active_executions = {}  # Track active graph executions
        
    def start_graph(self, graph_id: str, conversation_id: str, inputs: Dict[str, Any]) -> str:
        """Start a graph execution"""
        
    def continue_graph(self, execution_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Continue an active graph execution with new inputs"""
        
    def get_execution_state(self, execution_id: str) -> Dict[str, Any]:
        """Get the current state of a graph execution"""
        
    def abort_graph(self, execution_id: str) -> bool:
        """Abort an active graph execution"""
```

### Integration with Existing Backend

#### 2.3.1 API Endpoint Extensions

Add new endpoints to the API for LangGraph integration:

```python
@app.post("/api/graphs")
async def create_graph(request: CreateGraphRequest):
    """Create a new graph"""
    
@app.get("/api/graphs")
async def list_graphs():
    """List available graphs"""
    
@app.get("/api/graphs/{graph_id}")
async def get_graph(graph_id: str):
    """Get a graph by ID"""
    
@app.post("/api/graphs/{graph_id}/execute")
async def execute_graph(graph_id: str, request: ExecuteGraphRequest):
    """Execute a graph"""
```

#### 2.3.2 Chat API Enhancement for Co-pilot Mode

Further extend the chat API to support LangGraph co-pilot mode:

```python
@app.post("/api/chat")
async def handle_chat(request: ChatRequest):
    # Extract parameters
    message = request.message
    persona_id = request.personaId
    conversation_id = request.conversationId
    prompt_mode = request.promptMode or False
    autopilot_mode = request.autopilotMode or False
    copilot_mode = request.copilotMode or False  # New parameter
    graph_id = request.graphId  # Optional graph ID for co-pilot mode
    
    # Get or create conversation
    conversation = conversation_manager.get_or_create_conversation(
        user_id=user_id,
        conversation_id=conversation_id
    )
    
    # Handle co-pilot mode
    if copilot_mode:
        if graph_id:
            # Execute specific graph
            graph_execution = graph_execution_service.start_graph(
                graph_id=graph_id,
                conversation_id=conversation.id,
                inputs={"message": message, "persona_id": persona_id}
            )
        else:
            # Auto-select graph based on message content
            graph_id = graph_selection_service.select_graph(message)
            graph_execution = graph_execution_service.start_graph(
                graph_id=graph_id,
                conversation_id=conversation.id,
                inputs={"message": message, "persona_id": persona_id}
            )
        
        # Return initial response or next step
        return {
            "message": graph_execution.get("message", "Starting co-pilot mode..."),
            "conversationId": conversation.id,
            "copilotMode": True,
            "graphId": graph_id,
            "executionId": graph_execution.get("execution_id"),
            "agentId": graph_execution.get("current_agent"),
            "waitingForInput": graph_execution.get("waiting_for_input", False),
            "inputPrompt": graph_execution.get("input_prompt"),
            "thinking": graph_execution.get("thinking", False),
            "progress": graph_execution.get("progress", 0)
        }
    
    # Handle autopilot mode
    # (code from previous section)
    
    # Handle existing prompt mode and normal chat flow
    # (existing code)
```

## 3. Agent Orchestrator

To manage both Flowise and LangGraph integrations, we'll implement an `AgentOrchestrator` service:

```python
class AgentOrchestrator:
    """
    Service for orchestrating different agent systems (Flowise and LangGraph).
    """
    
    def __init__(
        self,
        flow_execution_service: FlowExecutionService = None,
        graph_execution_service: GraphExecutionService = None
    ):
        """
        Initialize the agent orchestrator.
        
        Args:
            flow_execution_service: Service for executing Flowise flows
            graph_execution_service: Service for executing LangGraph graphs
        """
        self.flow_execution_service = flow_execution_service or FlowExecutionService()
        self.graph_execution_service = graph_execution_service or GraphExecutionService()
        self.active_sessions = {}  # Track active orchestration sessions
        
    def start_session(
        self,
        conversation_id: str,
        message: str,
        mode: str = "auto",
        flow_id: str = None,
        graph_id: str = None
    ) -> Dict[str, Any]:
        """
        Start a new orchestration session.
        
        Args:
            conversation_id: ID of the conversation
            message: User message
            mode: Orchestration mode ("auto", "flowise", "langgraph")
            flow_id: Optional specific flow ID for Flowise mode
            graph_id: Optional specific graph ID for LangGraph mode
            
        Returns:
            Session information
        """
        # Implementation
        
    def continue_session(
        self,
        session_id: str,
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Continue an active orchestration session.
        
        Args:
            session_id: ID of the session to continue
            inputs: New inputs for the session
            
        Returns:
            Updated session information
        """
        # Implementation
        
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """
        Get the current state of an orchestration session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Current session state
        """
        # Implementation
        
    def abort_session(self, session_id: str) -> bool:
        """
        Abort an active orchestration session.
        
        Args:
            session_id: ID of the session to abort
            
        Returns:
            True if the session was aborted, False otherwise
        """
        # Implementation
```

## 4. Conversation State Extensions

Extend the existing conversation state to support Flowise and LangGraph:

```python
class ConversationState:
    id: str
    userId: str
    messages: List[Message]
    promptMode: bool
    autopilotMode: bool  # New field
    copilotMode: bool  # New field
    questionnaire?: {
        templateId: string
        currentQuestionIndex: number
        answers: Record<string, any>
        complete: boolean
    }
    autopilot?: {  # New field
        flowId: string
        executionId: string
        state: any
        waitingForInput: boolean
        inputPrompt?: string
    }
    copilot?: {  # New field
        graphId: string
        executionId: string
        state: any
        currentAgent: string
        waitingForInput: boolean
        inputPrompt?: string
        thinking: boolean
        progress: number
    }
```

## 5. Default Flows and Graphs

### 5.1 Default Flowise Flows

1. **Content Creation Flow**:
   - Analyzes user request for content creation
   - Researches relevant information
   - Generates draft content
   - Refines and formats the content
   - Returns the final content to the user

2. **Research Assistant Flow**:
   - Breaks down research question
   - Searches for information from multiple sources
   - Synthesizes findings
   - Generates a comprehensive report

3. **Code Generation Flow**:
   - Analyzes coding requirements
   - Generates code structure
   - Implements code with documentation
   - Tests and debugs the code
   - Returns the final code with usage examples

### 5.2 Default LangGraph Graphs

1. **Multi-Agent Problem Solving**:
   - Planning Agent: Breaks down complex problems
   - Research Agent: Gathers relevant information
   - Analysis Agent: Processes and analyzes information
   - Solution Agent: Generates solutions
   - Review Agent: Evaluates and refines solutions

2. **Content Creation Pipeline**:
   - Research Agent: Gathers information on the topic
   - Outline Agent: Creates a structured outline
   - Writing Agent: Drafts the content
   - Editing Agent: Refines and improves the content
   - Formatting Agent: Formats the content for the target medium

## 6. Implementation Phases

### Phase 1: Foundation
1. Set up basic Flowise and LangGraph controller classes
2. Implement API endpoints for flow and graph management
3. Extend conversation state to support new modes

### Phase 2: Flowise Integration
1. Implement flow execution service
2. Create default flows
3. Integrate with chat API
4. Test with simple workflows

### Phase 3: LangGraph Integration
1. Implement graph execution service
2. Create agent definitions
3. Implement default graphs
4. Integrate with chat API
5. Test with simple agent interactions

### Phase 4: Agent Orchestrator
1. Implement the agent orchestrator service
2. Create unified API for both systems
3. Add automatic mode selection
4. Test complex scenarios with both systems

### Phase 5: Advanced Features
1. Add support for custom flows and graphs
2. Implement persistent state management
3. Add monitoring and debugging tools
4. Optimize performance and resource usage

## 7. Frontend Considerations

While this design focuses on backend implementation, the frontend should:

1. Provide toggle buttons for autopilot and co-pilot modes
2. Display agent thinking and progress indicators
3. Show which agent is currently active in co-pilot mode
4. Allow users to provide feedback and guidance to agents
5. Visualize workflow and agent interactions
6. Provide debugging and monitoring tools for developers

## 8. Extension Points

The design allows for future extensions:

1. **Custom Agents**: Allow users to create and train their own agents
2. **Tool Integration**: Add support for external tools and APIs
3. **Multi-modal Support**: Extend to handle images, audio, and video
4. **Collaborative Agents**: Enable multiple agents to work together
5. **Learning from Feedback**: Improve agent performance based on user feedback

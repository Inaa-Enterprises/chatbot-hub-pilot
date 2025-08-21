"""
Agent orchestrator for managing both Flowise and LangGraph integrations.
"""

import os
import json
import uuid
import logging
from typing import Dict, List, Any, Optional

from flow_execution_service import FlowExecutionService
from graph_execution_service import GraphExecutionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Service for orchestrating different agent systems (Flowise and LangGraph).
    """
    
    def __init__(
        self,
        flow_execution_service: FlowExecutionService = None,
        graph_execution_service: GraphExecutionService = None,
        data_dir: str = None
    ):
        """
        Initialize the agent orchestrator.
        
        Args:
            flow_execution_service: Service for executing Flowise flows
            graph_execution_service: Service for executing LangGraph graphs
            data_dir: Directory for storing orchestration data
        """
        self.flow_execution_service = flow_execution_service or FlowExecutionService()
        self.graph_execution_service = graph_execution_service or GraphExecutionService()
        self.data_dir = data_dir or os.environ.get("ORCHESTRATOR_DATA_DIR", "data/orchestrator")
        self.active_sessions = {}  # Track active orchestration sessions
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
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
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Determine mode if auto
        if mode == "auto":
            # Simple heuristic for mode selection
            # In a real implementation, this would be more sophisticated
            if "code" in message.lower() or "program" in message.lower():
                mode = "langgraph"  # Use LangGraph for coding tasks
            else:
                mode = "flowise"  # Default to Flowise for other tasks
        
        # Create session state
        session_state = {
            "id": session_id,
            "conversation_id": conversation_id,
            "mode": mode,
            "status": "active",
            "execution_id": None,
            "flow_id": flow_id,
            "graph_id": graph_id,
            "created_at": None,  # Would be set in a real implementation
            "updated_at": None   # Would be set in a real implementation
        }
        
        # Start execution based on mode
        if mode == "flowise":
            # Determine flow ID if not provided
            if not flow_id:
                # In a real implementation, this would use a more sophisticated selection algorithm
                flow_id = "content_creation"  # Default flow
            
            # Start flow execution
            result = self.flow_execution_service.start_flow(
                flow_id=flow_id,
                conversation_id=conversation_id,
                inputs={"message": message}
            )
            
            # Update session state
            session_state["flow_id"] = flow_id
            session_state["execution_id"] = result.get("execution_id")
            
            # Store session state
            self.active_sessions[session_id] = session_state
            self._save_session_state(session_id, session_state)
            
            # Prepare response
            response = {
                "session_id": session_id,
                "mode": "flowise",
                "flow_id": flow_id,
                "execution_id": result.get("execution_id"),
                "message": result.get("message", "Started Flowise workflow."),
                "waiting_for_input": result.get("waiting_for_input", False),
                "input_prompt": result.get("input_prompt")
            }
            
            # Add error information if present
            if "error" in result:
                response["error"] = result["error"]
                response["details"] = result.get("details", "")
            
            return response
        
        elif mode == "langgraph":
            # Determine graph ID if not provided
            if not graph_id:
                # In a real implementation, this would use a more sophisticated selection algorithm
                graph_id = "multi_agent_problem_solving"  # Default graph
            
            # Start graph execution
            result = self.graph_execution_service.start_graph(
                graph_id=graph_id,
                conversation_id=conversation_id,
                inputs={"message": message}
            )
            
            # Update session state
            session_state["graph_id"] = graph_id
            session_state["execution_id"] = result.get("execution_id")
            
            # Store session state
            self.active_sessions[session_id] = session_state
            self._save_session_state(session_id, session_state)
            
            # Prepare response
            response = {
                "session_id": session_id,
                "mode": "langgraph",
                "graph_id": graph_id,
                "execution_id": result.get("execution_id"),
                "message": result.get("message", "Started LangGraph execution."),
                "waiting_for_input": result.get("waiting_for_input", False),
                "input_prompt": result.get("input_prompt"),
                "current_agent": result.get("current_agent"),
                "thinking": result.get("thinking", False),
                "progress": result.get("progress", 0)
            }
            
            # Add error information if present
            if "error" in result:
                response["error"] = result["error"]
                response["details"] = result.get("details", "")
            
            return response
        
        else:
            return {
                "error": "Invalid mode",
                "details": f"Mode '{mode}' is not supported. Use 'auto', 'flowise', or 'langgraph'."
            }
    
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
        # Get session state
        session_state = self.get_session_state(session_id)
        
        if not session_state:
            return {
                "error": "Session not found",
                "details": f"No active session found with ID: {session_id}"
            }
        
        if session_state["status"] != "active":
            return {
                "error": "Session not active",
                "details": f"Session {session_id} is not active (status: {session_state['status']})"
            }
        
        # Continue execution based on mode
        mode = session_state["mode"]
        execution_id = session_state["execution_id"]
        
        if mode == "flowise":
            # Continue flow execution
            result = self.flow_execution_service.continue_flow(
                execution_id=execution_id,
                inputs=inputs
            )
            
            # Prepare response
            response = {
                "session_id": session_id,
                "mode": "flowise",
                "flow_id": session_state["flow_id"],
                "execution_id": execution_id,
                "message": result.get("message", "Continued Flowise workflow."),
                "waiting_for_input": result.get("waiting_for_input", False),
                "input_prompt": result.get("input_prompt"),
                "status": result.get("status")
            }
            
            # Add error information if present
            if "error" in result:
                response["error"] = result["error"]
                response["details"] = result.get("details", "")
            
            # Update session status if execution is complete
            if result.get("status") == "completed":
                session_state["status"] = "completed"
                self._save_session_state(session_id, session_state)
            
            return response
        
        elif mode == "langgraph":
            # Continue graph execution
            result = self.graph_execution_service.continue_graph(
                execution_id=execution_id,
                inputs=inputs
            )
            
            # Prepare response
            response = {
                "session_id": session_id,
                "mode": "langgraph",
                "graph_id": session_state["graph_id"],
                "execution_id": execution_id,
                "message": result.get("message", "Continued LangGraph execution."),
                "waiting_for_input": result.get("waiting_for_input", False),
                "input_prompt": result.get("input_prompt"),
                "current_agent": result.get("current_agent"),
                "thinking": result.get("thinking", False),
                "progress": result.get("progress", 0),
                "status": result.get("status")
            }
            
            # Add error information if present
            if "error" in result:
                response["error"] = result["error"]
                response["details"] = result.get("details", "")
            
            # Update session status if execution is complete
            if result.get("status") == "completed":
                session_state["status"] = "completed"
                self._save_session_state(session_id, session_state)
            
            return response
        
        else:
            return {
                "error": "Invalid mode",
                "details": f"Mode '{mode}' is not supported. Use 'flowise' or 'langgraph'."
            }
    
    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current state of an orchestration session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Current session state or None if not found
        """
        # Check in-memory cache first
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Try to load from disk
        file_path = os.path.join(self.data_dir, f"{session_id}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    session_state = json.load(f)
                    
                    # Add to in-memory cache if still active
                    if session_state["status"] == "active":
                        self.active_sessions[session_id] = session_state
                    
                    return session_state
            except Exception as e:
                logger.exception(f"Error loading session state: {session_id}")
                return None
        
        return None
    
    def abort_session(self, session_id: str) -> Dict[str, Any]:
        """
        Abort an active orchestration session.
        
        Args:
            session_id: ID of the session to abort
            
        Returns:
            Success status or error details
        """
        # Get session state
        session_state = self.get_session_state(session_id)
        
        if not session_state:
            return {
                "error": "Session not found",
                "details": f"No active session found with ID: {session_id}"
            }
        
        if session_state["status"] != "active":
            return {
                "success": True,
                "message": f"Session {session_id} is already {session_state['status']}"
            }
        
        # Abort execution based on mode
        mode = session_state["mode"]
        execution_id = session_state["execution_id"]
        
        if mode == "flowise":
            # Abort flow execution
            self.flow_execution_service.abort_flow(execution_id)
        
        elif mode == "langgraph":
            # Abort graph execution
            self.graph_execution_service.abort_graph(execution_id)
        
        # Update session state
        session_state["status"] = "aborted"
        
        # Store updated session state
        if session_id in self.active_sessions:
            self.active_sessions[session_id] = session_state
        
        self._save_session_state(session_id, session_state)
        
        return {
            "success": True,
            "message": f"Session {session_id} aborted successfully"
        }
    
    def _save_session_state(self, session_id: str, session_state: Dict[str, Any]) -> None:
        """
        Save session state to disk.
        
        Args:
            session_id: ID of the session
            session_state: Session state to save
        """
        try:
            file_path = os.path.join(self.data_dir, f"{session_id}.json")
            
            with open(file_path, "w") as f:
                json.dump(session_state, f, indent=2)
        except Exception as e:
            logger.exception(f"Error saving session state: {session_id}")
    
    def list_sessions(self, conversation_id: str = None, status: str = None) -> List[Dict[str, Any]]:
        """
        List orchestration sessions.
        
        Args:
            conversation_id: Optional conversation ID to filter by
            status: Optional status to filter by
            
        Returns:
            List of sessions matching the filters
        """
        sessions = []
        
        # List files in data directory
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.data_dir, filename)
                
                try:
                    with open(file_path, "r") as f:
                        session_state = json.load(f)
                        
                        # Apply filters
                        if conversation_id and session_state.get("conversation_id") != conversation_id:
                            continue
                        
                        if status and session_state.get("status") != status:
                            continue
                        
                        # Add to list
                        sessions.append({
                            "id": session_state["id"],
                            "conversation_id": session_state["conversation_id"],
                            "mode": session_state["mode"],
                            "status": session_state["status"],
                            "flow_id": session_state.get("flow_id"),
                            "graph_id": session_state.get("graph_id"),
                            "created_at": session_state.get("created_at"),
                            "updated_at": session_state.get("updated_at")
                        })
                except Exception as e:
                    logger.exception(f"Error loading session state from {file_path}")
        
        return sessions

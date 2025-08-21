"""
Flow execution service for managing Flowise workflow execution and state.
"""

import os
import json
import uuid
import logging
from typing import Dict, List, Any, Optional

from flowise_controller import FlowiseController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlowExecutionService:
    """
    Service for executing Flowise flows and managing their state.
    """
    
    def __init__(self, flowise_controller: FlowiseController = None, data_dir: str = None):
        """
        Initialize the flow execution service.
        
        Args:
            flowise_controller: Controller for Flowise integration
            data_dir: Directory for storing execution data
        """
        self.flowise_controller = flowise_controller or FlowiseController()
        self.data_dir = data_dir or os.environ.get("FLOW_DATA_DIR", "data/flows")
        self.active_executions = {}  # Track active flow executions
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def start_flow(self, flow_id: str, conversation_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a flow execution.
        
        Args:
            flow_id: ID of the flow to execute
            conversation_id: ID of the conversation
            inputs: Input values for the flow
            
        Returns:
            Execution information
        """
        # Generate a unique execution ID
        execution_id = str(uuid.uuid4())
        
        # Execute the flow
        result = self.flowise_controller.execute_flow(flow_id, inputs)
        
        # Check for errors
        if "error" in result:
            return {
                "execution_id": execution_id,
                "error": result["error"],
                "details": result.get("details", ""),
                "message": f"Error executing flow: {result['error']}"
            }
        
        # Determine if the flow is waiting for input
        waiting_for_input = "waitForUserInput" in result and result["waitForUserInput"]
        input_prompt = result.get("inputPrompt", "Please provide additional information:")
        
        # Create execution state
        execution_state = {
            "id": execution_id,
            "flow_id": flow_id,
            "conversation_id": conversation_id,
            "status": "active",
            "waiting_for_input": waiting_for_input,
            "input_prompt": input_prompt,
            "result": result,
            "history": [
                {
                    "inputs": inputs,
                    "result": result
                }
            ]
        }
        
        # Store execution state
        self.active_executions[execution_id] = execution_state
        self._save_execution_state(execution_id, execution_state)
        
        # Prepare response
        response = {
            "execution_id": execution_id,
            "message": result.get("output", "Flow execution started."),
            "waiting_for_input": waiting_for_input,
            "input_prompt": input_prompt if waiting_for_input else None
        }
        
        return response
    
    def continue_flow(self, execution_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continue an active flow execution with new inputs.
        
        Args:
            execution_id: ID of the execution to continue
            inputs: New input values for the flow
            
        Returns:
            Updated execution information
        """
        # Get execution state
        execution_state = self.get_execution_state(execution_id)
        
        if not execution_state:
            return {
                "error": "Execution not found",
                "details": f"No active execution found with ID: {execution_id}"
            }
        
        if execution_state["status"] != "active":
            return {
                "error": "Execution not active",
                "details": f"Execution {execution_id} is not active (status: {execution_state['status']})"
            }
        
        # Execute the flow with new inputs
        flow_id = execution_state["flow_id"]
        result = self.flowise_controller.execute_flow(flow_id, inputs)
        
        # Check for errors
        if "error" in result:
            return {
                "execution_id": execution_id,
                "error": result["error"],
                "details": result.get("details", ""),
                "message": f"Error continuing flow: {result['error']}"
            }
        
        # Determine if the flow is waiting for input
        waiting_for_input = "waitForUserInput" in result and result["waitForUserInput"]
        input_prompt = result.get("inputPrompt", "Please provide additional information:")
        
        # Update execution state
        execution_state["waiting_for_input"] = waiting_for_input
        execution_state["input_prompt"] = input_prompt if waiting_for_input else None
        execution_state["result"] = result
        execution_state["history"].append({
            "inputs": inputs,
            "result": result
        })
        
        # Check if the flow is complete
        if not waiting_for_input and "output" in result:
            execution_state["status"] = "completed"
        
        # Store updated execution state
        self.active_executions[execution_id] = execution_state
        self._save_execution_state(execution_id, execution_state)
        
        # Prepare response
        response = {
            "execution_id": execution_id,
            "message": result.get("output", "Flow execution continued."),
            "waiting_for_input": waiting_for_input,
            "input_prompt": input_prompt if waiting_for_input else None,
            "status": execution_state["status"]
        }
        
        return response
    
    def get_execution_state(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current state of a flow execution.
        
        Args:
            execution_id: ID of the execution
            
        Returns:
            Current execution state or None if not found
        """
        # Check in-memory cache first
        if execution_id in self.active_executions:
            return self.active_executions[execution_id]
        
        # Try to load from disk
        file_path = os.path.join(self.data_dir, f"{execution_id}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    execution_state = json.load(f)
                    
                    # Add to in-memory cache if still active
                    if execution_state["status"] == "active":
                        self.active_executions[execution_id] = execution_state
                    
                    return execution_state
            except Exception as e:
                logger.exception(f"Error loading execution state: {execution_id}")
                return None
        
        return None
    
    def abort_flow(self, execution_id: str) -> Dict[str, Any]:
        """
        Abort an active flow execution.
        
        Args:
            execution_id: ID of the execution to abort
            
        Returns:
            Success status or error details
        """
        # Get execution state
        execution_state = self.get_execution_state(execution_id)
        
        if not execution_state:
            return {
                "error": "Execution not found",
                "details": f"No active execution found with ID: {execution_id}"
            }
        
        if execution_state["status"] != "active":
            return {
                "success": True,
                "message": f"Execution {execution_id} is already {execution_state['status']}"
            }
        
        # Update execution state
        execution_state["status"] = "aborted"
        
        # Store updated execution state
        if execution_id in self.active_executions:
            self.active_executions[execution_id] = execution_state
        
        self._save_execution_state(execution_id, execution_state)
        
        return {
            "success": True,
            "message": f"Execution {execution_id} aborted successfully"
        }
    
    def _save_execution_state(self, execution_id: str, execution_state: Dict[str, Any]) -> None:
        """
        Save execution state to disk.
        
        Args:
            execution_id: ID of the execution
            execution_state: Execution state to save
        """
        try:
            file_path = os.path.join(self.data_dir, f"{execution_id}.json")
            
            with open(file_path, "w") as f:
                json.dump(execution_state, f, indent=2)
        except Exception as e:
            logger.exception(f"Error saving execution state: {execution_id}")
    
    def list_executions(self, conversation_id: str = None, status: str = None) -> List[Dict[str, Any]]:
        """
        List flow executions.
        
        Args:
            conversation_id: Optional conversation ID to filter by
            status: Optional status to filter by
            
        Returns:
            List of executions matching the filters
        """
        executions = []
        
        # List files in data directory
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.data_dir, filename)
                
                try:
                    with open(file_path, "r") as f:
                        execution_state = json.load(f)
                        
                        # Apply filters
                        if conversation_id and execution_state.get("conversation_id") != conversation_id:
                            continue
                        
                        if status and execution_state.get("status") != status:
                            continue
                        
                        # Add to list
                        executions.append({
                            "id": execution_state["id"],
                            "flow_id": execution_state["flow_id"],
                            "conversation_id": execution_state["conversation_id"],
                            "status": execution_state["status"],
                            "waiting_for_input": execution_state.get("waiting_for_input", False),
                            "created_at": execution_state.get("created_at"),
                            "updated_at": execution_state.get("updated_at")
                        })
                except Exception as e:
                    logger.exception(f"Error loading execution state from {file_path}")
        
        return executions

"""
LangGraph controller for managing graph execution and state.
"""

import os
import sys
import json
import logging
import importlib.util
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        
        # Create module directory if it doesn't exist
        os.makedirs(self.module_path, exist_ok=True)
        
        # Add module path to Python path
        if self.module_path not in sys.path:
            sys.path.append(self.module_path)
    
    def load_graph(self, graph_id: str) -> Any:
        """
        Load a graph definition.
        
        Args:
            graph_id: ID of the graph to load
            
        Returns:
            Graph object or error details
        """
        if graph_id in self.graphs:
            return self.graphs[graph_id]
        
        try:
            # Check if module exists
            module_path = os.path.join(self.module_path, f"{graph_id}.py")
            
            if not os.path.exists(module_path):
                logger.error(f"Graph module not found: {module_path}")
                return {
                    "error": "Graph not found",
                    "details": f"No graph module found with ID: {graph_id}"
                }
            
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(graph_id, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get graph object
            if not hasattr(module, "graph"):
                logger.error(f"Graph object not found in module: {graph_id}")
                return {
                    "error": "Invalid graph module",
                    "details": f"No 'graph' object found in module: {graph_id}"
                }
            
            graph = module.graph
            self.graphs[graph_id] = graph
            
            return graph
        
        except Exception as e:
            logger.exception(f"Error loading graph {graph_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def execute_graph(self, graph_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a graph with the given inputs.
        
        Args:
            graph_id: ID of the graph to execute
            inputs: Input values for the graph
            
        Returns:
            Execution result or error details
        """
        try:
            # Load graph
            graph = self.load_graph(graph_id)
            
            if isinstance(graph, dict) and "error" in graph:
                return graph
            
            # Execute graph
            result = graph.invoke(inputs)
            
            return {
                "result": result,
                "status": "completed"
            }
        
        except Exception as e:
            logger.exception(f"Error executing graph {graph_id}")
            return {
                "error": "Execution error",
                "details": str(e)
            }
    
    def continue_graph_execution(self, execution_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continue an active graph execution with new inputs.
        
        Args:
            execution_id: ID of the execution to continue
            inputs: New input values for the graph
            
        Returns:
            Updated execution result or error details
        """
        try:
            # This is a simplified implementation
            # In a real implementation, you would need to maintain execution state
            # and use the LangGraph API to continue execution
            
            return {
                "error": "Not implemented",
                "details": "Continuing graph execution is not implemented yet"
            }
        
        except Exception as e:
            logger.exception(f"Error continuing graph execution {execution_id}")
            return {
                "error": "Execution error",
                "details": str(e)
            }
    
    def get_available_graphs(self) -> List[Dict[str, Any]]:
        """
        Get a list of available graphs.
        
        Returns:
            List of available graphs
        """
        graphs = []
        
        try:
            # List Python files in module directory
            for filename in os.listdir(self.module_path):
                if filename.endswith(".py"):
                    graph_id = os.path.splitext(filename)[0]
                    
                    # Load module to get metadata
                    try:
                        module_path = os.path.join(self.module_path, filename)
                        spec = importlib.util.spec_from_file_location(graph_id, module_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Get metadata
                        metadata = getattr(module, "metadata", {})
                        
                        graphs.append({
                            "id": graph_id,
                            "name": metadata.get("name", graph_id),
                            "description": metadata.get("description", ""),
                            "version": metadata.get("version", "1.0.0"),
                            "author": metadata.get("author", ""),
                            "tags": metadata.get("tags", [])
                        })
                    
                    except Exception as e:
                        logger.error(f"Error loading graph metadata for {graph_id}: {e}")
            
            return graphs
        
        except Exception as e:
            logger.exception("Error getting available graphs")
            return []
    
    def create_graph_module(self, graph_id: str, code: str) -> Dict[str, Any]:
        """
        Create a new graph module.
        
        Args:
            graph_id: ID for the new graph
            code: Python code for the graph module
            
        Returns:
            Success status or error details
        """
        try:
            # Validate graph_id
            if not graph_id.isalnum() and not "_" in graph_id:
                return {
                    "error": "Invalid graph ID",
                    "details": "Graph ID must contain only alphanumeric characters and underscores"
                }
            
            # Check if module already exists
            module_path = os.path.join(self.module_path, f"{graph_id}.py")
            
            if os.path.exists(module_path):
                return {
                    "error": "Graph already exists",
                    "details": f"A graph with ID '{graph_id}' already exists"
                }
            
            # Write module file
            with open(module_path, "w") as f:
                f.write(code)
            
            # Try to load the module to validate it
            try:
                spec = importlib.util.spec_from_file_location(graph_id, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if graph object exists
                if not hasattr(module, "graph"):
                    os.remove(module_path)
                    return {
                        "error": "Invalid graph module",
                        "details": "Module does not contain a 'graph' object"
                    }
                
                return {
                    "success": True,
                    "message": f"Graph '{graph_id}' created successfully"
                }
            
            except Exception as e:
                # Remove the file if validation fails
                os.remove(module_path)
                
                logger.exception(f"Error validating graph module {graph_id}")
                return {
                    "error": "Validation error",
                    "details": str(e)
                }
        
        except Exception as e:
            logger.exception(f"Error creating graph module {graph_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def update_graph_module(self, graph_id: str, code: str) -> Dict[str, Any]:
        """
        Update an existing graph module.
        
        Args:
            graph_id: ID of the graph to update
            code: New Python code for the graph module
            
        Returns:
            Success status or error details
        """
        try:
            # Check if module exists
            module_path = os.path.join(self.module_path, f"{graph_id}.py")
            
            if not os.path.exists(module_path):
                return {
                    "error": "Graph not found",
                    "details": f"No graph found with ID: {graph_id}"
                }
            
            # Create backup
            backup_path = f"{module_path}.bak"
            with open(module_path, "r") as src, open(backup_path, "w") as dst:
                dst.write(src.read())
            
            # Write new code
            with open(module_path, "w") as f:
                f.write(code)
            
            # Try to load the module to validate it
            try:
                # Clear from cache if present
                if graph_id in self.graphs:
                    del self.graphs[graph_id]
                
                spec = importlib.util.spec_from_file_location(graph_id, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if graph object exists
                if not hasattr(module, "graph"):
                    # Restore backup
                    os.remove(module_path)
                    os.rename(backup_path, module_path)
                    
                    return {
                        "error": "Invalid graph module",
                        "details": "Module does not contain a 'graph' object"
                    }
                
                # Remove backup
                os.remove(backup_path)
                
                return {
                    "success": True,
                    "message": f"Graph '{graph_id}' updated successfully"
                }
            
            except Exception as e:
                # Restore backup
                os.remove(module_path)
                os.rename(backup_path, module_path)
                
                logger.exception(f"Error validating updated graph module {graph_id}")
                return {
                    "error": "Validation error",
                    "details": str(e)
                }
        
        except Exception as e:
            logger.exception(f"Error updating graph module {graph_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def delete_graph_module(self, graph_id: str) -> Dict[str, Any]:
        """
        Delete a graph module.
        
        Args:
            graph_id: ID of the graph to delete
            
        Returns:
            Success status or error details
        """
        try:
            # Check if module exists
            module_path = os.path.join(self.module_path, f"{graph_id}.py")
            
            if not os.path.exists(module_path):
                return {
                    "error": "Graph not found",
                    "details": f"No graph found with ID: {graph_id}"
                }
            
            # Remove from cache if present
            if graph_id in self.graphs:
                del self.graphs[graph_id]
            
            # Delete file
            os.remove(module_path)
            
            return {
                "success": True,
                "message": f"Graph '{graph_id}' deleted successfully"
            }
        
        except Exception as e:
            logger.exception(f"Error deleting graph module {graph_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }

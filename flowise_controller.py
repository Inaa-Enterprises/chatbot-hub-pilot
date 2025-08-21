"""
Flowise controller for managing workflow execution and state.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        """
        Load a flow definition from Flowise.
        
        Args:
            flow_id: ID of the flow to load
            
        Returns:
            Flow definition or error details
        """
        if flow_id in self.flows:
            return self.flows[flow_id]
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(
                f"{self.api_url}/flows/{flow_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                flow_data = response.json()
                self.flows[flow_id] = flow_data
                return flow_data
            else:
                logger.error(f"Error loading flow {flow_id}: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception(f"Error loading flow {flow_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def execute_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a flow with the given inputs.
        
        Args:
            flow_id: ID of the flow to execute
            inputs: Input values for the flow
            
        Returns:
            Execution result or error details
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            data = {
                "inputs": inputs
            }
            
            response = requests.post(
                f"{self.api_url}/flows/{flow_id}/predict",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error executing flow {flow_id}: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception(f"Error executing flow {flow_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def get_available_flows(self) -> List[Dict[str, Any]]:
        """
        Get a list of available flows.
        
        Returns:
            List of available flows or empty list on error
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(
                f"{self.api_url}/flows",
                headers=headers
            )
            
            if response.status_code == 200:
                flows = response.json()
                
                # Update cache
                for flow in flows:
                    if "id" in flow:
                        self.flows[flow["id"]] = flow
                
                return flows
            else:
                logger.error(f"Error getting flows: {response.status_code} - {response.text}")
                return []
        
        except Exception as e:
            logger.exception("Error getting flows")
            return []
    
    def create_flow(self, flow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new flow in Flowise.
        
        Args:
            flow_definition: Definition of the flow to create
            
        Returns:
            Created flow data or error details
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.post(
                f"{self.api_url}/flows",
                headers=headers,
                json=flow_definition
            )
            
            if response.status_code == 201:
                flow_data = response.json()
                
                if "id" in flow_data:
                    self.flows[flow_data["id"]] = flow_data
                
                return flow_data
            else:
                logger.error(f"Error creating flow: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception("Error creating flow")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def update_flow(self, flow_id: str, flow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing flow in Flowise.
        
        Args:
            flow_id: ID of the flow to update
            flow_definition: New definition for the flow
            
        Returns:
            Updated flow data or error details
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.put(
                f"{self.api_url}/flows/{flow_id}",
                headers=headers,
                json=flow_definition
            )
            
            if response.status_code == 200:
                flow_data = response.json()
                
                if "id" in flow_data:
                    self.flows[flow_data["id"]] = flow_data
                
                return flow_data
            else:
                logger.error(f"Error updating flow {flow_id}: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception(f"Error updating flow {flow_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def delete_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Delete a flow from Flowise.
        
        Args:
            flow_id: ID of the flow to delete
            
        Returns:
            Success status or error details
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.delete(
                f"{self.api_url}/flows/{flow_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                # Remove from cache
                if flow_id in self.flows:
                    del self.flows[flow_id]
                
                return {"success": True}
            else:
                logger.error(f"Error deleting flow {flow_id}: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception(f"Error deleting flow {flow_id}")
            return {
                "error": "Service error",
                "details": str(e)
            }

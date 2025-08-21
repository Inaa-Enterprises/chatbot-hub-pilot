"""
Validation script for Flowise autopilot and LangGraph co-pilot functionality.
"""

import os
import sys
import json
import logging
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import modules to test
from flowise_controller import FlowiseController
from flow_execution_service import FlowExecutionService
from langgraph_controller import LangGraphController
from graph_execution_service import GraphExecutionService
from agent_orchestrator import AgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestFlowiseAutopilot(unittest.TestCase):
    """Test cases for Flowise autopilot functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock the Flowise controller
        self.flowise_controller = MagicMock(spec=FlowiseController)
        
        # Create a flow execution service with the mock controller
        self.flow_execution_service = FlowExecutionService(
            flowise_controller=self.flowise_controller,
            data_dir="./test_data/flows"
        )
        
        # Create test data directory if it doesn't exist
        os.makedirs("./test_data/flows", exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test data
        for filename in os.listdir("./test_data/flows"):
            os.remove(os.path.join("./test_data/flows", filename))
    
    def test_start_flow(self):
        """Test starting a flow execution."""
        # Mock the execute_flow method to return a successful result
        self.flowise_controller.execute_flow.return_value = {
            "output": "Flow started successfully",
            "waitForUserInput": True,
            "inputPrompt": "Please provide more information:"
        }
        
        # Start a flow execution
        result = self.flow_execution_service.start_flow(
            flow_id="test_flow",
            conversation_id="test_conversation",
            inputs={"message": "Hello, world!"}
        )
        
        # Check that the controller was called with the correct arguments
        self.flowise_controller.execute_flow.assert_called_once_with(
            "test_flow",
            {"message": "Hello, world!"}
        )
        
        # Check the result
        self.assertIn("execution_id", result)
        self.assertEqual(result["message"], "Flow started successfully")
        self.assertTrue(result["waiting_for_input"])
        self.assertEqual(result["input_prompt"], "Please provide more information:")
    
    def test_continue_flow(self):
        """Test continuing a flow execution."""
        # Mock the execute_flow method to return a successful result
        self.flowise_controller.execute_flow.return_value = {
            "output": "Flow continued successfully",
            "waitForUserInput": False
        }
        
        # Create a test execution state
        execution_id = "test_execution"
        execution_state = {
            "id": execution_id,
            "flow_id": "test_flow",
            "conversation_id": "test_conversation",
            "status": "active",
            "waiting_for_input": True,
            "input_prompt": "Please provide more information:",
            "result": {},
            "history": []
        }
        
        # Save the execution state
        self.flow_execution_service.active_executions[execution_id] = execution_state
        self.flow_execution_service._save_execution_state(execution_id, execution_state)
        
        # Continue the flow execution
        result = self.flow_execution_service.continue_flow(
            execution_id=execution_id,
            inputs={"response": "More information"}
        )
        
        # Check that the controller was called with the correct arguments
        self.flowise_controller.execute_flow.assert_called_once_with(
            "test_flow",
            {"response": "More information"}
        )
        
        # Check the result
        self.assertEqual(result["execution_id"], execution_id)
        self.assertEqual(result["message"], "Flow continued successfully")
        self.assertFalse(result["waiting_for_input"])
        self.assertEqual(result["status"], "completed")
    
    def test_error_handling(self):
        """Test error handling in flow execution."""
        # Mock the execute_flow method to return an error
        self.flowise_controller.execute_flow.return_value = {
            "error": "Flow execution failed",
            "details": "Invalid input"
        }
        
        # Start a flow execution
        result = self.flow_execution_service.start_flow(
            flow_id="test_flow",
            conversation_id="test_conversation",
            inputs={"message": "Hello, world!"}
        )
        
        # Check the result
        self.assertIn("execution_id", result)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Flow execution failed")
        self.assertEqual(result["details"], "Invalid input")


class TestLangGraphCopilot(unittest.TestCase):
    """Test cases for LangGraph co-pilot functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock the LangGraph controller
        self.langgraph_controller = MagicMock(spec=LangGraphController)
        
        # Create a graph execution service with the mock controller
        self.graph_execution_service = GraphExecutionService(
            langgraph_controller=self.langgraph_controller,
            data_dir="./test_data/graphs"
        )
        
        # Create test data directory if it doesn't exist
        os.makedirs("./test_data/graphs", exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test data
        for filename in os.listdir("./test_data/graphs"):
            os.remove(os.path.join("./test_data/graphs", filename))
    
    def test_start_graph(self):
        """Test starting a graph execution."""
        # Mock the execute_graph method to return a successful result
        self.langgraph_controller.execute_graph.return_value = {
            "result": {
                "output": "Graph started successfully"
            },
            "status": "completed",
            "waiting_for_input": True,
            "input_prompt": "Please provide more information:",
            "current_agent": "research_agent",
            "thinking": True,
            "progress": 0.25
        }
        
        # Start a graph execution
        result = self.graph_execution_service.start_graph(
            graph_id="test_graph",
            conversation_id="test_conversation",
            inputs={"message": "Hello, world!"}
        )
        
        # Check that the controller was called with the correct arguments
        self.langgraph_controller.execute_graph.assert_called_once_with(
            "test_graph",
            {"message": "Hello, world!"}
        )
        
        # Check the result
        self.assertIn("execution_id", result)
        self.assertEqual(result["message"], "Graph started successfully")
        self.assertTrue(result["waiting_for_input"])
        self.assertEqual(result["input_prompt"], "Please provide more information:")
        self.assertEqual(result["current_agent"], "research_agent")
        self.assertTrue(result["thinking"])
        self.assertEqual(result["progress"], 0.25)
    
    def test_continue_graph(self):
        """Test continuing a graph execution."""
        # Mock the continue_graph_execution method to return a successful result
        self.langgraph_controller.continue_graph_execution.return_value = {
            "result": {
                "output": "Graph continued successfully"
            },
            "status": "completed",
            "waiting_for_input": False,
            "current_agent": "writing_agent",
            "thinking": False,
            "progress": 0.75
        }
        
        # Create a test execution state
        execution_id = "test_execution"
        execution_state = {
            "id": execution_id,
            "graph_id": "test_graph",
            "conversation_id": "test_conversation",
            "status": "active",
            "waiting_for_input": True,
            "input_prompt": "Please provide more information:",
            "current_agent": "research_agent",
            "thinking": True,
            "progress": 0.25,
            "result": {},
            "history": []
        }
        
        # Save the execution state
        self.graph_execution_service.active_executions[execution_id] = execution_state
        self.graph_execution_service._save_execution_state(execution_id, execution_state)
        
        # Continue the graph execution
        result = self.graph_execution_service.continue_graph(
            execution_id=execution_id,
            inputs={"response": "More information"}
        )
        
        # Check that the controller was called with the correct arguments
        self.langgraph_controller.continue_graph_execution.assert_called_once_with(
            execution_id,
            {"response": "More information"}
        )
        
        # Check the result
        self.assertEqual(result["execution_id"], execution_id)
        self.assertEqual(result["message"], "Graph continued successfully")
        self.assertFalse(result["waiting_for_input"])
        self.assertEqual(result["current_agent"], "writing_agent")
        self.assertFalse(result["thinking"])
        self.assertEqual(result["progress"], 0.75)
        self.assertEqual(result["status"], "completed")


class TestAgentOrchestrator(unittest.TestCase):
    """Test cases for Agent Orchestrator."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock the flow execution service
        self.flow_execution_service = MagicMock(spec=FlowExecutionService)
        
        # Mock the graph execution service
        self.graph_execution_service = MagicMock(spec=GraphExecutionService)
        
        # Create an agent orchestrator with the mock services
        self.agent_orchestrator = AgentOrchestrator(
            flow_execution_service=self.flow_execution_service,
            graph_execution_service=self.graph_execution_service,
            data_dir="./test_data/orchestrator"
        )
        
        # Create test data directory if it doesn't exist
        os.makedirs("./test_data/orchestrator", exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test data
        for filename in os.listdir("./test_data/orchestrator"):
            os.remove(os.path.join("./test_data/orchestrator", filename))
    
    def test_start_session_flowise(self):
        """Test starting a Flowise session."""
        # Mock the start_flow method to return a successful result
        self.flow_execution_service.start_flow.return_value = {
            "execution_id": "test_execution",
            "message": "Flow started successfully",
            "waiting_for_input": True,
            "input_prompt": "Please provide more information:"
        }
        
        # Start a session
        result = self.agent_orchestrator.start_session(
            conversation_id="test_conversation",
            message="Hello, world!",
            mode="flowise",
            flow_id="test_flow"
        )
        
        # Check that the flow execution service was called with the correct arguments
        self.flow_execution_service.start_flow.assert_called_once_with(
            flow_id="test_flow",
            conversation_id="test_conversation",
            inputs={"message": "Hello, world!"}
        )
        
        # Check the result
        self.assertIn("session_id", result)
        self.assertEqual(result["mode"], "flowise")
        self.assertEqual(result["flow_id"], "test_flow")
        self.assertEqual(result["execution_id"], "test_execution")
        self.assertEqual(result["message"], "Flow started successfully")
        self.assertTrue(result["waiting_for_input"])
        self.assertEqual(result["input_prompt"], "Please provide more information:")
    
    def test_start_session_langgraph(self):
        """Test starting a LangGraph session."""
        # Mock the start_graph method to return a successful result
        self.graph_execution_service.start_graph.return_value = {
            "execution_id": "test_execution",
            "message": "Graph started successfully",
            "waiting_for_input": True,
            "input_prompt": "Please provide more information:",
            "current_agent": "research_agent",
            "thinking": True,
            "progress": 0.25
        }
        
        # Start a session
        result = self.agent_orchestrator.start_session(
            conversation_id="test_conversation",
            message="Hello, world!",
            mode="langgraph",
            graph_id="test_graph"
        )
        
        # Check that the graph execution service was called with the correct arguments
        self.graph_execution_service.start_graph.assert_called_once_with(
            graph_id="test_graph",
            conversation_id="test_conversation",
            inputs={"message": "Hello, world!"}
        )
        
        # Check the result
        self.assertIn("session_id", result)
        self.assertEqual(result["mode"], "langgraph")
        self.assertEqual(result["graph_id"], "test_graph")
        self.assertEqual(result["execution_id"], "test_execution")
        self.assertEqual(result["message"], "Graph started successfully")
        self.assertTrue(result["waiting_for_input"])
        self.assertEqual(result["input_prompt"], "Please provide more information:")
        self.assertEqual(result["current_agent"], "research_agent")
        self.assertTrue(result["thinking"])
        self.assertEqual(result["progress"], 0.25)
    
    def test_auto_mode_selection(self):
        """Test automatic mode selection."""
        # Mock the start_flow method to return a successful result
        self.flow_execution_service.start_flow.return_value = {
            "execution_id": "test_execution",
            "message": "Flow started successfully",
            "waiting_for_input": False
        }
        
        # Start a session with auto mode and a message about content creation
        result = self.agent_orchestrator.start_session(
            conversation_id="test_conversation",
            message="Can you help me write a blog post?",
            mode="auto"
        )
        
        # Check that the flow execution service was called
        self.flow_execution_service.start_flow.assert_called_once()
        self.graph_execution_service.start_graph.assert_not_called()
        
        # Check the result
        self.assertIn("session_id", result)
        self.assertEqual(result["mode"], "flowise")
        
        # Reset mocks
        self.flow_execution_service.reset_mock()
        self.graph_execution_service.reset_mock()
        
        # Mock the start_graph method to return a successful result
        self.graph_execution_service.start_graph.return_value = {
            "execution_id": "test_execution",
            "message": "Graph started successfully",
            "waiting_for_input": False
        }
        
        # Start a session with auto mode and a message about code
        result = self.agent_orchestrator.start_session(
            conversation_id="test_conversation",
            message="Can you help me write a Python program?",
            mode="auto"
        )
        
        # Check that the graph execution service was called
        self.flow_execution_service.start_flow.assert_not_called()
        self.graph_execution_service.start_graph.assert_called_once()
        
        # Check the result
        self.assertIn("session_id", result)
        self.assertEqual(result["mode"], "langgraph")


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestFlowiseAutopilot))
    test_suite.addTest(unittest.makeSuite(TestLangGraphCopilot))
    test_suite.addTest(unittest.makeSuite(TestAgentOrchestrator))
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Return success status
    return test_result.wasSuccessful()


if __name__ == "__main__":
    # Run tests
    success = run_tests()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

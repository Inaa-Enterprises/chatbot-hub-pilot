"""
API routes for Flowise and LangGraph integration.
"""

from flask import Blueprint, request, jsonify
import os
import json
import logging
from typing import Dict, Any

from flowise_controller import FlowiseController
from flow_execution_service import FlowExecutionService
from langgraph_controller import LangGraphController
from graph_execution_service import GraphExecutionService
from agent_orchestrator import AgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
flowise_controller = FlowiseController()
flow_execution_service = FlowExecutionService(flowise_controller=flowise_controller)
langgraph_controller = LangGraphController()
graph_execution_service = GraphExecutionService(langgraph_controller=langgraph_controller)
agent_orchestrator = AgentOrchestrator(
    flow_execution_service=flow_execution_service,
    graph_execution_service=graph_execution_service
)

# Create blueprint
agent_bp = Blueprint('agent', __name__)

# Flowise routes
@agent_bp.route('/flows', methods=['GET'])
def list_flows():
    """List available flows"""
    flows = flowise_controller.get_available_flows()
    return jsonify({"flows": flows})

@agent_bp.route('/flows/<flow_id>', methods=['GET'])
def get_flow(flow_id):
    """Get a flow by ID"""
    flow = flowise_controller.load_flow(flow_id)
    
    if isinstance(flow, dict) and "error" in flow:
        return jsonify(flow), 404
    
    return jsonify(flow)

@agent_bp.route('/flows', methods=['POST'])
def create_flow():
    """Create a new flow"""
    flow_definition = request.json
    result = flowise_controller.create_flow(flow_definition)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result), 201

@agent_bp.route('/flows/<flow_id>', methods=['PUT'])
def update_flow(flow_id):
    """Update a flow"""
    flow_definition = request.json
    result = flowise_controller.update_flow(flow_id, flow_definition)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/flows/<flow_id>', methods=['DELETE'])
def delete_flow(flow_id):
    """Delete a flow"""
    result = flowise_controller.delete_flow(flow_id)
    
    if "error" in result:
        return jsonify(result), 404
    
    return jsonify(result)

@agent_bp.route('/flows/<flow_id>/execute', methods=['POST'])
def execute_flow(flow_id):
    """Execute a flow"""
    inputs = request.json
    conversation_id = inputs.pop("conversation_id", "default")
    
    result = flow_execution_service.start_flow(
        flow_id=flow_id,
        conversation_id=conversation_id,
        inputs=inputs
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/flows/executions/<execution_id>', methods=['POST'])
def continue_flow(execution_id):
    """Continue a flow execution"""
    inputs = request.json
    
    result = flow_execution_service.continue_flow(
        execution_id=execution_id,
        inputs=inputs
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/flows/executions/<execution_id>', methods=['GET'])
def get_flow_execution(execution_id):
    """Get a flow execution"""
    execution = flow_execution_service.get_execution_state(execution_id)
    
    if not execution:
        return jsonify({"error": "Execution not found"}), 404
    
    return jsonify(execution)

@agent_bp.route('/flows/executions/<execution_id>/abort', methods=['POST'])
def abort_flow(execution_id):
    """Abort a flow execution"""
    result = flow_execution_service.abort_flow(execution_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

# LangGraph routes
@agent_bp.route('/graphs', methods=['GET'])
def list_graphs():
    """List available graphs"""
    graphs = langgraph_controller.get_available_graphs()
    return jsonify({"graphs": graphs})

@agent_bp.route('/graphs/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    """Get a graph by ID"""
    graph = langgraph_controller.load_graph(graph_id)
    
    if isinstance(graph, dict) and "error" in graph:
        return jsonify(graph), 404
    
    # Convert graph object to serializable format
    return jsonify({"id": graph_id, "status": "loaded"})

@agent_bp.route('/graphs', methods=['POST'])
def create_graph():
    """Create a new graph"""
    data = request.json
    graph_id = data.get("id")
    code = data.get("code")
    
    if not graph_id or not code:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = langgraph_controller.create_graph_module(graph_id, code)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result), 201

@agent_bp.route('/graphs/<graph_id>', methods=['PUT'])
def update_graph(graph_id):
    """Update a graph"""
    data = request.json
    code = data.get("code")
    
    if not code:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = langgraph_controller.update_graph_module(graph_id, code)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/graphs/<graph_id>', methods=['DELETE'])
def delete_graph(graph_id):
    """Delete a graph"""
    result = langgraph_controller.delete_graph_module(graph_id)
    
    if "error" in result:
        return jsonify(result), 404
    
    return jsonify(result)

@agent_bp.route('/graphs/<graph_id>/execute', methods=['POST'])
def execute_graph(graph_id):
    """Execute a graph"""
    inputs = request.json
    conversation_id = inputs.pop("conversation_id", "default")
    
    result = graph_execution_service.start_graph(
        graph_id=graph_id,
        conversation_id=conversation_id,
        inputs=inputs
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/graphs/executions/<execution_id>', methods=['POST'])
def continue_graph(execution_id):
    """Continue a graph execution"""
    inputs = request.json
    
    result = graph_execution_service.continue_graph(
        execution_id=execution_id,
        inputs=inputs
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/graphs/executions/<execution_id>', methods=['GET'])
def get_graph_execution(execution_id):
    """Get a graph execution"""
    execution = graph_execution_service.get_execution_state(execution_id)
    
    if not execution:
        return jsonify({"error": "Execution not found"}), 404
    
    return jsonify(execution)

@agent_bp.route('/graphs/executions/<execution_id>/abort', methods=['POST'])
def abort_graph(execution_id):
    """Abort a graph execution"""
    result = graph_execution_service.abort_graph(execution_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

# Agent orchestrator routes
@agent_bp.route('/sessions', methods=['POST'])
def start_session():
    """Start a new orchestration session"""
    data = request.json
    conversation_id = data.get("conversation_id", "default")
    message = data.get("message", "")
    mode = data.get("mode", "auto")
    flow_id = data.get("flow_id")
    graph_id = data.get("graph_id")
    
    result = agent_orchestrator.start_session(
        conversation_id=conversation_id,
        message=message,
        mode=mode,
        flow_id=flow_id,
        graph_id=graph_id
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/sessions/<session_id>', methods=['POST'])
def continue_session(session_id):
    """Continue an orchestration session"""
    inputs = request.json
    
    result = agent_orchestrator.continue_session(
        session_id=session_id,
        inputs=inputs
    )
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get an orchestration session"""
    session = agent_orchestrator.get_session_state(session_id)
    
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify(session)

@agent_bp.route('/sessions/<session_id>/abort', methods=['POST'])
def abort_session(session_id):
    """Abort an orchestration session"""
    result = agent_orchestrator.abort_session(session_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@agent_bp.route('/sessions', methods=['GET'])
def list_sessions():
    """List orchestration sessions"""
    conversation_id = request.args.get("conversation_id")
    status = request.args.get("status")
    
    sessions = agent_orchestrator.list_sessions(
        conversation_id=conversation_id,
        status=status
    )
    
    return jsonify({"sessions": sessions})

# Enhanced chat endpoint
@agent_bp.route('/chat', methods=['POST'])
def handle_chat():
    """Handle chat messages with support for autopilot and co-pilot modes"""
    data = request.json
    message = data.get("message", "")
    persona_id = data.get("personaId", "default")
    conversation_id = data.get("conversationId")
    prompt_mode = data.get("promptMode", False)
    autopilot_mode = data.get("autopilotMode", False)
    copilot_mode = data.get("copilotMode", False)
    flow_id = data.get("flowId")
    graph_id = data.get("graphId")
    
    # Handle autopilot mode
    if autopilot_mode:
        result = agent_orchestrator.start_session(
            conversation_id=conversation_id or "default",
            message=message,
            mode="flowise",
            flow_id=flow_id
        )
        
        if "error" in result:
            return jsonify({
                "message": f"Error starting autopilot: {result['error']}",
                "conversationId": conversation_id,
                "error": result["error"],
                "details": result.get("details", "")
            }), 400
        
        return jsonify({
            "message": result.get("message", "Starting automated workflow..."),
            "conversationId": conversation_id,
            "autopilotMode": True,
            "flowId": result.get("flow_id"),
            "sessionId": result.get("session_id"),
            "executionId": result.get("execution_id"),
            "waitingForInput": result.get("waiting_for_input", False),
            "inputPrompt": result.get("input_prompt")
        })
    
    # Handle co-pilot mode
    if copilot_mode:
        result = agent_orchestrator.start_session(
            conversation_id=conversation_id or "default",
            message=message,
            mode="langgraph",
            graph_id=graph_id
        )
        
        if "error" in result:
            return jsonify({
                "message": f"Error starting co-pilot: {result['error']}",
                "conversationId": conversation_id,
                "error": result["error"],
                "details": result.get("details", "")
            }), 400
        
        return jsonify({
            "message": result.get("message", "Starting co-pilot mode..."),
            "conversationId": conversation_id,
            "copilotMode": True,
            "graphId": result.get("graph_id"),
            "sessionId": result.get("session_id"),
            "executionId": result.get("execution_id"),
            "agentId": result.get("current_agent"),
            "waitingForInput": result.get("waiting_for_input", False),
            "inputPrompt": result.get("input_prompt"),
            "thinking": result.get("thinking", False),
            "progress": result.get("progress", 0)
        })
    
    # Handle prompt mode and normal chat flow
    # This would call the existing chat handler
    # For now, return a placeholder response
    return jsonify({
        "message": "This is a placeholder response. In a real implementation, this would call the existing chat handler.",
        "conversationId": conversation_id,
        "promptMode": prompt_mode
    })

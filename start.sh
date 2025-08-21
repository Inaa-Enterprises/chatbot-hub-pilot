#!/bin/bash

# Create necessary directories
mkdir -p data/flows
mkdir -p data/graphs
mkdir -p data/orchestrator
mkdir -p langgraph_modules

# Install required packages
pip install requests flask langchain langflow

# Set environment variables
export FLOWISE_API_URL="http://localhost:3000/api"
export FLOW_DATA_DIR="data/flows"
export GRAPH_DATA_DIR="data/graphs"
export ORCHESTRATOR_DATA_DIR="data/orchestrator"

# Start the server
echo "Starting the server..."
python main.py

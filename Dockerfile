# Dockerfile for Railway deployment
# This ensures only the Python backend is built and deployed

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the Python requirements file first to leverage Docker caching
COPY requirements.txt .

# Install only Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the Python application files
COPY main.py .
COPY personas.py .
COPY services.py .
COPY huggingface_service.py .
COPY user_api_service.py .
COPY agent_routes.py .
COPY flow_execution_service.py .
COPY flowise_controller.py .
COPY graph_execution_service.py .
COPY langgraph_controller.py .
COPY bot.py .
COPY bot_service.py .
COPY conversation.py .
COPY knowledge_base.py .
COPY llm_service.py .
COPY prompt_manager.py .
COPY speech_service.py .
COPY models.py .

# Expose port
EXPOSE $PORT

# Run the application
CMD gunicorn main:app
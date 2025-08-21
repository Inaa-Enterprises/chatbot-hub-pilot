# Synapse Backend - Flask Integration

This is a Flask-based backend server that integrates Flowise and LangGraph functionality with a RESTful API interface.

## Features

- **Flowise Integration**: Manage and execute Flowise workflows
- **LangGraph Integration**: Manage and execute LangGraph agents
- **Agent Orchestration**: Unified interface for both Flowise and LangGraph
- **Chat Interface**: Support for autopilot and co-pilot modes
- **Personas**: Pre-configured AI personalities
- **Templates**: Ready-to-use content templates

## API Endpoints

### Core Endpoints
- `GET /` - Basic health check
- `GET /health` - Detailed health status
- `GET /api/personas` - List available personas
- `GET /api/templates` - List available templates

### Flowise Endpoints
- `GET /api/flows` - List available flows
- `GET /api/flows/<flow_id>` - Get flow details
- `POST /api/flows` - Create new flow
- `PUT /api/flows/<flow_id>` - Update flow
- `DELETE /api/flows/<flow_id>` - Delete flow
- `POST /api/flows/<flow_id>/execute` - Execute flow
- `POST /api/flows/executions/<execution_id>` - Continue flow execution
- `GET /api/flows/executions/<execution_id>` - Get execution status
- `POST /api/flows/executions/<execution_id>/abort` - Abort execution

### LangGraph Endpoints
- `GET /api/graphs` - List available graphs
- `GET /api/graphs/<graph_id>` - Get graph details
- `POST /api/graphs/<graph_id>/execute` - Execute graph
- `POST /api/graphs/executions/<execution_id>` - Continue graph execution
- `GET /api/graphs/executions/<execution_id>` - Get execution status
- `POST /api/graphs/executions/<execution_id>/abort` - Abort execution

### Agent Orchestration Endpoints
- `POST /api/sessions` - Start new orchestration session
- `GET /api/sessions/<session_id>` - Get session status
- `POST /api/sessions/<session_id>/continue` - Continue session
- `POST /api/sessions/<session_id>/abort` - Abort session
- `GET /api/sessions` - List sessions

### Chat Endpoints
- `POST /api/chat` - Handle chat messages with autopilot/copilot support

## Quick Start

### 1. Install Dependencies
```bash
python run.py --install
```

### 2. Start the Server
```bash
# Basic start
python run.py

# With debug mode
python run.py --debug

# Custom port
python run.py --port 8080

# Install requirements and start
python run.py --install --debug
```

### 3. Test the Integration
```bash
# Run integration tests
python test_integration.py

# Run tests with server auto-start
python run.py --test
```

## Usage Examples

### Basic Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "personaId": "synapse"}'
```

### Autopilot Mode (Flowise)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to write a blog post",
    "autopilotMode": true,
    "flowId": "blog-post-generator"
  }'
```

### Co-pilot Mode (LangGraph)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Help me debug this code",
    "copilotMode": true,
    "graphId": "code-debugger"
  }'
```

### List Available Flows
```bash
curl http://localhost:8000/api/flows
```

### Execute a Flow
```bash
curl -X POST http://localhost:8000/api/flows/flow-id/execute \
  -H "Content-Type: application/json" \
  -d '{"input": "test input"}'
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` or `production`
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### Logging
Logs are written to `app.log` in the project root directory.

## Development

### Project Structure
```
.
├── main.py              # Main Flask application
├── agent_routes.py      # API routes for agents
├── personas.py          # Persona definitions
├── test_integration.py  # Integration tests
├── run.py              # Server runner script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Adding New Endpoints
1. Add routes to `agent_routes.py` for agent-related functionality
2. Add routes to `main.py` for general API endpoints
3. Update this README with new endpoints
4. Add tests to `test_integration.py`

## Testing

### Manual Testing
```bash
# Start server
python run.py --debug

# In another terminal, test endpoints
python test_integration.py
```

### Automated Testing
```bash
# Run all tests
python test_integration.py

# Run with server auto-start
python run.py --test
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   python run.py --port 8080
   ```

2. **Missing dependencies**
   ```bash
   python run.py --install
   ```

3. **CORS issues**
   - CORS is enabled for all origins in development
   - Configure CORS in production as needed

4. **Module not found**
   ```bash
   pip install -r requirements.txt
   ```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn main:app -b 0.0.0.0:8000 --workers=4
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "8000"]
```

## License

MIT License - see LICENSE file for details.

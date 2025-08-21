# Synapse Backend with Mobile Client

A Flask-based backend server that integrates Flowise and LangGraph functionality with a RESTful API interface, plus a responsive mobile client that works on all devices including foldable phones.

## Features

### Backend Features
- **Flowise Integration**: Manage and execute Flowise workflows
- **LangGraph Integration**: Manage and execute LangGraph agents
- **Agent Orchestration**: Unified interface for both Flowise and LangGraph
- **Chat Interface**: Support for autopilot and co-pilot modes
- **Personas**: Pre-configured AI personalities
- **Templates**: Ready-to-use content templates

### Mobile Client Features
- **Universal Device Support**: Works on all mobile devices including foldable phones
- **Responsive Design**: Automatically adjusts to any screen size
- **Portrait and Landscape**: Optimized for both orientations
- **Touch-Friendly Interface**: Appropriate sizing for all touch interactions
- **Cyberpunk Aesthetics**: Dark theme with gradient accents

## Quick Start

### 1. Deploy to Render (Recommended)
1. Fork this repository to your GitHub account
2. Go to [render.com](https://render.com) and sign up with GitHub
3. Click "New+" and select "Web Service"
4. Connect your forked repository
5. Fill in these settings:
   - Name: `synapse-backend`
   - Region: Choose the one closest to you
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment to complete
8. Note the URL provided (e.g., `https://synapse-backend-xxxx.onrender.com`)

### 2. Use the Mobile Client
1. Email `enhanced_mobile_client.html` to yourself
2. Open the email on your mobile device
3. Download and open the HTML file in any mobile browser
4. Enter your deployed backend URL
5. Start chatting with different AI personas!

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

## Personas

The system comes with several pre-configured personas:
- **Synapse**: Your core AI assistant
- **AI Tutor**: Explains complex topics simply
- **Content Creator**: Generates creative text formats

## Mobile Client Usage

The mobile client ([enhanced_mobile_client.html](file:///home/ali-asghar-rao/Documents/Simple%20Backend%20Design%20for%20Chatbot%20Hub%20(2)/enhanced_mobile_client.html)) is designed to work on:
- Regular smartphones (all sizes)
- Phablets
- Foldable devices (both folded and unfolded states)
- Tablets

### Features
- Automatic layout adjustment based on screen size
- Support for device orientation changes
- Safe area handling for notched devices
- Dynamic persona selection
- Real-time chat interface

## Development

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py [--debug] [--port PORT]
```

### Testing
```bash
# Run integration tests
python test_integration.py
```

## Deployment

### Render Deployment
Follow the quick start instructions above.

### Environment Variables
For production deployments, you may need to set:
- `PORT`: Port to bind to (provided by Render)
- `HOST`: Host to bind to (provided by Render)

## Troubleshooting

### Common Issues
1. **Application Error on Render**: Check logs in Render dashboard
2. **Can't Connect from Mobile**: Verify URL uses https:// and is accessible
3. **Personas Not Loading**: Check that backend is running and accessible

### Support
For issues, check the [Render documentation](https://render.com/docs) or open an issue on this repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

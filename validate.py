# Validation Test Script for Synapse Backend

import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    # Note: In a real environment, you would include an Authorization header
    # "Authorization": "Bearer YOUR_TOKEN_HERE"
}

def test_health_check():
    """Test the health check endpoint."""
    print("\n🔍 Testing health check endpoint...")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("✅ Health check successful")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_list_personas():
    """Test the list personas endpoint."""
    print("\n🔍 Testing list personas endpoint...")
    
    response = requests.get(f"{BASE_URL}/api/personas")
    
    if response.status_code == 200:
        personas = response.json()
        print(f"✅ Found {len(personas)} personas")
        for persona in personas:
            print(f"  - {persona['name']} ({persona['id']}): {persona['tagline']}")
        return True
    else:
        print(f"❌ List personas failed: {response.status_code}")
        return False

def test_normal_chat():
    """Test the normal chat flow."""
    print("\n🔍 Testing normal chat flow...")
    
    payload = {
        "personaId": "synapse",
        "message": "Hello, how are you today?",
        "promptMode": False
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Normal chat successful")
        print(f"  Message: {data['message'][:100]}...")
        print(f"  Conversation ID: {data['conversationId']}")
        print(f"  Prompt Mode: {data['promptMode']}")
        print(f"  Is Question: {data['isQuestion']}")
        return data['conversationId']
    else:
        print(f"❌ Normal chat failed: {response.status_code}")
        return None

def test_prompt_mode_chat():
    """Test the prompt mode chat flow."""
    print("\n🔍 Testing prompt mode chat flow...")
    
    # Initial message with prompt mode enabled
    payload = {
        "personaId": "synapse",
        "message": "I need help writing a blog post about artificial intelligence",
        "promptMode": True
    }
    
    print("  Sending initial message with prompt mode enabled...")
    response = requests.post(f"{BASE_URL}/api/chat", json=payload, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Prompt mode initialization failed: {response.status_code}")
        return None
    
    data = response.json()
    conversation_id = data['conversationId']
    
    print(f"  First question: {data['message']}")
    print(f"  Conversation ID: {conversation_id}")
    print(f"  Prompt Mode: {data['promptMode']}")
    print(f"  Is Question: {data['isQuestion']}")
    
    if not data['isQuestion']:
        print("❌ Expected a question but didn't receive one")
        return None
    
    # Simulate answering questions in the questionnaire
    questions_and_answers = [
        "Blog Post",  # Content Type
        "Tech enthusiasts and beginners",  # Target Audience
        "Conversational",  # Tone
        "The impact of AI on everyday life",  # Main Topic
        "1. Current AI applications\n2. Future possibilities\n3. Ethical considerations",  # Key Points
        "Medium (300-800 words)",  # Content Length
        "AI, machine learning, everyday applications, future tech",  # SEO Keywords
        "Include some real-world examples"  # Additional Instructions
    ]
    
    current_question = 0
    while current_question < len(questions_and_answers):
        answer = questions_and_answers[current_question]
        
        print(f"\n  Answering question {current_question + 1} with: {answer}")
        
        # Send the answer
        payload = {
            "personaId": "synapse",
            "message": answer,
            "promptMode": True,
            "conversationId": conversation_id
        }
        
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ Failed to answer question: {response.status_code}")
            return None
        
        data = response.json()
        
        # If we received the final response, break out of the loop
        if not data['isQuestion']:
            print("\n  ✅ Received final response after questionnaire")
            print(f"  Response: {data['message'][:100]}...")
            
            if data.get('enhancedPrompt'):
                print(f"\n  Enhanced Prompt: {data['enhancedPrompt']}")
            
            return conversation_id
        
        print(f"  Next question: {data['message']}")
        current_question += 1
    
    print("❌ Questionnaire did not complete properly")
    return None

def test_list_templates():
    """Test the list templates endpoint."""
    print("\n🔍 Testing list templates endpoint...")
    
    response = requests.get(f"{BASE_URL}/api/templates", headers=HEADERS)
    
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Found {len(templates)} templates")
        for template in templates:
            print(f"  - {template['name']} ({template['id']}): {template['description']}")
        return True
    else:
        print(f"❌ List templates failed: {response.status_code}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Synapse Backend Validation Tests")
    
    # Test health check
    if not test_health_check():
        print("\n❌ Health check failed. Is the server running?")
        sys.exit(1)
    
    # Test list personas
    test_list_personas()
    
    # Test list templates
    test_list_templates()
    
    # Test normal chat
    normal_conversation_id = test_normal_chat()
    
    # Test prompt mode chat
    prompt_conversation_id = test_prompt_mode_chat()
    
    print("\n🏁 Validation Tests Complete")
    
    if normal_conversation_id and prompt_conversation_id:
        print("✅ All tests passed successfully!")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()

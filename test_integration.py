#!/usr/bin/env python3
"""
Test script to validate the Flask backend integration with validate.py
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class BackendTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test an endpoint and return the response"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return {
                "status_code": response.status_code,
                "response": response.json() if response.content else None,
                "success": response.status_code < 400
            }
        except Exception as e:
            return {
                "status_code": 0,
                "response": str(e),
                "success": False
            }
    
    def run_tests(self):
        """Run all validation tests"""
        print("🧪 Starting Backend Integration Tests...")
        print("=" * 50)
        
        tests = [
            ("GET", "/", "Basic health check"),
            ("GET", "/health", "Health endpoint"),
            ("GET", "/api/personas", "Personas endpoint"),
            ("GET", "/api/templates", "Templates endpoint"),
            ("POST", "/api/chat", "Chat endpoint", {
                "message": "Hello, how are you?",
                "personaId": "synapse"
            }),
            ("POST", "/api/chat", "Chat with prompt mode", {
                "message": "I want to write a blog post",
                "personaId": "synapse",
                "promptMode": True
            }),
            ("GET", "/api/flows", "Flowise flows endpoint"),
            ("GET", "/api/graphs", "LangGraph graphs endpoint"),
            ("POST", "/api/sessions", "Agent orchestrator session", {
                "message": "Test message",
                "mode": "auto"
            })
        ]
        
        results = []
        for test in tests:
            method, endpoint, description = test[:3]
            data = test[3] if len(test) > 3 else None
            
            print(f"\n📋 Testing: {description}")
            print(f"   {method} {endpoint}")
            if data:
                print(f"   Data: {json.dumps(data, indent=2)}")
            
            result = self.test_endpoint(method, endpoint, data)
            results.append({
                "description": description,
                "method": method,
                "endpoint": endpoint,
                "data": data,
                **result
            })
            
            if result["success"]:
                print(f"   ✅ PASS (Status: {result['status_code']})")
            else:
                print(f"   ❌ FAIL (Status: {result['status_code']})")
                if result["response"]:
                    print(f"   Error: {result['response']}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['description']} ({result['method']} {result['endpoint']})")
        
        return passed == total

def wait_for_server(timeout: int = 30):
    """Wait for the server to be ready"""
    print(f"⏳ Waiting for server to start (timeout: {timeout}s)...")
    tester = BackendTester()
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = tester.test_endpoint("GET", "/health")
            if result["success"]:
                print("✅ Server is ready!")
                return True
        except:
            pass
        time.sleep(1)
    
    print("❌ Server did not start within timeout")
    return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Flask backend integration")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for the backend")
    parser.add_argument("--wait", action="store_true", help="Wait for server to start")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout for waiting")
    
    args = parser.parse_args()
    
    if args.wait:
        if not wait_for_server(args.timeout):
            sys.exit(1)
    
    tester = BackendTester(args.url)
    success = tester.run_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)
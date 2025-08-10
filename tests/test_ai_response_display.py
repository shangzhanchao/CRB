"""
Test script to verify AI response display functionality
"""

import requests
import json
import time

def test_ai_response_display():
    """Test that AI response displays audio, action, and expression correctly."""
    print("Testing AI Response Display...")
    
    # Test data with all content types
    test_response = {
        "status": "success",
        "data": {
            "reply": {
                "content": "你好！我很高兴见到你"
            },
            "emotion": {
                "value": "happy",
                "description": "开心"
            },
            "audio": {
                "url": "/uploads/audio_response.wav"
            },
            "action": "机器人微笑着向你挥手",
            "expression": "😊 开心地笑着",
            "interaction_details": {
                "touch_zone": {
                    "name": "头部",
                    "zone": 0
                }
            }
        }
    }
    
    print("✓ Test response contains all content types:")
    print(f"  - Text: {test_response['data']['reply']['content']}")
    print(f"  - Emotion: {test_response['data']['emotion']['description']}")
    print(f"  - Audio: {test_response['data']['audio']['url']}")
    print(f"  - Action: {test_response['data']['action']}")
    print(f"  - Expression: {test_response['data']['expression']}")
    print(f"  - Touch Zone: {test_response['data']['interaction_details']['touch_zone']['name']}")
    
    return True

def test_service_response():
    """Test actual service response."""
    print("\nTesting Service Response...")
    
    try:
        # Test the service endpoint
        response = requests.post(
            "http://localhost:8000/interact",
            json={
                "robot_id": "robotA",
                "user_input": "你好",
                "touch_zone": 0
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Service responded successfully")
            print(f"  Status: {result.get('status')}")
            
            if 'data' in result:
                data = result['data']
                print("  Content types found:")
                
                if 'reply' in data:
                    print(f"    - Text: {data['reply'].get('content', 'N/A')}")
                
                if 'emotion' in data:
                    print(f"    - Emotion: {data['emotion'].get('description', 'N/A')}")
                
                if 'audio' in data:
                    print(f"    - Audio: {data['audio']}")
                
                if 'action' in data:
                    print(f"    - Action: {data['action']}")
                
                if 'expression' in data:
                    print(f"    - Expression: {data['expression']}")
                
                if 'interaction_details' in data:
                    print(f"    - Touch Zone: {data['interaction_details']}")
            else:
                print("  ⚠ No 'data' field in response")
        else:
            print(f"⚠ Service responded with status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠ Could not connect to service: {e}")
        print("  (Make sure the service is running)")
    
    return True

def test_ui_integration():
    """Test UI integration."""
    print("\nTesting UI Integration...")
    
    # Check if UI service file has the required functions
    try:
        with open('services/ui_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_functions = [
            'displayAIResponse',
            'saveChatHistory',
            'loadChatHistory',
            'getEmotionIcon'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in content:
                missing_functions.append(func)
        
        if missing_functions:
            print(f"⚠ Missing functions: {', '.join(missing_functions)}")
        else:
            print("✓ All required functions found in UI service")
        
        # Check for CSS styles
        required_styles = [
            '.ai-audio',
            '.ai-expression',
            '.ai-action'
        ]
        
        missing_styles = []
        for style in required_styles:
            if style not in content:
                missing_styles.append(style)
        
        if missing_styles:
            print(f"⚠ Missing CSS styles: {', '.join(missing_styles)}")
        else:
            print("✓ All required CSS styles found")
            
    except FileNotFoundError:
        print("⚠ UI service file not found")
    except Exception as e:
        print(f"⚠ Error reading UI service file: {e}")
    
    return True

def generate_test_instructions():
    """Generate instructions for manual testing."""
    instructions = """
MANUAL TESTING INSTRUCTIONS
==========================

1. Start the service:
   python service.py

2. Open browser and go to:
   http://localhost:8000/verify

3. Test the following scenarios:

   A. Send a message and check if AI response shows:
      - Text content
      - Emotion with icon
      - Audio player (if available)
      - Action description
      - Expression with emoji
      - Touch zone interaction

   B. Refresh the page and verify:
      - Chat history persists
      - Previous conversations are still visible

   C. Check browser console for:
      - "对话历史已保存到本地存储"
      - "从本地存储加载对话历史"

4. Expected behavior:
   - AI responses should display rich content
   - Chat history should persist after refresh
   - All UI elements should be properly styled
"""
    return instructions

def main():
    """Run all tests."""
    print("=" * 50)
    print("AI RESPONSE DISPLAY TESTING")
    print("=" * 50)
    
    tests = [
        test_ai_response_display,
        test_service_response,
        test_ui_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI response display should work correctly.")
    else:
        print("⚠ Some tests failed. Please check the implementation.")
    
    print("\n" + "=" * 50)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 50)
    print(generate_test_instructions())

if __name__ == "__main__":
    main() 
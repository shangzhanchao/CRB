#!/usr/bin/env python3
"""Test UI interaction issues"""

import requests
import json
import time

def test_ui_page_content():
    """Test UI page content and structure"""
    try:
        response = requests.get('http://127.0.0.1:8000/verify')
        print(f"✅ UI page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for critical UI elements
            critical_elements = [
                ('sendMessage()', 'Send message function'),
                ('selectTouchZone(', 'Touch zone selection function'),
                ('main-action', 'Main action button styling'),
                ('touch-zones', 'Touch zones container'),
                ('onclick="sendMessage()"', 'Send message button click handler'),
                ('onclick="selectTouchZone(', 'Touch zone click handlers'),
                ('selectedTouchZone', 'Touch zone variable'),
                ('formData.append(\'touch_zone\'', 'Touch zone form data'),
                ('startRecording(', 'Recording functions'),
                ('stopRecording(', 'Stop recording function')
            ]
            
            missing_elements = []
            for element, description in critical_elements:
                if element not in content:
                    missing_elements.append(description)
                else:
                    print(f"   ✅ {description} found")
            
            if missing_elements:
                print(f"\n❌ Missing critical elements:")
                for element in missing_elements:
                    print(f"   - {element}")
                return False
            else:
                print(f"\n✅ All critical UI elements present")
                return True
        else:
            print(f"❌ UI page failed to load: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        return False

def test_javascript_functions():
    """Test if JavaScript functions are properly defined"""
    try:
        response = requests.get('http://127.0.0.1:8000/verify')
        content = response.text
        
        # Extract JavaScript functions
        js_functions = [
            'function sendMessage()',
            'function selectTouchZone(',
            'function startRecording(',
            'function stopRecording(',
            'function startSession(',
            'function clearSession(',
            'function getMemoryStats(',
            'function clearMemory('
        ]
        
        missing_functions = []
        for func in js_functions:
            if func not in content:
                missing_functions.append(func)
            else:
                print(f"   ✅ {func} found")
        
        if missing_functions:
            print(f"\n❌ Missing JavaScript functions:")
            for func in missing_functions:
                print(f"   - {func}")
            return False
        else:
            print(f"\n✅ All JavaScript functions present")
            return True
            
    except Exception as e:
        print(f"❌ JavaScript test failed: {e}")
        return False

def test_form_data_handling():
    """Test if form data is properly handled"""
    try:
        # Test with touch zone parameter
        data = {
            'robot_id': 'robotA',
            'user_input': 'Test message with touch zone',
            'touch_zone': '2',
            'session_id': ''
        }
        
        response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Form data handling: {response.status_code}")
            print(f"   Success: {result.get('success')}")
            print(f"   Reply: {result.get('reply', '')[:50]}...")
            print(f"   Session ID: {result.get('session_id')}")
            return True
        else:
            print(f"❌ Form data handling failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Form data test failed: {e}")
        return False

def test_recording_api_integration():
    """Test recording API integration"""
    try:
        # Test start recording
        start_data = {
            'recording_type': 'audio',
            'robot_id': 'robotA',
            'session_id': ''
        }
        
        response = requests.post('http://127.0.0.1:8000/start_recording', json=start_data)
        
        if response.status_code == 200:
            result = response.json()
            recording_id = result.get('recording_id')
            print(f"✅ Recording start: {response.status_code}")
            print(f"   Recording ID: {recording_id}")
            
            # Test stop recording
            if recording_id:
                stop_data = {'recording_id': recording_id}
                stop_response = requests.post('http://127.0.0.1:8000/stop_recording', json=stop_data)
                
                if stop_response.status_code == 200:
                    stop_result = stop_response.json()
                    print(f"✅ Recording stop: {stop_response.status_code}")
                    print(f"   Duration: {stop_result.get('duration', 0):.2f}s")
                    return True
                else:
                    print(f"❌ Recording stop failed: {stop_response.status_code}")
                    return False
            else:
                print(f"❌ No recording ID returned")
                return False
        else:
            print(f"❌ Recording start failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Recording integration test failed: {e}")
        return False

def main():
    """Run UI interaction tests"""
    print("🔍 Testing UI interaction issues...")
    print("=" * 50)
    
    tests = [
        ("UI Page Content", test_ui_page_content),
        ("JavaScript Functions", test_javascript_functions),
        ("Form Data Handling", test_form_data_handling),
        ("Recording API Integration", test_recording_api_integration)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        print("-" * 30)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("📊 UI Test Results:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} UI tests passed")
    
    if passed < total:
        print("\n🚨 UI Issues identified:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name} has problems")
    
    return passed == total

if __name__ == "__main__":
    main() 
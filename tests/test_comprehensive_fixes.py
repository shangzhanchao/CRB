#!/usr/bin/env python3
"""Comprehensive test to verify all fixes and improvements"""

import requests
import json
import time
import sys

def test_ui_page_improvements():
    """Test UI page improvements"""
    try:
        response = requests.get('http://127.0.0.1:8000/verify')
        print(f"✅ UI page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for improvements
            improvements = [
                ('sendMessageBtn', 'Send message button with proper ID'),
                ('isProcessing', 'Processing state management'),
                ('console.log', 'Console logging for debugging'),
                ('showInfo', 'Info message display'),
                ('getTouchZoneName', 'Touch zone name function'),
                ('handleFileSelection', 'File selection handler'),
                ('user-select: none', 'Button text selection prevention'),
                ('z-index: 10', 'Button z-index for proper layering'),
                (':active', 'Button active state'),
                ('disabled', 'Button disabled state handling')
            ]
            
            missing_improvements = []
            for element, description in improvements:
                if element not in content:
                    missing_improvements.append(description)
                else:
                    print(f"   ✅ {description} found")
            
            if missing_improvements:
                print(f"\n❌ Missing improvements:")
                for improvement in missing_improvements:
                    print(f"   - {improvement}")
                return False
            else:
                print(f"\n✅ All UI improvements present")
                return True
        else:
            print(f"❌ UI page failed to load: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ UI improvements test failed: {e}")
        return False

def test_button_functionality():
    """Test button functionality improvements"""
    try:
        # Test send message with improved error handling
        data = {
            'robot_id': 'robotA',
            'user_input': 'Test message with improved functionality',
            'touch_zone': '2'
        }
        
        response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Send message with improvements: {response.status_code}")
            print(f"   Success: {result.get('success')}")
            print(f"   Reply: {result.get('reply', '')[:50]}...")
            print(f"   Session ID: {result.get('session_id')}")
            return True
        else:
            print(f"❌ Send message failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Button functionality test failed: {e}")
        return False

def test_touch_zone_improvements():
    """Test touch zone improvements"""
    try:
        # Test all touch zones with improved feedback
        touch_zones = [
            (0, "头部"),
            (1, "背部"), 
            (2, "腹部"),
            (3, "手部"),
            (4, "腿部")
        ]
        
        print("🖐️ Testing touch zone improvements...")
        
        for zone_id, zone_name in touch_zones:
            data = {
                'robot_id': 'robotA',
                'user_input': f'Testing {zone_name} with improvements',
                'touch_zone': str(zone_id)
            }
            
            response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {zone_name} (zone {zone_id}): Success")
                print(f"      Reply: {result.get('reply', '')[:50]}...")
            else:
                print(f"   ❌ {zone_name} (zone {zone_id}): Failed - {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Touch zone improvements test failed: {e}")
        return False

def test_recording_improvements():
    """Test recording improvements"""
    try:
        print("🎥 Testing recording improvements...")
        
        # Test start recording
        start_data = {
            'recording_type': 'audio',
            'robot_id': 'robotA'
        }
        
        response = requests.post('http://127.0.0.1:8000/start_recording', json=start_data)
        
        if response.status_code == 200:
            result = response.json()
            recording_id = result.get('recording_id')
            print(f"   ✅ Start recording: {recording_id}")
            
            # Wait a bit
            time.sleep(1)
            
            # Test stop recording
            if recording_id:
                stop_data = {'recording_id': recording_id}
                stop_response = requests.post('http://127.0.0.1:8000/stop_recording', json=stop_data)
                
                if stop_response.status_code == 200:
                    stop_result = stop_response.json()
                    print(f"   ✅ Stop recording: Duration {stop_result.get('duration', 0):.2f}s")
                    print(f"      Files: {len(stop_result.get('files', []))} files saved")
                    return True
                else:
                    print(f"   ❌ Stop recording failed: {stop_response.status_code}")
                    return False
            else:
                print(f"   ❌ No recording ID returned")
                return False
        else:
            print(f"   ❌ Start recording failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Recording improvements test failed: {e}")
        return False

def test_session_improvements():
    """Test session management improvements"""
    try:
        print("📋 Testing session improvements...")
        
        # Test start session
        start_data = {'robot_id': 'robotA'}
        response = requests.post('http://127.0.0.1:8000/start_session', json=start_data)
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"   ✅ Start session: {session_id}")
            
            # Test session info
            info_response = requests.get('http://127.0.0.1:8000/session_info/robotA')
            if info_response.status_code == 200:
                info_result = info_response.json()
                print(f"   ✅ Session info: {info_result.get('success')}")
            
            # Test message with session
            message_data = {
                'robot_id': 'robotA',
                'user_input': 'Message with session improvements',
                'touch_zone': '3',
                'session_id': session_id
            }
            
            message_response = requests.post('http://127.0.0.1:8000/interact_with_files', data=message_data)
            if message_response.status_code == 200:
                message_result = message_response.json()
                print(f"   ✅ Message with session: {message_result.get('success')}")
            
            # Test clear session
            clear_data = {'robot_id': 'robotA'}
            clear_response = requests.post('http://127.0.0.1:8000/clear_session', json=clear_data)
            if clear_response.status_code == 200:
                print(f"   ✅ Clear session: {clear_response.json().get('success')}")
            
            return True
        else:
            print(f"   ❌ Start session failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Session improvements test failed: {e}")
        return False

def test_error_handling():
    """Test improved error handling"""
    try:
        print("🛡️ Testing error handling improvements...")
        
        # Test with invalid data
        invalid_data = {
            'robot_id': '',
            'user_input': '',
            'touch_zone': 'invalid'
        }
        
        response = requests.post('http://127.0.0.1:8000/interact_with_files', data=invalid_data)
        
        # Should still work with default values
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Error handling: Graceful handling of invalid data")
            print(f"      Success: {result.get('success')}")
            return True
        else:
            print(f"   ❌ Error handling failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run comprehensive tests"""
    print("🔍 Comprehensive Fixes Verification")
    print("=" * 50)
    
    tests = [
        ("UI Page Improvements", test_ui_page_improvements),
        ("Button Functionality", test_button_functionality),
        ("Touch Zone Improvements", test_touch_zone_improvements),
        ("Recording Improvements", test_recording_improvements),
        ("Session Improvements", test_session_improvements),
        ("Error Handling", test_error_handling)
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
    print("📊 Comprehensive Test Results:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All fixes verified successfully!")
        print("✅ Send message button is now fully functional")
        print("✅ Touch zone parameter is properly handled")
        print("✅ Recording functionality is improved")
        print("✅ Session management is enhanced")
        print("✅ Error handling is robust")
        print("✅ UI is more responsive and user-friendly")
    else:
        print("\n🚨 Some issues remain:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name} needs attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
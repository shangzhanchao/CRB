#!/usr/bin/env python3
"""Test script to identify current issues with the service"""

import requests
import json
import time
import sys

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get('http://127.0.0.1:8000/health')
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_send_message():
    """Test send message functionality"""
    try:
        data = {
            'robot_id': 'robotA',
            'user_input': 'Hello, this is a test message',
            'touch_zone': '1'
        }
        response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
        print(f"✅ Send message: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success')}")
            print(f"   Reply: {result.get('reply', '')[:100]}...")
            print(f"   Session ID: {result.get('session_id')}")
        else:
            print(f"   Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Send message failed: {e}")
        return False

def test_touch_zone_parameter():
    """Test touch zone parameter handling"""
    try:
        # Test different touch zones
        for zone in [0, 1, 2, 3, 4]:
            data = {
                'robot_id': 'robotA',
                'user_input': f'Test touch zone {zone}',
                'touch_zone': str(zone)
            }
            response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
            print(f"✅ Touch zone {zone}: {response.status_code}")
            if response.status_code != 200:
                print(f"   Error: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Touch zone test failed: {e}")
        return False

def test_recording_functionality():
    """Test recording functionality"""
    try:
        # Test start recording
        data = {
            'recording_type': 'audio',
            'robot_id': 'robotA'
        }
        response = requests.post('http://127.0.0.1:8000/start_recording', json=data)
        print(f"✅ Start recording: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            recording_id = result.get('recording_id')
            print(f"   Recording ID: {recording_id}")
            
            # Test stop recording
            if recording_id:
                stop_data = {'recording_id': recording_id}
                stop_response = requests.post('http://127.0.0.1:8000/stop_recording', json=stop_data)
                print(f"✅ Stop recording: {stop_response.status_code}")
                if stop_response.status_code == 200:
                    print(f"   Stop result: {stop_response.json()}")
        else:
            print(f"   Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Recording test failed: {e}")
        return False

def test_session_management():
    """Test session management"""
    try:
        # Test start session
        data = {'robot_id': 'robotA'}
        response = requests.post('http://127.0.0.1:8000/start_session', json=data)
        print(f"✅ Start session: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Session result: {result}")
            
            # Test session info
            info_response = requests.get('http://127.0.0.1:8000/session_info/robotA')
            print(f"✅ Session info: {info_response.status_code}")
            if info_response.status_code == 200:
                print(f"   Info: {info_response.json()}")
        else:
            print(f"   Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Session test failed: {e}")
        return False

def test_ui_page():
    """Test UI page loading"""
    try:
        response = requests.get('http://127.0.0.1:8000/verify')
        print(f"✅ UI page: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            # Check for key UI elements
            checks = [
                ('发送消息', 'Send message button'),
                ('抚摸区域', 'Touch zone section'),
                ('录音', 'Audio recording'),
                ('录像', 'Video recording'),
                ('main-action', 'Main action button class'),
                ('touch-zones', 'Touch zones container')
            ]
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} found")
                else:
                    print(f"   ❌ {description} missing")
        else:
            print(f"   Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ UI page test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Testing current service issues...")
    print("=" * 50)
    
    # Wait for service to start
    print("⏳ Waiting for service to start...")
    time.sleep(3)
    
    tests = [
        ("Health Check", test_health),
        ("Send Message", test_send_message),
        ("Touch Zone Parameter", test_touch_zone_parameter),
        ("Recording Functionality", test_recording_functionality),
        ("Session Management", test_session_management),
        ("UI Page", test_ui_page)
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
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed < total:
        print("\n🚨 Issues identified:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name} is not working properly")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
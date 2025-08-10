#!/usr/bin/env python3
"""Simulate browser interactions to identify issues"""

import requests
import json
import time

def simulate_send_message_click():
    """Simulate clicking the send message button"""
    try:
        # Simulate the exact form data that would be sent when clicking send message
        data = {
            'robot_id': 'robotA',
            'user_input': 'Test message from browser simulation',
            'touch_zone': '1',  # Simulate selecting touch zone 1
            'session_id': ''
        }
        
        print("🖱️ Simulating send message button click...")
        response = requests.post('http://127.0.0.1:8000/interact_with_files', data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Send message simulation successful")
            print(f"   Success: {result.get('success')}")
            print(f"   Reply: {result.get('reply', '')[:100]}...")
            print(f"   Session ID: {result.get('session_id')}")
            return True
        else:
            print(f"❌ Send message simulation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Send message simulation error: {e}")
        return False

def simulate_touch_zone_selection():
    """Simulate selecting different touch zones"""
    try:
        touch_zones = [
            (0, "头部"),
            (1, "背部"), 
            (2, "腹部"),
            (3, "手部"),
            (4, "腿部")
        ]
        
        print("🖐️ Simulating touch zone selections...")
        
        for zone_id, zone_name in touch_zones:
            data = {
                'robot_id': 'robotA',
                'user_input': f'Testing {zone_name} touch zone',
                'touch_zone': str(zone_id),
                'session_id': ''
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
        print(f"❌ Touch zone simulation error: {e}")
        return False

def simulate_recording_workflow():
    """Simulate the complete recording workflow"""
    try:
        print("🎥 Simulating recording workflow...")
        
        # Step 1: Start recording
        start_data = {
            'recording_type': 'audio',
            'robot_id': 'robotA',
            'session_id': ''
        }
        
        response = requests.post('http://127.0.0.1:8000/start_recording', json=start_data)
        
        if response.status_code == 200:
            result = response.json()
            recording_id = result.get('recording_id')
            print(f"   ✅ Start recording: {recording_id}")
            
            # Step 2: Wait a bit (simulate recording time)
            time.sleep(1)
            
            # Step 3: Stop recording
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
        print(f"❌ Recording workflow simulation error: {e}")
        return False

def simulate_session_management():
    """Simulate session management workflow"""
    try:
        print("📋 Simulating session management...")
        
        # Step 1: Start session
        start_data = {'robot_id': 'robotA'}
        response = requests.post('http://127.0.0.1:8000/start_session', json=start_data)
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"   ✅ Start session: {session_id}")
            
            # Step 2: Get session info
            info_response = requests.get('http://127.0.0.1:8000/session_info/robotA')
            if info_response.status_code == 200:
                info_result = info_response.json()
                print(f"   ✅ Session info: {info_result.get('success')}")
            
            # Step 3: Send message with session
            message_data = {
                'robot_id': 'robotA',
                'user_input': 'Message with active session',
                'touch_zone': '2',
                'session_id': session_id
            }
            
            message_response = requests.post('http://127.0.0.1:8000/interact_with_files', data=message_data)
            if message_response.status_code == 200:
                message_result = message_response.json()
                print(f"   ✅ Message with session: {message_result.get('success')}")
            
            # Step 4: Clear session
            clear_data = {'robot_id': 'robotA'}
            clear_response = requests.post('http://127.0.0.1:8000/clear_session', json=clear_data)
            if clear_response.status_code == 200:
                print(f"   ✅ Clear session: {clear_response.json().get('success')}")
            
            return True
        else:
            print(f"   ❌ Start session failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Session management simulation error: {e}")
        return False

def check_ui_issues():
    """Check for potential UI issues"""
    try:
        print("🔍 Checking for potential UI issues...")
        
        # Get the UI page
        response = requests.get('http://127.0.0.1:8000/verify')
        content = response.text
        
        # Check for potential issues
        issues = []
        
        # Check if sendMessage function has proper error handling
        if 'try {' in content and 'catch (error)' in content:
            print("   ✅ Error handling in sendMessage function")
        else:
            issues.append("Missing error handling in sendMessage")
        
        # Check if touch zone selection is properly initialized
        if 'selectTouchZone(0)' in content:
            print("   ✅ Touch zone default selection")
        else:
            issues.append("Missing default touch zone selection")
        
        # Check if form validation is present
        if 'userInput.trim()' in content:
            print("   ✅ Form validation present")
        else:
            issues.append("Missing form validation")
        
        # Check if loading states are handled
        if 'showLoading(true)' in content and 'showLoading(false)' in content:
            print("   ✅ Loading states handled")
        else:
            issues.append("Missing loading state handling")
        
        # Check if recording functions have proper cleanup
        if 'getTracks().forEach(track => track.stop())' in content:
            print("   ✅ Recording cleanup present")
        else:
            issues.append("Missing recording cleanup")
        
        if issues:
            print(f"\n❌ Potential UI issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print(f"\n✅ No obvious UI issues detected")
            return True
            
    except Exception as e:
        print(f"❌ UI issue check failed: {e}")
        return False

def main():
    """Run browser simulation tests"""
    print("🖥️ Browser Simulation Tests")
    print("=" * 50)
    
    tests = [
        ("Send Message Click", simulate_send_message_click),
        ("Touch Zone Selection", simulate_touch_zone_selection),
        ("Recording Workflow", simulate_recording_workflow),
        ("Session Management", simulate_session_management),
        ("UI Issues Check", check_ui_issues)
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
    print("📊 Browser Simulation Results:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} browser simulations passed")
    
    if passed < total:
        print("\n🚨 Browser interaction issues identified:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name} has problems")
    
    return passed == total

if __name__ == "__main__":
    main() 
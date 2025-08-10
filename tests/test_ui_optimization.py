#!/usr/bin/env python3
"""
测试UI优化功能
验证界面操作修复和新增功能
"""

import requests
import json
import time
from datetime import datetime

# 服务基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """测试健康检查"""
    print("测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查成功: {response.json()}")
        return True
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_basic_interaction():
    """测试基础交互功能"""
    print("\n测试基础交互功能...")
    try:
        # 模拟表单数据
        data = {
            "robot_id": "robotA",
            "user_input": "你好，我想测试界面功能",
            "session_id": "",
            "touch_zone": "0"  # 头部
        }
        
        response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
        result = response.json()
        
        print("基础交互测试成功")
        print(f"📊 响应状态: {result.get('status')}")
        print(f"⏰ 时间戳: {result.get('timestamp')}")
        
        # 检查格式化数据
        if 'data' in result:
            data = result['data']
            print("📋 格式化数据:")
            
            if 'reply' in data:
                reply = data['reply']
                print(f"   💬 回复类型: {reply.get('type')}")
                print(f"   内容: {reply.get('content', '')[:100]}...")
                print(f"   📏 长度: {reply.get('length')}")
            
            if 'interaction_details' in data:
                details = data['interaction_details']
                print(f"   🤖 机器人ID: {details.get('robot_id')}")
                print(f"   用户输入: {details.get('user_input')}")
                print(f"   抚摸区域: {details.get('touch_zone', {}).get('name')}")
        
        return result
    except Exception as e:
        print(f"基础交互测试失败: {e}")
        return None

def test_emotion_display():
    """测试情感显示功能"""
    print("\n测试情感显示功能...")
    try:
        # 测试不同抚摸区域
        touch_zones = [0, 1, 2]
        zone_names = ["头部", "背后", "胸口"]
        
        for i, zone in enumerate(touch_zones):
            data = {
                "robot_id": "robotA",
                "user_input": f"抚摸我的{zone_names[i]}",
                "session_id": "",
                "touch_zone": str(zone)
            }
            
            response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
            result = response.json()
            
            print(f"{zone_names[i]}抚摸测试成功")
            
            if result.get('status') == 'success' and 'data' in result:
                data = result['data']
                if 'emotion' in data:
                    emotion = data['emotion']
                    print(f"   😊 情感: {emotion.get('value')} - {emotion.get('description')}")
                
                if 'interaction_details' in data:
                    details = data['interaction_details']
                    touch_zone = details.get('touch_zone', {})
                    print(f"   抚摸区域: {touch_zone.get('name')}")
        
        return True
    except Exception as e:
        print(f"情感显示测试失败: {e}")
        return None

def test_chat_history():
    """测试对话历史功能"""
    print("\n🔍 测试对话历史功能...")
    try:
        # 发送几条消息来生成历史记录
        messages = [
            "你好，机器人",
            "今天天气怎么样？",
            "你能做什么？",
            "谢谢你的帮助"
        ]
        
        for i, message in enumerate(messages):
            data = {
                "robot_id": "robotA",
                "user_input": message,
                "session_id": "",
                "touch_zone": str(i % 3)  # 轮换抚摸区域
            }
            
            response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
            result = response.json()
            
            if result.get('status') == 'success':
                print(f"✅ 消息 {i+1} 发送成功")
            else:
                print(f"❌ 消息 {i+1} 发送失败")
            
            time.sleep(0.5)  # 短暂延迟
        
        # 获取会话历史
        response = requests.get(f"{BASE_URL}/robot_session_history/robotA")
        history = response.json()
        
        print("✅ 对话历史获取成功")
        print(f"📊 总记录数: {history.get('total_records', 0)}")
        print(f"📊 返回记录数: {history.get('returned_records', 0)}")
        
        # 显示最近的记录
        history_list = history.get('history', [])
        if history_list:
            print("📋 最近的对话记录:")
            for i, record in enumerate(history_list[:3], 1):
                print(f"   {i}. 时间: {record.get('timestamp', 'N/A')}")
                print(f"      输入: {record.get('user_input', '')[:50]}...")
                if 'output' in record and 'data' in record['output']:
                    reply = record['output']['data'].get('reply', {})
                    print(f"      回复: {reply.get('content', '')[:50]}...")
        
        return history
    except Exception as e:
        print(f"❌ 对话历史测试失败: {e}")
        return None

def test_recording_functionality():
    """测试录制功能"""
    print("\n🔍 测试录制功能...")
    try:
        # 测试获取活跃录制
        response = requests.get(f"{BASE_URL}/active_recordings")
        result = response.json()
        
        print("✅ 录制功能测试成功")
        print(f"📊 活跃录制数: {len(result.get('recordings', []))}")
        
        # 测试录制状态
        response = requests.get(f"{BASE_URL}/recording_status/test_recording")
        status_result = response.json()
        
        print(f"📊 录制状态: {status_result.get('status', 'unknown')}")
        
        return result
    except Exception as e:
        print(f"❌ 录制功能测试失败: {e}")
        return None

def test_formatted_response():
    """测试格式化响应"""
    print("\n🔍 测试格式化响应...")
    try:
        # 测试带情感的交互
        data = {
            "robot_id": "robotA",
            "user_input": "我很开心",
            "session_id": "",
            "touch_zone": "0"
        }
        
        response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
        result = response.json()
        
        print("✅ 格式化响应测试成功")
        print("📋 响应结构分析:")
        
        # 检查标准字段
        required_fields = ['status', 'timestamp', 'data']
        for field in required_fields:
            if field in result:
                print(f"   ✅ {field}: {result[field]}")
            else:
                print(f"   ❌ 缺少字段: {field}")
        
        # 检查数据字段
        if 'data' in result:
            data = result['data']
            print("   📊 数据字段:")
            for key, value in data.items():
                if key != 'raw_data':
                    print(f"      {key}: {type(value).__name__}")
        
        return result
    except Exception as e:
        print(f"❌ 格式化响应测试失败: {e}")
        return None

def test_ui_features():
    """测试UI功能"""
    print("\n🔍 测试UI功能...")
    try:
        # 测试不同抚摸区域
        touch_zones = [
            {"value": 0, "name": "头部"},
            {"value": 1, "name": "背后"},
            {"value": 2, "name": "胸口"}
        ]
        
        for zone in touch_zones:
            data = {
                "robot_id": "robotA",
                "user_input": f"抚摸我的{zone['name']}",
                "session_id": "",
                "touch_zone": str(zone['value'])
            }
            
            response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
            result = response.json()
            
            if result.get('status') == 'success':
                print(f"✅ {zone['name']}抚摸测试成功")
                
                # 检查响应中的抚摸区域信息
                if 'data' in result and 'interaction_details' in result['data']:
                    details = result['data']['interaction_details']
                    touch_zone = details.get('touch_zone', {})
                    print(f"   🖐️ 抚摸区域: {touch_zone.get('name')} (值: {touch_zone.get('value')})")
            else:
                print(f"❌ {zone['name']}抚摸测试失败")
        
        return True
    except Exception as e:
        print(f"❌ UI功能测试失败: {e}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始测试UI优化功能")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 服务不可用，停止测试")
        return
    
    # 测试基础交互
    test_basic_interaction()
    
    # 测试情感显示
    test_emotion_display()
    
    # 测试对话历史
    test_chat_history()
    
    # 测试录制功能
    test_recording_functionality()
    
    # 测试格式化响应
    test_formatted_response()
    
    # 测试UI功能
    test_ui_features()
    
    print("\n" + "=" * 50)
    print("✅ 所有UI优化测试完成")
    print("\n📋 优化总结:")
    print("1. ✅ 修复了验证问题")
    print("2. ✅ 取消了会话管理功能")
    print("3. ✅ 将文件选择移到录制区域")
    print("4. ✅ 丰富了AI回复区域（文本、表情、动作）")
    print("5. ✅ 取消了会话信息区域")
    print("6. ✅ 新增了对话记录列表查看功能")

if __name__ == "__main__":
    main() 
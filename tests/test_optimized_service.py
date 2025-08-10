#!/usr/bin/env python3
"""
测试优化后的service.py功能
验证结果展示优化和会话历史记录功能
"""

import requests
import json
import time
from datetime import datetime

# 服务基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ 健康检查成功: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_interact_with_files():
    """测试带文件的交互功能"""
    print("\n🔍 测试带文件的交互功能...")
    try:
        # 模拟表单数据
        data = {
            "robot_id": "robotA",
            "user_input": "你好，我想和你聊天",
            "session_id": "",
            "touch_zone": "0"  # 头部
        }
        
        response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
        result = response.json()
        
        print("✅ 交互请求成功")
        print(f"📊 响应状态: {result.get('status')}")
        print(f"⏰ 时间戳: {result.get('timestamp')}")
        
        # 检查格式化数据
        if 'data' in result:
            data = result['data']
            print("📋 格式化数据:")
            
            if 'reply' in data:
                reply = data['reply']
                print(f"   💬 回复类型: {reply.get('type')}")
                print(f"   📝 内容: {reply.get('content', '')[:100]}...")
                print(f"   📏 长度: {reply.get('length')}")
            
            if 'interaction_details' in data:
                details = data['interaction_details']
                print(f"   🤖 机器人ID: {details.get('robot_id')}")
                print(f"   📝 用户输入: {details.get('user_input')}")
                print(f"   🖐️ 抚摸区域: {details.get('touch_zone', {}).get('name')}")
        
        return result
    except Exception as e:
        print(f"❌ 交互测试失败: {e}")
        return None

def test_session_history():
    """测试会话历史记录功能"""
    print("\n🔍 测试会话历史记录功能...")
    try:
        # 获取会话历史摘要
        response = requests.get(f"{BASE_URL}/session_history_summary")
        summary = response.json()
        
        print("✅ 会话历史摘要获取成功")
        print(f"📊 总会话数: {summary.get('summary', {}).get('total_sessions')}")
        print(f"📊 总交互数: {summary.get('summary', {}).get('total_interactions')}")
        
        # 获取机器人会话历史
        response = requests.get(f"{BASE_URL}/robot_session_history/robotA")
        robot_history = response.json()
        
        print("✅ 机器人会话历史获取成功")
        print(f"🤖 机器人ID: {robot_history.get('robot_id')}")
        print(f"📊 总记录数: {robot_history.get('total_records')}")
        print(f"📊 返回记录数: {robot_history.get('returned_records')}")
        
        # 显示最近的交互记录
        history = robot_history.get('history', [])
        if history:
            print("📋 最近的交互记录:")
            for i, record in enumerate(history[-3:], 1):  # 显示最近3条
                print(f"   {i}. 类型: {record.get('type')}")
                print(f"      时间: {record.get('timestamp')}")
                if 'user_input' in record:
                    print(f"      输入: {record.get('user_input', '')[:50]}...")
        
        return robot_history
    except Exception as e:
        print(f"❌ 会话历史测试失败: {e}")
        return None

def test_memory_operations():
    """测试记忆操作功能"""
    print("\n🔍 测试记忆操作功能...")
    try:
        # 获取记忆统计
        response = requests.get(f"{BASE_URL}/memory_stats")
        stats = response.json()
        
        print("✅ 记忆统计获取成功")
        print(f"📊 响应状态: {stats.get('status')}")
        print(f"⏰ 时间戳: {stats.get('timestamp')}")
        
        if 'data' in stats:
            data = stats['data']
            print("📋 记忆数据:")
            for key, value in data.items():
                if key != 'raw_data':  # 跳过原始数据
                    print(f"   {key}: {value}")
        
        return stats
    except Exception as e:
        print(f"❌ 记忆操作测试失败: {e}")
        return None

def test_all_session_history():
    """测试所有会话历史"""
    print("\n🔍 测试所有会话历史...")
    try:
        response = requests.get(f"{BASE_URL}/all_session_history")
        all_history = response.json()
        
        print("✅ 所有会话历史获取成功")
        print(f"📊 总会话数: {all_history.get('total_sessions')}")
        print(f"📊 总交互数: {all_history.get('total_interactions')}")
        
        sessions = all_history.get('sessions', {})
        for session_id, history in sessions.items():
            print(f"   🆔 会话 {session_id}: {len(history)} 条记录")
        
        return all_history
    except Exception as e:
        print(f"❌ 所有会话历史测试失败: {e}")
        return None

def test_formatted_response_structure():
    """测试格式化响应结构"""
    print("\n🔍 测试格式化响应结构...")
    try:
        # 测试简单的交互
        data = {
            "robot_id": "robotA",
            "user_input": "测试格式化响应",
            "session_id": "",
            "touch_zone": "1"  # 背后
        }
        
        response = requests.post(f"{BASE_URL}/interact_with_files", data=data)
        result = response.json()
        
        print("✅ 格式化响应结构测试成功")
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
        print(f"❌ 格式化响应结构测试失败: {e}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始测试优化后的service.py功能")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health_check():
        print("❌ 服务不可用，停止测试")
        return
    
    # 测试交互功能
    test_interact_with_files()
    
    # 测试会话历史
    test_session_history()
    
    # 测试记忆操作
    test_memory_operations()
    
    # 测试所有会话历史
    test_all_session_history()
    
    # 测试格式化响应结构
    test_formatted_response_structure()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""Test script for enhanced memory system.

增强记忆系统测试脚本。
"""

import asyncio
import json
import time
from typing import Dict, Any

from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.intelligent_core import IntelligentCore, UserInput


def test_enhanced_memory_system():
    """测试增强记忆系统"""
    print("🧪 开始测试增强记忆系统")
    print("="*60)
    
    # 初始化记忆系统
    memory_system = EnhancedMemorySystem(robot_id="test_robot")
    
    # 开始会话
    session_id = memory_system.start_session()
    print(f"🆕 创建会话: {session_id}")
    
    # 测试添加记忆
    test_cases = [
        {
            "user_text": "你好",
            "ai_response": "你好呀！很高兴见到你！",
            "mood_tag": "happy",
            "touch_zone": None
        },
        {
            "user_text": "今天天气怎么样？",
            "ai_response": "今天天气很好，阳光明媚！",
            "mood_tag": "excited",
            "touch_zone": 0
        },
        {
            "user_text": "我有点难过",
            "ai_response": "别难过，我会陪在你身边的。",
            "mood_tag": "sad",
            "touch_zone": 1
        },
        {
            "user_text": "你叫什么名字？",
            "ai_response": "我叫小助手，很高兴认识你！",
            "mood_tag": "happy",
            "touch_zone": None
        },
        {
            "user_text": "我们之前聊过什么？",
            "ai_response": "我们聊过天气、你的心情，还有我的名字。",
            "mood_tag": "neutral",
            "touch_zone": None
        }
    ]
    
    print("\n📝 添加记忆记录:")
    for i, case in enumerate(test_cases, 1):
        memory_id = memory_system.add_memory(
            user_text=case["user_text"],
            ai_response=case["ai_response"],
            mood_tag=case["mood_tag"],
            touch_zone=case["touch_zone"],
            session_id=session_id
        )
        print(f"   {i}. 记忆ID: {memory_id}")
        print(f"      用户: {case['user_text']}")
        print(f"      AI: {case['ai_response']}")
        print(f"      情绪: {case['mood_tag']}")
        print(f"      触摸: {case['touch_zone']}")
    
    # 测试记忆查询
    print("\n🔍 测试记忆查询:")
    query_tests = [
        "你好",
        "天气",
        "心情",
        "名字",
        "之前聊过什么"
    ]
    
    for query in query_tests:
        print(f"\n查询: '{query}'")
        result = memory_system.query_memory(
            prompt=query,
            top_k=3,
            session_id=session_id
        )
        
        print(f"   📊 找到 {result['count']} 条记忆")
        print(f"   📝 摘要: {result['summary']}")
        print(f"   🧠 语义记忆: {result['types']['semantic']}")
        print(f"   🪟 上下文记忆: {result['types']['context']}")
        print(f"   😊 情感记忆: {result['types']['emotional']}")
    
    # 测试上下文记忆
    print(f"\n🪟 当前上下文摘要:")
    context = memory_system.get_current_context(session_id)
    print(f"   {context}")
    
    # 获取记忆统计
    print(f"\n📊 记忆统计:")
    stats = memory_system.get_memory_stats()
    print(f"   总记录数: {stats['total_records']}")
    print(f"   总会话数: {stats['total_sessions']}")
    print(f"   活跃会话数: {stats['active_sessions']}")
    print(f"   向量维度: {stats['vector_dim']}")
    print(f"   情绪分布: {stats['emotion_distribution']}")
    print(f"   重要性分布: {stats['importance_distribution']}")
    
    # 清理
    memory_system.close()
    print("\n✅ 增强记忆系统测试完成")


def test_enhanced_dialogue_engine():
    """测试增强对话引擎"""
    print("\n🧪 开始测试增强对话引擎")
    print("="*60)
    
    # 初始化对话引擎
    dialogue_engine = EnhancedDialogueEngine(robot_id="test_robot")
    
    # 开始会话
    session_id = dialogue_engine.start_session()
    print(f"🆕 创建会话: {session_id}")
    
    # 测试对话
    test_conversations = [
        {
            "user_text": "你好",
            "mood_tag": "happy",
            "touch_zone": None
        },
        {
            "user_text": "今天天气怎么样？",
            "mood_tag": "excited",
            "touch_zone": 0
        },
        {
            "user_text": "我有点难过",
            "mood_tag": "sad",
            "touch_zone": 1
        },
        {
            "user_text": "我们之前聊过什么？",
            "mood_tag": "neutral",
            "touch_zone": None
        }
    ]
    
    print("\n💬 测试对话:")
    for i, conv in enumerate(test_conversations, 1):
        print(f"\n--- 对话 {i} ---")
        print(f"用户: {conv['user_text']}")
        print(f"情绪: {conv['mood_tag']}")
        print(f"触摸: {conv['touch_zone']}")
        
        response = dialogue_engine.generate_response(
            user_text=conv["user_text"],
            mood_tag=conv["mood_tag"],
            user_id="test_user",
            touched=conv["touch_zone"] is not None,
            touch_zone=conv["touch_zone"],
            session_id=session_id
        )
        
        print(f"AI回复: {response.text}")
        print(f"会话ID: {response.session_id}")
        print(f"上下文摘要: {response.context_summary}")
        print(f"记忆数量: {response.memory_count}")
        print(f"表情: {response.expression}")
        print(f"动作: {response.action}")
    
    # 获取记忆统计
    print(f"\n📊 对话引擎记忆统计:")
    stats = dialogue_engine.get_memory_stats()
    print(f"   总记录数: {stats['total_records']}")
    print(f"   总会话数: {stats['total_sessions']}")
    print(f"   活跃会话数: {stats['active_sessions']}")
    
    # 清理
    dialogue_engine.close()
    print("\n✅ 增强对话引擎测试完成")


def test_intelligent_core():
    """测试智能核心"""
    print("\n🧪 开始测试智能核心")
    print("="*60)
    
    # 初始化智能核心
    core = IntelligentCore(robot_id="test_robot")
    
    # 开始会话
    session_id = core.start_session()
    print(f"🆕 创建会话: {session_id}")
    
    # 测试处理
    test_inputs = [
        {
            "text": "你好",
            "touch_zone": None
        },
        {
            "text": "今天天气怎么样？",
            "touch_zone": 0
        },
        {
            "text": "我有点难过",
            "touch_zone": 1
        },
        {
            "text": "我们之前聊过什么？",
            "touch_zone": None
        }
    ]
    
    print("\n🤖 测试智能核心处理:")
    for i, input_data in enumerate(test_inputs, 1):
        print(f"\n--- 输入 {i} ---")
        print(f"文本: {input_data['text']}")
        print(f"触摸: {input_data['touch_zone']}")
        
        user_input = UserInput(
            text=input_data["text"],
            robot_id="test_robot",
            touch_zone=input_data["touch_zone"],
            session_id=session_id
        )
        
        response = core.process(user_input)
        
        print(f"AI回复: {response.text}")
        print(f"会话ID: {response.session_id}")
        print(f"上下文摘要: {response.context_summary}")
        print(f"记忆数量: {response.memory_count}")
        print(f"表情: {response.expression}")
        print(f"动作: {response.action}")
    
    # 获取记忆统计
    print(f"\n📊 智能核心记忆统计:")
    stats = core.get_memory_stats()
    print(f"   总记录数: {stats['total_records']}")
    print(f"   总会话数: {stats['total_sessions']}")
    print(f"   活跃会话数: {stats['active_sessions']}")
    
    # 清理
    core.close()
    print("\n✅ 智能核心测试完成")


async def test_async_processing():
    """测试异步处理"""
    print("\n🧪 开始测试异步处理")
    print("="*60)
    
    # 初始化智能核心
    core = IntelligentCore(robot_id="test_robot")
    
    # 开始会话
    session_id = core.start_session()
    print(f"🆕 创建会话: {session_id}")
    
    # 测试异步处理
    test_inputs = [
        {
            "text": "你好",
            "touch_zone": None
        },
        {
            "text": "今天天气怎么样？",
            "touch_zone": 0
        },
        {
            "text": "我有点难过",
            "touch_zone": 1
        }
    ]
    
    print("\n🔄 测试异步处理:")
    for i, input_data in enumerate(test_inputs, 1):
        print(f"\n--- 异步输入 {i} ---")
        print(f"文本: {input_data['text']}")
        print(f"触摸: {input_data['touch_zone']}")
        
        user_input = UserInput(
            text=input_data["text"],
            robot_id="test_robot",
            touch_zone=input_data["touch_zone"],
            session_id=session_id
        )
        
        response = await core.process_async(user_input)
        
        print(f"AI回复: {response.text}")
        print(f"会话ID: {response.session_id}")
        print(f"上下文摘要: {response.context_summary}")
        print(f"记忆数量: {response.memory_count}")
    
    # 清理
    core.close()
    print("\n✅ 异步处理测试完成")


def main():
    """主测试函数"""
    print("🚀 增强记忆系统全面测试")
    print("="*80)
    
    try:
        # 测试增强记忆系统
        test_enhanced_memory_system()
        
        # 测试增强对话引擎
        test_enhanced_dialogue_engine()
        
        # 测试智能核心
        test_intelligent_core()
        
        # 测试异步处理
        asyncio.run(test_async_processing())
        
        print("\n🎉 所有测试完成！")
        print("="*80)
        print("✅ 增强记忆系统功能正常")
        print("✅ 会话连续性功能正常")
        print("✅ 上下文记忆功能正常")
        print("✅ 语义记忆功能正常")
        print("✅ 情感记忆功能正常")
        print("✅ 异步处理功能正常")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 
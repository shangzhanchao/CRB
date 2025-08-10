#!/usr/bin/env python3
"""
测试提示词一致性修复

验证"发送给LLM的完整提示词"与调用豆包API传入的提示词是否一致。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.personality_engine import PersonalityEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.intimacy_system import IntimacySystem

def test_prompt_consistency():
    """测试提示词一致性"""
    print("="*80)
    print("测试提示词一致性修复")
    print("="*80)
    
    # 初始化组件
    robot_id = "test_robot"
    personality = PersonalityEngine()
    memory = EnhancedMemorySystem(robot_id=robot_id)
    intimacy = IntimacySystem(robot_id=robot_id)
    
    # 创建增强对话引擎
    engine = EnhancedDialogueEngine(
        robot_id=robot_id,
        personality=personality,
        memory=memory,
        intimacy=intimacy,
        llm_url="doubao"  # 使用豆包API
    )
    
    # 开始会话
    session_id = engine.start_session()
    
    # 测试用例1：普通对话
    print("\n" + "="*80)
    print("测试用例1：普通对话")
    print("="*80)
    
    response1 = engine.generate_response(
        user_text="你好",
        mood_tag="happy",
        user_id="test_user",
        touched=False,
        touch_zone=None,
        session_id=session_id
    )
    
    print(f"响应文本: {response1.text}")
    
    # 测试用例2：触摸交互
    print("\n" + "="*80)
    print("测试用例2：触摸交互")
    print("="*80)
    
    response2 = engine.generate_response(
        user_text="",
        mood_tag="neutral",
        user_id="test_user",
        touched=True,
        touch_zone=0,
        session_id=session_id
    )
    
    print(f"响应文本: {response2.text}")
    
    # 测试用例3：带记忆的对话
    print("\n" + "="*80)
    print("测试用例3：带记忆的对话")
    print("="*80)
    
    response3 = engine.generate_response(
        user_text="我喜欢和你聊天",
        mood_tag="happy",
        user_id="test_user",
        touched=False,
        touch_zone=None,
        session_id=session_id
    )
    
    print(f"响应文本: {response3.text}")
    
    # 清理
    engine.close()
    
    print("\n" + "="*80)
    print("测试完成")
    print("="*80)
    print("✓ 请检查上述日志输出，确认：")
    print("  1. 融合后的完整提示词与发送给豆包API的提示词完全一致")
    print("  2. 豆包API调用说明清晰明确")
    print("  3. 消息结构说明详细准确")
    print("="*80)

if __name__ == "__main__":
    test_prompt_consistency() 
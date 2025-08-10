#!/usr/bin/env python3
"""测试提示词输出和LLM响应打印功能

验证新的提示词融合算法和详细的输出打印功能。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.dialogue_engine import DialogueEngine
from ai_core.intelligent_core import IntelligentCore, UserInput


def test_prompt_output():
    """测试提示词输出功能"""
    print("=== 测试提示词输出功能 ===")
    
    # 创建对话引擎
    dialogue_engine = DialogueEngine(
        llm_url="qwen",  # 使用百炼服务进行测试
        tts_url=None
    )
    
    # 测试用例
    test_cases = [
        {
            "name": "基础问候测试",
            "user_text": "你好，今天天气真不错！",
            "mood_tag": "happy",
            "user_id": "test_user_001",
            "touched": False,
            "touch_zone": None
        },
        {
            "name": "触摸交互测试",
            "user_text": "摸摸头",
            "mood_tag": "excited",
            "user_id": "test_user_002",
            "touched": True,
            "touch_zone": 0
        },
        {
            "name": "困惑情绪测试",
            "user_text": "我不太明白这个概念",
            "mood_tag": "confused",
            "user_id": "test_user_003",
            "touched": False,
            "touch_zone": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"🧪 测试用例 {i}: {test_case['name']}")
        print(f"{'='*80}")
        
        try:
            # 生成回复
            response = dialogue_engine.generate_response(
                user_text=test_case["user_text"],
                mood_tag=test_case["mood_tag"],
                user_id=test_case["user_id"],
                touched=test_case["touched"],
                touch_zone=test_case["touch_zone"]
            )
            
            print(f"\n✅ 测试用例 {i} 完成")
            print(f"📝 用户输入: {test_case['user_text']}")
            print(f"🤖 机器人回复: {response.text}")
            print(f"🎭 表情: {response.expression}")
            print(f"🤸 动作: {response.action}")
            
        except Exception as e:
            print(f"❌ 测试用例 {i} 失败: {e}")
            import traceback
            traceback.print_exc()


def test_intelligent_core():
    """测试智能核心的完整流程"""
    print("\n=== 测试智能核心完整流程 ===")
    
    # 创建智能核心
    core = IntelligentCore(
        llm_url="qwen",
        tts_url=None
    )
    
    # 测试用例
    test_inputs = [
        UserInput(
            robot_id="test_robot",
            text="你好，我是小明",
            touch_zone=None
        ),
        UserInput(
            robot_id="test_robot",
            text="摸摸头",
            touch_zone=0
        ),
        UserInput(
            robot_id="test_robot",
            text="我今天很开心！",
            touch_zone=None
        )
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{'='*80}")
        print(f"🧪 智能核心测试 {i}")
        print(f"{'='*80}")
        
        try:
            # 处理用户输入
            response = core.process(user_input)
            
            print(f"✅ 智能核心测试 {i} 完成")
            print(f"📝 用户输入: {user_input.text}")
            print(f"🤖 机器人回复: {response.text}")
            print(f"🎭 表情: {response.expression}")
            print(f"🤸 动作: {response.action}")
            
        except Exception as e:
            print(f"❌ 智能核心测试 {i} 失败: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    print("🤖 提示词输出和LLM响应打印功能测试")
    print("="*80)
    
    try:
        # 测试对话引擎
        test_prompt_output()
        
        # 测试智能核心
        test_intelligent_core()
        
        print("\n✅ 所有测试完成！")
        print("\n请检查输出中是否包含:")
        print("1. 🤖 LLM提示词融合详细信息")
        print("2. 📋 融合后的完整提示词")
        print("3. 🚀 LLM调用详细信息")
        print("4. 📤 LLM原始输出")
        print("5. 🎭 表情输出")
        print("6. 🤸 动作输出")
        print("7. 🎯 最终生成的回复")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 
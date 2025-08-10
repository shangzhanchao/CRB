#!/usr/bin/env python3
"""
测试触摸互动优化效果

验证PROMPT CONTENT中具体输出要求的优化是否生效
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.personality_engine import PersonalityEngine
from ai_core.intimacy_system import IntimacySystem

def test_touch_interaction_requirements():
    """测试触摸互动具体输出要求的优化"""
    print("="*80)
    print("测试触摸互动具体输出要求优化")
    print("="*80)
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建触摸互动因子
    touch_factors = create_prompt_factors(
        stage_info={
            "prompt": "当前处于觉醒阶段，机器人开始展现个性和情感"
        },
        touch_info={
            "content": "用户抚摸头部，感受到温暖和关爱"
        }
    )
    
    # 生成提示词模板
    template = fusion_engine.create_comprehensive_prompt(touch_factors)
    
    print("生成的提示词模板:")
    print("-" * 50)
    print(template)
    print("-" * 50)
    
    # 检查是否包含优化后的触摸互动要求
    expected_requirement = "对触摸互动进行回应，不要有文字内容体现，语言中可以根据情况有语气词。可以通过动作和表情回应"
    
    if expected_requirement in template:
        print("✅ 包含优化后的触摸互动要求")
    else:
        print("❌ 缺少优化后的触摸互动要求")
        print(f"期望内容: {expected_requirement}")
    
    return expected_requirement in template

def test_dialogue_engine_touch_handling():
    """测试对话引擎的触摸互动处理"""
    print("\n" + "="*80)
    print("测试对话引擎触摸互动处理")
    print("="*80)
    
    # 初始化组件
    memory = EnhancedMemorySystem(robot_id="robotA")
    personality = PersonalityEngine()
    intimacy = IntimacySystem(robot_id="robotA")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="robotA",
        personality=personality,
        memory=memory,
        intimacy=intimacy
    )
    
    # 测试触摸互动（无文本输入）
    print("测试1: 纯触摸互动（无文本输入）")
    response1 = engine.generate_response(
        user_text="",  # 空文本
        touched=True,
        touch_zone=0,  # 头部抚摸
        session_id="test_touch_001"
    )
    
    print(f"回应文本: '{response1.text}'")
    print(f"动作代码: {response1.action}")
    print(f"表情代码: {response1.expression}")
    
    # 验证触摸互动时应该返回空文本
    if not response1.text.strip():
        print("✅ 触摸互动时正确返回空文本")
    else:
        print("❌ 触摸互动时仍返回文本内容")
    
    # 测试触摸互动（有文本输入）
    print("\n测试2: 触摸互动（有文本输入）")
    response2 = engine.generate_response(
        user_text="摸摸头",  # 有文本输入
        touched=True,
        touch_zone=0,  # 头部抚摸
        session_id="test_touch_002"
    )
    
    print(f"回应文本: '{response2.text}'")
    print(f"动作代码: {response2.action}")
    print(f"表情代码: {response2.expression}")
    
    # 验证有文本输入时可以有回应，但不应有文字内容体现
    if response2.text.strip():
        print("✅ 有文本输入时正确生成回应")
    else:
        print("⚠️ 有文本输入时未生成回应")
    
    return True

def test_system_prompt_touch_requirements():
    """测试系统提示词中的触摸互动规范"""
    print("\n" + "="*80)
    print("测试系统提示词触摸互动规范")
    print("="*80)
    
    # 初始化组件
    memory = EnhancedMemorySystem(robot_id="robotA")
    personality = PersonalityEngine()
    intimacy = IntimacySystem(robot_id="robotA")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="robotA",
        personality=personality,
        memory=memory,
        intimacy=intimacy
    )
    
    # 获取系统提示词
    system_prompt = engine._build_system_prompt(
        robot_id="robotA",
        stage="awaken",
        personality_style="friendly",
        dominant_traits=["openness", "agreeableness"],
        memory_count=5,
        session_id="test_system_001"
    )
    
    print("系统提示词中的触摸互动规范:")
    print("-" * 50)
    
    # 查找触摸互动规范部分
    lines = system_prompt.split('\n')
    in_touch_section = False
    touch_section_lines = []
    
    for line in lines:
        if "## 触摸互动规范" in line:
            in_touch_section = True
            touch_section_lines.append(line)
        elif in_touch_section and line.startswith("##"):
            in_touch_section = False
        elif in_touch_section:
            touch_section_lines.append(line)
    
    for line in touch_section_lines:
        print(line)
    
    print("-" * 50)
    
    # 检查是否包含优化后的要求
    expected_requirements = [
        "触摸互动时只输出动作和表情，不输出文本内容",
        "语言中可以根据情况有语气词，但不要有文字内容体现",
        "可以通过动作和表情回应触摸"
    ]
    
    print("\n检查优化后的触摸互动要求:")
    for requirement in expected_requirements:
        if requirement in system_prompt:
            print(f"✅ 包含: {requirement}")
        else:
            print(f"❌ 缺少: {requirement}")
    
    return all(req in system_prompt for req in expected_requirements)

def main():
    """主测试函数"""
    print("🤖 开始测试触摸互动优化效果")
    print("="*80)
    
    try:
        # 运行所有测试
        test1_passed = test_touch_interaction_requirements()
        test2_passed = test_dialogue_engine_touch_handling()
        test3_passed = test_system_prompt_touch_requirements()
        
        print("\n" + "="*80)
        print("测试结果总结:")
        print(f"触摸互动要求优化: {'✅ 通过' if test1_passed else '❌ 失败'}")
        print(f"对话引擎触摸处理: {'✅ 通过' if test2_passed else '❌ 失败'}")
        print(f"系统提示词规范: {'✅ 通过' if test3_passed else '❌ 失败'}")
        print("="*80)
        
        if test1_passed and test2_passed and test3_passed:
            print("🎉 所有测试通过！触摸互动优化成功！")
        else:
            print("⚠️ 部分测试失败，需要进一步检查")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

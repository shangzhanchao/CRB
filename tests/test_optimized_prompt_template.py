#!/usr/bin/env python3
"""
测试优化后的提示词模板系统
Test the optimized prompt template system

验证以下功能:
1. 完整的动作和表情参数定义
2. 触摸互动特殊处理（只返回动作和表情）
3. 输出格式规范
4. 分层结构化提示词
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.personality_engine import PersonalityEngine
from ai_core.intimacy_system import IntimacySystem
from ai_core.constants import FACE_ANIMATION_MAP, ACTION_MAP

def test_prompt_template_structure():
    """测试提示词模板的分层结构化"""
    print("="*80)
    print("测试1: 提示词模板分层结构化")
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
    
    # 测试不同成长阶段的提示词
    stages = ["sprout", "enlighten", "resonate", "awaken"]
    
    for stage in stages:
        print(f"\n--- 成长阶段: {stage} ---")
        
        # 构建系统提示词
        system_prompt = engine._build_system_prompt(
            robot_id="robotA",
            stage=stage,
            personality_style="外向开朗",
            dominant_traits=["extraversion", "agreeableness"],
            memory_count=10,
            session_id="test_session_001"
        )
        
        # 检查关键部分是否存在
        sections = [
            "# 机器人身份与基础信息",
            "# 机器人状态与能力", 
            "# 记忆信息",
            "# 交互上下文",
            "# 输出要求",
            "### 5. 输出格式规范",
            "# 行为指导"
        ]
        
        print(f"提示词长度: {len(system_prompt)} 字符")
        
        for section in sections:
            if section in system_prompt:
                print(f"✓ 包含: {section}")
            else:
                print(f"✗ 缺少: {section}")
        
        # 检查动作和表情参数定义
        if "动作表达参数定义:" in system_prompt and "表情表达参数定义:" in system_prompt:
            print("✓ 包含完整的动作和表情参数定义")
        else:
            print("✗ 缺少动作和表情参数定义")
        
        # 检查触摸互动特殊要求
        if "触摸互动特殊要求:" in system_prompt:
            print("✓ 包含触摸互动特殊要求")
        else:
            print("✗ 缺少触摸互动特殊要求")

def test_action_expression_definitions():
    """测试动作和表情参数定义的完整性"""
    print("\n" + "="*80)
    print("测试2: 动作和表情参数定义完整性")
    print("="*80)
    
    # 检查常量文件中的定义
    print("FACE_ANIMATION_MAP 包含的表情:")
    for emotion, (expression_code, description) in FACE_ANIMATION_MAP.items():
        print(f"  {emotion}: {expression_code}")
    
    print("\nACTION_MAP 包含的动作:")
    for emotion, action_code in ACTION_MAP.items():
        print(f"  {emotion}: {action_code}")
    
    # 验证参数格式
    print("\n验证参数格式:")
    for emotion, (expression_code, description) in FACE_ANIMATION_MAP.items():
        if expression_code.startswith("E") and ":" in expression_code:
            print(f"✓ 表情 {emotion}: 格式正确")
        else:
            print(f"✗ 表情 {emotion}: 格式错误")
    
    for emotion, action_code in ACTION_MAP.items():
        if "A" in action_code and "|" in action_code:
            print(f"✓ 动作 {emotion}: 格式正确")
        else:
            print(f"✗ 动作 {emotion}: 格式错误")

def test_touch_interaction_handling():
    """测试触摸互动特殊处理"""
    print("\n" + "="*80)
    print("测试3: 触摸互动特殊处理")
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
    
    # 测试不同触摸区域
    touch_zones = [0, 1, 2]
    
    for zone in touch_zones:
        print(f"\n--- 触摸区域: {zone} ---")
        
        # 测试有文本输入的触摸互动
        print("1. 有文本输入的触摸互动:")
        response1 = engine.generate_response(
            user_text="你好",
            touched=True,
            touch_zone=zone,
            session_id="test_touch_001"
        )
        print(f"   文本: '{response1.text}'")
        print(f"   动作: {response1.action}")
        print(f"   表情: {response1.expression}")
        
        # 测试无文本输入的触摸互动（应该只返回动作和表情）
        print("2. 无文本输入的触摸互动:")
        response2 = engine.generate_response(
            user_text="",  # 空文本
            touched=True,
            touch_zone=zone,
            session_id="test_touch_002"
        )
        print(f"   文本: '{response2.text}' (应该为空)")
        print(f"   动作: {response2.action}")
        print(f"   表情: {response2.expression}")
        
        # 验证触摸互动时无文本输入应该返回空文本
        if not response2.text.strip():
            print("✓ 触摸互动无文本输入时正确返回空文本")
        else:
            print("✗ 触摸互动无文本输入时仍返回文本内容")

def test_output_format_specifications():
    """测试输出格式规范"""
    print("\n" + "="*80)
    print("测试4: 输出格式规范")
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
    
    # 构建系统提示词并检查输出格式规范
    system_prompt = engine._build_system_prompt(
        robot_id="robotA",
        stage="enlighten",
        personality_style="外向开朗",
        dominant_traits=["extraversion"],
        memory_count=5,
        session_id="test_format_001"
    )
    
    # 检查输出格式规范部分
    format_sections = [
        "文本输出格式:",
        "动作输出格式:",
        "表情输出格式:",
        "触摸互动输出格式:",
        "音频输出格式:",
        "记忆输出格式:",
        "错误处理格式:"
    ]
    
    print("检查输出格式规范包含的子部分:")
    for section in format_sections:
        if section in system_prompt:
            print(f"✓ 包含: {section}")
        else:
            print(f"✗ 缺少: {section}")
    
    # 检查具体的格式规范
    format_checks = [
        ("动作代码格式", "A001:nod±15°"),
        ("表情代码格式", "E001:微笑+眨眼+眼神上扬"),
        ("触摸互动时只输出动作和表情", "触摸互动时只输出动作和表情"),
        ("支持多组动作", "支持多组动作"),
        ("支持多组表情", "支持多组表情")
    ]
    
    print("\n检查具体的格式规范:")
    for check_name, check_content in format_checks:
        if check_content in system_prompt:
            print(f"✓ 包含: {check_name}")
        else:
            print(f"✗ 缺少: {check_name}")

def test_memory_integration():
    """测试记忆系统集成"""
    print("\n" + "="*80)
    print("测试5: 记忆系统集成")
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
    
    # 添加一些测试记忆
    test_memories = [
        ("你好", "你好！很高兴见到你", "happy"),
        ("今天天气怎么样？", "今天天气很好呢", "happy"),
        ("我感觉有点累", "要不要休息一下？", "concerned")
    ]
    
    for user_text, ai_response, mood in test_memories:
        memory.add_memory(
            user_text=user_text,
            ai_response=ai_response,
            mood_tag=mood,
            session_id="test_memory_001"
        )
    
    # 测试记忆查询
    memories = memory.query_memory("你好", session_id="test_memory_001")
    print(f"记忆查询结果数量: {len(memories)}")
    
    # 测试生成回应（应该包含记忆信息）
    response = engine.generate_response(
        user_text="你还记得我们之前聊过什么吗？",
        session_id="test_memory_001"
    )
    
    print(f"生成的回应: {response.text}")
    print(f"记忆数量: {response.memory_count}")

def main():
    """主测试函数"""
    print("🤖 开始测试优化后的提示词模板系统")
    print("="*80)
    
    try:
        # 运行所有测试
        test_prompt_template_structure()
        test_action_expression_definitions()
        test_touch_interaction_handling()
        test_output_format_specifications()
        test_memory_integration()
        
        print("\n" + "="*80)
        print("✅ 所有测试完成！")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
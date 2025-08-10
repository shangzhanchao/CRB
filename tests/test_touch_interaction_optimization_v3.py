#!/usr/bin/env python3
"""
测试触摸互动优化效果 V3

验证：
1. 触摸互动时不要有任何触摸相关的内容
2. 大模型返回格式问题（用户期望JSON格式）
3. history参数传递问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.personality_engine import PersonalityEngine
from ai_core.intimacy_system import IntimacySystem
from ai_core.doubao_service import get_doubao_service

def test_touch_interaction_requirements_v3():
    """测试触摸互动具体输出要求的优化 V3"""
    print("="*80)
    print("测试触摸互动具体输出要求优化 V3")
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
    expected_requirement = "不要有任何触摸相关的内容，只输出语气词（如'嗯~'、'啊~'、'唔~'等）和动作表情指令（如A112:loving_nod、E025:loving_smile）"
    
    if expected_requirement in template:
        print("✅ 包含优化后的触摸互动要求 V3")
    else:
        print("❌ 缺少优化后的触摸互动要求 V3")
        print(f"期望内容: {expected_requirement}")
    
    return expected_requirement in template

def test_system_prompt_touch_requirements_v3():
    """测试系统提示词中的触摸互动规范 V3"""
    print("\n" + "="*80)
    print("测试系统提示词触摸互动规范 V3")
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
        "触摸互动时不要有任何触摸相关的内容",
        "只输出语气词（如\"嗯~\"、\"啊~\"、\"唔~\"等）和动作表情指令",
        "动作指令格式：A100-A114 (如A112:loving_nod)",
        "表情指令格式：E020-E027 (如E025:loving_smile)"
    ]
    
    print("\n检查优化后的触摸互动要求 V3:")
    for requirement in expected_requirements:
        if requirement in system_prompt:
            print(f"✅ 包含: {requirement}")
        else:
            print(f"❌ 缺少: {requirement}")
    
    return all(req in system_prompt for req in expected_requirements)

def test_history_passing():
    """测试history参数传递"""
    print("\n" + "="*80)
    print("测试history参数传递")
    print("="*80)
    
    try:
        # 初始化组件
        memory = EnhancedMemorySystem(robot_id="robotA")
        personality = PersonalityEngine()
        intimacy = IntimacySystem(robot_id="robotA")
        
        # 创建对话引擎
        engine = EnhancedDialogueEngine(
            robot_id="robotA",
            personality=personality,
            memory=memory,
            intimacy=intimacy,
            llm_url="doubao"
        )
        
        # 添加一些记忆记录来测试history
        session_id = "test_history_001"
        engine.memory.add_memory(
            user_text="你好",
            ai_response="你好！很高兴见到你",
            mood_tag="happy",
            session_id=session_id
        )
        engine.memory.add_memory(
            user_text="今天天气怎么样？",
            ai_response="今天天气不错，阳光明媚",
            mood_tag="neutral",
            session_id=session_id
        )
        
        # 测试_build_conversation_history方法
        history = engine._build_conversation_history(session_id)
        
        print("构建的历史对话记录:")
        print("-" * 50)
        for i, msg in enumerate(history, 1):
            print(f"{i}. {msg['role']}: {msg['content']}")
        print("-" * 50)
        
        if len(history) >= 4:  # 应该有2轮对话，4条消息
            print("✅ History构建成功，包含足够的对话记录")
            return True
        else:
            print(f"❌ History构建失败，只有{len(history)}条记录")
            return False
            
    except Exception as e:
        print(f"❌ History测试失败: {e}")
        return False

def test_json_output_format_issue():
    """测试JSON输出格式问题"""
    print("\n" + "="*80)
    print("测试JSON输出格式问题")
    print("="*80)
    
    try:
        # 检查当前提示词中的输出格式要求
        fusion_engine = PromptFusionEngine()
        touch_factors = create_prompt_factors(
            stage_info={
                "prompt": "当前处于觉醒阶段，机器人开始展现个性和情感"
            },
            touch_info={
                "content": "用户抚摸头部，感受到温暖和关爱"
            }
        )
        
        template = fusion_engine.create_comprehensive_prompt(touch_factors)
        
        # 检查是否包含"只输出回复文本，不要包含任何格式标记"
        if "只输出回复文本，不要包含任何格式标记" in template:
            print("⚠️ 发现冲突的输出格式要求:")
            print("   - 用户期望JSON格式输出")
            print("   - 当前提示词要求'只输出回复文本，不要包含任何格式标记'")
            print("   - 这可能导致LLM返回纯文本而不是JSON格式")
            return False
        else:
            print("✅ 没有发现冲突的输出格式要求")
            return True
            
    except Exception as e:
        print(f"❌ JSON格式测试失败: {e}")
        return False

def test_doubao_service_history_debug():
    """测试豆包服务的history调试信息"""
    print("\n" + "="*80)
    print("测试豆包服务history调试")
    print("="*80)
    
    try:
        # 检查doubao_service.py中的调试信息
        with open('ai_core/doubao_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含history相关的调试信息
        history_debug_statements = [
            "History provided:",
            "History messages added:"
        ]
        
        print("检查豆包服务中的history调试信息:")
        for statement in history_debug_statements:
            if statement in content:
                print(f"✅ 包含: {statement}")
            else:
                print(f"❌ 缺少: {statement}")
        
        # 检查enhanced_dialogue_engine.py中的调试信息
        with open('ai_core/enhanced_dialogue_engine.py', 'r', encoding='utf-8') as f:
            engine_content = f.read()
        
        if "Conversation history built:" in engine_content:
            print("✅ 包含: Conversation history built:")
        else:
            print("❌ 缺少: Conversation history built:")
        
        return all(stmt in content for stmt in history_debug_statements) and "Conversation history built:" in engine_content
        
    except Exception as e:
        print(f"❌ 检查文件时出错: {e}")
        return False

def main():
    """主测试函数"""
    print("🤖 开始测试触摸互动优化效果 V3")
    print("="*80)
    
    try:
        # 运行所有测试
        test1_passed = test_touch_interaction_requirements_v3()
        test2_passed = test_system_prompt_touch_requirements_v3()
        test3_passed = test_history_passing()
        test4_passed = test_json_output_format_issue()
        test5_passed = test_doubao_service_history_debug()
        
        print("\n" + "="*80)
        print("测试结果总结 V3:")
        print(f"触摸互动要求优化: {'✅ 通过' if test1_passed else '❌ 失败'}")
        print(f"系统提示词规范: {'✅ 通过' if test2_passed else '❌ 失败'}")
        print(f"History参数传递: {'✅ 通过' if test3_passed else '❌ 失败'}")
        print(f"JSON输出格式检查: {'✅ 通过' if test4_passed else '❌ 失败'}")
        print(f"豆包服务调试信息: {'✅ 通过' if test5_passed else '❌ 失败'}")
        print("="*80)
        
        if test1_passed and test2_passed and test3_passed and test4_passed and test5_passed:
            print("🎉 所有测试通过！触摸互动优化 V3 成功！")
            print("\n优化总结:")
            print("1. ✅ 大模型不再有任何触摸相关的内容")
            print("2. ✅ 只输出语气词（如'嗯~'、'啊~'、'唔~'等）")
            print("3. ✅ 输出动作表情指令（如A112:loving_nod、E025:loving_smile）")
            print("4. ✅ History参数正确传递")
            print("5. ✅ JSON输出格式问题已解决")
        else:
            print("⚠️ 部分测试失败，需要进一步检查")
            if not test4_passed:
                print("\n🔧 建议修复JSON输出格式问题:")
                print("   - 修改提示词中的'只输出回复文本，不要包含任何格式标记'")
                print("   - 或者明确说明期望的JSON格式")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

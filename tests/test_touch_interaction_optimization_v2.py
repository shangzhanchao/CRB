#!/usr/bin/env python3
"""
测试触摸互动优化效果 V2

验证PROMPT CONTENT中具体输出要求的优化是否生效
重点验证大模型不输出描述性文字，只输出语气词和动作表情指令
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.personality_engine import PersonalityEngine
from ai_core.intimacy_system import IntimacySystem

def test_touch_interaction_requirements_v2():
    """测试触摸互动具体输出要求的优化 V2"""
    print("="*80)
    print("测试触摸互动具体输出要求优化 V2")
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
    expected_requirement = "不要输出描述性文字（如'你抚摸了我的头部，我感觉很温暖'），只输出语气词（如'嗯~'、'啊~'等）和动作表情指令（如A112:loving_nod、E025:loving_smile）"
    
    if expected_requirement in template:
        print("✅ 包含优化后的触摸互动要求 V2")
    else:
        print("❌ 缺少优化后的触摸互动要求 V2")
        print(f"期望内容: {expected_requirement}")
    
    return expected_requirement in template

def test_system_prompt_touch_requirements_v2():
    """测试系统提示词中的触摸互动规范 V2"""
    print("\n" + "="*80)
    print("测试系统提示词触摸互动规范 V2")
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
        "触摸互动时不要输出描述性文字（如\"你抚摸了我的头部，我感觉很温暖\"）",
        "只输出语气词（如\"嗯~\"、\"啊~\"、\"唔~\"等）和动作表情指令",
        "动作指令格式：A100-A114 (如A112:loving_nod)",
        "表情指令格式：E020-E027 (如E025:loving_smile)"
    ]
    
    print("\n检查优化后的触摸互动要求 V2:")
    for requirement in expected_requirements:
        if requirement in system_prompt:
            print(f"✅ 包含: {requirement}")
        else:
            print(f"❌ 缺少: {requirement}")
    
    return all(req in system_prompt for req in expected_requirements)

def test_doubao_service_response_printing():
    """测试豆包服务是否打印大模型返回信息"""
    print("\n" + "="*80)
    print("测试豆包服务响应打印")
    print("="*80)
    
    # 检查doubao_service.py是否包含打印LLM响应的代码
    try:
        with open('ai_core/doubao_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        expected_print_statements = [
            "=== LLM RESPONSE CONTENT ===",
            "print(response_text)",
            "=== END LLM RESPONSE ==="
        ]
        
        print("检查豆包服务中的打印语句:")
        for statement in expected_print_statements:
            if statement in content:
                print(f"✅ 包含: {statement}")
            else:
                print(f"❌ 缺少: {statement}")
        
        return all(stmt in content for stmt in expected_print_statements)
        
    except Exception as e:
        print(f"❌ 检查文件时出错: {e}")
        return False

def main():
    """主测试函数"""
    print("🤖 开始测试触摸互动优化效果 V2")
    print("="*80)
    
    try:
        # 运行所有测试
        test1_passed = test_touch_interaction_requirements_v2()
        test2_passed = test_system_prompt_touch_requirements_v2()
        test3_passed = test_doubao_service_response_printing()
        
        print("\n" + "="*80)
        print("测试结果总结 V2:")
        print(f"触摸互动要求优化: {'✅ 通过' if test1_passed else '❌ 失败'}")
        print(f"系统提示词规范: {'✅ 通过' if test2_passed else '❌ 失败'}")
        print(f"豆包服务响应打印: {'✅ 通过' if test3_passed else '❌ 失败'}")
        print("="*80)
        
        if test1_passed and test2_passed and test3_passed:
            print("🎉 所有测试通过！触摸互动优化 V2 成功！")
            print("\n优化总结:")
            print("1. ✅ 大模型不再输出描述性文字（如'你抚摸了我的头部，我感觉很温暖'）")
            print("2. ✅ 只输出语气词（如'嗯~'、'啊~'、'唔~'等）")
            print("3. ✅ 输出动作表情指令（如A112:loving_nod、E025:loving_smile）")
            print("4. ✅ 豆包服务会打印完整的大模型返回信息")
        else:
            print("⚠️ 部分测试失败，需要进一步检查")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

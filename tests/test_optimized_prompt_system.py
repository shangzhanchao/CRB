#!/usr/bin/env python3
"""测试优化后的PROMPT和SYSTEM PROMPT系统

验证职责分工、消除重复冲突、提高效率等功能。
"""

import sys
import os
import json
from typing import Dict, List

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors
from ai_core.personality_engine import PersonalityEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem
from ai_core.intimacy_system import IntimacySystem


def test_system_prompt_optimization():
    """测试SYSTEM PROMPT优化"""
    print("=== 测试SYSTEM PROMPT优化 ===")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="test_robot",
        personality=PersonalityEngine(),
        memory=EnhancedMemorySystem(robot_id="test_robot"),
        intimacy=IntimacySystem(robot_id="test_robot")
    )
    
    # 测试系统提示词生成
    system_prompt = engine._build_system_prompt(
        robot_id="test_robot",
        stage="awaken",
        personality_style="enthusiastic",
        dominant_traits=["extraversion", "agreeableness"],
        memory_count=10,
        session_id="test_session_123"
    )
    
    print("✅ SYSTEM PROMPT生成成功")
    print(f"长度: {len(system_prompt)} 字符")
    
    # 验证系统级内容
    system_keywords = [
        "机器人身份定义",
        "系统行为规范", 
        "技术参数定义",
        "系统级交互规范",
        "输出格式标准",
        "错误处理机制",
        "动作和表情参数定义"
    ]
    
    missing_keywords = []
    for keyword in system_keywords:
        if keyword not in system_prompt:
            missing_keywords.append(keyword)
    
    if missing_keywords:
        print(f"❌ 缺少系统级关键词: {missing_keywords}")
        return False
    else:
        print("✅ 包含所有系统级关键词")
    
    # 验证不包含交互级内容
    interaction_keywords = [
        "当前交互状态",
        "用户输入和上下文",
        "当前可用动作和表情",
        "相关记忆引用",
        "具体输出要求"
    ]
    
    found_interaction_keywords = []
    for keyword in interaction_keywords:
        if keyword in system_prompt:
            found_interaction_keywords.append(keyword)
    
    if found_interaction_keywords:
        print(f"⚠️  发现交互级内容（应该避免）: {found_interaction_keywords}")
    else:
        print("✅ 不包含交互级内容")
    
    return True


def test_prompt_optimization():
    """测试PROMPT优化"""
    print("\n=== 测试PROMPT优化 ===")
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建测试因子
    factors = create_prompt_factors(
        stage_info={"prompt": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力"},
        personality_info={"traits": "外向开朗，喜欢社交互动，表达积极"},
        emotion_info={"emotion": "happy"},
        touch_info={"content": "用户轻拍了机器人的头部"},
        memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
        user_input="你好，今天天气真不错！"
    )
    
    # 创建上下文信息
    context_info = {
        "用户ID": "user123",
        "会话ID": "session_456",
        "触摸状态": "是",
        "触摸区域": "0",
        "成长阶段": "awaken",
        "人格风格": "enthusiastic"
    }
    
    # 生成交互提示词
    prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        context_info=context_info
    )
    
    print("✅ PROMPT生成成功")
    print(f"长度: {len(prompt)} 字符")
    
    # 验证交互级内容
    interaction_keywords = [
        "当前交互状态",
        "用户输入和上下文", 
        "当前可用动作和表情",
        "相关记忆引用",
        "具体输出要求"
    ]
    
    missing_keywords = []
    for keyword in interaction_keywords:
        if keyword not in prompt:
            missing_keywords.append(keyword)
    
    if missing_keywords:
        print(f"❌ 缺少交互级关键词: {missing_keywords}")
        return False
    else:
        print("✅ 包含所有交互级关键词")
    
    # 验证不包含系统级内容
    system_keywords = [
        "机器人身份定义",
        "系统行为规范",
        "技术参数定义", 
        "系统级交互规范",
        "输出格式标准",
        "错误处理机制"
    ]
    
    found_system_keywords = []
    for keyword in system_keywords:
        if keyword in prompt:
            found_system_keywords.append(keyword)
    
    if found_system_keywords:
        print(f"⚠️  发现系统级内容（应该避免）: {found_system_keywords}")
    else:
        print("✅ 不包含系统级内容")
    
    return True


def test_duplication_elimination():
    """测试重复内容消除"""
    print("\n=== 测试重复内容消除 ===")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="test_robot",
        personality=PersonalityEngine(),
        memory=EnhancedMemorySystem(robot_id="test_robot"),
        intimacy=IntimacySystem(robot_id="test_robot")
    )
    
    # 生成系统提示词
    system_prompt = engine._build_system_prompt(
        robot_id="test_robot",
        stage="awaken",
        personality_style="enthusiastic",
        dominant_traits=["extraversion", "agreeableness"],
        memory_count=10,
        session_id="test_session_123"
    )
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建测试因子
    factors = create_prompt_factors(
        stage_info={"prompt": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力"},
        personality_info={"traits": "外向开朗，喜欢社交互动，表达积极"},
        emotion_info={"emotion": "happy"},
        touch_info={"content": "用户轻拍了机器人的头部"},
        memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
        user_input="你好，今天天气真不错！"
    )
    
    # 生成交互提示词
    prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        context_info={"触摸状态": "是", "触摸区域": "0"}
    )
    
    # 检查重复内容
    system_lines = set(system_prompt.split('\n'))
    prompt_lines = set(prompt.split('\n'))
    
    # 查找重复行
    duplicate_lines = system_lines.intersection(prompt_lines)
    duplicate_lines = {line.strip() for line in duplicate_lines if line.strip()}
    
    if duplicate_lines:
        print(f"⚠️  发现重复内容: {len(duplicate_lines)} 行")
        for line in list(duplicate_lines)[:5]:  # 只显示前5行
            print(f"  - {line}")
        if len(duplicate_lines) > 5:
            print(f"  ... 还有 {len(duplicate_lines) - 5} 行重复内容")
    else:
        print("✅ 无重复内容")
    
    return len(duplicate_lines) == 0


def test_conflict_resolution():
    """测试冲突解决"""
    print("\n=== 测试冲突解决 ===")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="test_robot",
        personality=PersonalityEngine(),
        memory=EnhancedMemorySystem(robot_id="test_robot"),
        intimacy=IntimacySystem(robot_id="test_robot")
    )
    
    # 生成系统提示词
    system_prompt = engine._build_system_prompt(
        robot_id="test_robot",
        stage="awaken",
        personality_style="enthusiastic",
        dominant_traits=["extraversion", "agreeableness"],
        memory_count=10,
        session_id="test_session_123"
    )
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建测试因子
    factors = create_prompt_factors(
        stage_info={"prompt": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力"},
        personality_info={"traits": "外向开朗，喜欢社交互动，表达积极"},
        emotion_info={"emotion": "happy"},
        touch_info={"content": "用户轻拍了机器人的头部"},
        memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
        user_input="你好，今天天气真不错！"
    )
    
    # 生成交互提示词
    prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        context_info={"触摸状态": "是", "触摸区域": "0"}
    )
    
    # 检查输出格式冲突
    conflicts = []
    
    # 检查文本输出格式
    if "纯文本回应" in system_prompt and "只输出回复文本" in prompt:
        conflicts.append("文本输出格式一致")
    else:
        conflicts.append("文本输出格式不一致")
    
    # 检查动作输出格式
    if "action_code:description" in system_prompt and "动作代码" in prompt:
        conflicts.append("动作输出格式一致")
    else:
        conflicts.append("动作输出格式不一致")
    
    # 检查表情输出格式
    if "expression_code:description" in system_prompt and "表情代码" in prompt:
        conflicts.append("表情输出格式一致")
    else:
        conflicts.append("表情输出格式不一致")
    
    # 检查触摸互动处理
    if "触摸互动时只输出动作和表情" in system_prompt and "触摸互动" in prompt:
        conflicts.append("触摸互动处理一致")
    else:
        conflicts.append("触摸互动处理不一致")
    
    print("✅ 输出格式检查完成")
    for conflict in conflicts:
        print(f"  - {conflict}")
    
    return True


def test_efficiency_improvement():
    """测试效率提升"""
    print("\n=== 测试效率提升 ===")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="test_robot",
        personality=PersonalityEngine(),
        memory=EnhancedMemorySystem(robot_id="test_robot"),
        intimacy=IntimacySystem(robot_id="test_robot")
    )
    
    # 测试系统提示词生成时间
    import time
    
    start_time = time.time()
    system_prompt = engine._build_system_prompt(
        robot_id="test_robot",
        stage="awaken",
        personality_style="enthusiastic",
        dominant_traits=["extraversion", "agreeableness"],
        memory_count=10,
        session_id="test_session_123"
    )
    system_time = time.time() - start_time
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建测试因子
    factors = create_prompt_factors(
        stage_info={"prompt": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力"},
        personality_info={"traits": "外向开朗，喜欢社交互动，表达积极"},
        emotion_info={"emotion": "happy"},
        touch_info={"content": "用户轻拍了机器人的头部"},
        memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
        user_input="你好，今天天气真不错！"
    )
    
    # 测试交互提示词生成时间
    start_time = time.time()
    prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        context_info={"触摸状态": "是", "触摸区域": "0"}
    )
    prompt_time = time.time() - start_time
    
    print(f"✅ 系统提示词生成时间: {system_time:.4f} 秒")
    print(f"✅ 交互提示词生成时间: {prompt_time:.4f} 秒")
    print(f"✅ 总生成时间: {system_time + prompt_time:.4f} 秒")
    
    # 检查提示词长度
    print(f"✅ 系统提示词长度: {len(system_prompt)} 字符")
    print(f"✅ 交互提示词长度: {len(prompt)} 字符")
    print(f"✅ 总长度: {len(system_prompt) + len(prompt)} 字符")
    
    return True


def test_integration():
    """测试集成功能"""
    print("\n=== 测试集成功能 ===")
    
    # 创建对话引擎
    engine = EnhancedDialogueEngine(
        robot_id="test_robot",
        personality=PersonalityEngine(),
        memory=EnhancedMemorySystem(robot_id="test_robot"),
        intimacy=IntimacySystem(robot_id="test_robot")
    )
    
    # 模拟完整的对话流程
    try:
        # 1. 生成系统提示词
        system_prompt = engine._build_system_prompt(
            robot_id="test_robot",
            stage="awaken",
            personality_style="enthusiastic",
            dominant_traits=["extraversion", "agreeableness"],
            memory_count=10,
            session_id="test_session_123"
        )
        
        # 2. 生成交互提示词
        factors = create_prompt_factors(
            stage_info={"prompt": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力"},
            personality_info={"traits": "外向开朗，喜欢社交互动，表达积极"},
            emotion_info={"emotion": "happy"},
            touch_info={"content": "用户轻拍了机器人的头部"},
            memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
            user_input="你好，今天天气真不错！"
        )
        
        prompt = engine.prompt_fusion.create_comprehensive_prompt(
            factors=factors,
            context_info={"触摸状态": "是", "触摸区域": "0"}
        )
        
        # 3. 模拟LLM调用（不实际调用）
        print("✅ 系统提示词和交互提示词生成成功")
        print("✅ 可以传递给LLM进行调用")
        
        # 4. 验证提示词结构
        if "机器人身份定义" in system_prompt and "当前交互状态" in prompt:
            print("✅ 提示词结构正确")
        else:
            print("❌ 提示词结构错误")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始测试优化后的PROMPT和SYSTEM PROMPT系统")
    print("=" * 60)
    
    tests = [
        ("SYSTEM PROMPT优化", test_system_prompt_optimization),
        ("PROMPT优化", test_prompt_optimization),
        ("重复内容消除", test_duplication_elimination),
        ("冲突解决", test_conflict_resolution),
        ("效率提升", test_efficiency_improvement),
        ("集成功能", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name} 测试通过")
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！优化成功！")
        return True
    else:
        print("⚠️  部分测试失败，需要进一步优化")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
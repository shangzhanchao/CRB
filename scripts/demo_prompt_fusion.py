#!/usr/bin/env python3
"""提示词融合算法演示脚本

展示新的专业提示词融合算法的使用方法和效果。
"""

import sys
import os
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.prompt_fusion import (
    PromptFusionEngine,
    PromptFactor,
    RobotAction,
    RobotExpression,
    create_prompt_factors,
    create_robot_actions_from_emotion,
    create_robot_expressions_from_emotion
)


def demo_basic_prompt_fusion():
    """演示基础提示词融合"""
    print("=== 基础提示词融合演示 ===")
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建各种影响因子
    factors = [
        PromptFactor(
            name="growth_stage",
            content="觉醒期 - 能够主动回忆过去的交互经历，并根据记忆提供个性化的建议和回应",
            weight=1.5,
            priority=5,
            is_required=True
        ),
        PromptFactor(
            name="personality_traits",
            content="外向、友善、好奇",
            weight=1.2,
            priority=4
        ),
        PromptFactor(
            name="user_emotion",
            content="开心",
            weight=1.0,
            priority=3
        ),
        PromptFactor(
            name="touch_interaction",
            content="用户轻拍了机器人的头部",
            weight=0.8,
            priority=2
        ),
        PromptFactor(
            name="memory_summary",
            content="用户之前提到过喜欢音乐，特别是古典音乐",
            weight=0.6,
            priority=1
        ),
        PromptFactor(
            name="user_input",
            content="你好，今天天气真不错！",
            weight=2.0,
            priority=6,
            is_required=True
        )
    ]
    
    # 创建机器人动作和表情指令
    robot_actions = create_robot_actions_from_emotion("happy")
    robot_expressions = create_robot_expressions_from_emotion("happy")
    
    # 创建上下文信息
    context_info = {
        "时间": "下午3点",
        "地点": "客厅",
        "交互历史": "这是今天的第5次交互"
    }
    
    # 生成综合提示词
    comprehensive_prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        robot_actions=robot_actions,
        robot_expressions=robot_expressions,
        context_info=context_info
    )
    
    print("生成的综合提示词：")
    print("=" * 80)
    print(comprehensive_prompt)
    print("=" * 80)
    
    return comprehensive_prompt


def demo_advanced_prompt_fusion():
    """演示高级提示词融合"""
    print("\n=== 高级提示词融合演示 ===")
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 使用便捷函数创建因子
    factors = create_prompt_factors(
        stage_info={
            "prompt": "共鸣期 - 能够理解用户的情感状态，并做出相应的回应"
        },
        personality_info={
            "traits": "温暖、善解人意、有耐心",
            "style": "语言风格温和，善于倾听和安慰"
        },
        emotion_info={
            "emotion": "困惑"
        },
        touch_info={
            "content": "用户轻抚了机器人的手臂"
        },
        memory_info={
            "summary": "用户之前询问过关于学习编程的问题，表现出对新知识的渴望"
        },
        user_input="我不太明白这个编程概念，能再解释一下吗？"
    )
    
    # 创建机器人动作和表情指令
    robot_actions = create_robot_actions_from_emotion("confused")
    robot_expressions = create_robot_expressions_from_emotion("confused")
    
    # 创建上下文信息
    context_info = {
        "学习主题": "Python编程基础",
        "用户水平": "初学者",
        "当前时间": "晚上8点",
        "学习环境": "安静的书房"
    }
    
    # 生成综合提示词
    comprehensive_prompt = fusion_engine.create_comprehensive_prompt(
        factors=factors,
        robot_actions=robot_actions,
        robot_expressions=robot_expressions,
        context_info=context_info
    )
    
    print("生成的综合提示词：")
    print("=" * 80)
    print(comprehensive_prompt)
    print("=" * 80)
    
    return comprehensive_prompt


def demo_emotion_based_actions():
    """演示基于情绪的动作和表情生成"""
    print("\n=== 基于情绪的动作和表情生成演示 ===")
    
    emotions = ["happy", "sad", "confused", "excited", "surprised"]
    
    for emotion in emotions:
        print(f"\n情绪: {emotion}")
        print("-" * 40)
        
        # 生成动作指令
        actions = create_robot_actions_from_emotion(emotion)
        print("动作指令:")
        for action in actions:
            print(f"  - {action.action_code}: {action.description}")
        
        # 生成表情指令
        expressions = create_robot_expressions_from_emotion(emotion)
        print("表情指令:")
        for expr in expressions:
            print(f"  - {expr.expression_code}: {expr.description}")


def demo_prompt_structure_analysis():
    """演示提示词结构分析"""
    print("\n=== 提示词结构分析演示 ===")
    
    # 创建提示词融合引擎
    fusion_engine = PromptFusionEngine()
    
    # 创建测试因子
    factors = create_prompt_factors(
        stage_info={"prompt": "萌芽期 - 发出简单的咿咿呀呀声音"},
        personality_info={"traits": "好奇、活泼"},
        emotion_info={"emotion": "neutral"},
        user_input="你好"
    )
    
    # 生成提示词
    prompt = fusion_engine.create_comprehensive_prompt(factors)
    
    # 分析提示词结构
    sections = prompt.split("\n\n")
    
    print("提示词结构分析:")
    print("=" * 50)
    
    for i, section in enumerate(sections, 1):
        if section.strip():
            title = section.split("\n")[0] if section.split("\n") else "未知部分"
            print(f"{i}. {title}")
            print(f"   长度: {len(section)} 字符")
            print(f"   行数: {len(section.split(chr(10)))} 行")
            print()


def demo_json_output_format():
    """演示JSON输出格式"""
    print("\n=== JSON输出格式演示 ===")
    
    # 模拟大模型输出
    sample_output = {
        "text": "你好！今天天气确实很棒呢！我也很开心能和你聊天。",
        "actions": [
            {
                "code": "A001",
                "description": "点头动作±15度",
                "parameters": {"angle": 15, "duration": 1.0}
            },
            {
                "code": "A003",
                "description": "手臂上举10度",
                "parameters": {"angle": 10, "duration": 0.8}
            }
        ],
        "expressions": [
            {
                "code": "E001",
                "description": "微笑+眨眼+眼神上扬",
                "animation": {"intensity": 0.8, "duration": 2.0}
            }
        ]
    }
    
    print("期望的JSON输出格式:")
    print("=" * 50)
    print(json.dumps(sample_output, ensure_ascii=False, indent=2))
    print()


def main():
    """主函数"""
    print("提示词融合算法演示")
    print("=" * 80)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 基础演示
        demo_basic_prompt_fusion()
        
        # 高级演示
        demo_advanced_prompt_fusion()
        
        # 情绪动作演示
        demo_emotion_based_actions()
        
        # 结构分析演示
        demo_prompt_structure_analysis()
        
        # JSON格式演示
        demo_json_output_format()
        
        print("\n✅ 所有演示完成！")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 
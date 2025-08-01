"""测试提示词融合算法

验证提示词融合算法是否正确处理各种影响因子。
"""

import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors, PromptFactor


def test_prompt_fusion_engine():
    """测试提示词融合引擎"""
    print("=== 测试提示词融合引擎 ===")
    
    fusion_engine = PromptFusionEngine()
    
    # 测试用例1：基础融合
    print("\n--- 测试用例1：基础融合 ---")
    factors1 = [
        PromptFactor("growth_stage", "You are in the resonate stage", weight=1.5, priority=5),
        PromptFactor("personality_traits", "curious, outgoing, kind", weight=1.2, priority=4),
        PromptFactor("user_input", "你好，我是小明", weight=2.0, priority=6, is_required=True)
    ]
    
    result1 = fusion_engine.fuse_prompts(factors1)
    print(f"结果1: {result1}")
    
    # 测试用例2：复杂融合
    print("\n--- 测试用例2：复杂融合 ---")
    factors2 = [
        PromptFactor("growth_stage", "You are in the resonate stage. 你已进入共鸣期", weight=1.5, priority=5),
        PromptFactor("personality_traits", "curious, outgoing, kind", weight=1.2, priority=4),
        PromptFactor("personality_style", "enthusiastic", weight=1.0, priority=3),
        PromptFactor("user_emotion", "happy", weight=1.0, priority=3),
        PromptFactor("touch_interaction", "The user touched your head", weight=0.8, priority=2),
        PromptFactor("memory_summary", "之前我们聊过天气", weight=0.6, priority=1),
        PromptFactor("user_input", "摸摸头，今天天气怎么样？", weight=2.0, priority=6, is_required=True)
    ]
    
    result2 = fusion_engine.fuse_prompts(factors2)
    print(f"结果2: {result2}")
    
    # 测试用例3：使用create_prompt_factors函数
    print("\n--- 测试用例3：使用create_prompt_factors ---")
    stage_info = {"prompt": "You are in the resonate stage. 你已进入共鸣期"}
    personality_info = {
        "traits": "curious, outgoing, kind (好奇、外向、友善)",
        "style": "enthusiastic",
        "summary": "high_extraversion, high_openness",
        "dominant_traits": ["high_extraversion", "high_openness"]
    }
    emotion_info = {"emotion": "excited"}
    touch_info = {"content": "The user touched your head. 用户触摸了你的头部"}
    memory_info = {"summary": "之前我们聊过天气和心情", "count": 3}
    user_input = "摸摸头，今天天气怎么样？"
    
    factors3 = create_prompt_factors(
        stage_info=stage_info,
        personality_info=personality_info,
        emotion_info=emotion_info,
        touch_info=touch_info,
        memory_info=memory_info,
        user_input=user_input
    )
    
    result3 = fusion_engine.fuse_prompts(factors3)
    print(f"结果3: {result3}")
    
    print("\n✅ 提示词融合引擎测试完成")


def test_robot_with_fusion():
    """测试机器人使用融合算法"""
    print("\n=== 测试机器人使用融合算法 ===")
    
    try:
        from ai_core.intelligent_core import IntelligentCore, UserInput
        
        core = IntelligentCore()
        
        # 测试不同类型的交互
        test_cases = [
            {
                "name": "基础问候",
                "input": UserInput(robot_id="robotA", text="你好"),
                "description": "测试基础文本交互"
            },
            {
                "name": "触摸交互",
                "input": UserInput(robot_id="robotA", text="摸摸头", touch_zone=0),
                "description": "测试触摸头部交互"
            },
            {
                "name": "情绪交互",
                "input": UserInput(robot_id="robotA", text="我今天很开心！"),
                "description": "测试情绪识别交互"
            },
            {
                "name": "复杂交互",
                "input": UserInput(robot_id="robotA", text="你能记住我们之前的对话吗？", touch_zone=1),
                "description": "测试记忆和触摸组合交互"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试 {i}: {test_case['name']} ---")
            print(f"描述: {test_case['description']}")
            print(f"输入: {test_case['input'].text}")
            if test_case['input'].touch_zone is not None:
                print(f"触摸区域: {test_case['input'].touch_zone}")
            
            # 处理请求
            response = core.process(test_case['input'])
            
            print(f"回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
            print("-" * 50)
        
        print("\n✅ 机器人融合算法测试完成")
        
    except Exception as e:
        print(f"❌ 机器人融合算法测试失败: {e}")


def test_fusion_algorithm_details():
    """测试融合算法细节"""
    print("\n=== 测试融合算法细节 ===")
    
    fusion_engine = PromptFusionEngine()
    
    # 测试不同数量的因子
    test_cases = [
        {
            "name": "最少因子",
            "factors": [
                PromptFactor("user_input", "你好", weight=2.0, priority=6, is_required=True)
            ]
        },
        {
            "name": "中等因子",
            "factors": [
                PromptFactor("growth_stage", "You are in the resonate stage", weight=1.5, priority=5),
                PromptFactor("personality_traits", "curious, outgoing", weight=1.2, priority=4),
                PromptFactor("user_input", "你好", weight=2.0, priority=6, is_required=True)
            ]
        },
        {
            "name": "最多因子",
            "factors": [
                PromptFactor("growth_stage", "You are in the resonate stage", weight=1.5, priority=5),
                PromptFactor("personality_traits", "curious, outgoing, kind", weight=1.2, priority=4),
                PromptFactor("personality_style", "enthusiastic", weight=1.0, priority=3),
                PromptFactor("user_emotion", "happy", weight=1.0, priority=3),
                PromptFactor("touch_interaction", "The user touched your head", weight=0.8, priority=2),
                PromptFactor("memory_summary", "之前我们聊过天气", weight=0.6, priority=1),
                PromptFactor("user_input", "摸摸头，今天天气怎么样？", weight=2.0, priority=6, is_required=True)
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"因子数量: {len(test_case['factors'])}")
        
        result = fusion_engine.fuse_prompts(test_case['factors'])
        print(f"融合结果: {result}")
        print(f"结果长度: {len(result)}")
    
    print("\n✅ 融合算法细节测试完成")


def main():
    """主函数"""
    print("🤖 测试提示词融合算法")
    print("=" * 60)
    
    # 测试融合引擎
    test_prompt_fusion_engine()
    
    # 测试机器人使用融合算法
    test_robot_with_fusion()
    
    # 测试融合算法细节
    test_fusion_algorithm_details()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成！")
    print("\n请查看日志输出，确认:")
    print("1. 提示词融合算法是否正确工作")
    print("2. 各种因子是否正确融合")
    print("3. 最终提示词是否优化")
    print("4. 机器人回复是否更智能")


if __name__ == "__main__":
    main() 
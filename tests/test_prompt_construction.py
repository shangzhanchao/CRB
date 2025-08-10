"""测试提示词构建和LLM调用

验证人格特质、情绪识别、成长阶段等所有因素是否正确组合到最终提示词中。
"""

import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置详细日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.intelligent_core import IntelligentCore, UserInput
from ai_core.constants import STAGE_LLM_PROMPTS, STAGE_LLM_PROMPTS_CN, OCEAN_LLM_PROMPTS, OCEAN_LLM_PROMPTS_CN, TOUCH_ZONE_PROMPTS


def test_prompt_construction():
    """测试提示词构建"""
    print("=== 测试提示词构建 ===")
    
    # 显示所有可用的提示词模板
    print("\n1. 成长阶段提示词:")
    for stage, prompt in STAGE_LLM_PROMPTS.items():
        print(f"  {stage}: {prompt}")
    
    print("\n2. 成长阶段提示词(中文):")
    for stage, prompt in STAGE_LLM_PROMPTS_CN.items():
        print(f"  {stage}: {prompt}")
    
    print("\n3. 人格特质提示词:")
    for trait, prompt in OCEAN_LLM_PROMPTS.items():
        print(f"  {trait}: {prompt}")
    
    print("\n4. 人格特质提示词(中文):")
    for trait, prompt in OCEAN_LLM_PROMPTS_CN.items():
        print(f"  {trait}: {prompt}")
    
    print("\n5. 触摸区域提示词:")
    for zone, prompt in TOUCH_ZONE_PROMPTS.items():
        print(f"  {zone}: {prompt}")


def test_robot_interactions():
    """测试机器人交互，观察提示词构建"""
    print("\n=== 测试机器人交互 ===")
    
    try:
        core = IntelligentCore()
        
        # 测试不同类型的交互
        test_cases = [
            {
                "name": "基础问候",
                "input": UserInput(robot_id="robotA", text="你好，我是小明"),
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
            },
            {
                "name": "纯触摸",
                "input": UserInput(robot_id="robotA", text="", touch_zone=2),
                "description": "测试纯触摸交互"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试 {i}: {test_case['name']} ---")
            print(f"描述: {test_case['description']}")
            print(f"输入: {test_case['input'].text or '无文本'}")
            if test_case['input'].touch_zone is not None:
                print(f"触摸区域: {test_case['input'].touch_zone}")
            
            # 处理请求
            response = core.process(test_case['input'])
            
            print(f"机器人回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
            print("-" * 50)
        
        print("\n✅ 机器人交互测试完成")
        
    except Exception as e:
        print(f"❌ 机器人交互测试失败: {e}")


def test_growth_stage_prompts():
    """测试不同成长阶段的提示词"""
    print("\n=== 测试不同成长阶段 ===")
    
    try:
        # 测试不同成长阶段
        stages = ["sprout", "enlighten", "resonate", "awaken"]
        
        for stage in stages:
            print(f"\n--- 测试成长阶段: {stage} ---")
            
            # 创建临时状态来测试不同阶段
            import json
            from datetime import datetime, timezone, timedelta
            
            # 根据阶段设置不同的状态
            stage_thresholds = {
                "sprout": {"interactions": 10, "audio_seconds": 100, "days": 5},
                "enlighten": {"interactions": 25, "audio_seconds": 400, "days": 15},
                "resonate": {"interactions": 60, "audio_seconds": 1000, "days": 35},
                "awaken": {"interactions": 85, "audio_seconds": 1600, "days": 50}
            }
            
            threshold = stage_thresholds[stage]
            test_state = {
                "interaction_count": threshold["interactions"],
                "audio_seconds": threshold["audio_seconds"],
                "start_time": (datetime.now(timezone.utc) - timedelta(days=threshold["days"])).isoformat()
            }
            
            # 临时保存状态
            with open('data/state.json', 'w', encoding='utf-8') as f:
                json.dump(test_state, f, indent=2, ensure_ascii=False)
            
            # 创建核心并测试
            core = IntelligentCore()
            user_input = UserInput(robot_id="robotA", text="你好，测试不同成长阶段")
            
            response = core.process(user_input)
            print(f"阶段: {stage}")
            print(f"回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
        
        # 恢复原始状态
        original_state = {
            "interaction_count": 60,
            "audio_seconds": 1000.0,
            "start_time": "2024-01-01T00:00:00+00:00"
        }
        with open('data/state.json', 'w', encoding='utf-8') as f:
            json.dump(original_state, f, indent=2, ensure_ascii=False)
        
        print("\n✅ 成长阶段测试完成")
        
    except Exception as e:
        print(f"❌ 成长阶段测试失败: {e}")


def main():
    """主函数"""
    print("🤖 测试提示词构建和LLM调用")
    print("=" * 60)
    
    # 测试提示词构建
    test_prompt_construction()
    
    # 测试机器人交互
    test_robot_interactions()
    
    # 测试不同成长阶段
    test_growth_stage_prompts()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("\n请查看日志输出，确认:")
    print("1. 成长阶段提示词是否正确应用")
    print("2. 人格特质是否包含在提示词中")
    print("3. 情绪识别是否影响提示词构建")
    print("4. 触摸交互是否添加到提示词中")
    print("5. 历史记忆是否正确引用")
    print("6. 最终提示词是否完整组合所有因素")


if __name__ == "__main__":
    main() 
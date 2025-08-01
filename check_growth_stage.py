"""检查机器人成长阶段

验证robotA机器人是否成功提升到共鸣期。
"""

import sys
import os
import json
from datetime import datetime, timezone

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core import global_state
from ai_core.intelligent_core import IntelligentCore, UserInput


def check_growth_stage():
    """检查成长阶段"""
    print("=== 检查机器人成长阶段 ===")
    
    # 读取当前状态
    try:
        with open('state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        print(f"当前状态:")
        print(f"  交互次数: {state.get('interaction_count', 0)}")
        print(f"  语音时长: {state.get('audio_seconds', 0.0)} 秒")
        print(f"  开始时间: {state.get('start_time', 'Unknown')}")
        
        # 计算运行天数
        start_time = datetime.fromisoformat(state['start_time'].replace('Z', '+00:00'))
        current_time = datetime.now(timezone.utc)
        days_running = (current_time - start_time).days
        
        print(f"  运行天数: {days_running} 天")
        
    except Exception as e:
        print(f"❌ 读取状态文件失败: {e}")
        return
    
    # 检查成长阶段
    try:
        current_stage = global_state.get_growth_stage()
        print(f"\n当前成长阶段: {current_stage}")
        
        # 显示各阶段阈值
        from ai_core.constants import STAGE_THRESHOLDS, STAGE_ORDER
        print(f"\n成长阶段阈值:")
        for stage in STAGE_ORDER:
            threshold = STAGE_THRESHOLDS[stage]
            print(f"  {stage}: 天数={threshold['days']}, 交互={threshold['interactions']}, 语音={threshold['audio_seconds']}秒")
        
        # 检查是否达到共鸣期
        if current_stage == "resonate":
            print("\n🎉 成功！robotA已提升到共鸣期！")
        elif current_stage == "awaken":
            print("\n🌟 太棒了！robotA已达到觉醒期！")
        else:
            print(f"\n⚠️ robotA当前处于{current_stage}阶段，还未达到共鸣期")
            
    except Exception as e:
        print(f"❌ 检查成长阶段失败: {e}")


def test_robot_interaction():
    """测试机器人交互"""
    print("\n=== 测试机器人交互 ===")
    
    try:
        core = IntelligentCore()
        
        # 测试不同类型的交互
        test_inputs = [
            UserInput(robot_id="robotA", text="你好，我是小明"),
            UserInput(robot_id="robotA", text="今天天气怎么样？"),
            UserInput(robot_id="robotA", text="你能做什么？", touch_zone=0),
        ]
        
        for i, user_input in enumerate(test_inputs, 1):
            print(f"\n--- 交互测试 {i} ---")
            print(f"用户输入: {user_input.text}")
            
            response = core.process(user_input)
            print(f"机器人回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
        
        print("\n✅ 机器人交互测试完成")
        
    except Exception as e:
        print(f"❌ 机器人交互测试失败: {e}")


def main():
    """主函数"""
    print("🤖 检查robotA机器人成长阶段")
    print("=" * 50)
    
    # 检查成长阶段
    check_growth_stage()
    
    # 测试交互
    test_robot_interaction()
    
    print("\n" + "=" * 50)
    print("检查完成！")


if __name__ == "__main__":
    main() 
"""成长阶段管理脚本

可以手动调整机器人的成长阶段，用于测试和开发。
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core import global_state
from ai_core.constants import STAGE_THRESHOLDS, STAGE_ORDER


def show_current_state():
    """显示当前状态"""
    print("=== 当前状态 ===")
    
    try:
        with open('state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        print(f"交互次数: {state.get('interaction_count', 0)}")
        print(f"语音时长: {state.get('audio_seconds', 0.0)} 秒")
        print(f"开始时间: {state.get('start_time', 'Unknown')}")
        
        # 计算运行天数
        start_time = datetime.fromisoformat(state['start_time'].replace('Z', '+00:00'))
        current_time = datetime.now(timezone.utc)
        days_running = (current_time - start_time).days
        print(f"运行天数: {days_running} 天")
        
        # 显示当前成长阶段
        current_stage = global_state.get_growth_stage()
        print(f"当前成长阶段: {current_stage}")
        
        return state
        
    except Exception as e:
        print(f"❌ 读取状态失败: {e}")
        return None


def show_stage_thresholds():
    """显示各阶段阈值"""
    print("\n=== 成长阶段阈值 ===")
    for stage in STAGE_ORDER:
        threshold = STAGE_THRESHOLDS[stage]
        print(f"{stage:12}: 天数={threshold['days']:2d}, 交互={threshold['interactions']:2d}, 语音={threshold['audio_seconds']:4.0f}秒")


def set_growth_stage(target_stage):
    """设置成长阶段"""
    if target_stage not in STAGE_ORDER:
        print(f"❌ 无效的成长阶段: {target_stage}")
        print(f"有效的阶段: {', '.join(STAGE_ORDER)}")
        return False
    
    # 获取目标阶段的阈值
    threshold = STAGE_THRESHOLDS[target_stage]
    
    # 设置状态以满足目标阶段
    state = {
        "interaction_count": threshold["interactions"] + 10,  # 稍微超过阈值
        "audio_seconds": threshold["audio_seconds"] + 100,    # 稍微超过阈值
        "start_time": (datetime.now(timezone.utc) - timedelta(days=threshold["days"] + 5)).isoformat()  # 稍微超过天数
    }
    
    try:
        with open('state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 成功设置成长阶段为: {target_stage}")
        print(f"  交互次数: {state['interaction_count']}")
        print(f"  语音时长: {state['audio_seconds']} 秒")
        print(f"  开始时间: {state['start_time']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 设置成长阶段失败: {e}")
        return False


def reset_to_sprout():
    """重置到萌芽期"""
    state = {
        "interaction_count": 0,
        "audio_seconds": 0.0,
        "start_time": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        with open('state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print("✅ 成功重置到萌芽期")
        return True
        
    except Exception as e:
        print(f"❌ 重置失败: {e}")
        return False


def main():
    """主函数"""
    print("🤖 机器人成长阶段管理工具")
    print("=" * 50)
    
    # 显示当前状态
    current_state = show_current_state()
    if current_state is None:
        return
    
    # 显示阈值
    show_stage_thresholds()
    
    print("\n=== 操作选项 ===")
    print("1. 设置为萌芽期 (sprout)")
    print("2. 设置为启蒙期 (enlighten)")
    print("3. 设置为共鸣期 (resonate)")
    print("4. 设置为觉醒期 (awaken)")
    print("5. 重置到萌芽期")
    print("6. 退出")
    
    while True:
        try:
            choice = input("\n请选择操作 (1-6): ").strip()
            
            if choice == "1":
                set_growth_stage("sprout")
            elif choice == "2":
                set_growth_stage("enlighten")
            elif choice == "3":
                set_growth_stage("resonate")
            elif choice == "4":
                set_growth_stage("awaken")
            elif choice == "5":
                reset_to_sprout()
            elif choice == "6":
                print("👋 退出管理工具")
                break
            else:
                print("❌ 无效选择，请输入 1-6")
                continue
            
            # 显示更新后的状态
            print("\n" + "=" * 30)
            show_current_state()
            show_stage_thresholds()
            
        except KeyboardInterrupt:
            print("\n👋 退出管理工具")
            break
        except Exception as e:
            print(f"❌ 操作失败: {e}")


if __name__ == "__main__":
    main() 
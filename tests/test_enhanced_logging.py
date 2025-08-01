"""增强日志输出和动作表情格式测试

验证：
1. 后台可以看到调用大模型时的详细参数
2. 动作和表情格式优化
"""

import sys
import os
import logging
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置详细日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.intelligent_core import IntelligentCore, UserInput
from ai_core.constants import FACE_ANIMATION_MAP, ACTION_MAP


def test_enhanced_logging():
    """测试增强的日志输出"""
    print("🔍 测试增强的日志输出")
    print("=" * 60)
    
    try:
        # 创建智能核心
        core = IntelligentCore()
        print("✅ 智能核心创建成功")
        
        # 测试不同情绪的处理
        test_cases = [
            {"text": "你好", "expected_mood": "happy"},
            {"text": "我很伤心", "expected_mood": "sad"},
            {"text": "这太奇怪了", "expected_mood": "confused"},
            {"text": "哇！太棒了！", "expected_mood": "excited"},
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试用例 {i}: {test_case['text']} ---")
            
            # 创建用户输入
            user_input = UserInput(
                robot_id="robotA", 
                text=test_case['text']
            )
            
            # 处理输入
            response = core.process(user_input)
            
            print(f"✅ 处理成功")
            print(f"📝 回复: {response.text}")
            print(f"🎭 表情: {response.expression}")
            print(f"🤸 动作: {response.action}")
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_action_expression_format():
    """测试动作和表情格式"""
    print("\n🔍 测试动作和表情格式")
    print("=" * 60)
    
    try:
        # 测试表情格式
        print("🎭 表情格式测试:")
        for mood, (expression, desc) in FACE_ANIMATION_MAP.items():
            print(f"  {mood}: {expression} | {desc}")
        
        print("\n🤸 动作格式测试:")
        for mood, action_str in ACTION_MAP.items():
            print(f"  {mood}: {action_str}")
            
        # 测试动作解析
        print("\n📋 动作解析测试:")
        test_actions = [
            "A001:nod±15°|头部点头动作±15度|A002:sway±10°|身体轻微摇摆±10度|A003:hands_up10°|手臂上举10度",
            "A004:tilt_oscillate±10°|头部左右摆动±10度|A005:gaze_switch|眼神切换|A006:hands_still|手臂静止",
            "A007:head_down_slow-15°|头部缓慢低下-15度|A008:arms_arc_in|手臂向内弧形收回"
        ]
        
        for action_str in test_actions:
            parts = action_str.split("|")
            actions = []
            for i in range(0, len(parts), 2):
                if i + 1 < len(parts):
                    action_code = parts[i].strip()
                    action_desc = parts[i + 1].strip()
                    actions.append(f"{action_code}|{action_desc}")
                else:
                    actions.append(parts[i].strip())
            print(f"  解析结果: {actions}")
        
        return True
        
    except Exception as e:
        print(f"❌ 格式测试失败: {e}")
        return False


def test_touch_actions():
    """测试触摸动作"""
    print("\n🔍 测试触摸动作")
    print("=" * 60)
    
    try:
        core = IntelligentCore()
        
        # 测试不同触摸区域
        touch_zones = [0, 1, 2]
        touch_names = ["头部", "后背", "前胸"]
        
        for zone, name in zip(touch_zones, touch_names):
            print(f"\n--- 测试触摸{name} (区域{zone}) ---")
            
            # 模拟触摸
            user_input = UserInput(
                robot_id="robotA", 
                text="你好",
                touched=True,
                touch_zone=zone
            )
            
            response = core.process(user_input)
            
            print(f"✅ 触摸{name}处理成功")
            print(f"📝 回复: {response.text}")
            print(f"🎭 表情: {response.expression}")
            print(f"🤸 动作: {response.action}")
            
        return True
        
    except Exception as e:
        print(f"❌ 触摸测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始测试增强功能\n" + "="*60)
    
    # 1. 测试增强日志输出
    test_enhanced_logging()
    
    # 2. 测试动作表情格式
    test_action_expression_format()
    
    # 3. 测试触摸动作
    test_touch_actions()
    
    print("\n" + "=" * 60)
    print("🎯 增强功能测试完成！")
    print("\n请检查上面的输出，确认:")
    print("1. 后台是否显示详细的LLM调用参数")
    print("2. 动作格式是否为: 动作编号+动作+角度+说明")
    print("3. 表情格式是否为: 表情编号+说明")
    print("4. 触摸动作是否正确添加")


if __name__ == "__main__":
    main() 
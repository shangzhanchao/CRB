"""快速测试提示词构建

验证人格特质、情绪识别、成长阶段等所有因素是否正确组合。
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


def quick_test():
    """快速测试提示词构建"""
    print("🤖 快速测试提示词构建")
    print("=" * 50)
    
    try:
        core = IntelligentCore()
        
        # 测试用例
        test_inputs = [
            UserInput(robot_id="robotA", text="你好"),
            UserInput(robot_id="robotA", text="摸摸头", touch_zone=0),
            UserInput(robot_id="robotA", text="我今天很开心！"),
            UserInput(robot_id="robotA", text="你能记住我们之前的对话吗？", touch_zone=1),
        ]
        
        for i, user_input in enumerate(test_inputs, 1):
            print(f"\n--- 测试 {i} ---")
            print(f"输入: {user_input.text}")
            if user_input.touch_zone is not None:
                print(f"触摸区域: {user_input.touch_zone}")
            
            # 处理请求
            response = core.process(user_input)
            
            print(f"回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
            print("-" * 30)
        
        print("\n✅ 测试完成！")
        print("\n请查看上面的日志输出，确认:")
        print("1. 成长阶段提示词是否正确应用")
        print("2. 人格特质是否包含在提示词中")
        print("3. 情绪识别是否影响提示词构建")
        print("4. 触摸交互是否添加到提示词中")
        print("5. 历史记忆是否正确引用")
        print("6. 最终提示词是否完整组合所有因素")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    quick_test() 
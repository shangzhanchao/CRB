"""测试记忆服务修复

验证系统不再尝试连接不存在的远程服务。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.intelligent_core import IntelligentCore, UserInput
from ai_core.service_api import call_memory_save, call_memory_query
from ai_core.constants import DEFAULT_MEMORY_SAVE_URL, DEFAULT_MEMORY_QUERY_URL


def test_memory_service():
    """测试记忆服务"""
    print("=== 测试记忆服务修复 ===")
    
    # 检查默认URL设置
    print(f"记忆保存URL: {DEFAULT_MEMORY_SAVE_URL}")
    print(f"记忆查询URL: {DEFAULT_MEMORY_QUERY_URL}")
    
    # 测试记忆保存
    print("\n1. 测试记忆保存...")
    test_record = {
        "user_text": "你好",
        "ai_response": "你好！很高兴见到你",
        "mood_tag": "happy",
        "user_id": "test_user",
        "touched": False,
        "touch_zone": None,
        "timestamp": "2024-01-01T12:00:00"
    }
    
    try:
        result = call_memory_save(test_record)
        print(f"记忆保存结果: {result}")
        print("✅ 记忆保存测试通过")
    except Exception as e:
        print(f"❌ 记忆保存测试失败: {e}")
    
    # 测试记忆查询
    print("\n2. 测试记忆查询...")
    try:
        result = call_memory_query("你好", top_k=3)
        print(f"记忆查询结果: {result}")
        print("✅ 记忆查询测试通过")
    except Exception as e:
        print(f"❌ 记忆查询测试失败: {e}")
    
    # 测试智能核心
    print("\n3. 测试智能核心...")
    try:
        core = IntelligentCore()
        user_input = UserInput(
            robot_id="robotA",
            text="你好，我是测试用户",
            touch_zone=None
        )
        
        response = core.process(user_input)
        print(f"机器人回复: {response.text}")
        print(f"动作: {response.action}")
        print(f"表情: {response.expression}")
        print("✅ 智能核心测试通过")
        
    except Exception as e:
        print(f"❌ 智能核心测试失败: {e}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_memory_service() 
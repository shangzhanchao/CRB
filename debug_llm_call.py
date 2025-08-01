"""调试LLM调用问题

排查为什么没有调用大模型。
"""

import sys
import os
import logging
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.intelligent_core import IntelligentCore, UserInput
from ai_core.constants import DEFAULT_LLM_URL
from ai_core.service_api import call_llm, async_call_llm
from ai_core.qwen_service import get_qwen_service


def test_constants():
    """测试常量配置"""
    print("=== 测试常量配置 ===")
    print(f"DEFAULT_LLM_URL: {DEFAULT_LLM_URL}")
    print(f"类型: {type(DEFAULT_LLM_URL)}")
    print()


def test_qwen_service():
    """测试百炼服务"""
    print("=== 测试百炼服务 ===")
    try:
        service = get_qwen_service()
        print("✅ 百炼服务实例创建成功")
        print(f"app_id: {service.app_id}")
        print(f"api_key: {service.api_key[:8]}...{service.api_key[-4:]}")
        print("=== 测试百炼调用 ===")
        text = service._call_sync("你好，请简单回复一下", session_id="default", stream=False)
        print(f"百炼返回: {text}")
    except Exception as e:
        print(f"❌ 百炼服务异常: {e}")
    print()


async def test_qwen_call():
    """测试百炼调用"""
    print("=== 测试百炼调用 ===")
    try:
        service = get_qwen_service()
        result = await service._call_async("你好，请简单回复一下", session_id="default", stream=False)
        print(f"✅ 百炼调用成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 百炼调用失败: {e}")
        return False


def test_service_api():
    """测试服务API"""
    print("=== 测试服务API ===")
    try:
        # 测试同步调用
        result = call_llm("你好", "qwen")
        print(f"✅ 同步调用结果: {result}")
        
        # 测试异步调用
        result = asyncio.run(async_call_llm("你好", "qwen"))
        print(f"✅ 异步调用结果: {result}")
        
        return True
    except Exception as e:
        print(f"❌ 服务API调用失败: {e}")
        return False


def test_intelligent_core():
    """测试智能核心"""
    print("=== 测试智能核心 ===")
    try:
        core = IntelligentCore()
        print(f"✅ 智能核心创建成功")
        print(f"LLM URL: {core.dialogue.llm_url}")
        
        # 测试处理
        user_input = UserInput(robot_id="robotA", text="你好")
        response = core.process(user_input)
        
        print(f"✅ 处理成功")
        print(f"回复: {response.text}")
        print(f"动作: {response.action}")
        print(f"表情: {response.expression}")
        
        return True
    except Exception as e:
        print(f"❌ 智能核心测试失败: {e}")
        return False


def test_dialogue_engine():
    """测试对话引擎"""
    print("=== 测试对话引擎 ===")
    try:
        from ai_core.dialogue_engine import DialogueEngine
        
        engine = DialogueEngine()
        print(f"✅ 对话引擎创建成功")
        print(f"LLM URL: {engine.llm_url}")
        
        # 测试生成回复
        response = engine.generate_response("你好")
        print(f"✅ 回复生成成功")
        print(f"回复: {response.text}")
        
        return True
    except Exception as e:
        print(f"❌ 对话引擎测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🔍 开始调试LLM调用问题\n" + "="*60)
    
    # 1. 测试常量配置
    test_constants()
    
    # 2. 测试百炼服务
    test_qwen_service()
    
    # 3. 测试百炼调用
    if True: # Always run this test
        test_qwen_call()
    
    # 4. 测试服务API
    test_service_api()
    
    # 5. 测试对话引擎
    test_dialogue_engine()
    
    # 6. 测试智能核心
    test_intelligent_core()
    
    print("\n" + "=" * 60)
    print("🎯 调试完成！")
    print("\n请检查上面的输出，确认:")
    print("1. 常量配置是否正确")
    print("2. 百炼服务是否正常")
    print("3. API调用是否成功")
    print("4. 对话引擎是否工作")
    print("5. 智能核心是否正常")


if __name__ == "__main__":
    main() 
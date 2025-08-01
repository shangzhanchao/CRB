"""豆包API集成测试

验证豆包API的调用功能是否正常工作。
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

from ai_core.doubao_service import get_doubao_service, call_doubao_llm
from ai_core.service_api import call_llm, async_call_llm
from ai_core.constants import DEFAULT_LLM_URL
from ai_core.intelligent_core import IntelligentCore, UserInput


def test_doubao_service():
    """测试豆包服务"""
    print("=== 测试豆包服务 ===")
    try:
        service = get_doubao_service()
        print("✅ 豆包服务实例创建成功")
        print(f"api_key: {service.api_key[:8]}...{service.api_key[-4:]}")
        print(f"base_url: {service.base_url}")
        print(f"model: {service.model}")
        
        # 测试同步调用
        print("\n=== 测试豆包同步调用 ===")
        text = service._call_sync("你好，请简单回复一下", system_prompt="你是一个友好的助手")
        print(f"豆包返回: {text}")
        
        return True
    except Exception as e:
        print(f"❌ 豆包服务异常: {e}")
        return False


async def test_doubao_async():
    """测试豆包异步调用"""
    print("\n=== 测试豆包异步调用 ===")
    try:
        service = get_doubao_service()
        result = await service.call("你好，请简单回复一下", system_prompt="你是一个友好的助手")
        print(f"✅ 豆包异步调用成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 豆包异步调用失败: {e}")
        return False


def test_service_api():
    """测试服务API"""
    print("\n=== 测试服务API ===")
    try:
        # 测试同步调用
        result = call_llm("你好", "doubao")
        print(f"✅ 同步调用结果: {result}")
        
        # 测试异步调用
        result = asyncio.run(async_call_llm("你好", "doubao"))
        print(f"✅ 异步调用结果: {result}")
        
        return True
    except Exception as e:
        print(f"❌ 服务API调用失败: {e}")
        return False


def test_intelligent_core():
    """测试智能核心"""
    print("\n=== 测试智能核心 ===")
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


def test_doubao_stream():
    """测试豆包流式调用"""
    print("\n=== 测试豆包流式调用 ===")
    try:
        service = get_doubao_service()
        
        async def test_stream():
            async for chunk in service.stream("请介绍一下你自己", system_prompt="你是一个友好的助手"):
                print(chunk, end="", flush=True)
            print()
        
        asyncio.run(test_stream())
        print("✅ 豆包流式调用成功")
        return True
    except Exception as e:
        print(f"❌ 豆包流式调用失败: {e}")
        return False


def main():
    """主函数"""
    print("🔍 开始测试豆包API集成\n" + "="*60)
    
    # 1. 测试豆包服务
    test_doubao_service()
    
    # 2. 测试豆包异步调用
    asyncio.run(test_doubao_async())
    
    # 3. 测试服务API
    test_service_api()
    
    # 4. 测试智能核心
    test_intelligent_core()
    
    # 5. 测试豆包流式调用
    test_doubao_stream()
    
    print("\n" + "=" * 60)
    print("🎯 豆包API集成测试完成！")
    print("\n请检查上面的输出，确认:")
    print("1. 豆包服务是否正常创建")
    print("2. 同步调用是否成功")
    print("3. 异步调用是否成功")
    print("4. 服务API是否正常工作")
    print("5. 智能核心是否正常")
    print("6. 流式调用是否正常")


if __name__ == "__main__":
    main() 
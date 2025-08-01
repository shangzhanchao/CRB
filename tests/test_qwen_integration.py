"""测试百炼服务集成

这个文件用于测试阿里百炼大语言模型的集成功能。
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.qwen_service import QwenService, QwenConfig, get_qwen_service
from ai_core.intelligent_core import IntelligentCore, UserInput


async def test_qwen_service():
    """测试百炼服务基本功能"""
    print("=== 测试百炼服务基本功能 ===")
    
    try:
        # 创建服务实例
        config = QwenConfig(
            app_id="03b39bdb6f0846d7a1b05b0cc37dbbe9",
            api_key="sk-5857a06baafb454fb85288170ee68dc0"
        )
        service = QwenService(config)
        
        # 测试文本生成
        print("1. 测试文本生成...")
        text = await service.generate_text("你好，请介绍一下你自己")
        print(f"生成文本: {text}")
        
        # 测试流式输出
        print("\n2. 测试流式输出...")
        async for chunk in service.generate_stream("请写一首关于春天的诗"):
            print(chunk, end="", flush=True)
        print()
        
        print("✅ 百炼服务基本功能测试通过")
        
    except Exception as e:
        print(f"❌ 百炼服务测试失败: {e}")
        return False
    
    return True


async def test_intelligent_core():
    """测试智能核心集成"""
    print("\n=== 测试智能核心集成 ===")
    
    try:
        # 创建智能核心实例
        core = IntelligentCore()
        
        # 创建用户输入
        user_input = UserInput(
            robot_id="robotA",
            text="你好，我是小明",
            touch_zone=None
        )
        
        # 处理请求
        print("处理用户输入...")
        response = core.process(user_input)
        
        print(f"机器人回复: {response.text}")
        print(f"动作: {response.action}")
        print(f"表情: {response.expression}")
        
        print("✅ 智能核心集成测试通过")
        
    except Exception as e:
        print(f"❌ 智能核心集成测试失败: {e}")
        return False
    
    return True


async def test_service_api():
    """测试服务API集成"""
    print("\n=== 测试服务API集成 ===")
    
    try:
        from ai_core.service_api import call_llm, async_call_llm
        
        # 测试同步调用
        print("1. 测试同步LLM调用...")
        result = call_llm("你好，请简单介绍一下自己", "qwen")
        print(f"同步调用结果: {result[:100]}...")
        
        # 测试异步调用
        print("\n2. 测试异步LLM调用...")
        result = await async_call_llm("请写一首短诗", "qwen")
        print(f"异步调用结果: {result[:100]}...")
        
        print("✅ 服务API集成测试通过")
        
    except Exception as e:
        print(f"❌ 服务API集成测试失败: {e}")
        return False
    
    return True


async def main():
    """主测试函数"""
    print("开始测试百炼服务集成...")
    
    # 检查dashscope是否安装
    try:
        import dashscope
        print("✅ dashscope已安装")
    except ImportError:
        print("❌ dashscope未安装，请运行: pip install dashscope")
        return
    
    # 运行测试
    tests = [
        test_qwen_service,
        test_intelligent_core,
        test_service_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！百炼服务集成成功！")
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接")


if __name__ == "__main__":
    asyncio.run(main()) 
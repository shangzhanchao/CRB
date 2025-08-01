"""百炼服务演示脚本

这个脚本演示如何使用阿里百炼大语言模型服务。
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.qwen_service import get_qwen_service, QwenConfig
from ai_core.intelligent_core import IntelligentCore, UserInput


async def demo_basic_qwen():
    """演示基本的百炼服务功能"""
    print("=== 百炼服务基本功能演示 ===")
    
    try:
        # 获取服务实例
        service = get_qwen_service()
        
        # 演示文本生成
        print("\n1. 文本生成演示")
        prompts = [
            "你好，请介绍一下你自己",
            "请写一首关于春天的诗",
            "解释一下什么是人工智能",
            "给我一个简单的Python代码示例"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n--- 示例 {i} ---")
            print(f"输入: {prompt}")
            response = await service.generate_text(prompt)
            print(f"输出: {response}")
        
        # 演示流式输出
        print("\n2. 流式输出演示")
        print("输入: 请写一首关于秋天的诗")
        print("输出: ", end="", flush=True)
        
        async for chunk in service.generate_stream("请写一首关于秋天的诗"):
            print(chunk, end="", flush=True)
        print()
        
        print("\n✅ 百炼服务基本功能演示完成")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


async def demo_robot_interaction():
    """演示机器人交互功能"""
    print("\n=== 机器人交互演示 ===")
    
    try:
        # 创建智能核心实例
        core = IntelligentCore()
        
        # 演示不同类型的用户输入
        user_inputs = [
            UserInput(robot_id="robotA", text="你好，我是小明"),
            UserInput(robot_id="robotA", text="今天天气怎么样？"),
            UserInput(robot_id="robotA", text="你能做什么？", touch_zone=0),
            UserInput(robot_id="robotA", text="", touch_zone=1),  # 只有触摸输入
        ]
        
        for i, user_input in enumerate(user_inputs, 1):
            print(f"\n--- 交互 {i} ---")
            print(f"用户输入: {user_input.text or '无文本'}")
            if user_input.touch_zone is not None:
                print(f"触摸区域: {user_input.touch_zone}")
            
            # 处理请求
            response = core.process(user_input)
            
            print(f"机器人回复: {response.text}")
            print(f"动作: {response.action}")
            print(f"表情: {response.expression}")
        
        print("\n✅ 机器人交互演示完成")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


async def demo_custom_config():
    """演示自定义配置"""
    print("\n=== 自定义配置演示 ===")
    
    try:
        # 创建自定义配置
        config = QwenConfig(
            app_id="appid",
            api_key="sk-key",
            model_name="qwen-turbo",
            max_tokens=1024,
            temperature=0.8,
            top_p=0.9
        )
        
        # 创建服务实例
        service = get_qwen_service(config)
        
        # 测试不同参数的生成效果
        prompts = [
            "写一个创意故事",
            "解释一个复杂概念",
            "给出实用的建议"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n--- 自定义配置示例 {i} ---")
            print(f"输入: {prompt}")
            response = await service.generate_text(prompt)
            print(f"输出: {response[:200]}...")
        
        print("\n✅ 自定义配置演示完成")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


async def main():
    """主演示函数"""
    print("🤖 百炼服务演示开始")
    print("=" * 50)
    
    # 检查依赖
    try:
        import dashscope
        print("✅ dashscope已安装")
    except ImportError:
        print("❌ dashscope未安装，请运行: pip install dashscope")
        return
    
    # 运行演示
    demos = [
        demo_basic_qwen,
        demo_robot_interaction,
        demo_custom_config
    ]
    
    for demo in demos:
        try:
            await demo()
        except Exception as e:
            print(f"❌ 演示异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 百炼服务演示完成！")
    print("\n使用说明:")
    print("1. 启动服务: python service.py")
    print("2. 访问界面: http://127.0.0.1:8000/verify")
    print("3. 开始与机器人交互！")


if __name__ == "__main__":
    asyncio.run(main()) 
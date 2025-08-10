"""启动服务脚本

验证修复后的服务是否能正常启动。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试导入是否正常"""
    print("=== 测试模块导入 ===")
    
    try:
        from ai_core.intelligent_core import IntelligentCore, UserInput
        print("✅ IntelligentCore 导入成功")
    except Exception as e:
        print(f"❌ IntelligentCore 导入失败: {e}")
        return False
    
    try:
        from ai_core.service_api import call_memory_save, call_memory_query
        print("✅ Service API 导入成功")
    except Exception as e:
        print(f"❌ Service API 导入失败: {e}")
        return False
    
    try:
        from ai_core.constants import DEFAULT_MEMORY_SAVE_URL, DEFAULT_MEMORY_QUERY_URL
        print("✅ Constants 导入成功")
    except Exception as e:
        print(f"❌ Constants 导入失败: {e}")
        return False
    
    return True


def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 测试基本功能 ===")
    
    try:
        from ai_core.intelligent_core import IntelligentCore, UserInput
        
        # 测试智能核心创建
        core = IntelligentCore()
        print("✅ 智能核心创建成功")
        
        # 测试用户输入处理
        user_input = UserInput(
            robot_id="robotA",
            text="测试消息",
            touch_zone=None
        )
        print("✅ 用户输入创建成功")
        
        # 测试处理请求
        response = core.process(user_input)
        print(f"✅ 请求处理成功，回复: {response.text[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始验证服务修复...")
    
    # 测试导入
    if not test_imports():
        print("❌ 模块导入失败，请检查依赖")
        return
    
    # 测试基本功能
    if not test_basic_functionality():
        print("❌ 基本功能测试失败")
        return
    
    print("\n🎉 所有测试通过！服务修复成功！")
    print("\n现在可以启动服务:")
    print("python service.py")
    print("\n然后访问:")
    print("http://127.0.0.1:8000/verify")


if __name__ == "__main__":
    main() 
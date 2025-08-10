#!/usr/bin/env python3
"""
测试DoubaoService参数校验功能

验证：
1. API Key校验
2. Base URL校验  
3. Model校验
4. 异常处理
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.doubao_service import DoubaoService

def test_valid_parameters():
    """测试有效参数"""
    try:
        service = DoubaoService(
            api_key="4b76f73c-147f-419c-9f30-4e916c47d111",
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            model="ep-20250604180101-5chxn"
        )
        print("✅ 有效参数测试: 通过")
        return True
    except Exception as e:
        print(f"❌ 有效参数测试: 失败 - {e}")
        return False

def test_invalid_api_key():
    """测试无效API Key"""
    test_cases = [
        ("", "空API Key"),
        ("invalid-key", "无效格式API Key"),
        ("12345678-1234-1234-1234-123456789xyz", "错误UUID格式")
    ]
    
    for api_key, description in test_cases:
        try:
            service = DoubaoService(api_key=api_key)
            print(f"❌ {description}测试: 应该失败但通过了")
            return False
        except ValueError as e:
            print(f"✅ {description}测试: 通过 - {e}")
        except Exception as e:
            print(f"✅ {description}测试: 通过 - {e}")
    
    return True

def test_invalid_base_url():
    """测试无效Base URL"""
    test_cases = [
        ("", "空Base URL"),
        ("invalid-url", "无效URL格式"),
        ("ftp://example.com", "不支持协议"),
        ("not-a-url", "非URL格式")
    ]
    
    for base_url, description in test_cases:
        try:
            service = DoubaoService(base_url=base_url)
            print(f"❌ {description}测试: 应该失败但通过了")
            return False
        except ValueError as e:
            print(f"✅ {description}测试: 通过 - {e}")
        except Exception as e:
            print(f"✅ {description}测试: 通过 - {e}")
    
    return True

def test_invalid_model():
    """测试无效Model"""
    test_cases = [
        ("", "空Model名称"),
        ("invalid-model", "无效Model格式"),
        ("gpt-3.5-turbo", "非豆包Model格式")
    ]
    
    for model, description in test_cases:
        try:
            service = DoubaoService(model=model)
            print(f"❌ {description}测试: 应该失败但通过了")
            return False
        except ValueError as e:
            print(f"✅ {description}测试: 通过 - {e}")
        except Exception as e:
            print(f"✅ {description}测试: 通过 - {e}")
    
    return True

def test_parameter_validation_integration():
    """测试参数校验集成"""
    print("\n=== 参数校验集成测试 ===")
    
    # 测试所有有效参数
    valid_result = test_valid_parameters()
    
    # 测试无效参数
    invalid_api_result = test_invalid_api_key()
    invalid_url_result = test_invalid_base_url()
    invalid_model_result = test_invalid_model()
    
    all_passed = all([
        valid_result,
        invalid_api_result,
        invalid_url_result,
        invalid_model_result
    ])
    
    if all_passed:
        print("\n🎉 所有参数校验测试通过!")
    else:
        print("\n❌ 部分参数校验测试失败!")
    
    return all_passed

def main():
    """主测试函数"""
    print("开始测试DoubaoService参数校验功能...")
    
    success = test_parameter_validation_integration()
    
    if success:
        print("\n✅ 参数校验功能测试完成，所有测试通过!")
    else:
        print("\n❌ 参数校验功能测试完成，部分测试失败!")
    
    return success

if __name__ == "__main__":
    main()

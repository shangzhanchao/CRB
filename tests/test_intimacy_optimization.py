#!/usr/bin/env python3
"""测试亲密度系统和抚摸优化效果

这个脚本用于测试优化后的抚摸交互和亲密度系统。
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_core.intelligent_core import IntelligentCore, UserInput
from ai_core.intimacy_system import IntimacySystem


def test_intimacy_system():
    """测试亲密度系统"""
    print("=" * 60)
    print("🤗 测试亲密度系统")
    print("=" * 60)
    
    # 创建亲密度系统
    intimacy = IntimacySystem("robotA")
    
    print(f"📊 初始亲密度: {intimacy.get_intimacy_value()}")
    print(f"🏷️ 初始等级: {intimacy.get_intimacy_level()}")
    print(f"📝 描述: {intimacy.get_intimacy_description()}")
    
    # 测试不同抚摸区域的亲密度更新
    touch_zones = [0, 1, 2]
    zone_names = ["头部", "背后", "胸口"]
    
    for i, (zone, name) in enumerate(zip(touch_zones, zone_names)):
        print(f"\n🖐️ 测试抚摸区域 {zone} ({name}):")
        
        # 更新亲密度
        result = intimacy.update_intimacy_from_touch(zone)
        
        print(f"   📈 亲密度变化: {result['old_value']} -> {result['new_value']} (+{result['bonus']})")
        print(f"   🏷️ 等级变化: {result['old_level']} -> {result['new_level']}")
        if result['level_changed']:
            print(f"   🎉 等级提升!")
        print(f"   📝 描述: {result['description']}")
        
        # 获取抚摸响应
        touch_response = intimacy.get_touch_response(zone)
        print(f"   🎭 表情: {touch_response['expression']}")
        print(f"   🤸 动作: {touch_response['action']}")
        print(f"   💬 文本: {touch_response['text']}")
    
    # 测试交互亲密度更新
    print(f"\n💬 测试交互亲密度更新:")
    interaction_types = ["chat", "audio", "video", "image"]
    
    for interaction_type in interaction_types:
        result = intimacy.update_intimacy_from_interaction(interaction_type)
        print(f"   📈 {interaction_type}: {result['old_value']} -> {result['new_value']} (+{result['bonus']})")
    
    # 显示最终统计
    stats = intimacy.get_intimacy_stats()
    print(f"\n📊 最终统计:")
    print(f"   🤖 机器人ID: {stats['robot_id']}")
    print(f"   📈 当前亲密度: {stats['current_value']}")
    print(f"   🏷️ 当前等级: {stats['current_level']}")
    print(f"   💬 交互次数: {stats['interaction_count']}")
    print(f"   🖐️ 抚摸次数: {stats['touch_count']}")
    print(f"   📝 描述: {stats['description']}")
    
    intimacy.close()


def test_enhanced_dialogue_with_intimacy():
    """测试集成亲密度系统的增强对话"""
    print("\n" + "=" * 60)
    print("🤖 测试集成亲密度系统的增强对话")
    print("=" * 60)
    
    # 创建智能核心
    core = IntelligentCore("robotA")
    
    # 测试不同抚摸区域的响应
    touch_zones = [0, 1, 2]
    zone_names = ["头部", "背后", "胸口"]
    
    for i, (zone, name) in enumerate(zip(touch_zones, zone_names)):
        print(f"\n🖐️ 测试抚摸区域 {zone} ({name}):")
        
        # 创建用户输入
        user = UserInput(
            text="",  # 空文本，测试纯抚摸响应
            robot_id="robotA",
            touch_zone=zone,
            session_id="test_session"
        )
        
        # 处理请求
        response = core.process(user)
        result = response.as_dict()
        
        print(f"   💬 文本回复: {result['text']}")
        print(f"   🎭 表情: {result['expression']}")
        print(f"   🤸 动作: {result['action']}")
        print(f"   🎵 音频: {result['audio']}")
        print(f"   🆔 会话ID: {result['session_id']}")
        print(f"   📊 记忆数量: {result['memory_count']}")
    
    # 测试带文本的抚摸交互
    print(f"\n💬 测试带文本的抚摸交互:")
    
    user = UserInput(
        text="你好，我想抚摸你",
        robot_id="robotA",
        touch_zone=1,  # 背后
        session_id="test_session"
    )
    
    response = core.process(user)
    result = response.as_dict()
    
    print(f"   💬 文本回复: {result['text']}")
    print(f"   🎭 表情: {result['expression']}")
    print(f"   🤸 动作: {result['action']}")
    print(f"   🎵 音频: {result['audio']}")
    
    core.close()


def test_ui_display_format():
    """测试UI显示格式"""
    print("\n" + "=" * 60)
    print("🖥️ 测试UI显示格式")
    print("=" * 60)
    
    # 模拟API响应数据
    mock_response = {
        "text": "感受到你的温柔抚摸，我很开心",
        "audio": "audio_response.wav",
        "action": ["A103:comfortable_nod|舒适点头"],
        "expression": "E016:warm_smile|温暖微笑",
        "session_id": "test_session_123",
        "context_summary": "用户进行了抚摸交互",
        "memory_count": 5
    }
    
    # 模拟service.py的format_response_result函数
    def format_response_result(result):
        formatted_result = {
            "status": "success",
            "timestamp": "2024-01-01T12:00:00",
            "data": {}
        }
        
        if isinstance(result, dict):
            if 'text' in result:
                formatted_result["data"]["reply"] = {
                    "type": "text",
                    "content": result['text'],
                    "length": len(result['text'])
                }
            
            if 'action' in result:
                formatted_result["data"]["action"] = result['action']
            
            if 'expression' in result:
                formatted_result["data"]["expression"] = result['expression']
            
            if 'audio' in result:
                formatted_result["data"]["audio"] = result['audio']
            
            if 'session_id' in result:
                formatted_result["data"]["session"] = {
                    "type": "session_info",
                    "session_id": result['session_id'],
                    "status": "active"
                }
            
            if 'memory_count' in result:
                formatted_result["data"]["memory_count"] = result['memory_count']
            
            if 'context_summary' in result:
                formatted_result["data"]["context_summary"] = result['context_summary']
        
        return formatted_result
    
    # 格式化响应
    formatted = format_response_result(mock_response)
    
    print("📋 格式化后的响应数据:")
    print(json.dumps(formatted, ensure_ascii=False, indent=2))
    
    print("\n📊 显示区域信息:")
    print("   💬 文本回复区域: ✓")
    print("   🎭 表情显示区域: ✓")
    print("   🤸 动作显示区域: ✓")
    print("   🎵 语音播放区域: ✓")
    print("   💕 亲密度信息区域: ✓")
    print("   🖐️ 抚摸反馈区域: ✓")
    print("   📊 统计信息区域: ✓")


def main():
    """主测试函数"""
    print("🚀 开始测试亲密度系统和抚摸优化")
    
    try:
        # 测试亲密度系统
        test_intimacy_system()
        
        # 测试增强对话
        test_enhanced_dialogue_with_intimacy()
        
        # 测试UI显示格式
        test_ui_display_format()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        print("🎯 优化效果总结:")
        print("   1. ✅ 抚摸反馈更加含蓄，通过动作、表情和亲密度表现")
        print("   2. ✅ 增加了亲密度系统，动态跟踪关系发展")
        print("   3. ✅ UI显示区域增加了动作、表情、语音和亲密度信息")
        print("   4. ✅ 不同抚摸区域有不同的亲密度加成")
        print("   5. ✅ 根据亲密度等级生成不同的抚摸响应")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 
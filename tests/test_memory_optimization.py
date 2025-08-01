"""记忆系统优化测试

验证优化后的记忆系统是否正常工作。
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

from ai_core.semantic_memory import SemanticMemory
from ai_core.dialogue_engine import DialogueEngine
from ai_core.personality_engine import PersonalityEngine


def test_improved_memory_query():
    """测试改进的记忆查询功能"""
    print("🔍 测试改进的记忆查询功能")
    print("=" * 60)
    
    try:
        memory = SemanticMemory()
        
        # 添加一些测试记忆
        test_memories = [
            ("你好", "你好呀！很高兴见到你！", "happy", "test_user"),
            ("今天天气怎么样", "今天天气很不错呢，阳光明媚的！", "happy", "test_user"),
            ("我有点难过", "别难过，有什么事情可以和我分享吗？", "sad", "test_user"),
            ("你能安慰我吗", "当然可以！我会一直陪在你身边的。", "sad", "test_user"),
            ("谢谢你的安慰", "不客气！看到你心情变好我也很开心。", "happy", "test_user"),
        ]
        
        print("📝 添加测试记忆...")
        for user_text, ai_response, mood, user_id in test_memories:
            memory.add_memory(user_text, ai_response, mood, user_id)
        
        # 测试查询
        test_queries = [
            ("你好", "应该找到'你好'相关的记忆"),
            ("难过", "应该找到'我有点难过'相关的记忆"),
            ("安慰", "应该找到'你能安慰我吗'相关的记忆"),
            ("天气", "应该找到'今天天气怎么样'相关的记忆"),
            ("谢谢", "应该找到'谢谢你的安慰'相关的记忆"),
        ]
        
        print("\n🔍 测试记忆查询...")
        for query, expected in test_queries:
            print(f"\n查询: '{query}'")
            results = memory.query_memory(query, top_k=2)
            
            if results:
                print(f"  找到 {len(results)} 条相关记忆:")
                for i, result in enumerate(results, 1):
                    print(f"    {i}. 用户: {result['user_text']}")
                    print(f"       AI: {result['ai_response']}")
                    print(f"       情绪: {result['mood_tag']}")
            else:
                print("  ⚠️ 未找到相关记忆")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆查询测试失败: {e}")
        return False


def test_memory_in_dialogue():
    """测试对话中的记忆使用"""
    print("\n🔍 测试对话中的记忆使用")
    print("=" * 60)
    
    try:
        # 创建对话引擎
        personality = PersonalityEngine()
        memory = SemanticMemory()
        dialogue = DialogueEngine(
            personality=personality,
            memory=memory,
            llm_url="doubao"
        )
        
        print("✅ 对话引擎创建成功")
        
        # 模拟对话序列
        test_conversations = [
            ("你好", "user1", "happy"),
            ("今天心情怎么样", "user1", "happy"),
            ("我有点难过", "user2", "sad"),
            ("你能安慰我吗", "user2", "sad"),
            ("谢谢你的安慰", "user2", "happy"),
        ]
        
        print("\n🗣️ 开始模拟对话...")
        for i, (text, user_id, mood) in enumerate(test_conversations, 1):
            print(f"\n--- 对话 {i} ---")
            print(f"用户: {text}")
            print(f"用户ID: {user_id}")
            print(f"情绪: {mood}")
            
            # 生成回复
            response = dialogue.generate_response(
                user_text=text,
                mood_tag=mood,
                user_id=user_id
            )
            
            print(f"AI回复: {response.text}")
            print(f"表情: {response.expression}")
            print(f"动作: {response.action}")
            
            # 检查记忆
            print(f"📊 当前记忆记录数: {len(memory.records)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 对话记忆测试失败: {e}")
        return False


def test_memory_quality():
    """测试记忆质量"""
    print("\n🔍 测试记忆质量")
    print("=" * 60)
    
    try:
        memory = SemanticMemory()
        
        # 分析现有记忆的质量
        print("📊 记忆质量分析:")
        print(f"   总记录数: {len(memory.records)}")
        
        if memory.records:
            # 统计有效记忆
            valid_memories = 0
            empty_memories = 0
            short_memories = 0
            
            for record in memory.records:
                response = record['ai_response'].strip()
                if not response:
                    empty_memories += 1
                elif len(response) <= 2:
                    short_memories += 1
                else:
                    valid_memories += 1
            
            print(f"   有效记忆: {valid_memories}")
            print(f"   空记忆: {empty_memories}")
            print(f"   短记忆: {short_memories}")
            
            # 显示一些高质量的记忆
            print("\n📋 高质量记忆示例:")
            high_quality = []
            for record in memory.records:
                response = record['ai_response'].strip()
                if response and len(response) > 10 and not response.startswith("["):
                    high_quality.append(record)
            
            for i, record in enumerate(high_quality[:5], 1):
                print(f"   {i}. 用户: {record['user_text']}")
                print(f"      AI: {record['ai_response']}")
                print(f"      情绪: {record['mood_tag']}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆质量测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始记忆系统优化测试\n" + "="*60)
    
    # 1. 测试改进的记忆查询
    test_improved_memory_query()
    
    # 2. 测试对话中的记忆使用
    test_memory_in_dialogue()
    
    # 3. 测试记忆质量
    test_memory_quality()
    
    print("\n" + "=" * 60)
    print("🎯 记忆系统优化测试完成！")
    print("\n请检查上面的输出，确认:")
    print("1. 记忆查询是否更准确")
    print("2. 记忆是否在对话中有效使用")
    print("3. 记忆质量是否有所改善")


if __name__ == "__main__":
    main() 